"""PACKET-018: mistral's casting trait on verified mixed ground.

Two cells on longest_word, the ground PACKET-017's stage 1 verified
mixed at the rule-check level for this seat (rule checks 1/6 and 1/6,
empty-input boundary 3/6, live watch ground). none against armed, the
armed cell riding the two production tie lessons byte-copied from
PACKET-012-lessons_prod.jsonl, the exact tools on the exact ground where
the amplifier seat lost three measurements running. R=12 each,
interleaved per rep (none then armed), performer mistral:7b, audience
llama3.1:8b, pins live.

The signed three-exit reading (bar 4 of 24 on the pooled rule checks,
HARM pre-registered as ambiguous by design on this idiom-conflict
ground) and the no-name boundary-watch live in the packet and are
applied in its RESULTS by the reader. The seat neither teaches nor
learns. The harness reports, it does not rule."""

import json
import os
import sys
import time

import lesson
import menu
import runner
from probe_tasks import APPLY_TASKS, CRITERIA, FEATURES

PERFORMER = "mistral:7b"
AUDIENCE = "llama3.1:8b"
TASK = "longest_word"
CELLS = ("none", "armed")
R = 12

_PACKETS = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        "packets")
STORE = os.path.join(_PACKETS, "PACKET-018-lessons_prod.jsonl")
SOURCE = os.path.join(_PACKETS, "PACKET-012-lessons_prod.jsonl")

# the boundary-watch checks, pre-registered, reported with no name
WATCH_CHECKS = ("longest_word('')", "longest_word('one')")

_TASKS = {t["name"]: t for t in APPLY_TASKS}

_TS = time.strftime("%Y%m%d-%H%M%S")
_LOG = os.path.join(runner.RUNS, f"trait18-{_TS}.log")
_ROWS = os.path.join(runner.RUNS, f"trait18-{_TS}.rows.jsonl")
_REPORT = os.path.join(runner.RUNS, f"trait18-{_TS}.report.json")


def _set_ts(ts):
    """Rebind the run id and its file paths. Resume reuses a prior id so
    the checkpoint rows, the log, and the report stay one record."""
    global _TS, _LOG, _ROWS, _REPORT
    _TS = ts
    _LOG = os.path.join(runner.RUNS, f"trait18-{_TS}.log")
    _ROWS = os.path.join(runner.RUNS, f"trait18-{_TS}.rows.jsonl")
    _REPORT = os.path.join(runner.RUNS, f"trait18-{_TS}.report.json")


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


def byte_check():
    with open(STORE, "rb") as f:
        local = f.read()
    with open(SOURCE, "rb") as f:
        ok = f.read() == local
    if not ok:
        raise SystemExit("byte check failed, the lessons were touched")
    return ok


def load_store():
    lessons = lesson.load(STORE)
    if len(lessons) != 2:
        raise SystemExit(f"store must hold 2 lessons, "
                         f"found {len(lessons)}")
    for l in lessons:
        lesson.validate(l)
    return lessons


def cell_tools(cell, lessons):
    if cell == "none":
        return []
    tools = menu.query(lessons, _features(_TASKS[TASK]))
    if len(tools) != 2:
        raise SystemExit(f"armed cell expected 2 tools, got {len(tools)}")
    return tools


def run_cells(repeats=R, prior_rows=None):
    lessons = load_store()
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
            tools = cell_tools(cell, lessons)
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
                                      "watch": call in WATCH_CHECKS,
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
    ok = byte_check()
    _p(f"TRAIT ON MIXED GROUND {_TS} (PACKET-018)")
    _p(f"performer={PERFORMER}  audience={AUDIENCE} (v1, production)")
    _p(f"task={TASK}  cells={CELLS}  R={repeats}  interleaved per rep  "
       f"bar=4 of 24 pooled  byte check={ok}")

    rows = run_cells(repeats, prior_rows)
    table = check_table(rows)
    pooled = pooled_rule_checks(rows)
    audit_ok = all(
        r["tools"] == (2 if r["cell"] == "armed" else 0) for r in rows)

    report = {
        "trait18_id": _TS, "performer": PERFORMER, "audience": AUDIENCE,
        "task": TASK, "cells": CELLS, "repeats": repeats,
        "drift_bar": "4 of 24 pooled", "byte_check": ok,
        "lessons": [{"concept": l["concept"], "rule": l["rule"]}
                    for l in load_store()],
        "check_table": table, "pooled_rule_checks": pooled,
        "watch_checks": list(WATCH_CHECKS),
        "tool_audit_ok": audit_ok,
        "n_note": ("R=12 per cell, one task, interleaved. The three-exit "
                   "reading, the pre-registered HARM ambiguity, and the "
                   "no-name boundary-watch live in the packet and are "
                   "applied in its RESULTS, not here."),
    }
    with open(_REPORT, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    _p("== POOLED RULE CHECKS (passed/n per cell) ==")
    for cell in CELLS:
        if cell in pooled:
            _p(f"  {cell}: {pooled[cell]['passed']}/{pooled[cell]['n']}")
    _p("== PER-CHECK (none / armed) ==")
    for call, c in table.items():
        rates = " / ".join(f"{c['cells'].get(a, {}).get('rate', 0.0):.2f}"
                           for a in CELLS)
        mark = ("  <-- rule" if c["rule_check"] else
                "  <-- watch" if c["watch"] else "")
        _p(f"  {call}: {rates}{mark}")

    counts_ok = all(
        sum(1 for r in rows if r["cell"] == c) == repeats for c in CELLS)
    gate = counts_ok and audit_ok and os.path.exists(_ROWS)
    _p(f"GATE: {'PASSED' if gate else 'FAILED'}. two cells at "
       f"R={repeats} interleaved, byte check asserted, tool audit "
       f"{'clean' if audit_ok else 'BROKEN'}, every run checkpointed, "
       f"report persisted. The reading is applied in the packet RESULTS. "
       f"The seat neither taught nor learned.")


if __name__ == "__main__":
    main(repeats=int(sys.argv[1]) if len(sys.argv) > 1 else R,
         resume_ts=sys.argv[2] if len(sys.argv) > 2 else None)
