"""PACKET-011: the reverse cell. The single most informative unmeasured
cell in the record, made reachable by PACKET-010's conjunction-filtered
supply: two llama-origin tie lessons, fully pinned, delivered to qwen on
longest_word through the production menu.

Two pre-registered questions in one run, read independently: does
transfer run in the reverse direction (llama teaching qwen), and does
the amplifier seat under matched, fully pinned tools gain without harm.
Arms none and menu, R=12 per arm, one task, detached, checkpointed,
resume-capable. The reading rules live in the packet and are applied in
its RESULTS by the reader. The harness reports, it does not rule."""

import json
import os
import sys
import time

import lesson
import menu
import runner
from probe_tasks import APPLY_TASKS, CRITERIA, FEATURES

PERFORMER = "qwen2.5-coder:7b"
AUDIENCE = "llama3.1:8b"
TASK = "longest_word"
ARMS = ("none", "menu")
R = 12

STORE = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                     "packets", "PACKET-011-lessons_B.jsonl")
STORE_SIZE = 2

_TASKS = {t["name"]: t for t in APPLY_TASKS}

_TS = time.strftime("%Y%m%d-%H%M%S")
_LOG = os.path.join(runner.RUNS, f"reverse-{_TS}.log")
_ROWS = os.path.join(runner.RUNS, f"reverse-{_TS}.rows.jsonl")
_REPORT = os.path.join(runner.RUNS, f"reverse-{_TS}.report.json")


def _set_ts(ts):
    """Rebind the run id and its file paths. Resume reuses a prior id so
    the checkpoint rows, the log, and the report stay one record."""
    global _TS, _LOG, _ROWS, _REPORT
    _TS = ts
    _LOG = os.path.join(runner.RUNS, f"reverse-{_TS}.log")
    _ROWS = os.path.join(runner.RUNS, f"reverse-{_TS}.rows.jsonl")
    _REPORT = os.path.join(runner.RUNS, f"reverse-{_TS}.report.json")


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
    if "rule_topic" in t:
        f["rule_topic"] = t["rule_topic"]
    if "stated_direction" in t:
        f["stated_direction"] = t["stated_direction"]
    return f


def load_store():
    """The packet-local copy of the 081801 B store, size-checked, every
    lesson through the full gates. A failure here means the materials
    were touched."""
    lessons = lesson.load(STORE)
    if len(lessons) != STORE_SIZE:
        raise SystemExit(f"store must hold {STORE_SIZE} lessons, "
                         f"found {len(lessons)}")
    for l in lessons:
        lesson.validate(l)
    return lessons


def run_arms(repeats=R, prior_rows=None):
    t = _TASKS[TASK]
    lessons = load_store()
    prior = list(prior_rows or [])
    done = {(r["arm"], r["rep"]) for r in prior}
    if prior:
        _p(f"resuming past {len(prior)} checkpointed runs")
    rows = list(prior)
    for arm in ARMS:
        for rep in range(repeats):
            if (arm, rep) in done:
                continue
            tools = []
            if arm == "menu":
                tools = menu.query(lessons, _features(t))
                if not tools:
                    raise SystemExit("armed run delivered no tools, the "
                                     "instrument is broken")
            r = runner.run_once(t["task"], CRITERIA, _features(t),
                                model=PERFORMER, audience_model=AUDIENCE,
                                landscape=tools or None,
                                evidence_checks=t["checks"])
            row = {"arm": arm, "task": TASK, "rep": rep,
                   "run_id": r["run_id"], "verdict": r["verdict"],
                   "tools": len(tools),
                   "tool_concepts": [x["concept"] for x in tools],
                   "ev": ev_fraction(r["evidence"]),
                   "checks": {c["call"]: bool(c["ok"]) for c in
                              (r["evidence"] or {}).get("results") or []}}
            _row(row)
            rows.append(row)
            _p(f"{arm} rep {rep}: ev={row['ev']:.2f} tools={row['tools']}")
    return rows


def check_table(rows):
    rule_checks = set(_TASKS[TASK].get("rule_checks", []))
    table = {}
    for r in rows:
        for call, ok in (r.get("checks") or {}).items():
            cell = (table.setdefault(call,
                                     {"rule_check": call in rule_checks,
                                      "arms": {}})
                    ["arms"].setdefault(r["arm"], {"n": 0, "passed": 0}))
            cell["n"] += 1
            cell["passed"] += 1 if ok else 0
    for c in table.values():
        for a in c["arms"].values():
            a["rate"] = a["passed"] / a["n"] if a["n"] else 0.0
    return table


def pooled_rule_checks(rows):
    rule_checks = set(_TASKS[TASK].get("rule_checks", []))
    pooled = {}
    for r in rows:
        for call, ok in (r.get("checks") or {}).items():
            if call not in rule_checks:
                continue
            cell = pooled.setdefault(r["arm"], {"n": 0, "passed": 0})
            cell["n"] += 1
            cell["passed"] += 1 if ok else 0
    for a in pooled.values():
        a["rate"] = a["passed"] / a["n"] if a["n"] else 0.0
    return pooled


def main(repeats=R, resume_ts=None):
    prior_rows = []
    if resume_ts:
        _set_ts(resume_ts)
        prior_rows = _load_rows()
        _p(f"RESUME {_TS}: {len(prior_rows)} checkpointed rows found")
    lessons = load_store()
    _p(f"REVERSE CELL {_TS} (PACKET-011)")
    _p(f"performer={PERFORMER}  audience={AUDIENCE} (v1, production)")
    _p(f"task={TASK}  arms={ARMS}  R={repeats}  "
       f"lessons={len(lessons)} llama-origin, pins live")

    rows = run_arms(repeats, prior_rows)
    table = check_table(rows)
    pooled = pooled_rule_checks(rows)
    armed = [r for r in rows if r["arm"] == "menu"]
    min_tools = min((r["tools"] for r in armed), default=0)

    report = {
        "reverse_id": _TS, "performer": PERFORMER, "audience": AUDIENCE,
        "task": TASK, "arms": ARMS, "repeats": repeats,
        "lessons": [{"concept": l["concept"], "rule": l["rule"],
                     "applies_when": l["applies_when"],
                     "trail": {k: l["trail"].get(k) for k in
                               ("gen_task", "contrast_type")}}
                    for l in lessons],
        "check_table": table, "pooled_rule_checks": pooled,
        "min_tools_armed": min_tools,
        "n_note": (f"R={repeats} per arm, one task, per-check cells are "
                   f"n={repeats}. The reading rules live in the packet "
                   f"and are applied in its RESULTS, not here."),
    }
    with open(_REPORT, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    _p("== POOLED RULE CHECKS (passed/n per arm) ==")
    for arm in ARMS:
        if arm in pooled:
            _p(f"  {arm}: {pooled[arm]['passed']}/{pooled[arm]['n']}")
    _p("== PER-CHECK (none / menu) ==")
    for call, c in table.items():
        rates = " / ".join(f"{c['arms'].get(a, {}).get('rate', 0.0):.2f}"
                           for a in ARMS)
        mark = "  <-- rule" if c["rule_check"] else ""
        _p(f"  {call}: {rates}{mark}")

    counts_ok = all(
        sum(1 for r in rows if r["arm"] == a) == repeats for a in ARMS)
    gate = (counts_ok and min_tools > 0 and os.path.exists(_ROWS))
    _p(f"GATE: {'PASSED' if gate else 'FAILED'}. both arms at "
       f"R={repeats}, every armed run carried tools (min={min_tools}), "
       f"every run checkpointed, report persisted. The reading is applied "
       f"in the packet RESULTS.")


if __name__ == "__main__":
    main(repeats=int(sys.argv[1]) if len(sys.argv) > 1 else R,
         resume_ts=sys.argv[2] if len(sys.argv) > 2 else None)
