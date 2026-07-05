"""PACKET-012: the residue diagnosis. What harmed the amplifier.

Three arms on PACKET-011's exact cell (performer qwen, audience llama,
task longest_word, v1 production path, pins live), R=12 each:
- none: no tools, replicating the 0.67 baseline.
- prod: the two llama-origin tie lessons, packet-local verbatim,
  identical to PACKET-011's menu arm.
- hand: the conductor-authored residue-free lesson, used exactly as
  printed in the packet. The printed lesson carries no confidence and no
  provenance field, so the production load gates reject it and
  menu.query cannot rank it; per the packet's own contingency this is
  reported as a FINDINGS item and the arm runs with the lesson injected
  by the mechanism PACKET-007 used: the delivery surface receives
  exactly what the menu emits for a matched lesson, concept plus
  applies_when, after the public matcher confirms the match. The lesson
  text itself is never touched.

Four pre-registered readings with stated signs live in the packet and
are applied in its RESULTS by the reader. The harness reports, it does
not rule."""

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
ARMS = ("none", "prod", "hand")
R = 12

_PACKETS = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        "packets")
PROD_STORE = os.path.join(_PACKETS, "PACKET-012-lessons_prod.jsonl")
HAND_FILE = os.path.join(_PACKETS, "PACKET-012-lesson_hand.json")

_TASKS = {t["name"]: t for t in APPLY_TASKS}

_TS = time.strftime("%Y%m%d-%H%M%S")
_LOG = os.path.join(runner.RUNS, f"diagnose-{_TS}.log")
_ROWS = os.path.join(runner.RUNS, f"diagnose-{_TS}.rows.jsonl")
_REPORT = os.path.join(runner.RUNS, f"diagnose-{_TS}.report.json")


def _set_ts(ts):
    """Rebind the run id and its file paths. Resume reuses a prior id so
    the checkpoint rows, the log, and the report stay one record."""
    global _TS, _LOG, _ROWS, _REPORT
    _TS = ts
    _LOG = os.path.join(runner.RUNS, f"diagnose-{_TS}.log")
    _ROWS = os.path.join(runner.RUNS, f"diagnose-{_TS}.rows.jsonl")
    _REPORT = os.path.join(runner.RUNS, f"diagnose-{_TS}.report.json")


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


def load_prod():
    """The prod store, size-checked, through the full gates."""
    lessons = lesson.load(PROD_STORE)
    if len(lessons) != 2:
        raise SystemExit(f"prod store must hold 2 lessons, "
                         f"found {len(lessons)}")
    for l in lessons:
        lesson.validate(l)
    return lessons


def load_hand():
    """The hand lesson exactly as printed in the packet."""
    with open(HAND_FILE, encoding="utf-8") as f:
        return json.load(f)


def hand_gate_check(hand):
    """What the production gates say about the printed lesson, recorded
    for the FINDINGS item. Returns (validate_error, query_error)."""
    validate_error = None
    query_error = None
    try:
        lesson.validate(dict(hand))
    except lesson.LessonError as e:
        validate_error = str(e)
    try:
        menu.query([dict(hand)], _features(_TASKS[TASK]))
    except Exception as e:  # menu ranks by a field the lesson lacks
        query_error = f"{type(e).__name__}: {e}"
    return validate_error, query_error


def hand_tools(hand):
    """The PACKET-007 injection mechanism: the delivery surface gets
    exactly what the menu emits for a matched lesson, concept plus
    applies_when, after the public matcher confirms the match."""
    t = _TASKS[TASK]
    score = menu.matches(hand["applies_when"], _features(t))
    if score < 1:
        raise SystemExit("hand lesson does not match the task, "
                         "the instrument is broken")
    return [{"concept": hand["concept"],
             "applies_when": hand["applies_when"]}]


def arm_tools(arm, prod, hand):
    if arm == "none":
        return []
    if arm == "prod":
        tools = menu.query(prod, _features(_TASKS[TASK]))
        if len(tools) != 2:
            raise SystemExit(f"prod arm expected 2 tools, got {len(tools)}")
        return tools
    return hand_tools(hand)


def run_arms(repeats=R, prior_rows=None):
    t = _TASKS[TASK]
    prod = load_prod()
    hand = load_hand()
    prior = list(prior_rows or [])
    done = {(r["arm"], r["rep"]) for r in prior}
    if prior:
        _p(f"resuming past {len(prior)} checkpointed runs")
    rows = list(prior)
    for arm in ARMS:
        for rep in range(repeats):
            if (arm, rep) in done:
                continue
            tools = arm_tools(arm, prod, hand)
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
    prod = load_prod()
    hand = load_hand()
    validate_error, query_error = hand_gate_check(hand)
    _p(f"RESIDUE DIAGNOSIS {_TS} (PACKET-012)")
    _p(f"performer={PERFORMER}  audience={AUDIENCE} (v1, production)")
    _p(f"task={TASK}  arms={ARMS}  R={repeats}")
    _p(f"hand lesson gate check: validate={validate_error or 'passes'}; "
       f"menu.query={query_error or 'passes'}")

    rows = run_arms(repeats, prior_rows)
    table = check_table(rows)
    pooled = pooled_rule_checks(rows)
    armed = [r for r in rows if r["arm"] != "none"]
    audit_ok = all(
        (r["arm"] == "prod" and r["tools"] == 2)
        or (r["arm"] == "hand" and r["tools"] == 1)
        for r in armed)

    report = {
        "diagnose_id": _TS, "performer": PERFORMER, "audience": AUDIENCE,
        "task": TASK, "arms": ARMS, "repeats": repeats,
        "prod_lessons": [{"concept": l["concept"], "rule": l["rule"]}
                         for l in prod],
        "hand_lesson": hand,
        "hand_gate_check": {"validate": validate_error,
                            "menu_query": query_error},
        "check_table": table, "pooled_rule_checks": pooled,
        "tool_audit_ok": audit_ok,
        "n_note": (f"R={repeats} per arm, one task, per-check cells are "
                   f"n={repeats}. Directional results are leans, never "
                   f"rates. The four signed readings live in the packet "
                   f"and are applied in its RESULTS, not here."),
    }
    with open(_REPORT, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    _p("== POOLED RULE CHECKS (passed/n per arm) ==")
    for arm in ARMS:
        if arm in pooled:
            _p(f"  {arm}: {pooled[arm]['passed']}/{pooled[arm]['n']}")
    _p("== PER-CHECK (none / prod / hand) ==")
    for call, c in table.items():
        rates = " / ".join(f"{c['arms'].get(a, {}).get('rate', 0.0):.2f}"
                           for a in ARMS)
        mark = "  <-- rule" if c["rule_check"] else ""
        _p(f"  {call}: {rates}{mark}")

    counts_ok = all(
        sum(1 for r in rows if r["arm"] == a) == repeats for a in ARMS)
    gate = counts_ok and audit_ok and os.path.exists(_ROWS)
    _p(f"GATE: {'PASSED' if gate else 'FAILED'}. three arms at "
       f"R={repeats}, tool audit {'clean' if audit_ok else 'BROKEN'} "
       f"(prod=2, hand=1 on every armed run), every run checkpointed, "
       f"report persisted. The readings are applied in the packet "
       f"RESULTS.")


if __name__ == "__main__":
    main(repeats=int(sys.argv[1]) if len(sys.argv) > 1 else R,
         resume_ts=sys.argv[2] if len(sys.argv) > 2 else None)
