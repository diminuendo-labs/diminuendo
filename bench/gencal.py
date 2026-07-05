"""Generation-pool headroom calibration. PACKET-005, work item 3.

Every named candidate runs R_G times per seat, no lessons, cross-family
audience, exactly the probe's generation conditions. The record is the
case per task per seat: mixed (fails and passes, within-task contrast),
all_pass (no headroom), all_fail (break-rich, needs a passing sibling).
A class has supply when at least one seat-task in it produces a failing
run. Selection happens outside this harness and is recorded in
probe_tasks.py, the same discipline calibrate.py set for the apply pool.

By default this measures only the PACKET-005 harder candidates: the
incumbent eight already carry two probes of R_G=3 evidence
(gen_accounting in the PACKET-002 and PACKET-003 reports), and that
record is cited in the selection instead of being re-bought.
"""

import json
import os
import sys
import time

import runner
from probe_tasks import CANDIDATE_GEN_TASKS, CRITERIA, FEATURES

MODELS = {"A": "qwen2.5-coder:7b", "B": "llama3.1:8b"}
AUDIENCE = {"A": "llama3.1:8b", "B": "qwen2.5-coder:7b"}
R_G = 3

NEW_CANDIDATES = ("count_distinct_pairs", "sum_of_modes", "weighted_mean",
                  "range_step", "title_words", "count_token")

_TS = time.strftime("%Y%m%d-%H%M%S")
_LOG = os.path.join(runner.RUNS, f"gencal-{_TS}.log")
_ROWS = os.path.join(runner.RUNS, f"gencal-{_TS}.rows.jsonl")
_REPORT = os.path.join(runner.RUNS, f"gencal-{_TS}.report.json")


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


def _features(t):
    f = {**FEATURES, "rule_class": t["rule_class"]}
    if "rule_topic" in t:
        f["rule_topic"] = t["rule_topic"]
    if "stated_direction" in t:
        f["stated_direction"] = t["stated_direction"]
    return f


def main(names=None):
    names = list(names or NEW_CANDIDATES)
    by_name = {t["name"]: t for t in CANDIDATE_GEN_TASKS}
    missing = [n for n in names if n not in by_name]
    if missing:
        raise SystemExit(f"unknown candidates: {missing}")
    os.makedirs(runner.RUNS, exist_ok=True)
    _p(f"GEN CALIBRATION {_TS}: {len(names)} candidates x 2 seats x "
       f"R_G={R_G}")
    _p(f"A={MODELS['A']}  B={MODELS['B']}  no lessons, cross-family "
       f"audience")
    table = {}
    for name in names:
        t = by_name[name]
        table[name] = {"rule_class": t["rule_class"]}
        for seat in ("A", "B"):
            evs = []
            fails = 0
            for rep in range(R_G):
                r = runner.run_once(t["task"], CRITERIA, _features(t),
                                    model=MODELS[seat],
                                    audience_model=AUDIENCE[seat],
                                    evidence_checks=t["checks"])
                ev = ev_fraction(r["evidence"])
                passed = bool((r["evidence"] or {}).get("passed"))
                fails += 0 if passed else 1
                evs.append(ev)
                _row({"task": name, "seat": seat, "rep": rep,
                      "run_id": r["run_id"], "verdict": r["verdict"],
                      "ev": ev, "ev_passed": passed})
            case = ("mixed" if 0 < fails < R_G else
                    "all_pass" if fails == 0 else "all_fail")
            table[name][seat] = {"case": case, "fails": fails,
                                 "ev": [round(e, 2) for e in evs]}
            _p(f"{name} seat {seat}: {case} ({fails}/{R_G} failed)")

    report = {"gencal_id": _TS, "models": MODELS, "audience": AUDIENCE,
              "r_g": R_G, "table": table,
              "n_note": (f"R_G={R_G} per task per seat. Cases are "
                         f"direction for pool selection, not rates.")}
    with open(_REPORT, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)
    _p("== TABLE (case per task per seat) ==")
    for name, row in table.items():
        _p(f"  {name:22s} [{row['rule_class']:12s}] "
           f"A={row['A']['case']:8s} B={row['B']['case']}")
    _p(f"report: {os.path.basename(_REPORT)}")


if __name__ == "__main__":
    main(sys.argv[1:] or None)
