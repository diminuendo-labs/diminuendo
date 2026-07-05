"""PACKET-021: the reverse and parity replication. PACKET-015 re-run
whole with nothing varied, per the replication doctrine: the thesis
sentence at n=1 stays a lean until this run speaks.

Three cells on range_summary, R=12 each, interleaved per rep in the
fixed order none, rev, hand. rev is the PACKET-014 llama-origin lesson,
hand is the PACKET-007 concept-shape lesson, both riding byte-verbatim
from this packet's own copies, byte-checked against their sources
before any arm runs, both loading through the production path with pins
live. The drift bar is 2 of 12 as stated in the packet before the run.

The four signed readings, identical to PACKET-015's, live in the packet
and are applied in its RESULTS by the reader; any reading that fired
there and fails here is named a failed replication. The harness
reports, it does not rule."""

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
TASK = "range_summary"
CELLS = ("none", "rev", "hand")
EXPECT_TOOLS = {"none": 0, "rev": 1, "hand": 1}
R = 12

_PACKETS = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        "packets")
STORES = {"rev": {"path": os.path.join(_PACKETS,
                                       "PACKET-021-lesson_rev.jsonl"),
                  "source": os.path.join(_PACKETS,
                                         "PACKET-014-lessons.jsonl")},
          "hand": {"path": os.path.join(_PACKETS,
                                        "PACKET-021-lesson_hand.jsonl"),
                   "source": os.path.join(_PACKETS,
                                          "PACKET-013-lesson_hand.jsonl")}}

_TASKS = {t["name"]: t for t in APPLY_TASKS}

_TS = time.strftime("%Y%m%d-%H%M%S")
_LOG = os.path.join(runner.RUNS, f"parity21-{_TS}.log")
_ROWS = os.path.join(runner.RUNS, f"parity21-{_TS}.rows.jsonl")
_REPORT = os.path.join(runner.RUNS, f"parity21-{_TS}.report.json")


def _set_ts(ts):
    """Rebind the run id and its file paths. Resume reuses a prior id so
    the checkpoint rows, the log, and the report stay one record."""
    global _TS, _LOG, _ROWS, _REPORT
    _TS = ts
    _LOG = os.path.join(runner.RUNS, f"parity21-{_TS}.log")
    _ROWS = os.path.join(runner.RUNS, f"parity21-{_TS}.rows.jsonl")
    _REPORT = os.path.join(runner.RUNS, f"parity21-{_TS}.report.json")


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
    before any arm runs."""
    out = {}
    for key, cfg in STORES.items():
        with open(cfg["path"], "rb") as f:
            local = f.read()
        with open(cfg["source"], "rb") as f:
            out[key] = f.read() == local
    if not all(out.values()):
        raise SystemExit(f"byte check failed: {out}, the materials were "
                         f"touched")
    return out


def load_stores():
    stores = {}
    for key, cfg in STORES.items():
        lessons = lesson.load(cfg["path"])
        if len(lessons) != 1:
            raise SystemExit(f"{key} store must hold 1 lesson, "
                             f"found {len(lessons)}")
        lesson.validate(lessons[0])
        stores[key] = lessons
    return stores


def cell_tools(cell, stores):
    if cell == "none":
        return []
    tools = menu.query(stores[cell], _features(_TASKS[TASK]))
    if len(tools) != EXPECT_TOOLS[cell]:
        raise SystemExit(f"{cell}: expected {EXPECT_TOOLS[cell]} tools, "
                         f"got {len(tools)}")
    return tools


def run_cells(repeats=R, prior_rows=None):
    stores = load_stores()
    t = _TASKS[TASK]
    prior = list(prior_rows or [])
    done = {(r["cell"], r["rep"]) for r in prior}
    if prior:
        _p(f"resuming past {len(prior)} checkpointed runs")
    rows = list(prior)
    for rep in range(repeats):
        for cell in CELLS:
            if (cell, rep) in done:
                continue
            tools = cell_tools(cell, stores)
            r = runner.run_once(t["task"], CRITERIA, _features(t),
                                model=PERFORMER, audience_model=AUDIENCE,
                                landscape=tools or None,
                                evidence_checks=t["checks"])
            row = {"cell": cell, "task": TASK, "rep": rep,
                   "run_id": r["run_id"], "verdict": r["verdict"],
                   "tools": len(tools),
                   "tool_concepts": [x["concept"] for x in tools],
                   "ev": ev_fraction(r["evidence"]),
                   "checks": {c["call"]: bool(c["ok"]) for c in
                              (r["evidence"] or {}).get("results") or []}}
            _row(row)
            rows.append(row)
            _p(f"rep {rep} {cell}: ev={row['ev']:.2f} "
               f"tools={row['tools']}")
    return rows


def check_table(rows):
    rule_checks = set(_TASKS[TASK].get("rule_checks", []))
    table = {}
    for r in rows:
        for call, ok in (r.get("checks") or {}).items():
            cell = (table.setdefault(call,
                                     {"rule_check": call in rule_checks,
                                      "cells": {}})
                    ["cells"].setdefault(r["cell"], {"n": 0, "passed": 0}))
            cell["n"] += 1
            cell["passed"] += 1 if ok else 0
    for c in table.values():
        for a in c["cells"].values():
            a["rate"] = a["passed"] / a["n"] if a["n"] else 0.0
    return table


def pooled_rule_checks(rows):
    rule_checks = set(_TASKS[TASK].get("rule_checks", []))
    pooled = {}
    for r in rows:
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
    _p(f"REVERSE AND PARITY REPLICATION {_TS} (PACKET-021)")
    _p(f"performer={PERFORMER}  audience={AUDIENCE} (v1, production)")
    _p(f"task={TASK}  cells={CELLS}  R={repeats}  interleaved per rep "
       f"in that fixed order  drift bar=2 of 12 (stated in the packet)")
    _p(f"byte checks: rev={checks['rev']} hand={checks['hand']}")

    rows = run_cells(repeats, prior_rows)
    table = check_table(rows)
    pooled = pooled_rule_checks(rows)
    audit_ok = all(r["tools"] == EXPECT_TOOLS[r["cell"]] for r in rows)

    report = {
        "parity21_id": _TS, "performer": PERFORMER, "audience": AUDIENCE,
        "task": TASK, "cells": CELLS, "repeats": repeats,
        "drift_bar": "2 of 12", "byte_checks": checks,
        "lessons": {k: {"concept": stores[k][0]["concept"],
                        "rule": stores[k][0]["rule"],
                        "provenance": stores[k][0]["provenance"]}
                    for k in stores},
        "priors": {"P15": {"none": "8/12", "rev": "12/12",
                           "hand": "12/12"},
                   "P13": {"R-none": "8/12", "R-hand": "12/12"},
                   "P7": {"none": "0.50 at n=24"}},
        "check_table": table, "pooled_rule_checks": pooled,
        "tool_audit_ok": audit_ok,
        "n_note": (f"R={repeats} per cell, one task, interleaved. The "
                   f"four signed readings and the 2-of-12 bar live in "
                   f"the packet; failed replications are named in its "
                   f"RESULTS."),
    }
    with open(_REPORT, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    _p("== POOLED RULE CHECK (passed/n per cell) ==")
    for cell in CELLS:
        if cell in pooled:
            _p(f"  {cell}: {pooled[cell]['passed']}/{pooled[cell]['n']}")
    _p("== PER-CHECK (none / rev / hand) ==")
    for call, c in table.items():
        rates = " / ".join(f"{c['cells'].get(a, {}).get('rate', 0.0):.2f}"
                           for a in CELLS)
        mark = "  <-- rule" if c["rule_check"] else ""
        _p(f"  {call}: {rates}{mark}")

    counts_ok = all(
        sum(1 for r in rows if r["cell"] == c) == repeats for c in CELLS)
    gate = counts_ok and audit_ok and os.path.exists(_ROWS)
    _p(f"GATE: {'PASSED' if gate else 'FAILED'}. three cells at "
       f"R={repeats} interleaved, byte checks asserted, tool audit "
       f"{'clean' if audit_ok else 'BROKEN'}, every run checkpointed, "
       f"report persisted. The readings are applied in the packet "
       f"RESULTS.")


if __name__ == "__main__":
    main(repeats=int(sys.argv[1]) if len(sys.argv) > 1 else R,
         resume_ts=sys.argv[2] if len(sys.argv) > 2 else None)
