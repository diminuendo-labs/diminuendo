"""PACKET-013: the task-and-topic contrast. One seat, two tasks, one
interleaved run, the drift doctrine executed: same-run baselines only,
sub-drift gaps claim nothing.

Four cells, R=12 each, interleaved by rep in the fixed order L-none,
L-prod, R-none, R-hand, so time-of-run effects land evenly across all
four. L-prod rides the two llama-origin tie lessons byte-copied from
PACKET-012's store; R-hand rides the PACKET-007 concept-shape
distinctness lesson byte-copied from its packet store, which carries
confidence and provenance and therefore loads through the production
path. Both byte checks are asserted at load and reported.

The four signed readings live in the packet and are applied in its
RESULTS by the reader. The harness reports, it does not rule."""

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
R = 12

_PACKETS = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        "packets")
PROD_STORE = os.path.join(_PACKETS, "PACKET-013-lessons_prod.jsonl")
PROD_SOURCE = os.path.join(_PACKETS, "PACKET-012-lessons_prod.jsonl")
HAND_STORE = os.path.join(_PACKETS, "PACKET-013-lesson_hand.jsonl")
HAND_SOURCE = os.path.join(_PACKETS, "PACKET-007-lessons.jsonl")

# the fixed interleave order, logged per rep
CELLS = (
    {"id": "L-none", "task": "longest_word", "store": None},
    {"id": "L-prod", "task": "longest_word", "store": "prod"},
    {"id": "R-none", "task": "range_summary", "store": None},
    {"id": "R-hand", "task": "range_summary", "store": "hand"},
)
EXPECT_TOOLS = {"L-none": 0, "L-prod": 2, "R-none": 0, "R-hand": 1}

_TASKS = {t["name"]: t for t in APPLY_TASKS}

_TS = time.strftime("%Y%m%d-%H%M%S")
_LOG = os.path.join(runner.RUNS, f"contrast13-{_TS}.log")
_ROWS = os.path.join(runner.RUNS, f"contrast13-{_TS}.rows.jsonl")
_REPORT = os.path.join(runner.RUNS, f"contrast13-{_TS}.report.json")


def _set_ts(ts):
    """Rebind the run id and its file paths. Resume reuses a prior id so
    the checkpoint rows, the log, and the report stay one record."""
    global _TS, _LOG, _ROWS, _REPORT
    _TS = ts
    _LOG = os.path.join(runner.RUNS, f"contrast13-{_TS}.log")
    _ROWS = os.path.join(runner.RUNS, f"contrast13-{_TS}.rows.jsonl")
    _REPORT = os.path.join(runner.RUNS, f"contrast13-{_TS}.report.json")


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


def byte_checks():
    """Both packet-local stores byte-checked against their sources
    before any arm runs. The hand source check finds the exact line."""
    with open(PROD_STORE, "rb") as f:
        prod_bytes = f.read()
    with open(PROD_SOURCE, "rb") as f:
        prod_ok = f.read() == prod_bytes
    with open(HAND_STORE, "rb") as f:
        hand_bytes = f.read()
    with open(HAND_SOURCE, "rb") as f:
        hand_ok = hand_bytes in f.read()
    if not (prod_ok and hand_ok):
        raise SystemExit(f"byte check failed: prod={prod_ok} "
                         f"hand={hand_ok}, the materials were touched")
    return {"prod_byte_identical": prod_ok,
            "hand_line_byte_identical": hand_ok}


def load_stores():
    prod = lesson.load(PROD_STORE)
    if len(prod) != 2:
        raise SystemExit(f"prod store must hold 2 lessons, "
                         f"found {len(prod)}")
    hand = lesson.load(HAND_STORE)
    if len(hand) != 1:
        raise SystemExit(f"hand store must hold 1 lesson, "
                         f"found {len(hand)}")
    for l in prod:
        lesson.validate(l)
    lesson.validate(hand[0])
    return {"prod": prod, "hand": hand}


def cell_tools(cell, stores):
    if cell["store"] is None:
        return []
    t = _TASKS[cell["task"]]
    tools = menu.query(stores[cell["store"]], _features(t))
    if len(tools) != EXPECT_TOOLS[cell["id"]]:
        raise SystemExit(f"{cell['id']}: expected "
                         f"{EXPECT_TOOLS[cell['id']]} tools, "
                         f"got {len(tools)}")
    return tools


def run_cells(repeats=R, prior_rows=None):
    stores = load_stores()
    prior = list(prior_rows or [])
    done = {(r["cell"], r["rep"]) for r in prior}
    if prior:
        _p(f"resuming past {len(prior)} checkpointed runs")
    rows = list(prior)
    for rep in range(repeats):
        for cell in CELLS:
            if (cell["id"], rep) in done:
                continue
            t = _TASKS[cell["task"]]
            tools = cell_tools(cell, stores)
            r = runner.run_once(t["task"], CRITERIA, _features(t),
                                model=PERFORMER, audience_model=AUDIENCE,
                                landscape=tools or None,
                                evidence_checks=t["checks"])
            row = {"cell": cell["id"], "task": cell["task"], "rep": rep,
                   "run_id": r["run_id"], "verdict": r["verdict"],
                   "tools": len(tools),
                   "tool_concepts": [x["concept"] for x in tools],
                   "ev": ev_fraction(r["evidence"]),
                   "checks": {c["call"]: bool(c["ok"]) for c in
                              (r["evidence"] or {}).get("results") or []}}
            _row(row)
            rows.append(row)
            _p(f"rep {rep} {cell['id']}: ev={row['ev']:.2f} "
               f"tools={row['tools']}")
    return rows


def check_table(rows):
    """Per task: per check per cell, rule checks marked. Each task reads
    only against its own same-run none cell."""
    table = {}
    for r in rows:
        rule_checks = set(_TASKS[r["task"]].get("rule_checks", []))
        for call, ok in (r.get("checks") or {}).items():
            cell = (table.setdefault(r["task"], {})
                    .setdefault(call, {"rule_check": call in rule_checks,
                                       "cells": {}})
                    ["cells"].setdefault(r["cell"], {"n": 0, "passed": 0}))
            cell["n"] += 1
            cell["passed"] += 1 if ok else 0
    for t in table.values():
        for c in t.values():
            for a in c["cells"].values():
                a["rate"] = a["passed"] / a["n"] if a["n"] else 0.0
    return table


def pooled_rule_checks(rows):
    pooled = {}
    for r in rows:
        rule_checks = set(_TASKS[r["task"]].get("rule_checks", []))
        for call, ok in (r.get("checks") or {}).items():
            if call not in rule_checks:
                continue
            cell = pooled.setdefault(r["cell"], {"n": 0, "passed": 0})
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
    checks = byte_checks()
    stores = load_stores()
    _p(f"TASK-AND-TOPIC CONTRAST {_TS} (PACKET-013)")
    _p(f"performer={PERFORMER}  audience={AUDIENCE} (v1, production)")
    _p(f"cells={[c['id'] for c in CELLS]}  R={repeats}  interleaved by "
       f"rep in that fixed order")
    _p(f"byte checks: prod={checks['prod_byte_identical']} "
       f"hand={checks['hand_line_byte_identical']}")

    rows = run_cells(repeats, prior_rows)
    table = check_table(rows)
    pooled = pooled_rule_checks(rows)
    audit_ok = all(r["tools"] == EXPECT_TOOLS[r["cell"]] for r in rows)

    report = {
        "contrast13_id": _TS, "performer": PERFORMER,
        "audience": AUDIENCE, "cells": [c["id"] for c in CELLS],
        "repeats": repeats, "byte_checks": checks,
        "prod_lessons": [{"concept": l["concept"], "rule": l["rule"]}
                         for l in stores["prod"]],
        "hand_lesson": {"concept": stores["hand"][0]["concept"],
                        "rule": stores["hand"][0]["rule"],
                        "provenance": stores["hand"][0]["provenance"]},
        "check_table": table, "pooled_rule_checks": pooled,
        "tool_audit_ok": audit_ok,
        "n_note": (f"R={repeats} per cell, interleaved. Each task reads "
                   f"only against its own same-run none cell. Gaps under "
                   f"4 of 24 claim nothing, per the drift doctrine. The "
                   f"four signed readings live in the packet and are "
                   f"applied in its RESULTS, not here."),
    }
    with open(_REPORT, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    _p("== POOLED RULE CHECKS (passed/n per cell) ==")
    for cell in CELLS:
        cid = cell["id"]
        if cid in pooled:
            _p(f"  {cid}: {pooled[cid]['passed']}/{pooled[cid]['n']}")
    _p("== PER-CHECK (per task, cells in run order) ==")
    for tname in sorted(table):
        cells_for_task = [c["id"] for c in CELLS if c["task"] == tname]
        for call, c in table[tname].items():
            rates = " / ".join(
                f"{c['cells'].get(cid, {}).get('rate', 0.0):.2f}"
                for cid in cells_for_task)
            mark = "  <-- rule" if c["rule_check"] else ""
            _p(f"  {call} ({' / '.join(cells_for_task)}): {rates}{mark}")

    counts_ok = all(
        sum(1 for r in rows if r["cell"] == c["id"]) == repeats
        for c in CELLS)
    gate = counts_ok and audit_ok and os.path.exists(_ROWS)
    _p(f"GATE: {'PASSED' if gate else 'FAILED'}. four cells at "
       f"R={repeats} interleaved, byte checks asserted, tool audit "
       f"{'clean' if audit_ok else 'BROKEN'}, every run checkpointed, "
       f"report persisted. The readings are applied in the packet "
       f"RESULTS.")


if __name__ == "__main__":
    main(repeats=int(sys.argv[1]) if len(sys.argv) > 1 else R,
         resume_ts=sys.argv[2] if len(sys.argv) > 2 else None)
