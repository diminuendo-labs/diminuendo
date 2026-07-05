"""Headroom calibration for the probe's apply pool. PACKET-001, step 2.

Every candidate apply task runs once per performer seat, no lessons,
cross-family audience, and the evidence fraction lands in the table per
task per seat. Selection happens after the run, from the persisted
report: a task is kept only if at least one seat scored below 1.0, and
the kept pool must leave each seat's baseline mean between 0.3 and 0.9.
The instrument gets measured before it measures anything.

One run per task per seat, so each cell of the table is n=1. That is
noise territory for any single task. The selection reads the table as
direction, and the band check runs on the pool mean, where the n is the
pool size.
"""

import json
import os
import time

import runner
from probe_tasks import CANDIDATE_APPLY_TASKS, CRITERIA, FEATURES

MODELS = {"A": "qwen2.5-coder:7b", "B": "llama3.1:8b"}
AUDIENCE = {"A": "llama3.1:8b", "B": "qwen2.5-coder:7b"}

_TS = time.strftime("%Y%m%d-%H%M%S")
_LOG = os.path.join(runner.RUNS, f"calibrate-{_TS}.log")
_ROWS = os.path.join(runner.RUNS, f"calibrate-{_TS}.rows.jsonl")
_REPORT = os.path.join(runner.RUNS, f"calibrate-{_TS}.report.json")


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
    results = (ev or {}).get("results") or []
    if not results:
        return 0.0
    return sum(1 for r in results if r["ok"]) / len(results)


def _mean(xs):
    return sum(xs) / len(xs) if xs else 0.0


def main():
    os.makedirs(runner.RUNS, exist_ok=True)
    _p(f"CALIBRATION {_TS}: {len(CANDIDATE_APPLY_TASKS)} candidates x 2 seats")
    _p(f"A={MODELS['A']}  B={MODELS['B']}  no lessons, cross-family audience")
    table = {}
    for t in CANDIDATE_APPLY_TASKS:
        table[t["name"]] = {}
        for seat in ("A", "B"):
            r = runner.run_once(t["task"], CRITERIA, FEATURES,
                                model=MODELS[seat],
                                audience_model=AUDIENCE[seat],
                                evidence_checks=t["checks"])
            ev = ev_fraction(r["evidence"])
            table[t["name"]][seat] = ev
            _row({"task": t["name"], "seat": seat, "run_id": r["run_id"],
                  "verdict": r["verdict"], "ev": ev})
            _p(f"{t['name']} seat {seat}: ev={ev:.2f} verdict={r['verdict']}")

    pool_mean = {s: _mean([table[n][s] for n in table]) for s in ("A", "B")}
    headroom = [n for n in table if table[n]["A"] < 1.0 or table[n]["B"] < 1.0]
    report = {
        "calibrate_id": _TS, "models": MODELS, "audience": AUDIENCE,
        "table": table, "candidate_pool_mean": pool_mean,
        "tasks_with_headroom": headroom,
        "n_note": ("One run per task per seat. Each table cell is n=1, "
                   "direction only. The kept-pool band check applies to the "
                   "pool mean, selection happens outside this harness and "
                   "is recorded in probe_tasks.py."),
    }
    with open(_REPORT, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    _p("== TABLE (ev fraction, task x seat) ==")
    for n in table:
        _p(f"  {n:18s} A={table[n]['A']:.2f}  B={table[n]['B']:.2f}")
    _p(f"candidate pool mean: A={pool_mean['A']:.2f}  B={pool_mean['B']:.2f}")
    _p(f"tasks with headroom (some seat < 1.0): {len(headroom)}"
       f" of {len(table)}")
    _p(f"report: {os.path.basename(_REPORT)}")


if __name__ == "__main__":
    main()
