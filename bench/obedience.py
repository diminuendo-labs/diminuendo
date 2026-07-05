"""PACKET-007, work item 2: the qwen delivery decomposition.

PACKET-006 measured menu harm on qwen carried by the one recipe-shaped
lesson. This decomposes the harm: same rule content, two shapes (concept
and recipe), delivered through the production menu to qwen on a matched
task (range_summary, distinctness) and a deliberately contradicting task
(most_common_word, whose alphabetical tie rule contradicts the tie
lessons' last direction, direction pin stripped in the packet-local
copies so the menu serves them). Three arms per task: none,
menu_concept, menu_recipe. The none baselines run at double R because
both comparisons anchor on them.

The materials are hand-authored, provenance hand, and live only in the
packet-local store. The recipe variants are deliberately gate-violating
instruments: the loader checks structure and labels and does NOT run
lesson.validate, because the current gates (correctly) refuse recipe
shapes and this experiment exists to measure exactly that hazard. The
shapes ride in the concept field because the menu delivers concept plus
applies_when and nothing else; the rule fields carry the same shapes for
store faithfulness. See the packet RESULTS for what that implies.

The pre-registered reading lives in the packet and is applied in RESULTS
by the reader. The harness reports, it does not rule.
"""

import json
import os
import sys
import time

import menu
import runner
from probe_tasks import APPLY_TASKS, CRITERIA, FEATURES

PERFORMER = "qwen2.5-coder:7b"
AUDIENCE = "llama3.1:8b"
ARMS = ("none", "menu_concept", "menu_recipe")
R_NONE = 24
R_MENU = 12

TASK_TOPIC = {"range_summary": "distinctness", "most_common_word": "tie"}

STORE = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                     "packets", "PACKET-007-lessons.jsonl")

_TASKS = {t["name"]: t for t in APPLY_TASKS}

_TS = time.strftime("%Y%m%d-%H%M%S")
_LOG = os.path.join(runner.RUNS, f"obedience-{_TS}.log")
_ROWS = os.path.join(runner.RUNS, f"obedience-{_TS}.rows.jsonl")
_REPORT = os.path.join(runner.RUNS, f"obedience-{_TS}.report.json")


def _set_ts(ts):
    """Rebind the run id and its file paths. Resume reuses a prior id so
    the checkpoint rows, the log, and the report stay one record."""
    global _TS, _LOG, _ROWS, _REPORT
    _TS = ts
    _LOG = os.path.join(runner.RUNS, f"obedience-{_TS}.log")
    _ROWS = os.path.join(runner.RUNS, f"obedience-{_TS}.rows.jsonl")
    _REPORT = os.path.join(runner.RUNS, f"obedience-{_TS}.report.json")


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


def ev_fraction(ev):
    results = (ev or {}).get("results") or []
    if not results:
        return 0.0
    return sum(1 for r in results if r["ok"]) / len(results)


def _features(t):
    f = {**FEATURES, "rule_class": t["rule_class"]}
    if "stated_direction" in t:
        f["stated_direction"] = t["stated_direction"]
    return f


def load_materials():
    """The four hand-authored variants, structure-checked and
    label-checked. lesson.validate is deliberately NOT run here: the
    recipe variants exist to measure the hazard the gates now refuse."""
    lessons = []
    with open(STORE, encoding="utf-8") as f:
        for line in f:
            if line.strip():
                lessons.append(json.loads(line))
    if len(lessons) != 4:
        raise SystemExit(f"store must hold 4 variants, found {len(lessons)}")
    labels = {(l.get("topic"), l.get("shape")) for l in lessons}
    expect = {("distinctness", "concept"), ("distinctness", "recipe"),
              ("tie", "concept"), ("tie", "recipe")}
    if labels != expect:
        raise SystemExit(f"variant labels wrong: {sorted(labels)}")
    for l in lessons:
        if l.get("provenance") != "hand":
            raise SystemExit("every variant must carry provenance hand")
        if l["topic"] == "tie":
            if l["applies_when"].get("stated_direction") != "*":
                raise SystemExit("tie variants must strip the direction pin")
            if not l.get("deliberately_mismatched"):
                raise SystemExit("tie variants must be labeled mismatched")
    return {(l["topic"], l["shape"]): l for l in lessons}


def run_task(name, variants, prior_rows=None):
    """One task, all three arms. Runs already checkpointed by an
    interrupted run are counted, not repeated."""
    t = _TASKS[name]
    topic = TASK_TOPIC[name]
    prior = [r for r in prior_rows or [] if r.get("task") == name]
    done = {(r["arm"], r["rep"]) for r in prior}
    if prior:
        _p(f"{name}: resuming past {len(prior)} checkpointed runs")
    rows = list(prior)
    for arm in ARMS:
        repeats = R_NONE if arm == "none" else R_MENU
        for rep in range(repeats):
            if (arm, rep) in done:
                continue
            tools = []
            if arm != "none":
                shape = arm.split("_", 1)[1]
                variant = variants[(topic, shape)]
                tools = menu.query([variant], _features(t))
                if len(tools) != 1:
                    raise SystemExit(f"{name} {arm}: expected exactly one "
                                     f"tool, got {len(tools)}")
            r = runner.run_once(t["task"], CRITERIA, _features(t),
                                model=PERFORMER, audience_model=AUDIENCE,
                                landscape=tools or None,
                                evidence_checks=t["checks"])
            row = {"task": name, "topic": topic, "arm": arm, "rep": rep,
                   "mismatched": bool(variants[(topic, "concept")].get(
                       "deliberately_mismatched")) if arm != "none"
                   else None,
                   "run_id": r["run_id"], "verdict": r["verdict"],
                   "tools": len(tools),
                   "tool_concepts": [x["concept"] for x in tools],
                   "ev": ev_fraction(r["evidence"]),
                   "checks": {c["call"]: bool(c["ok"]) for c in
                              (r["evidence"] or {}).get("results") or []}}
            _row(row)
            rows.append(row)
            _p(f"{name} {arm} rep {rep}: ev={row['ev']:.2f} "
               f"tools={row['tools']}")
    return rows


def check_table(rows):
    """Per task, per check, per arm: pass rate, rule checks marked. The
    non-rule checks are the harm column."""
    table = {}
    for r in rows:
        rule_checks = set(_TASKS[r["task"]].get("rule_checks", []))
        for call, ok in (r.get("checks") or {}).items():
            cell = (table.setdefault(r["task"], {})
                    .setdefault(call, {"rule_check": call in rule_checks,
                                       "arms": {}})
                    ["arms"].setdefault(r["arm"], {"n": 0, "passed": 0}))
            cell["n"] += 1
            cell["passed"] += 1 if ok else 0
    for t in table.values():
        for c in t.values():
            for a in c["arms"].values():
                a["rate"] = a["passed"] / a["n"] if a["n"] else 0.0
    return table


def pooled_rule_checks(rows):
    pooled = {}
    for r in rows:
        rule_checks = set(_TASKS[r["task"]].get("rule_checks", []))
        for call, ok in (r.get("checks") or {}).items():
            if call not in rule_checks:
                continue
            cell = (pooled.setdefault(r["task"], {})
                    .setdefault(r["arm"], {"n": 0, "passed": 0}))
            cell["n"] += 1
            cell["passed"] += 1 if ok else 0
    for p in pooled.values():
        for a in p.values():
            a["rate"] = a["passed"] / a["n"] if a["n"] else 0.0
    return pooled


def main(resume_ts=None):
    prior_rows = []
    if resume_ts:
        _set_ts(resume_ts)
        prior_rows = _load_rows()
        _p(f"RESUME {_TS}: {len(prior_rows)} checkpointed rows found")
    variants = load_materials()
    total = len(TASK_TOPIC) * (R_NONE + 2 * R_MENU)
    _p(f"OBEDIENCE DECOMPOSITION {_TS} (PACKET-007)")
    _p(f"performer={PERFORMER}  audience={AUDIENCE} (v1, production)")
    _p(f"tasks={sorted(TASK_TOPIC)}  arms={ARMS}  "
       f"R none={R_NONE} menu={R_MENU}  total runs={total}")
    all_rows = []
    for name in sorted(TASK_TOPIC):
        all_rows.extend(run_task(name, variants, prior_rows))

    table = check_table(all_rows)
    pooled = pooled_rule_checks(all_rows)
    armed = [r for r in all_rows if r["arm"] != "none"]
    tools_ok = all(r["tools"] == 1 for r in armed)

    report = {
        "obedience_id": _TS, "performer": PERFORMER, "audience": AUDIENCE,
        "arms": ARMS, "r_none": R_NONE, "r_menu": R_MENU,
        "tasks": TASK_TOPIC,
        "variants": {f"{k[0]}/{k[1]}": {"concept": v["concept"],
                                        "rule": v["rule"],
                                        "applies_when": v["applies_when"]}
                     for k, v in variants.items()},
        "check_table": table, "pooled_rule_checks": pooled,
        "tools_always_one_when_armed": tools_ok,
        "n_note": (f"none arms n={R_NONE}, menu arms n={R_MENU} per check "
                   f"cell. The reading rules live in the packet and are "
                   f"applied in its RESULTS, not here."),
    }
    with open(_REPORT, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    _p("== POOLED RULE CHECKS (passed/n per arm) ==")
    for name in sorted(pooled):
        cells = "  ".join(
            f"{a}={pooled[name][a]['passed']}/{pooled[name][a]['n']}"
            for a in ARMS if a in pooled[name])
        _p(f"  {name}: {cells}")
    _p("== PER-CHECK (none / menu_concept / menu_recipe) ==")
    for name in sorted(table):
        for call, c in table[name].items():
            rates = " / ".join(
                f"{c['arms'].get(a, {}).get('rate', 0.0):.2f}"
                for a in ARMS)
            mark = "  <-- rule" if c["rule_check"] else ""
            _p(f"  {call}: {rates}{mark}")

    counts_ok = all(
        sum(1 for r in all_rows if r["task"] == name and r["arm"] == arm)
        == (R_NONE if arm == "none" else R_MENU)
        for name in TASK_TOPIC for arm in ARMS)
    gate = counts_ok and tools_ok and os.path.exists(_ROWS)
    _p(f"GATE: {'PASSED' if gate else 'FAILED'}. both tasks, three arms "
       f"at stated R, every armed run carried exactly one tool, every "
       f"run checkpointed, report persisted. The reading is applied in "
       f"the packet RESULTS.")


if __name__ == "__main__":
    main(resume_ts=sys.argv[1] if len(sys.argv) > 1 else None)
