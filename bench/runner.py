"""The minimal loop runner. Tech Spec Section 11, first half.

One task, one Performer, one blind Audience. The Performer receives task,
criteria, landscape, and returns output, tools, trace. The Audience is a fresh
call that sees task, criteria, output, and returns a verdict per criterion.
Costs land in the ledger, the record lands in the breadcrumb file, the trace is
kept as its own file. The performer prompt is built only from the guarded
context, so the firewall is exercised on every real run, not only in tests.
"""

import json
import os
import re
import time
import uuid

import breadcrumb
import evidence
import flagtally
import ollama_client
import watchlist as watchlist_mod
from contracts import (audience_packet, guard_no_metric, performer_context,
                       validate_performer_output)
from ledger import Ledger

RUNS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "runs")


def _performer_prompt(ctx, directives=None):
    lines = ["You are completing one scoped task.",
             f"TASK: {ctx['task']}",
             "CRITERIA your work will be judged against:"]
    lines += [f"- {c}" for c in ctx["criteria"]]
    if ctx["landscape"]:
        lines.append("APPROACHES available to you (choose what fits):")
        for tool in ctx["landscape"]:
            lines.append(f"- {json.dumps(tool)}")
    if directives:
        lines.append("APPLY THESE RULES:")
        lines += [f"- {d}" for d in directives]
    lines += ["Respond in exactly two sections:",
              "OUTPUT: the deliverable itself.",
              "APPROACH: 2-4 sentences on how you did it and what you chose."]
    return "\n".join(lines)


def _audience_prompt(pkt, watches=None, protocol="v1"):
    if protocol == "v2":
        return _audience_prompt_v2(pkt, watches)
    lines = ["You are a blind evaluator. Judge only what is in front of you.",
             f"TASK: {pkt['task']}",
             "CRITERIA:"]
    lines += [f"- {c}" for c in pkt["criteria"]]
    if watches:
        lines.append("WATCH-ITEMS learned from past misses. Verify each one "
                     "explicitly before deciding:")
        lines += [f"- {w}" for w in watches]
    lines += ["OUTPUT TO JUDGE:", pkt["output"],
              "Respond with JSON only, no prose, in this shape:",
              '{"per_criterion": {"<criterion>": <1-5>}, '
              '"verdict": "pass" or "fail", "reason": "<one sentence>"}']
    return "\n".join(lines)


def _audience_prompt_v2(pkt, watches=None):
    """The substantiation protocol. Built against the recorded failure mode:
    the judge asserting violations it never verified. A fail now requires
    cited evidence, and a correctness fail requires a hand trace."""
    lines = ["You are a blind evaluator. Judge only what is in front of you.",
             f"TASK: {pkt['task']}",
             "CRITERIA:"]
    lines += [f"- {c}" for c in pkt["criteria"]]
    if watches:
        lines.append("WATCH-ITEMS learned from past misses. Verify each one "
                     "explicitly before deciding:")
        lines += [f"- {w}" for w in watches]
    lines += [
        "OUTPUT TO JUDGE:", pkt["output"],
        "JUDGING PROTOCOL, follow it exactly:",
        "1. For each criterion, look for concrete evidence in the output: "
        "the part that satisfies it, or the element that is absent.",
        "2. A criterion fails ONLY if you cite the specific evidence of the "
        "violation in your reason.",
        "3. For any claim that the code is incorrect, first trace the code "
        "by hand on the exact input you believe fails, and put that trace "
        "in your reason. No trace, no correctness fail.",
        "4. Uncertainty is a score of 3 with a note. Uncertainty is never "
        "a fail.",
        "5. verdict is \"fail\" only when at least one criterion clearly "
        "fails with cited evidence. Otherwise \"pass\".",
        "Respond with JSON only, in this shape:",
        '{"per_criterion": {"<criterion>": <1-5>}, '
        '"verdict": "pass" or "fail", '
        '"reason": "<the cited evidence or the trace>"}']
    return "\n".join(lines)


def _split_output_approach(text):
    m = re.split(r"\bAPPROACH\s*:?", text, maxsplit=1)
    output = re.sub(r"^\s*OUTPUT\s*:?", "", m[0]).strip()
    trace = m[1].strip() if len(m) > 1 else "(no approach section returned)"
    return output, trace


def _parse_json_blob(text):
    m = re.search(r"\{.*\}", text, re.DOTALL)
    if not m:
        return None
    try:
        return json.loads(m.group(0))
    except json.JSONDecodeError:
        return None


def judge_output(task, criteria, output, audience_model, watches=None,
                 options=None, protocol="v1"):
    """One blind judgment of one output. The single judging path: run_once
    and the unarmed control both call this, so the instrument and the live
    loop cannot drift apart. Returns the report with its cost attached."""
    pkt = audience_packet(task, criteria, output)
    aud = ollama_client.generate(audience_model,
                                 _audience_prompt(pkt, watches or [],
                                                  protocol=protocol),
                                 options=options)
    report = _parse_json_blob(aud["text"]) or {
        "per_criterion": {}, "verdict": "unscorable",
        "reason": "audience returned no parseable JSON"}
    report["_cost"] = {"time_s": aud["time_s"],
                       "tokens": aud["prompt_tokens"] + aud["output_tokens"]}
    return report


def run_once(task, criteria, work_features, model="qwen2.5-coder:7b",
             landscape=None, run_id=None, evidence_checks=None,
             audience_model=None, flag_path=None, parent_concept=None,
             blast_radius=1.0, mutate_code=None, watchlist_path=None,
             directives=None):
    """One task through the loop. Returns a summary dict.
    audience_model defaults to the performer's model, and a different family
    there is the better arrangement: same-model audiences share the
    performer's blind spots and self-score generously.
    flag_path: a break appends a flag there, a raised hand, never a push.
    mutate_code: seeded-fault hook, one of the spec's own Seam 3 signals for
    testing detectors. Its use is recorded in the summary, never hidden.
    directives: explicit instruction lines for the performer prompt
    (PACKET-004's delivery arm). Performer-bound, so guarded like
    everything else that crosses the firewall."""
    os.makedirs(RUNS, exist_ok=True)
    run_id = run_id or time.strftime("%Y%m%d-%H%M%S") + "-" + uuid.uuid4().hex[:6]
    node_id = f"task-{run_id}"
    crumbs = os.path.join(RUNS, f"{run_id}.crumbs.jsonl")
    ledger = Ledger(path=os.path.join(RUNS, f"{run_id}.ledger.jsonl"))

    # ---- performer (sees only the guarded context) ----
    ctx = performer_context(task, criteria, landscape)
    directives = guard_no_metric(list(directives or []), "directives")
    perf = ollama_client.generate(model, _performer_prompt(ctx, directives))
    output, trace = _split_output_approach(perf["text"])
    performer_out = validate_performer_output({
        "output": output, "tools_chosen": [t.get("concept", "?")
                                           for t in ctx["landscape"]] or ["direct"],
        "work_features": work_features, "trace": trace,
    })
    trace_path = os.path.join(RUNS, f"{run_id}.trace.txt")
    with open(trace_path, "w", encoding="utf-8") as f:
        f.write(trace)

    # ---- blind audience (fresh call, no trace, no chair memory) ----
    aud_model = audience_model or model
    watches = []
    if watchlist_path:
        watches = watchlist_mod.query(watchlist_mod.load(watchlist_path),
                                      work_features)
    report = judge_output(task, criteria, performer_out["output"], aud_model,
                          watches=watches)
    aud_cost = report.pop("_cost")

    # ---- executable evidence (decorrelated: execution, not opinion) ----
    ev = None
    verdict = report["verdict"]
    error_class = None
    if evidence_checks:
        code = evidence.extract_python(performer_out["output"])
        if mutate_code:
            code = mutate_code(code)
        ev = evidence.run_checks(code, evidence_checks)
        if not ev["passed"]:
            # evidence outranks the audience on the checks it covers
            if verdict == "pass":
                error_class = "evidence_caught_audience_pass"
            else:
                error_class = "evidence_fail"
            verdict = "fail"

    # ---- ledger (the metric, audience side only) ----
    run_time = perf["time_s"]
    run_tokens = perf["prompt_tokens"] + perf["output_tokens"]
    if verdict == "pass":
        ledger.post(node_id, "clean", run_time, run_tokens, "performer run")
    else:
        # caught at the output: the failure posts as a minus. No correction
        # step exists yet in the minimal loop, so none is invented.
        ledger.post(node_id, "failure", run_time, run_tokens,
                    f"verdict: {verdict}" +
                    (f" ({error_class})" if error_class else ""))
    ledger.post(node_id, "clean", aud_cost["time_s"],
                aud_cost["tokens"], "audience scoring")

    # ---- breadcrumb (forward record, provisional outcome) ----
    crumb = {
        "node_id": node_id, "model": model, "role": "musician",
        "work_features": work_features,
        "cost_time": run_time, "cost_tokens": run_tokens,
        "outcome": f"provisional_{verdict}",
        "trace_ref": os.path.basename(trace_path),
    }
    if error_class:
        crumb["error_class"] = error_class
    if parent_concept:
        crumb["parent_concept_id"] = parent_concept
    breadcrumb.write(crumbs, crumb)

    # ---- the break raises a flag: a claim into the tally, never a push ----
    flagged = False
    if flag_path and verdict != "pass":
        flagtally.raise_flag(
            flag_path,
            concept=parent_concept or work_features.get("operation", "unknown"),
            node_id=node_id, level="musician", blast_radius=blast_radius,
            credibility=1.0, surprise=1.0,
            note=error_class or report.get("reason", ""))
        flagged = True

    summary = {"run_id": run_id, "node_id": node_id,
               "task": task,
               "verdict": verdict,
               "audience_verdict": report["verdict"],
               "audience_model": aud_model,
               "watches_used": len(watches),
               "directives_used": len(directives),
               "reason": report.get("reason", ""),
               "per_criterion": report.get("per_criterion", {}),
               "evidence": ev,
               "code_mutated": bool(mutate_code),
               "flagged": flagged,
               "output": performer_out["output"],
               "trace": performer_out["trace"],
               "totals": ledger.totals(),
               "files": [os.path.basename(crumbs),
                         os.path.basename(trace_path)]}
    # the run persists its own summary, so a dead pipe can never strand it
    with open(os.path.join(RUNS, f"{run_id}.summary.json"), "w",
              encoding="utf-8") as f:
        json.dump(summary, f, indent=2)
    return summary


if __name__ == "__main__":
    result = run_once(
        task=("Write a Python function reverse_words(s) that reverses the "
              "order of words in a sentence, normalizing runs of whitespace "
              "to single spaces. Note one edge case it handles."),
        criteria=["the function is correct",
                  "the code is concise and readable",
                  "at least one edge case is named"],
        work_features={"operation": "write_code", "target": "function",
                       "language": "python", "size": "small"},
    )
    print(json.dumps(result, indent=2))
