"""The unarmed control: attribute a live catch to the watch item, or don't.

Protocol. The same output is judged twice by the same audience model at
temperature 0 with a fixed seed. The only varied factor is the watchlist. Any
verdict change is attributable to the watch items and nothing else.

Both columns, always. On outputs execution proves broken: does arming flip a
miss into a live catch (the win)? On outputs execution proves clean: does
arming flip a pass into a false alarm (the cost)? A loop that converts misses
by rejecting everything is not a win, so the cost column is never omitted.

Caveat, stated where the instrument lives: temperature 0 is the instrument's
setting, not production's. The control measures the watch item's effect on a
deterministic judge, which is the attributable question. It does not replay a
production judgment.
"""

import glob
import json
import os
import sys
import time

import evidence
import runner
import watchlist

DETERMINISTIC = {"temperature": 0, "seed": 7}


def judge_pair(task, criteria, output, audience_model, watches):
    """Two deterministic judgments of one output: unarmed, then armed."""
    unarmed = runner.judge_output(task, criteria, output, audience_model,
                                  watches=[], options=DETERMINISTIC)
    armed = runner.judge_output(task, criteria, output, audience_model,
                                watches=watches, options=DETERMINISTIC)
    return {"unarmed": unarmed["verdict"], "armed": armed["verdict"],
            "unarmed_reason": unarmed.get("reason", ""),
            "armed_reason": armed.get("reason", "")}


def classify(evidence_passed, unarmed, armed):
    """One cell of the control table per judged output."""
    if evidence_passed is False:
        if unarmed == "pass" and armed == "fail":
            return "miss_converted_to_catch"       # the win
        if unarmed == "fail":
            return "caught_without_watch"          # audience needed no help
        if armed == "pass":
            return "missed_even_armed"             # the watch did not reach
        return "broken_other"
    if evidence_passed is True:
        if unarmed == "pass" and armed == "fail":
            return "false_alarm_induced"           # the cost
        if unarmed == "pass" and armed == "pass":
            return "clean_no_harm"
        if unarmed == "fail":
            return "unarmed_false_alarm"           # audience noise, pre-watch
        return "clean_other"
    return "no_ground_truth"


FEATURES = {"operation": "write_code", "target": "function",
            "language": "python", "size": "small"}
CRITERIA = ["the function is correct",
            "the code is concise and readable",
            "at least one edge case is named"]
PERFORMER = "llama3.1:8b"
AUDIENCE = "qwen2.5-coder:7b"
WATCHES = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       "watchlist.jsonl")

# three trap-class tasks (a tie rule stated, commonly ignored) and two
# straightforward tasks likely to produce clean outputs for the cost column
POOL = [
    {"task": ("Write a Python function min_mode(nums) returning the most "
              "frequent value in the list, breaking ties by the smaller "
              "value. An empty list returns None. Note one edge case."),
     "checks": [{"call": "min_mode([1, 2, 2, 1, 3])", "expect": "1"},
                {"call": "min_mode([5])", "expect": "5"},
                {"call": "min_mode([])", "expect": "None"},
                {"call": "min_mode([2, 2, 3])", "expect": "2"}]},
    {"task": ("Write a Python function longest_word(s) returning the longest "
              "whitespace-separated word, breaking ties alphabetically. An "
              "empty string returns ''. Note one edge case."),
     "checks": [{"call": "longest_word('bb aa')", "expect": "'aa'"},
                {"call": "longest_word('a bbb')", "expect": "'bbb'"},
                {"call": "longest_word('')", "expect": "''"},
                {"call": "longest_word('cc bb')", "expect": "'bb'"}]},
    {"task": ("Write a Python function max_run_char(s) returning the "
              "character of the longest consecutive run in s, breaking ties "
              "alphabetically. An empty string returns ''. Note one edge "
              "case."),
     "checks": [{"call": "max_run_char('aaab')", "expect": "'a'"},
                {"call": "max_run_char('bbaa')", "expect": "'a'"},
                {"call": "max_run_char('')", "expect": "''"},
                {"call": "max_run_char('ab')", "expect": "'a'"}]},
    {"task": ("Write a Python function square(n) returning n squared. Note "
              "one edge case it handles."),
     "checks": [{"call": "square(3)", "expect": "9"},
                {"call": "square(-2)", "expect": "4"}]},
    {"task": ("Write a Python function is_even(n) returning True when n is "
              "even. Note one edge case it handles."),
     "checks": [{"call": "is_even(2)", "expect": "True"},
                {"call": "is_even(3)", "expect": "False"},
                {"call": "is_even(0)", "expect": "True"}]},
]


_TS = time.strftime("%Y%m%d-%H%M%S")
_LOG = os.path.join(runner.RUNS, f"control-{_TS}.log")
_REPORT = os.path.join(runner.RUNS, f"control-{_TS}.report.json")


def _p(*parts):
    line = " ".join(str(p) for p in parts)
    print(line, flush=True)
    with open(_LOG, "a", encoding="utf-8") as f:
        f.write(line + "\n")


def retro_control(watches):
    """Judge last night's caught output armed and unarmed, deterministically.
    Directly interrogates the anecdote: did the watch cause that catch?"""
    target = None
    for path in sorted(glob.glob(os.path.join(runner.RUNS,
                                              "*.summary.json"))):
        with open(path, encoding="utf-8") as f:
            s = json.load(f)
        if "most_common_char" in s.get("task", "") and s.get("watches_used"):
            target = s
    if not target:
        _p("retro-control: target run not found, skipping")
        return None
    pair = judge_pair(target["task"], CRITERIA, target["output"],
                      AUDIENCE, watches)
    ev_passed = (target.get("evidence") or {}).get("passed")
    cell = classify(ev_passed, pair["unarmed"], pair["armed"])
    _p(f"retro-control on {target['node_id']}: unarmed={pair['unarmed']} "
       f"armed={pair['armed']} evidence_passed={ev_passed} -> {cell}")
    _p(f"  unarmed reason: {pair['unarmed_reason']}")
    _p(f"  armed reason:   {pair['armed_reason']}")
    return {"node_id": target["node_id"], "cell": cell, **pair}


def main():
    _p(f"UNARMED CONTROL {_TS}")
    watches = watchlist.query(watchlist.load(WATCHES), FEATURES)
    _p(f"watch items in play: {len(watches)}")
    for w in watches:
        _p("  -", w)
    if not watches:
        _p("no watch items on file, nothing to control. Run catchbetter "
           "first.")
        return

    retro = retro_control(watches)

    _p("-- batch protocol: fresh outputs, paired judgments --")
    rows = []
    for t in POOL:
        r = runner.run_once(t["task"], CRITERIA, FEATURES, model=PERFORMER,
                            audience_model=AUDIENCE,
                            evidence_checks=t["checks"])
        ev_passed = (r["evidence"] or {}).get("passed")
        pair = judge_pair(t["task"], CRITERIA, r["output"], AUDIENCE, watches)
        cell = classify(ev_passed, pair["unarmed"], pair["armed"])
        row = {"run_id": r["run_id"], "evidence_passed": ev_passed,
               "cell": cell, **pair}
        rows.append(row)
        _p(f"{r['run_id']}: evidence_passed={ev_passed} "
           f"unarmed={pair['unarmed']} armed={pair['armed']} -> {cell}")

    table = {}
    for row in rows:
        table[row["cell"]] = table.get(row["cell"], 0) + 1
    report = {"control_id": _TS, "watches": watches, "retro": retro,
              "rows": rows, "table": table,
              "n_note": ("Five outputs, deterministic paired judgments. "
                         "Attribution is per output and real. Rates are "
                         "not, the n is too small for rates.")}
    with open(_REPORT, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)
    _p("== CONTROL TABLE ==", json.dumps(table))
    gate = len(rows) == len(POOL) and all(
        r["cell"] != "no_ground_truth" for r in rows)
    _p(f"CONTROL GATE: {'PASSED' if gate else 'FAILED'}. every output "
       f"judged paired with ground truth, both columns reported.")


if __name__ == "__main__":
    main()
