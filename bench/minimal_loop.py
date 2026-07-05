"""The Section 11 minimal loop, live end to end.

Run 1 performs a task with no landscape. The engine distills a lesson from the
run's criteria-shaped feedback and the trace. The lesson commits through the
gates. Run 2 performs a related task with the lesson on its menu. The gate is
that an engine-produced lesson was consumed, not that a number moved: at n=1,
improvement is noise, and the log says so.
"""

import json
import os
import sys
import time

import lesson
import menu
import runner

_LOG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "runs",
                    time.strftime("loop-%Y%m%d-%H%M%S.log"))


def _p(*parts):
    """Print and append to the loop log, so a dead pipe strands nothing."""
    line = " ".join(str(p) for p in parts)
    print(line, flush=True)
    with open(_LOG, "a", encoding="utf-8") as f:
        f.write(line + "\n")

LESSONS = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       "lessons.jsonl")
FEATURES = {"operation": "write_code", "target": "function",
            "language": "python", "size": "small"}
CRITERIA = ["the function is correct",
            "the code is concise and readable",
            "at least one edge case is named"]

TASK_A = ("Write a Python function longest_common_prefix(strings) that "
          "returns the longest common prefix of a list of strings. An empty "
          "list returns ''. Note one edge case it handles.")
CHECKS_A = [
    {"call": "longest_common_prefix(['flower','flow','flight'])", "expect": "'fl'"},
    {"call": "longest_common_prefix([])", "expect": "''"},
    {"call": "longest_common_prefix(['dog','racecar','car'])", "expect": "''"},
    {"call": "longest_common_prefix(['same'])", "expect": "'same'"},
]

TASK_B = ("Write a Python function first_unique_char(s) that returns the "
          "index of the first character that appears exactly once in s, or "
          "-1 if none does. Note one edge case it handles.")
CHECKS_B = [
    {"call": "first_unique_char('leetcode')", "expect": "0"},
    {"call": "first_unique_char('aabb')", "expect": "-1"},
    {"call": "first_unique_char('')", "expect": "-1"},
]


def _brief(r):
    return {k: r[k] for k in ("run_id", "verdict", "audience_verdict",
                              "reason", "evidence")}


def main(audience_model=None):
    _p("== RUN 1: no landscape ==")
    r1 = runner.run_once(TASK_A, CRITERIA, FEATURES,
                         evidence_checks=CHECKS_A,
                         audience_model=audience_model)
    _p(json.dumps(_brief(r1), indent=2, default=str))

    _p("== LESSON: engine distillation ==")
    cand = None
    err = None
    for attempt in range(2):
        try:
            cand = lesson.generate({**r1, "task_text": TASK_A}, FEATURES)
            committed = lesson.commit(LESSONS, cand)
            break
        except lesson.LessonError as e:
            err = e
            _p(f"attempt {attempt + 1} rejected by the gates: {e}")
            cand = None
    if cand is None:
        _p("lesson generation failed both attempts, stopping honestly:", err)
        return
    _p(json.dumps(committed, indent=2))

    _p("== RUN 2: consumes the menu ==")
    tools = menu.query(lesson.load(LESSONS), FEATURES)
    _p("landscape handed to the performer:", json.dumps(tools, indent=2))
    r2 = runner.run_once(TASK_B, CRITERIA, FEATURES,
                         landscape=tools, evidence_checks=CHECKS_B,
                         audience_model=audience_model)
    _p(json.dumps(_brief(r2), indent=2, default=str))
    gate = committed["provenance"] == "engine" and len(tools) > 0
    _p(f"GATE 2: {'PASSED' if gate else 'FAILED'}. "
          f"engine-produced={committed['provenance'] == 'engine'}, "
          f"tools consumed by run 2={len(tools)}. "
          "n=1, any 'improvement' is noise either way.")


if __name__ == "__main__":
    main(audience_model=sys.argv[1] if len(sys.argv) > 1 else None)

