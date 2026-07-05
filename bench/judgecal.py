"""Judge calibration: measure the audience's baseline noise on the record.

The day's run record is a labeled corpus: every summary carries an output and
an execution ground truth. This harness re-judges those outputs under a 2x2,
protocol v1/v2 by judge model, all unarmed, temperature 0, and reports two
rates per condition: false alarms on clean outputs and misses on broken ones.

One factor per axis. Ground truth comes from execution, never from a model.
Production stays on protocol v1 until this table says otherwise.
"""

import glob
import json
import os
import time

import runner

CRITERIA = ["the function is correct",
            "the code is concise and readable",
            "at least one edge case is named"]
JUDGES = {"qwen": "qwen2.5-coder:7b", "llama": "llama3.1:8b"}
PROTOCOLS = ("v1", "v2")
DETERMINISTIC = {"temperature": 0, "seed": 7}
MAX_BROKEN = 6
MAX_CLEAN = 8


def select_corpus(summaries, max_broken=MAX_BROKEN, max_clean=MAX_CLEAN):
    """All usable outputs with execution ground truth: no seeded runs, no
    missing evidence, dedup by node. Broken outputs are rare, take them all
    up to the cap, then fill with clean."""
    broken, clean, seen = [], [], set()
    for s in summaries:
        ev = s.get("evidence") or {}
        if (s.get("code_mutated") or ev.get("passed") is None
                or s["node_id"] in seen or not s.get("output")
                or not s.get("task")):
            # the filter requires every field the harness consumes. Records
            # from before the task field existed are excluded, not guessed.
            continue
        seen.add(s["node_id"])
        (clean if ev["passed"] else broken).append(s)
    return broken[:max_broken] + clean[:max_clean]


def rates(rows):
    """False-alarm rate on clean outputs, miss rate on broken outputs, and
    the unscorable count, per condition. Unscorables are excluded from the
    rates and reported on their own."""
    clean = [r for r in rows if r["truth_clean"] and r["verdict"] != "unscorable"]
    broken = [r for r in rows if not r["truth_clean"]
              and r["verdict"] != "unscorable"]
    fa = sum(1 for r in clean if r["verdict"] == "fail")
    miss = sum(1 for r in broken if r["verdict"] == "pass")
    return {
        "clean_n": len(clean), "false_alarms": fa,
        "false_alarm_rate": round(fa / len(clean), 2) if clean else None,
        "broken_n": len(broken), "misses": miss,
        "miss_rate": round(miss / len(broken), 2) if broken else None,
        "unscorable": sum(1 for r in rows if r["verdict"] == "unscorable"),
    }


def load_summaries(runs_dir):
    out = []
    for path in sorted(glob.glob(os.path.join(runs_dir, "*.summary.json"))):
        with open(path, encoding="utf-8") as f:
            out.append(json.load(f))
    return out


_TS = time.strftime("%Y%m%d-%H%M%S")
_LOG = os.path.join(runner.RUNS, f"judgecal-{_TS}.log")
_ROWS = os.path.join(runner.RUNS, f"judgecal-{_TS}.rows.jsonl")
_REPORT = os.path.join(runner.RUNS, f"judgecal-{_TS}.report.json")


def _p(*parts):
    line = " ".join(str(p) for p in parts)
    print(line, flush=True)
    with open(_LOG, "a", encoding="utf-8") as f:
        f.write(line + "\n")


def main():
    corpus = select_corpus(load_summaries(runner.RUNS))
    n_broken = sum(1 for s in corpus if not s["evidence"]["passed"])
    _p(f"JUDGE CALIBRATION {_TS}: corpus={len(corpus)} outputs "
       f"({n_broken} broken, {len(corpus) - n_broken} clean)")

    results = {}
    for pname in PROTOCOLS:
        for jname, jmodel in JUDGES.items():
            cond = f"{pname}|{jname}"
            rows = []
            for s in corpus:
                rep = runner.judge_output(s["task"], CRITERIA, s["output"],
                                          jmodel, watches=[],
                                          options=DETERMINISTIC,
                                          protocol=pname)
                row = {"cond": cond, "node_id": s["node_id"],
                       "truth_clean": bool(s["evidence"]["passed"]),
                       "verdict": rep["verdict"],
                       "reason": rep.get("reason", "")[:300]}
                rows.append(row)
                with open(_ROWS, "a", encoding="utf-8") as f:
                    f.write(json.dumps(row) + "\n")
            results[cond] = rates(rows)
            _p(f"{cond}: {json.dumps(results[cond])}")

    report = {"cal_id": _TS, "corpus_n": len(corpus),
              "broken_n": n_broken, "conditions": results,
              "n_note": ("One deterministic judgment per output per "
                         "condition. Rates on this n are directional, "
                         "not settled.")}
    with open(_REPORT, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)
    gate = (len(results) == 4 and n_broken >= 2
            and len(corpus) - n_broken >= 2)
    _p(f"CALIBRATION GATE: {'PASSED' if gate else 'FAILED'}. four "
       f"conditions, both classes represented, every judgment on disk.")


if __name__ == "__main__":
    main()
