"""The catch-better loop, live. Spec Section 5, loop L5.

Phase 1: an unarmed run on a trap task, a tie-breaking rule stated in the
task that plausible solutions silently ignore. The code reads right and runs
wrong, the shape audiences miss and execution catches.
Phase 2: the hindsight sweep over the whole run record. Every untaught
natural miss (audience passed, execution failed, not seeded) becomes one
watch item on the audience's watchlist.
Phase 3: an armed run on a second task of the same trap class. The audience
now reads with the watch items in hand.

The gate is on the mechanism: a natural miss existed, a watch item passed the
gates and committed, and a later audience call consumed it. Whether the armed
audience actually catches the trap live is model behavior at n=1 and is
reported as exactly that, an anecdote either way.
"""

import json
import os
import sys
import time

import hindsight
import runner
import watchlist

WATCHES = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       "watchlist.jsonl")
FEATURES = {"operation": "write_code", "target": "function",
            "language": "python", "size": "small"}
CRITERIA = ["the function is correct",
            "the code is concise and readable",
            "at least one edge case is named"]
PERFORMER = "llama3.1:8b"
AUDIENCE = "qwen2.5-coder:7b"

TASK_1 = {
    "task": ("Write a Python function most_frequent_letter(s) returning the "
             "most frequent lowercase letter in s, breaking ties "
             "alphabetically. An empty string returns ''. Note one edge case "
             "it handles."),
    "checks": [{"call": "most_frequent_letter('bab')", "expect": "'b'"},
               {"call": "most_frequent_letter('ab')", "expect": "'a'"},
               {"call": "most_frequent_letter('ba')", "expect": "'a'"},
               {"call": "most_frequent_letter('')", "expect": "''"}],
}
TASK_2 = {
    "task": ("Write a Python function most_common_char(s) returning the most "
             "frequent character in s, breaking ties alphabetically. An "
             "empty string returns ''. Note one edge case it handles."),
    "checks": [{"call": "most_common_char('bab')", "expect": "'b'"},
               {"call": "most_common_char('xyyx')", "expect": "'x'"},
               {"call": "most_common_char('ba')", "expect": "'a'"},
               {"call": "most_common_char('')", "expect": "''"}],
}

_LOG = os.path.join(runner.RUNS, time.strftime("catchbetter-%Y%m%d-%H%M%S.log"))


def _p(*parts):
    line = " ".join(str(p) for p in parts)
    print(line, flush=True)
    with open(_LOG, "a", encoding="utf-8") as f:
        f.write(line + "\n")


def _brief(r):
    ev = r["evidence"] or {}
    return (f"verdict={r['verdict']} audience={r['audience_verdict']} "
            f"evidence_passed={ev.get('passed')} "
            f"watches_used={r['watches_used']}")


def main():
    _p("== CATCH-BETTER, live ==")
    _p("mix before:", json.dumps(hindsight.latency_mix(runner.RUNS)))

    _p("-- phase 1: unarmed run on the trap --")
    r1 = runner.run_once(TASK_1["task"], CRITERIA, FEATURES,
                         model=PERFORMER, audience_model=AUDIENCE,
                         evidence_checks=TASK_1["checks"])
    _p("phase 1:", _brief(r1))

    _p("-- phase 2: hindsight sweep over the whole record --")
    taught = hindsight.scan_runs(runner.RUNS, WATCHES, FEATURES, log=_p)
    _p(f"taught {len(taught)} watch item(s) from natural misses")
    for w in watchlist.load(WATCHES):
        _p("  watch:", w["watch"])

    _p("-- phase 3: armed run, same trap class --")
    r2 = runner.run_once(TASK_2["task"], CRITERIA, FEATURES,
                         model=PERFORMER, audience_model=AUDIENCE,
                         evidence_checks=TASK_2["checks"],
                         watchlist_path=WATCHES)
    _p("phase 3:", _brief(r2))
    _p("mix after:", json.dumps(hindsight.latency_mix(runner.RUNS)))

    gate = len(taught) >= 1 and r2["watches_used"] >= 1
    _p(f"CATCH-BETTER GATE: {'PASSED' if gate else 'FAILED'}. "
       f"misses taught={len(taught)}, watches consumed by the armed "
       f"audience={r2['watches_used']}.")
    caught_live = r2["audience_verdict"] != "pass" and (
        (r2["evidence"] or {}).get("passed") is False)
    _p("anecdote (n=1, not a claim): armed audience "
       + ("caught a real break live." if caught_live
          else "did not catch a break live this run "
               "(or no break occurred to catch)."))


if __name__ == "__main__":
    main()
