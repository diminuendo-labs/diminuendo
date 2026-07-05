"""Two-level cascade: one Principal over Musicians. Spec Section 10, minimal.

The loop rule and the drift rule are enforced by structure, not policy:

- Musicians are pure function calls made BY the principal's scheduler loop.
  A musician holds no reference to the principal, the score, or another
  musician. There is no code path by which a musician pushes anything upward.
  Its only products are its return value and its files.
- The one ambient signal is the flag tally, an append-only file the run layer
  writes on a break. The principal reads it on its own cadence, after the
  section completes, and verifies each claim against the flagged node's own
  record before believing it. A flag is a claim, never a verdict.
- Verification is read-only. It writes nothing, re-runs nothing, re-triggers
  nothing. Termination is by construction: the scheduler releases each node
  exactly once, and the test asserts iterations equal nodes.
"""

import json
import os
import re
import time

import flagtally
import runner
from score import Score


def seeded_fault(code):
    """Override the first defined function with a raiser. A deliberate,
    labeled fault for testing the detectors, per the spec's seeded-failure
    signal. Deterministic, so the induced break is guaranteed."""
    m = re.search(r"^def\s+(\w+)\s*\(", code, re.MULTILINE)
    if not m:
        return code + "\nraise RuntimeError('seeded fault')\n"
    fn = m.group(1)
    return code + (f"\n\ndef {fn}(*a, **k):\n"
                   f"    raise RuntimeError('seeded fault')\n")


def principal_review(flags_path, results, log):
    """The upper level's own read. Pull-initiated, read-only. It watches the
    tally, then verifies each flagged node against that node's own record,
    trusting the evidence over the claim."""
    tally = flagtally.read_tally(flags_path)
    verified = []
    for concept, agg in tally.items():
        for nid in agg["nodes"]:
            summ = next((r for r in results.values()
                         if r["node_id"] == nid), None)
            ev = (summ or {}).get("evidence") or {}
            verified.append({
                "concept": concept, "node_id": nid,
                "claim_upheld": bool(summ) and summ["verdict"] != "pass",
                "evidence_confirms": (ev.get("passed") is False
                                      or bool(ev.get("error"))),
            })
    review = {
        "section_pass": all(r["verdict"] == "pass" for r in results.values()),
        "flags_seen": sum(a["count"] for a in tally.values()),
        "verified": verified,
    }
    log("principal review: " + json.dumps(review))
    return review


def run_section(tasks, audience_model=None, seed_fault_in=None, log=print,
                run_task=None):
    """tasks: list of {name, task, criteria, work_features, evidence_checks,
    parent_concept}. seed_fault_in: name of the node to sabotage, labeled.
    run_task: injection point for tests, defaults to the real runner."""
    run_task = run_task or runner.run_once
    sid = time.strftime("%Y%m%d-%H%M%S") + "-sec"
    flags = os.path.join(runner.RUNS, f"{sid}.flags.jsonl")
    os.makedirs(runner.RUNS, exist_ok=True)

    s = Score()
    for t in tasks:
        s.add_node(t["name"])
    s.add_node("principal_review",
               depends_on=[t["name"] for t in tasks], source="structural")

    results = {}
    review = None
    iterations = 0
    while not s.is_done():
        ready = s.ready_nodes()
        if not ready:
            raise RuntimeError("scheduler stalled: nothing ready, not done")
        for node in ready:
            iterations += 1
            if node == "principal_review":
                review = principal_review(flags, results, log)
            else:
                t = next(x for x in tasks if x["name"] == node)
                r = run_task(
                    t["task"], t["criteria"], t["work_features"],
                    evidence_checks=t["evidence_checks"],
                    audience_model=audience_model, flag_path=flags,
                    parent_concept=t["parent_concept"], blast_radius=1.0,
                    mutate_code=seeded_fault if seed_fault_in == node else None)
                results[node] = r
                log(f"musician {node}: verdict={r['verdict']}"
                    f"{' (seeded fault)' if seed_fault_in == node else ''}")
            s.mark_complete(node)

    flag_lines = flagtally.read_tally(flags)
    return {"section_id": sid, "iterations": iterations,
            "nodes": len(tasks) + 1, "review": review,
            "flag_count": sum(a["count"] for a in flag_lines.values()),
            "flags_file": os.path.basename(flags)}


if __name__ == "__main__":
    import sys

    _LOG = os.path.join(runner.RUNS, time.strftime("section-%Y%m%d-%H%M%S.log"))

    def _p(*parts):
        line = " ".join(str(p) for p in parts)
        print(line, flush=True)
        with open(_LOG, "a", encoding="utf-8") as f:
            f.write(line + "\n")

    CRIT = ["the function is correct",
            "the code is concise and readable",
            "at least one edge case is named"]
    FEAT = {"operation": "write_code", "target": "function",
            "language": "python", "size": "small"}
    TASKS = [
        {"name": "m_wordcount", "parent_concept": "text_stats",
         "task": ("Write a Python function word_count(s) returning the "
                  "number of whitespace-separated words in s. Note one edge "
                  "case it handles."),
         "criteria": CRIT, "work_features": FEAT,
         "evidence_checks": [
             {"call": "word_count('a b  c')", "expect": "3"},
             {"call": "word_count('')", "expect": "0"},
             {"call": "word_count('  ')", "expect": "0"}]},
        {"name": "m_unique", "parent_concept": "text_stats",
         "task": ("Write a Python function unique_words(s) returning the "
                  "count of distinct lowercase whitespace-separated words in "
                  "s. Note one edge case it handles."),
         "criteria": CRIT, "work_features": FEAT,
         "evidence_checks": [
             {"call": "unique_words('a B b a')", "expect": "2"},
             {"call": "unique_words('')", "expect": "0"}]},
    ]

    out = run_section(TASKS, audience_model=(sys.argv[1] if len(sys.argv) > 1
                                             else None),
                      seed_fault_in="m_unique", log=_p)
    _p(json.dumps(out, indent=2))
    gate = (out["iterations"] == out["nodes"] and out["flag_count"] == 1
            and out["review"]["verified"]
            and all(v["claim_upheld"] and v["evidence_confirms"]
                    for v in out["review"]["verified"]))
    _p(f"GATE 3: {'PASSED' if gate else 'FAILED'}. "
       f"iterations={out['iterations']}/{out['nodes']} (each node once, "
       f"terminated), flags={out['flag_count']} (the seeded break, no echo), "
       f"claims verified by the principal's own read against evidence.")
