"""The Hindsight pass, minimal form: the catch-better teacher.

Sweeps the run records for natural audience misses, breaks the audience
passed and execution caught, and turns each into one watch item for the
audience's watchlist. Two hard rules:

- Seeded runs (code_mutated) are never teachers. The fault existed only in
  the executed copy, the audience's input was clean, so no criterion could
  have caught it. Teaching from it would mint a watch item that cannot work.
- A miss teaches once. Nodes already on the watchlist are skipped.

Also carries the slope's ruler in miniature: latency_mix counts how breaks
were discovered across the record, the mix that should shift earlier as the
audience learns.
"""

import glob
import json
import os
import re

import ollama_client
import watchlist

GENERATOR = "qwen2.5-coder:7b"


def natural_miss(summary):
    """Audience passed, the final verdict failed on execution, no seeding."""
    return (summary.get("audience_verdict") == "pass"
            and summary.get("verdict") == "fail"
            and not summary.get("code_mutated")
            and (summary.get("evidence") or {}).get("passed") is False)


def teach_audience(summary, work_features, model=GENERATOR, generate_fn=None):
    """Distill one watch item from a natural miss. Sees the task, the output
    the audience accepted, and the checks that failed. Returns a candidate,
    unvalidated, so the caller watches the gates pass or fail explicitly."""
    ev = summary.get("evidence") or {}
    failed = [r for r in ev.get("results", []) if not r["ok"]]
    fail_lines = [f"- {r['call']} produced {r['got']}, expected {r['expect']}"
                  for r in failed]
    prompt = "\n".join([
        "A blind evaluator approved a piece of work that execution later",
        "proved wrong. Write ONE watch-item: an instruction telling a future",
        "evaluator WHAT TO VERIFY in outputs of this kind, so this class of",
        "miss is caught by reading, before execution.",
        f"THE TASK: {summary.get('task', '(unknown)')}",
        "THE OUTPUT THE EVALUATOR APPROVED:",
        summary.get("output", "")[:2000],
        "THE EXECUTION CHECKS THAT FAILED:",
        *fail_lines,
        "Rules:",
        "- Name the property to verify, never the fix or the code to write.",
        "- It must be checkable by reading the output against the task.",
        "- Never mention speed, cost, or any quantity of effort.",
        "- applies_when values MUST be the exact value shown or \"*\".",
        f"WORK FEATURES: {json.dumps(work_features)}",
        "Respond with JSON only, in this exact shape:",
        json.dumps({"watch": "<one or two sentences>",
                    "applies_when": dict(work_features),
                    "confidence": 0.5}),
    ])
    text = (generate_fn or
            (lambda p: ollama_client.generate(model, p)["text"]))(prompt)
    m = re.search(r"\{.*\}", text, re.DOTALL)
    if not m:
        raise watchlist.WatchError("teacher returned no parseable JSON")
    cand = json.loads(m.group(0))
    cand["provenance"] = "engine"
    cand["source_node"] = summary["node_id"]
    return cand


def scan_runs(runs_dir, watch_path, work_features, model=GENERATOR,
              generate_fn=None, log=print):
    """The backward pass at a window: find untaught natural misses in the
    record, teach the audience one watch item per miss."""
    already = watchlist.taught_nodes(watchlist.load(watch_path))
    taught = []
    for path in sorted(glob.glob(os.path.join(runs_dir, "*.summary.json"))):
        with open(path, encoding="utf-8") as f:
            s = json.load(f)
        if not natural_miss(s) or s["node_id"] in already:
            continue
        committed = False
        for attempt in range(2):
            try:
                cand = teach_audience(s, work_features, model, generate_fn)
                watchlist.commit(watch_path, cand)
                committed = True
                break
            except watchlist.WatchError as e:
                log(f"watch attempt {attempt + 1} for {s['node_id']} "
                    f"rejected: {e}")
        if committed:
            taught.append(s["node_id"])
            log(f"taught from miss {s['node_id']}")
    return taught


def latency_mix(runs_dir):
    """How breaks were discovered, across the record. The mix that should
    shift earlier over time is the slope's measurable signature."""
    mix = {"clean_pass": 0, "caught_live_by_audience": 0,
           "caught_by_evidence_after_audience_pass": 0,
           "seeded": 0, "unscorable": 0}
    for path in glob.glob(os.path.join(runs_dir, "*.summary.json")):
        with open(path, encoding="utf-8") as f:
            s = json.load(f)
        if s.get("code_mutated"):
            mix["seeded"] += 1
        elif s.get("audience_verdict") == "unscorable":
            mix["unscorable"] += 1
        elif s.get("verdict") == "pass":
            mix["clean_pass"] += 1
        elif s.get("audience_verdict") != "pass":
            mix["caught_live_by_audience"] += 1
        else:
            mix["caught_by_evidence_after_audience_pass"] += 1
    return mix
