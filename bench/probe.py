"""Phase 4: the transfer probe. Does the memory live in the seat or the model?

Held fixed: the distillation generator (one model distills every lesson, so a
lesson's origin varies only by whose trace and feedback seeded it), the
cross-family audience rule, the tasks, the features, the prompts. Varied: the
performer model, and which lesson store the performer consumes.

Six cells: performer {A, B} x lessons {none, A, B}. Baselines included
because at tiny n they carry the most information. Generation tasks and
application tasks are disjoint, so a consumed lesson is never a replay of the
task that produced it. Rule classes (PACKET-002) overlap the pools instead:
the same class of stated-rule trap appears in both, in different tasks, which
is what makes transfer possible without task overlap.

Lessons come from contrast (PACKET-002, widened by PACKET-003): each
generation task runs R_G times per seat, then contrasts build per rule
class: within-task fail-and-pass first, sibling pairs (fail on one sibling,
pass on the other, same seat, same class) as the fallback for classes still
without a lesson. At most two lessons per class per seat. No contrast, no
lesson; lessons come from breaks, never from averages. The report carries
per-seat per-class accounting.

The task pools live in probe_tasks.py. The apply pool is calibrated for
headroom per seat (see calibrate.py). The repeats parameter runs every apply
task R times per cell, the report states the per-cell n and a per-rule-class
breakdown. The n decides what the matrix is allowed to mean.
"""

import json
import os
import sys
import time

import lesson
import menu
import runner
from probe_tasks import APPLY_TASKS, CRITERIA, FEATURES, GEN_TASKS

MODELS = {"A": "qwen2.5-coder:7b", "B": "llama3.1:8b"}
AUDIENCE = {"A": "llama3.1:8b", "B": "qwen2.5-coder:7b"}
GENERATOR = "qwen2.5-coder:7b"
R_G = 3  # performer attempts per generation task, the contrast's raw material

_CLASS_OF = {t["name"]: t["rule_class"] for t in APPLY_TASKS}

_TS = time.strftime("%Y%m%d-%H%M%S")
_LOG = os.path.join(runner.RUNS, f"probe-{_TS}.log")
_ROWS = os.path.join(runner.RUNS, f"probe-{_TS}.rows.jsonl")
_REPORT = os.path.join(runner.RUNS, f"probe-{_TS}.report.json")


def _set_ts(ts):
    """Rebind the run id and its file paths. Resume reuses a prior id so
    the checkpoint rows, the log, and the report stay one record."""
    global _TS, _LOG, _ROWS, _REPORT
    _TS = ts
    _LOG = os.path.join(runner.RUNS, f"probe-{_TS}.log")
    _ROWS = os.path.join(runner.RUNS, f"probe-{_TS}.rows.jsonl")
    _REPORT = os.path.join(runner.RUNS, f"probe-{_TS}.report.json")


def _load_rows():
    """The checkpoint rows already on disk for this run id."""
    rows = []
    try:
        with open(_ROWS, encoding="utf-8") as f:
            rows = [json.loads(l) for l in f if l.strip()]
    except FileNotFoundError:
        pass
    return rows


def _load_summary(run_id):
    """A completed run's own record, or None when it is not on disk. A
    missing or unreadable summary means the run gets done again live."""
    try:
        with open(os.path.join(runner.RUNS, f"{run_id}.summary.json"),
                  encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return None


def _p(*parts):
    line = " ".join(str(p) for p in parts)
    print(line, flush=True)
    with open(_LOG, "a", encoding="utf-8") as f:
        f.write(line + "\n")


def _row(d):
    """Checkpoint every run as it lands. A dead pipe strands nothing."""
    with open(_ROWS, "a", encoding="utf-8") as f:
        f.write(json.dumps(d) + "\n")


def ev_fraction(ev):
    """Share of evidence checks passed, finer-grained than pass/fail."""
    results = (ev or {}).get("results") or []
    if not results:
        return 0.0
    return sum(1 for r in results if r["ok"]) / len(results)


def _mean(xs):
    return sum(xs) / len(xs) if xs else 0.0


def _features(t):
    """Task work features: the shared dict plus the task's rule class,
    its rule topic, and its stated direction when it has one, so lessons
    can pin all three and the menu never surfaces a mismatched lesson."""
    f = {**FEATURES, "rule_class": t["rule_class"]}
    if "rule_topic" in t:
        f["rule_topic"] = t["rule_topic"]
    if "stated_direction" in t:
        f["stated_direction"] = t["stated_direction"]
    return f


def store(key):
    return os.path.join(runner.RUNS, f"probe-{_TS}-lessons_{key}.jsonl")


def _partition(summaries):
    fails = [s for s in summaries if not (s["evidence"] or {}).get("passed")]
    passes = [s for s in summaries if (s["evidence"] or {}).get("passed")]
    return fails, passes


def _distill(key, kind, cand_fn, gen_task, committed_nodes, fails):
    """Run one distillation with two attempts through the gates. Returns
    True when a lesson landed in the store. A lesson whose fail node is
    already in the store was committed by an interrupted run and is not
    distilled twice; the trail carries the true contrast type either way."""
    if any(s["node_id"] in committed_nodes for s in fails):
        _p(f"gen {key} ({gen_task}): {kind} lesson already committed, "
           f"resumed")
        return True
    for attempt in range(2):
        try:
            cand = cand_fn()
            cand.setdefault("trail", {})["gen_task"] = gen_task
            cand["trail"].setdefault("contrast_type", kind)
            lesson.commit(store(key), cand)
            _p(f"gen {key} ({gen_task}): {kind} lesson committed")
            return True
        except lesson.LessonError as e:
            _p(f"  {kind} lesson attempt {attempt + 1} rejected: {e}")
    _p(f"gen {key} ({gen_task}): {kind} contrast REJECTED both attempts")
    return False


def gen_lessons(key, prior_rows=None):
    """Model `key` attempts each generation task R_G times, then contrasts
    are built per rule class: within-task pairs first (only sampling
    varied, the cleaner comparison), sibling pairs as the fallback for
    classes still without a lesson (same seat, same class, different
    task). At most two lessons per class per seat. All-fail on both
    siblings yields no lesson and the accounting says so: lessons come
    from contrast, never from averages. Returns per-class accounting.
    prior_rows: checkpointed rows from an interrupted run. A checkpointed
    attempt is reloaded from its own summary instead of run again."""
    _p(f"-- generating lessons from model {key} ({MODELS[key]}), "
       f"contrastive with sibling fallback, R_G={R_G} --")
    prior = {}
    for r in prior_rows or []:
        if r.get("phase") == "gen" and r.get("model") == key:
            prior.setdefault(r["task"], {})[r["rep"]] = r
    committed_nodes = {l.get("trail", {}).get("node_id")
                       for l in lesson.load(store(key))}

    # ---- every attempt first, so contrasts can cross sibling tasks ----
    runs = {}
    for t in GEN_TASKS:
        summaries = []
        for rep in range(R_G):
            done = prior.get(t["name"], {}).get(rep)
            r = _load_summary(done["run_id"]) if done else None
            if r is None:
                r = runner.run_once(t["task"], CRITERIA, _features(t),
                                    model=MODELS[key],
                                    audience_model=AUDIENCE[key],
                                    evidence_checks=t["checks"])
                _row({"phase": "gen", "model": key, "task": t["name"],
                      "rule_class": t["rule_class"], "rep": rep,
                      "run_id": r["run_id"], "verdict": r["verdict"],
                      "ev": ev_fraction(r["evidence"]),
                      "ev_passed": bool((r["evidence"] or {}).get("passed"))})
            summaries.append(r)
        fails, passes = _partition(summaries)
        runs[t["name"]] = {"task": t, "fails": fails, "passes": passes,
                           "case": ("mixed" if fails and passes else
                                    "all_pass" if not fails else "all_fail")}

    # ---- contrasts per class: within-task first, sibling fallback ----
    by_class = {}
    for t in GEN_TASKS:
        by_class.setdefault(t["rule_class"], []).append(t)
    accounting = []
    for cls, tasks in by_class.items():
        entry = {"rule_class": cls,
                 "cases": {t["name"]: runs[t["name"]]["case"] for t in tasks},
                 "lessons": []}
        for t in tasks:
            if len(entry["lessons"]) >= 2:
                break
            r = runs[t["name"]]
            if r["case"] != "mixed":
                continue
            ok = _distill(
                key, "within_task",
                lambda t=t, r=r: lesson.generate_contrastive(
                    t["task"], _features(t), r["fails"][0], r["passes"][0],
                    model=GENERATOR),
                t["name"], committed_nodes, r["fails"])
            entry["lessons"].append({"task": t["name"],
                                     "type": "within_task",
                                     "committed": ok})
        # sibling mining under the per-class cap (PACKET-005, approved):
        # any fail-task not already mined pairs with a passing sibling
        # while the cap has room, so an all-fail sibling with a passing
        # partner gets mined even when the class already has a lesson.
        mined = {l["task"] for l in entry["lessons"] if l["committed"]}
        committed_count = len(mined)
        for tf in tasks:
            if committed_count >= 2:
                break
            if tf["name"] in mined or not runs[tf["name"]]["fails"]:
                continue
            tp = next((x for x in tasks if x["name"] != tf["name"]
                       and runs[x["name"]]["passes"]), None)
            if tp is None:
                continue
            rf, rp = runs[tf["name"]], runs[tp["name"]]
            ok = _distill(
                key, "sibling",
                lambda tf=tf, tp=tp, rf=rf, rp=rp:
                    lesson.generate_sibling_contrast(
                        tf["task"], tp["task"], cls, _features(tf),
                        rf["fails"][0], rp["passes"][0], model=GENERATOR),
                tf["name"], committed_nodes, rf["fails"])
            entry["lessons"].append({"task": tf["name"],
                                     "sibling": tp["name"],
                                     "type": "sibling",
                                     "committed": ok})
            if ok:
                committed_count += 1
                mined.add(tf["name"])
        if not entry["lessons"]:
            cases = set(entry["cases"].values())
            entry["reason"] = ("both siblings all_pass, nothing broke"
                               if cases == {"all_pass"} else
                               "all_fail with no passing sibling")
            _p(f"gen {key} ({cls}): no contrast, {entry['reason']}")
        accounting.append(entry)
    n = len(lesson.load(store(key)))
    _p(f"store {key}: {n} lessons committed")
    return accounting


_RULE_CHECKS = {t["name"]: set(t.get("rule_checks", []))
                for t in APPLY_TASKS}


def check_table(rows):
    """The check-level treatment readout (PACKET-005): for every apply
    check, the pass rate per cell, with the checks that encode the task's
    stated rule marked. The sharp level PACKET-004 proved necessary:
    task-mean aggregation diluted a check-local effect three probes
    running."""
    table = {}
    for r in rows:
        if r.get("phase") != "apply":
            continue
        for call, ok in (r.get("checks") or {}).items():
            cell = (table.setdefault(r["task"], {})
                    .setdefault(call, {"rule_check": call in
                                       _RULE_CHECKS.get(r["task"], set()),
                                       "cells": {}})
                    ["cells"].setdefault(r["cell"], {"n": 0, "passed": 0}))
            cell["n"] += 1
            cell["passed"] += 1 if ok else 0
    for t in table.values():
        for c in t.values():
            for a in c["cells"].values():
                a["rate"] = a["passed"] / a["n"] if a["n"] else 0.0
    return table


def run_cell(perf, src, repeats=1, prior_rows=None):
    """One cell: performer `perf` consumes the lesson store `src` (or none)
    across the application tasks, `repeats` passes over the pool. Lessons
    are queried per task, because matching now includes the rule class.
    prior_rows: checkpointed rows from an interrupted run. Runs already on
    disk are counted, not repeated."""
    lessons = lesson.load(store(src)) if src else []
    name = f"{perf}|{src or 'none'}"
    prior_cell = [r for r in prior_rows or []
                  if r.get("phase") == "apply" and r.get("cell") == name]
    done = {(r["task"], r["rep"]) for r in prior_cell}
    if prior_cell:
        _p(f"cell {name}: resuming past {len(prior_cell)} checkpointed runs")
    rows = list(prior_cell)
    tools_seen = set()
    for rep in range(repeats):
        for t in APPLY_TASKS:
            tools = menu.query(lessons, _features(t)) if src else []
            tools_seen.update(x["concept"] for x in tools)
            if (t["name"], rep) in done:
                continue
            r = runner.run_once(t["task"], CRITERIA, _features(t),
                                model=MODELS[perf],
                                audience_model=AUDIENCE[perf],
                                landscape=tools,
                                evidence_checks=t["checks"])
            row = {"phase": "apply", "cell": name, "task": t["name"],
                   "rule_class": t["rule_class"], "rep": rep,
                   "run_id": r["run_id"], "tools": len(tools),
                   "verdict": r["verdict"], "ev": ev_fraction(r["evidence"]),
                   "checks": {c["call"]: bool(c["ok"]) for c in
                              (r["evidence"] or {}).get("results") or []}}
            _row(row)
            rows.append(row)
            _p(f"cell {name} rep {rep} ({t['name']}): "
               f"verdict={r['verdict']} ev={row['ev']:.2f} "
               f"tools={len(tools)}")
    by_class = {}
    for x in rows:
        by_class.setdefault(x["rule_class"], []).append(x["ev"])
    return {"cell": name, "tools": len(tools_seen), "n": len(rows),
            "pass_rate": _mean([1.0 if x["verdict"] == "pass" else 0.0
                                for x in rows]),
            "ev_mean": _mean([x["ev"] for x in rows]),
            "per_class": {c: {"n": len(v), "ev_mean": _mean(v)}
                          for c, v in sorted(by_class.items())}}


def main(repeats=1, resume_ts=None):
    prior_rows = []
    if resume_ts:
        _set_ts(resume_ts)
        prior_rows = _load_rows()
        _p(f"RESUME {_TS}: {len(prior_rows)} checkpointed rows found")
    per_cell_n = len(APPLY_TASKS) * repeats
    _p(f"TRANSFER PROBE {_TS} (contrastive lessons, rule classes)")
    _p(f"A={MODELS['A']}  B={MODELS['B']}  generator={GENERATOR} (fixed)")
    _p(f"apply pool={len(APPLY_TASKS)} tasks  repeats={repeats}  "
       f"per-cell n={per_cell_n}  gen pool={len(GEN_TASKS)} tasks x R_G={R_G}")
    accounting = {k: gen_lessons(k, prior_rows) for k in ("A", "B")}
    counts = {k: len(lesson.load(store(k))) for k in ("A", "B")}

    cells = []
    for perf in ("A", "B"):
        for src in (None, "A", "B"):
            cells.append(run_cell(perf, src, repeats=repeats,
                                  prior_rows=prior_rows))

    per_class = {}
    for c in cells:
        for cls, agg in c["per_class"].items():
            per_class.setdefault(cls, {})[c["cell"]] = agg
    # the checkpoint rows are the single source, so resume-completed runs
    # land in the check-level readout too
    checks = check_table(_load_rows())

    report = {
        "probe_id": _TS, "models": MODELS, "audience": AUDIENCE,
        "generator": GENERATOR, "r_g": R_G,
        "gen_accounting": accounting, "lesson_counts": counts,
        "apply_pool": [t["name"] for t in APPLY_TASKS],
        "repeats": repeats, "per_cell_n": per_cell_n, "cells": cells,
        "per_class": per_class, "check_table": checks,
        "n_note": (f"{len(APPLY_TASKS)} apply tasks x {repeats} repeats = "
                   f"n={per_cell_n} per cell. Per-class n is per-cell and "
                   f"smaller, stated in per_class. Direction at this n, "
                   f"not rates. Volume decides."),
    }
    with open(_REPORT, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    _p("== MATRIX (ev_mean / pass_rate, rows=performer, cols=lessons) ==")
    for perf in ("A", "B"):
        line = [f"{perf}:"]
        for src in ("none", "A", "B"):
            c = next(x for x in cells if x["cell"] == f"{perf}|{src}")
            line.append(f"{src}={c['ev_mean']:.2f}/{c['pass_rate']:.2f}")
        _p("  " + "  ".join(line))
    _p("== PER-CLASS (ev_mean, cells as perf|src, n in parens) ==")
    for cls in sorted(per_class):
        line = [f"{cls}:"]
        for perf in ("A", "B"):
            for src in ("none", "A", "B"):
                agg = per_class[cls].get(f"{perf}|{src}")
                if agg:
                    line.append(f"{perf}|{src}={agg['ev_mean']:.2f}"
                                f"({agg['n']})")
        _p("  " + "  ".join(line))
    _p("== RULE CHECKS (pass rate per cell, the treatment readout) ==")
    for tname in sorted(checks):
        for call, c in checks[tname].items():
            if not c["rule_check"]:
                continue
            rates = "  ".join(
                f"{cell}={c['cells'][cell]['rate']:.2f}"
                for cell in sorted(c["cells"]))
            _p(f"  {call}: {rates}")

    kinds = {}
    for k in ("A", "B"):
        kinds[k] = {"within_task": 0, "sibling": 0}
        for e in accounting[k]:
            for l in e["lessons"]:
                if l["committed"]:
                    kinds[k][l["type"]] += 1
    gate = (len(cells) == 6 and all(c["n"] == per_cell_n for c in cells)
            and os.path.exists(_ROWS) and bool(per_class) and bool(checks)
            and all(len(accounting[k]) == 4 for k in ("A", "B")))
    _p(f"GATE: {'PASSED' if gate else 'FAILED'}. six cells ran at "
       f"n={per_cell_n} each, every run checkpointed, per-class breakdown "
       f"and per-class contrast accounting present. Lessons committed "
       f"A={counts['A']} ({kinds['A']['within_task']} within-task, "
       f"{kinds['A']['sibling']} sibling), "
       f"B={counts['B']} ({kinds['B']['within_task']} within-task, "
       f"{kinds['B']['sibling']} sibling). A thin store is a finding, "
       f"not a failure, and the accounting is in the report.")


if __name__ == "__main__":
    main(repeats=int(sys.argv[1]) if len(sys.argv) > 1 else 1,
         resume_ts=sys.argv[2] if len(sys.argv) > 2 else None)
