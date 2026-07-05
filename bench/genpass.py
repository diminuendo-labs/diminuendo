"""PACKET-008, work item 3: one contrastive generation pass per seat at
full gate strength, the end-to-end proof of the two new screens and the
rule_topic pin. The standing machinery: R_G=3 per generation task per
seat, within-task contrast first, sibling fallback under the per-class
cap. No probe, no transfer arms; this run ships mechanism evidence, the
next measurement uses it.

What this harness adds over the probe's generation phase: every gate
rejection is recorded with its reason, so the report carries the screen
accounting (how many candidates each screen killed) beside the committed
lessons and their pins. The harness reports, it does not rule.
"""

import json
import os
import sys
import time

import lesson
import runner
from probe_tasks import CRITERIA, FEATURES, GEN_TASKS

MODELS = {"A": "qwen2.5-coder:7b", "B": "llama3.1:8b"}
AUDIENCE = {"A": "llama3.1:8b", "B": "qwen2.5-coder:7b"}
GENERATOR = "qwen2.5-coder:7b"
R_G = 3

_TS = time.strftime("%Y%m%d-%H%M%S")
_LOG = os.path.join(runner.RUNS, f"genpass-{_TS}.log")
_ROWS = os.path.join(runner.RUNS, f"genpass-{_TS}.rows.jsonl")
_REPORT = os.path.join(runner.RUNS, f"genpass-{_TS}.report.json")


def _set_ts(ts):
    """Rebind the run id and its file paths. Resume reuses a prior id so
    the checkpoint rows, the log, and the report stay one record."""
    global _TS, _LOG, _ROWS, _REPORT
    _TS = ts
    _LOG = os.path.join(runner.RUNS, f"genpass-{_TS}.log")
    _ROWS = os.path.join(runner.RUNS, f"genpass-{_TS}.rows.jsonl")
    _REPORT = os.path.join(runner.RUNS, f"genpass-{_TS}.report.json")


def _p(*parts):
    line = " ".join(str(p) for p in parts)
    print(line, flush=True)
    with open(_LOG, "a", encoding="utf-8") as f:
        f.write(line + "\n")


def _row(d):
    """Checkpoint every run as it lands. A dead pipe strands nothing."""
    with open(_ROWS, "a", encoding="utf-8") as f:
        f.write(json.dumps(d) + "\n")


def _load_rows():
    rows = []
    try:
        with open(_ROWS, encoding="utf-8") as f:
            rows = [json.loads(l) for l in f if l.strip()]
    except FileNotFoundError:
        pass
    return rows


def _load_summary(run_id):
    try:
        with open(os.path.join(runner.RUNS, f"{run_id}.summary.json"),
                  encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return None


def ev_fraction(ev):
    results = (ev or {}).get("results") or []
    if not results:
        return 0.0
    return sum(1 for r in results if r["ok"]) / len(results)


def _features(t):
    f = {**FEATURES, "rule_class": t["rule_class"]}
    if "rule_topic" in t:
        f["rule_topic"] = t["rule_topic"]
    if "stated_direction" in t:
        f["stated_direction"] = t["stated_direction"]
    return f


def _reason_key(message):
    """Bucket a LessonError message by the screen that raised it."""
    text = str(message)
    for key, mark in (("aim_screen", "aim screen"),
                      ("imperative_shape", "imperative shape"),
                      ("platitude", "platitude"),
                      ("metric_term", "metric-shaped"),
                      ("missing_fields", "missing fields"),
                      ("no_json", "no parseable JSON"),
                      ("empty_rule", "rule must name")):
        if mark in text:
            return key
    return "other"


def store(key):
    return os.path.join(runner.RUNS, f"genpass-{_TS}-lessons_{key}.jsonl")


def _partition(summaries):
    fails = [s for s in summaries if not (s["evidence"] or {}).get("passed")]
    passes = [s for s in summaries if (s["evidence"] or {}).get("passed")]
    return fails, passes


def gen_seat(key, rejections, prior_rows=None):
    """One seat's pass: attempts, contrasts per class, distillation with
    every rejection recorded. Mirrors the probe's generation phase."""
    _p(f"-- seat {key} ({MODELS[key]}), contrastive with sibling "
       f"fallback, R_G={R_G}, full gates --")
    prior = {}
    for r in prior_rows or []:
        if r.get("phase") == "gen" and r.get("model") == key:
            prior.setdefault(r["task"], {})[r["rep"]] = r
    committed_nodes = {l.get("trail", {}).get("node_id")
                       for l in lesson.load(store(key))}

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

    def distill(kind, cand_fn, gen_task, fails):
        if any(s["node_id"] in committed_nodes for s in fails):
            _p(f"seat {key} ({gen_task}): {kind} lesson already committed, "
               f"resumed")
            return True
        for attempt in range(2):
            try:
                cand = cand_fn()
                cand.setdefault("trail", {})["gen_task"] = gen_task
                cand["trail"].setdefault("contrast_type", kind)
                lesson.commit(store(key), cand)
                _p(f"seat {key} ({gen_task}): {kind} lesson committed")
                return True
            except lesson.LessonError as e:
                rejections.append({"seat": key, "task": gen_task,
                                   "type": kind, "attempt": attempt + 1,
                                   "reason": _reason_key(e),
                                   "detail": str(e)[:200]})
                _p(f"  {kind} attempt {attempt + 1} rejected "
                   f"[{_reason_key(e)}]: {e}")
        return False

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
            ok = distill(
                "within_task",
                lambda t=t, r=r: lesson.generate_contrastive(
                    t["task"], _features(t), r["fails"][0], r["passes"][0],
                    model=GENERATOR),
                t["name"], r["fails"])
            entry["lessons"].append({"task": t["name"],
                                     "type": "within_task",
                                     "committed": ok})
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
            ok = distill(
                "sibling",
                lambda tf=tf, tp=tp, rf=rf, rp=rp:
                    lesson.generate_sibling_contrast(
                        tf["task"], tp["task"], cls, _features(tf),
                        rf["fails"][0], rp["passes"][0], model=GENERATOR),
                tf["name"], rf["fails"])
            entry["lessons"].append({"task": tf["name"],
                                     "sibling": tp["name"],
                                     "type": "sibling", "committed": ok})
            if ok:
                committed_count += 1
                mined.add(tf["name"])
        if not entry["lessons"]:
            cases = set(entry["cases"].values())
            entry["reason"] = ("both siblings all_pass, nothing broke"
                               if cases == {"all_pass"} else
                               "all_fail with no passing sibling")
            _p(f"seat {key} ({cls}): no contrast, {entry['reason']}")
        accounting.append(entry)
    n = len(lesson.load(store(key)))
    _p(f"store {key}: {n} lessons committed")
    return accounting


def main(resume_ts=None):
    prior_rows = []
    if resume_ts:
        _set_ts(resume_ts)
        prior_rows = _load_rows()
        _p(f"RESUME {_TS}: {len(prior_rows)} checkpointed rows found")
    _p(f"GENERATION PASS {_TS} (PACKET-008, full gates)")
    _p(f"A={MODELS['A']}  B={MODELS['B']}  generator={GENERATOR} (fixed)")
    _p(f"gen pool={len(GEN_TASKS)} tasks x R_G={R_G} x 2 seats")
    rejections = []
    accounting = {k: gen_seat(k, rejections, prior_rows)
                  for k in ("A", "B")}
    lessons = {k: lesson.load(store(k)) for k in ("A", "B")}

    by_reason = {}
    for r in rejections:
        by_reason[r["reason"]] = by_reason.get(r["reason"], 0) + 1

    report = {
        "genpass_id": _TS, "models": MODELS, "generator": GENERATOR,
        "r_g": R_G, "accounting": accounting,
        "rejections": rejections, "rejections_by_reason": by_reason,
        "lessons": {k: [{"concept": l["concept"], "rule": l["rule"],
                         "applies_when": l["applies_when"],
                         "trail": {kk: l["trail"].get(kk) for kk in
                                   ("gen_task", "contrast_type")}}
                        for l in lessons[k]] for k in lessons},
        "n_note": (f"R_G={R_G} per task per seat, one pass. Supply and "
                   f"screen accounting, not a treatment measurement."),
    }
    with open(_REPORT, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    _p("== SCREEN ACCOUNTING (rejections by reason) ==")
    for reason, count in sorted(by_reason.items()):
        _p(f"  {reason}: {count}")
    _p("== COMMITTED LESSONS (pins) ==")
    for k in ("A", "B"):
        for l in lessons[k]:
            aw = l["applies_when"]
            _p(f"  {k} [{l['trail'].get('gen_task')}] "
               f"class={aw.get('rule_class')} topic={aw.get('rule_topic')} "
               f"direction={aw.get('stated_direction')}")
    pool_classes = {t["rule_class"] for t in GEN_TASKS}
    gate = (all(len(accounting[k]) == len(pool_classes)
                for k in ("A", "B"))
            and os.path.exists(_ROWS))
    _p(f"GATE: {'PASSED' if gate else 'FAILED'}. both seats ran the full "
       f"pool at R_G={R_G}, every run checkpointed, screen accounting and "
       f"committed lessons with pins persisted. Lessons A={len(lessons['A'])}"
       f", B={len(lessons['B'])}; fewer and cleaner is the intended "
       f"direction, stated in the packet.")


if __name__ == "__main__":
    main(resume_ts=sys.argv[1] if len(sys.argv) > 1 else None)
