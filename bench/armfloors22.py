"""PACKET-022: arm the floors. First delivery cells for the admitted
boundary and normalize lessons at the deepest unarmed apply floors,
llama3.1:8b receiving, audience qwen2.5-coder:7b, v1 production path.

Stage A qualifies ground per class in ranked order (boundary:
merge_ranges, median, flatten_once; normalize: snake_to_camel,
balanced), a none cell at R=12 per candidate, stopping each sweep at
its first qualifier. Qualification pools the rule-check readings per
the task's standing annotation at the PACKET-019 fraction: at least 2
passes AND 2 fails of 12 pooled on one-rule ground, at least 4 AND 4
of 24 on two-rule ground. Stage A cells gate; they are never the
treatment baseline. A sweep that exhausts its candidates closes its
class on the supply answer.

Stage B, on qualified ground only: three fresh cells at R=12 each,
interleaved per rep in the fixed order none, armed-1, armed-2, the
boundary block whole before the normalize block starts. Each armed
cell delivers exactly one production lesson through the menu path from
its single-lesson packet-local store, byte-checked against its
production line before any run. Drift bar per comparison scales the
same way: 2 of 12 pooled one-rule, 4 of 24 pooled two-rule.

The four signed three-exit readings, the two-cause HARM sentences for
armed-B2 (the wildcard pin) and armed-N2 (the cross-topic residue),
the no-name watch columns, and the transfer note live in the packet
and are applied in its RESULTS by the reader. The seat neither teaches
nor learns. The harness reports, it does not rule."""

import json
import os
import sys
import time

import lesson
import menu
import runner
from probe_tasks import APPLY_TASKS, CRITERIA, FEATURES

PERFORMER = "llama3.1:8b"
AUDIENCE = "qwen2.5-coder:7b"
R = 12

SWEEPS = {"boundary": ("merge_ranges", "median", "flatten_once"),
          "normalize": ("snake_to_camel", "balanced")}
BLOCK_CELLS = {"boundary": ("none", "armed-B1", "armed-B2"),
               "normalize": ("none", "armed-N1", "armed-N2")}
EXPECT_TOOLS = {"none": 0, "armed-B1": 1, "armed-B2": 1,
                "armed-N1": 1, "armed-N2": 1}

_BENCH = os.path.dirname(os.path.abspath(__file__))
_PACKETS = os.path.join(_BENCH, "packets")
LESSONS_PROD = os.path.join(_BENCH, "lessons.jsonl")
ARMS = {"armed-B1": {"gen_task": "chunk",
                     "path": os.path.join(_PACKETS,
                                          "PACKET-022-lesson_B1.jsonl")},
        "armed-B2": {"gen_task": "weighted_mean",
                     "path": os.path.join(_PACKETS,
                                          "PACKET-022-lesson_B2.jsonl")},
        "armed-N1": {"gen_task": "split_csvish",
                     "path": os.path.join(_PACKETS,
                                          "PACKET-022-lesson_N1.jsonl")},
        "armed-N2": {"gen_task": "depth_max",
                     "path": os.path.join(_PACKETS,
                                          "PACKET-022-lesson_N2.jsonl")}}

PRIORS = {
    "calibration_n1_seatB": {"merge_ranges": 0.75, "median": 0.75,
                             "flatten_once": 0.33, "snake_to_camel": 0.25,
                             "balanced": 0.75},
    "P9_llama_receiving": ("qwen tie lessons through the production menu "
                           "moved llama rule checks 0.17 to 0.92, pooled "
                           "4/24 to 22/24, non-rule checks unharmed"),
    "P19_mistral_receiving": "FLAT, armed 13/24 against none 12/24",
    "P15_qwen_receiving": "none 8/12, rev 12/12, hand 12/12",
    "P21_qwen_receiving": "none 4/12, rev 11/12, hand 10/12",
}

_TASKS = {t["name"]: t for t in APPLY_TASKS}

_TS = time.strftime("%Y%m%d-%H%M%S")
_LOG = os.path.join(runner.RUNS, f"armfloors22-{_TS}.log")
_ROWS = os.path.join(runner.RUNS, f"armfloors22-{_TS}.rows.jsonl")
_REPORT = os.path.join(runner.RUNS, f"armfloors22-{_TS}.report.json")


def _set_ts(ts):
    """Rebind the run id and its file paths. Resume reuses a prior id so
    the checkpoint rows, the log, and the report stay one record."""
    global _TS, _LOG, _ROWS, _REPORT
    _TS = ts
    _LOG = os.path.join(runner.RUNS, f"armfloors22-{_TS}.log")
    _ROWS = os.path.join(runner.RUNS, f"armfloors22-{_TS}.rows.jsonl")
    _REPORT = os.path.join(runner.RUNS, f"armfloors22-{_TS}.report.json")


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


def rule_n(task_name):
    return len(_TASKS[task_name]["rule_checks"])


def qualify_min(task_name):
    """The PACKET-019 fraction, scaled to the ground's rule-check count:
    2 of 12 pooled on one-rule ground, 4 of 24 on two-rule ground."""
    return 2 * rule_n(task_name)


def drift_bar(task_name):
    """Same scaling as qualification, per the packet."""
    return 2 * rule_n(task_name)


def byte_checks():
    """Each packet-local store byte-identical to its production line,
    asserted before any stage B run. The line is found by its trail
    gen_task, and a duplicate match fails loudly instead of guessing."""
    with open(LESSONS_PROD, "rb") as f:
        prod_lines = [l for l in f.read().split(b"\n") if l.strip()]
    by_gen = {}
    for line in prod_lines:
        gt = (json.loads(line).get("trail") or {}).get("gen_task")
        if gt is None:
            continue
        by_gen.setdefault(gt, []).append(line)
    out = {}
    for key, cfg in ARMS.items():
        matches = by_gen.get(cfg["gen_task"], [])
        if len(matches) != 1:
            raise SystemExit(f"{key}: {len(matches)} production lines "
                             f"carry gen_task {cfg['gen_task']}, expected "
                             f"exactly 1")
        with open(cfg["path"], "rb") as f:
            out[key] = f.read() == matches[0] + b"\n"
    if not all(out.values()):
        raise SystemExit(f"byte check failed: {out}, the materials were "
                         f"touched")
    return out


def load_stores():
    stores = {}
    for key, cfg in ARMS.items():
        lessons = lesson.load(cfg["path"])
        if len(lessons) != 1:
            raise SystemExit(f"{key} store must hold 1 lesson, "
                             f"found {len(lessons)}")
        lesson.validate(lessons[0])
        stores[key] = lessons
    return stores


def cell_tools(cell, stores, task_name):
    if cell == "none":
        return []
    tools = menu.query(stores[cell], _features(_TASKS[task_name]))
    if len(tools) != EXPECT_TOOLS[cell]:
        raise SystemExit(f"{cell} on {task_name}: expected "
                         f"{EXPECT_TOOLS[cell]} tools, got {len(tools)}")
    return tools


def _run_one(t, tools, stage, block, cell, rep):
    r = runner.run_once(t["task"], CRITERIA, _features(t),
                        model=PERFORMER, audience_model=AUDIENCE,
                        landscape=tools or None,
                        evidence_checks=t["checks"])
    row = {"stage": stage, "block": block, "cell": cell,
           "task": t["name"], "rep": rep, "run_id": r["run_id"],
           "verdict": r["verdict"], "tools": len(tools),
           "tool_concepts": [x["concept"] for x in tools],
           "ev": ev_fraction(r["evidence"]),
           "checks": {c["call"]: bool(c["ok"]) for c in
                      (r["evidence"] or {}).get("results") or []}}
    _row(row)
    _p(f"{stage} {block} {t['name']} {cell} rep {rep}: "
       f"ev={row['ev']:.2f} tools={row['tools']}")
    return row


def pooled_rule(rows, task_name):
    rule_checks = set(_TASKS[task_name]["rule_checks"])
    out = {"n": 0, "passed": 0}
    for r in rows:
        for call, ok in (r.get("checks") or {}).items():
            if call in rule_checks:
                out["n"] += 1
                out["passed"] += 1 if ok else 0
    return out


def qualify(block, task_name, repeats=R, prior_rows=None):
    """Stage A gate cell: none at R, rule readings pooled per the
    standing annotation, mixed at the scaled minimum. Gate only, never
    a baseline."""
    t = _TASKS[task_name]
    qmin = qualify_min(task_name)
    prior = [r for r in prior_rows or []
             if r.get("stage") == "A" and r.get("task") == task_name]
    done = {r["rep"] for r in prior}
    rows = list(prior)
    for rep in range(repeats):
        if rep in done:
            continue
        rows.append(_run_one(t, [], "A", block, "none", rep))
    pooled = pooled_rule(rows, task_name)
    fails = pooled["n"] - pooled["passed"]
    qualified = pooled["passed"] >= qmin and fails >= qmin
    _p(f"stage A {block} {task_name}: pooled rule {pooled['passed']} "
       f"passes, {fails} fails of {pooled['n']} "
       f"({rule_n(task_name)} rule check(s) x {repeats}); "
       f"{'QUALIFIES' if qualified else 'does not qualify'} "
       f"(mixed means at least {qmin} of each)")
    return {"task": task_name, "rule_checks": rule_n(task_name),
            "pooled": pooled, "fails": fails, "qualify_min": qmin,
            "qualified": qualified}


def sweep(block, repeats=R, prior_rows=None):
    """One class sweep in ranked order, stopping at its first
    qualifier. An exhausted sweep closes its class on the supply
    answer."""
    results = []
    for name in SWEEPS[block]:
        result = qualify(block, name, repeats, prior_rows)
        results.append(result)
        if result["qualified"]:
            _p(f"{block} sweep stops at its first qualifier: {name}")
            return results, name
    _p(f"{block} sweep exhausted with no qualifier: the class closes "
       f"on the supply answer, the next ground is the conductor's cut")
    return results, None


def run_block(block, ground, stores, repeats=R, prior_rows=None):
    """Stage B: three fresh cells on the qualified ground, interleaved
    per rep in the fixed block order."""
    t = _TASKS[ground]
    prior = [r for r in prior_rows or []
             if r.get("stage") == "B" and r.get("block") == block]
    done = {(r["cell"], r["rep"]) for r in prior}
    rows = list(prior)
    for rep in range(repeats):
        for cell in BLOCK_CELLS[block]:
            if (cell, rep) in done:
                continue
            tools = cell_tools(cell, stores, ground)
            rows.append(_run_one(t, tools, "B", block, cell, rep))
    return rows


def check_table(rows, task_name):
    rule_checks = set(_TASKS[task_name]["rule_checks"])
    table = {}
    for r in rows:
        for call, ok in (r.get("checks") or {}).items():
            cell = (table.setdefault(call,
                                     {"rule_check": call in rule_checks,
                                      "cells": {}})
                    ["cells"].setdefault(r["cell"], {"n": 0, "passed": 0}))
            cell["n"] += 1
            cell["passed"] += 1 if ok else 0
    for c in table.values():
        for a in c["cells"].values():
            a["rate"] = a["passed"] / a["n"] if a["n"] else 0.0
    return table


def main(repeats=R, resume_ts=None):
    prior_rows = []
    if resume_ts:
        _set_ts(resume_ts)
        prior_rows = _load_rows()
        _p(f"RESUME {_TS}: {len(prior_rows)} checkpointed rows found")
    checks = byte_checks()
    stores = load_stores()
    _p(f"ARM THE FLOORS {_TS} (PACKET-022)")
    _p(f"performer={PERFORMER}  audience={AUDIENCE} (v1, production)")
    _p(f"sweeps (ranked): boundary={SWEEPS['boundary']}  "
       f"normalize={SWEEPS['normalize']}  R={repeats}")
    _p(f"qualification, the PACKET-019 fraction scaled to the ground: "
       f"at least 2 passes AND 2 fails of 12 pooled on one-rule ground, "
       f"at least 4 AND 4 of 24 on two-rule ground")
    _p(f"drift bar per comparison, same scaling: 2 of 12 pooled "
       f"one-rule, 4 of 24 pooled two-rule")
    _p(f"byte checks against the production lines: " +
       " ".join(f"{k}={checks[k]}" for k in sorted(checks)))
    for key in ("armed-B1", "armed-B2", "armed-N1", "armed-N2"):
        les = stores[key][0]
        aw = les["applies_when"]
        _p(f"{key}: gen_task={les['trail']['gen_task']}  "
           f"pins {aw['rule_class']}/{aw['rule_topic']}  "
           f"origin={les['trail']['origin_seat']}")
    for block in ("boundary", "normalize"):
        for name in SWEEPS[block]:
            _p(f"rule checks for {name} (the standing annotation): "
               f"{_TASKS[name]['rule_checks']}")

    # Stage A: both sweeps complete before any stage B run.
    stage_a = {}
    grounds = {}
    for block in ("boundary", "normalize"):
        stage_a[block], grounds[block] = sweep(block, repeats, prior_rows)

    # Stage B: the boundary block whole before the normalize block.
    stage_b = {}
    for block in ("boundary", "normalize"):
        if not grounds[block]:
            continue
        _p(f"stage B {block} block on qualified ground "
           f"{grounds[block]}: fresh interleaved cells in the fixed "
           f"order {BLOCK_CELLS[block]}, the stage A cell gates and is "
           f"never the baseline")
        rows = run_block(block, grounds[block], stores, repeats,
                         prior_rows)
        pooled = {cell: pooled_rule(
            [r for r in rows if r["cell"] == cell], grounds[block])
            for cell in BLOCK_CELLS[block]}
        stage_b[block] = {"ground": grounds[block],
                          "cells": list(BLOCK_CELLS[block]),
                          "drift_bar": f"{drift_bar(grounds[block])} of "
                                       f"{repeats * rule_n(grounds[block])}"
                                       f" pooled",
                          "rows": rows,
                          "check_table": check_table(rows,
                                                     grounds[block]),
                          "pooled_rule_checks": pooled}

    b_rows = [r for blk in stage_b.values() for r in blk["rows"]]
    audit_ok = all(r["tools"] == EXPECT_TOOLS[r["cell"]] for r in b_rows)

    report = {
        "armfloors22_id": _TS, "packet": "PACKET-022",
        "performer": PERFORMER, "audience": AUDIENCE, "repeats": repeats,
        "sweeps": {k: list(v) for k, v in SWEEPS.items()},
        "qualify_rule": "PACKET-019 fraction scaled: 2 of 12 pooled "
                        "one-rule, 4 of 24 pooled two-rule, passes AND "
                        "fails",
        "byte_checks": checks,
        "annotations": {name: _TASKS[name]["rule_checks"]
                        for b in SWEEPS for name in SWEEPS[b]},
        "lessons": {k: {"concept": stores[k][0]["concept"],
                        "rule": stores[k][0]["rule"],
                        "pins": stores[k][0]["applies_when"],
                        "gen_task": stores[k][0]["trail"]["gen_task"],
                        "origin_seat": stores[k][0]["trail"]
                        ["origin_seat"]} for k in stores},
        "stage_a": stage_a, "grounds": grounds,
        "stage_b": {b: {k: v for k, v in blk.items() if k != "rows"}
                    for b, blk in stage_b.items()},
        "tool_audit_ok": audit_ok,
        "priors": PRIORS,
        "n_note": ("Stage A gates only. The four signed readings, the "
                   "two-cause HARM sentences for armed-B2 and armed-N2, "
                   "the no-name watch columns, and the transfer note "
                   "live in the packet and are applied in its RESULTS. "
                   "armed-B2 is the wildcard pin's first exposure "
                   "reading; armed-N2's cell is its residue watch."),
    }
    with open(_REPORT, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    for block, blk in stage_b.items():
        ground = blk["ground"]
        _p(f"== STAGE B {block.upper()} ({ground}) POOLED RULE CHECKS "
           f"(passed/n per cell, bar {blk['drift_bar']}) ==")
        for cell in blk["cells"]:
            p = blk["pooled_rule_checks"][cell]
            _p(f"  {cell}: {p['passed']}/{p['n']}")
        _p(f"== STAGE B {block.upper()} PER-CHECK "
           f"({' / '.join(blk['cells'])}) ==")
        for call, c in blk["check_table"].items():
            rates = " / ".join(
                f"{c['cells'].get(a, {}).get('rate', 0.0):.2f}"
                for a in blk["cells"])
            mark = "  <-- rule" if c["rule_check"] else "  <-- watch"
            _p(f"  {call}: {rates}{mark}")

    counts_ok = all(
        sum(1 for r in stage_b[b]["rows"] if r["cell"] == c) == repeats
        for b in stage_b for c in BLOCK_CELLS[b])
    gate = counts_ok and audit_ok and os.path.exists(_ROWS)
    ran = [f"{b} on {stage_b[b]['ground']}" for b in stage_b]
    closed = [b for b in ("boundary", "normalize") if not grounds[b]]
    _p(f"GATE: {'PASSED' if gate else 'FAILED'}. both sweeps ran in "
       f"ranked order with the arithmetic printed, stage B "
       f"{', '.join(ran) if ran else 'did not run'}"
       + (f", {', '.join(closed)} closed on the supply answer"
          if closed else "")
       + f", all four byte checks asserted, tool audit "
       f"{'clean' if audit_ok else 'BROKEN'}, every run checkpointed, "
       f"report persisted. The readings are applied in the packet "
       f"RESULTS. The seat neither taught nor learned.")


if __name__ == "__main__":
    main(repeats=int(sys.argv[1]) if len(sys.argv) > 1 else R,
         resume_ts=sys.argv[2] if len(sys.argv) > 2 else None)
