"""PACKET-024: self-delivery. The production store's admitted eight
are all mistral-origin and none has ever been delivered back to its
origin seat. This packet runs the PACKET-022 design whole on that
seat: the same five apply floors, the same four lessons, mistral:7b
receiving its own store, audience llama3.1:8b (P019 precedent), v1
production path. Every armed cell is self-delivery, pre-registered as
such: it extends no transfer edge and is never pooled with the P022
llama cells, which sit beside it in RESULTS as the cross-seat exhibit.

Stage A qualifies ground per class in P022's ranked order (boundary:
merge_ranges, median, flatten_once; normalize: snake_to_camel,
balanced), a none cell at R=12 per candidate, stopping each sweep at
its first qualifier, canonical unrunnable-as-fail accounting
(DECISIONS 2026-07-04) with the per-cell unrunnable count reported and
readings-present beside as the diagnostic. A sweep that exhausts its
candidates closes that side on the supply answer, the third seat's
floors said plainly, a paid result.

Stage B, on qualified ground only: three fresh cells at R=12 each,
interleaved per rep in the fixed order none, armed-1, armed-2, the
boundary block whole before the normalize block. Each armed cell
delivers one production lesson through the menu path from its
single-lesson packet-local store, byte-checked against its production
line before any run. Drift bars: 2 of 12 pooled one-rule, 4 of 24
pooled two-rule.

The census, standing instrument, descriptive only: every output in
every cell classified by the shape it reached for, taxonomy printed
before any run, deterministic and re-runnable: py selfdeliv24.py
census <rows-file>. The moderator23 classifiers are reused unchanged
for merge_ranges, median, and flatten_once (imported, not copied); the
snake_to_camel and balanced classifiers are new here and commit with
this harness. Census data feeds the per-seat criterion table for
mistral and never flips a signed exit.

The four signed readings live in the packet and are applied in its
RESULTS by the reader. The seat neither teaches nor learns. The
harness reports, it does not rule."""

import ast
import json
import os
import sys
import time

import evidence
import lesson
import menu
import moderator23
import runner
from probe_tasks import APPLY_TASKS, CRITERIA, FEATURES

PERFORMER = "mistral:7b"
AUDIENCE = "llama3.1:8b"
R = 12

SWEEPS = {"boundary": ("merge_ranges", "median", "flatten_once"),
          "normalize": ("snake_to_camel", "balanced")}
BLOCKS = ("boundary", "normalize")
BLOCK_CELLS = {"boundary": ("none", "armed-B1", "armed-B2"),
               "normalize": ("none", "armed-N1", "armed-N2")}
EXPECT_TOOLS = {"none": 0, "armed-B1": 1, "armed-B2": 1,
                "armed-N1": 1, "armed-N2": 1}

_BENCH = os.path.dirname(os.path.abspath(__file__))
_PACKETS = os.path.join(_BENCH, "packets")
LESSONS_PROD = os.path.join(_BENCH, "lessons.jsonl")
ARMS = {"armed-B1": {"gen_task": "chunk",
                     "path": os.path.join(_PACKETS,
                                          "PACKET-024-lesson_B1.jsonl")},
        "armed-B2": {"gen_task": "weighted_mean",
                     "path": os.path.join(_PACKETS,
                                          "PACKET-024-lesson_B2.jsonl")},
        "armed-N1": {"gen_task": "split_csvish",
                     "path": os.path.join(_PACKETS,
                                          "PACKET-024-lesson_N1.jsonl")},
        "armed-N2": {"gen_task": "depth_max",
                     "path": os.path.join(_PACKETS,
                                          "PACKET-024-lesson_N2.jsonl")}}

PRIORS = {
    "P022_llama_same_lessons_and_grounds": {
        "stage_a": ("merge_ranges 0/12, median 24/24, flatten_once "
                    "8p/4f QUALIFIED, snake_to_camel 0/12, balanced "
                    "19p/5f QUALIFIED"),
        "flatten_once_block": ("canonical none 4/12, armed-B1 4/12, "
                               "armed-B2 2/12; unrunnable 2, 2, 4; "
                               "all FLAT"),
        "balanced_block": ("none 16/24, armed-N1 15/24, armed-N2 "
                           "20/24; all FLAT"),
        "note": "transfer cells, read beside, never pooled"},
    "P019_mistral_trait": ("qualified reproduced ground "
                           "second_largest, FLAT armed 13/24 against "
                           "none 12/24, the tool-indifference one-cell "
                           "lean"),
    "P017_mistral_stage1_R6_runlevel": {
        "merge_ranges": "all_fail 6/6", "median": "mixed 1/6 pass",
        "flatten_once": "all_fail 6/6",
        "snake_to_camel": "all_fail 6/6", "balanced": "all_pass",
        "note": ("run-level evidence counts at R=6, not rule-check "
                 "counts; no calibration-table prior exists for this "
                 "seat")},
}

_TASKS = {t["name"]: t for t in APPLY_TASKS}

_TS = time.strftime("%Y%m%d-%H%M%S")
_LOG = os.path.join(runner.RUNS, f"selfdeliv24-{_TS}.log")
_ROWS = os.path.join(runner.RUNS, f"selfdeliv24-{_TS}.rows.jsonl")
_REPORT = os.path.join(runner.RUNS, f"selfdeliv24-{_TS}.report.json")


def _set_ts(ts):
    """Rebind the run id and its file paths. Resume reuses a prior id so
    the checkpoint rows, the log, and the report stay one record."""
    global _TS, _LOG, _ROWS, _REPORT
    _TS = ts
    _LOG = os.path.join(runner.RUNS, f"selfdeliv24-{_TS}.log")
    _ROWS = os.path.join(runner.RUNS, f"selfdeliv24-{_TS}.rows.jsonl")
    _REPORT = os.path.join(runner.RUNS, f"selfdeliv24-{_TS}.report.json")


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
    return 2 * rule_n(task_name)


def drift_bar(task_name):
    return 2 * rule_n(task_name)


# ---------------------------------------------------------------------------
# The census. merge_ranges, median, and flatten_once reuse the
# committed moderator23 classifiers unchanged, imported not copied, so
# the two packets' censuses stay one instrument. snake_to_camel and
# balanced are new here, same discipline: deterministic AST logic over
# the persisted output text, re-runnable by the conductor. Precedence
# per task is stated in each function; "unrunnable" means the extracted
# code does not parse, and the rule tables' unrunnable column counts
# rows with zero evidence readings, any divergence reported.
# ---------------------------------------------------------------------------

CENSUS_TAXONOMY = {
    "merge_ranges": moderator23.CENSUS_TAXONOMY["merge_ranges"],
    "median": moderator23.CENSUS_TAXONOMY["median"],
    "flatten_once": moderator23.CENSUS_TAXONOMY["flatten_once"],
    "snake_to_camel": ("split-and-join", "regex", "char-walk", "other",
                       "unrunnable"),
    "balanced": ("counter-or-stack sweep", "count-equality shortcut",
                 "other", "unrunnable"),
}


def _uses_re(tree):
    for node in ast.walk(tree):
        if isinstance(node, ast.Attribute):
            if isinstance(node.value, ast.Name) and node.value.id == "re":
                return True
        if isinstance(node, ast.ImportFrom) and node.module == "re":
            return True
    return False


def _calls_attr(tree, attr):
    return any(isinstance(n, ast.Call)
               and isinstance(n.func, ast.Attribute)
               and n.func.attr == attr for n in ast.walk(tree))


def _sum_over_comprehension(tree):
    for node in ast.walk(tree):
        if (isinstance(node, ast.Call)
                and isinstance(node.func, ast.Name)
                and node.func.id == "sum"
                and any(isinstance(a, (ast.GeneratorExp, ast.ListComp))
                        for a in node.args)):
            return True
    return False


def _shape_snake_to_camel(tree):
    """Precedence: regex beats split-and-join beats char-walk beats
    other. split presence defines the split family whether the parts
    are joined or accumulated; a loop without split is the char walk."""
    if _uses_re(tree):
        return "regex"
    if _calls_attr(tree, "split"):
        return "split-and-join"
    if any(isinstance(n, (ast.For, ast.While)) for n in ast.walk(tree)):
        return "char-walk"
    return "other"


def _shape_balanced(tree):
    """Precedence: a loop with a branch is the sweep (counter or stack,
    the order-checking family) even when count calls also appear; a
    count comparison without the sweep loop is the shortcut, whether by
    .count or by sum over a comprehension."""
    if moderator23._loop_with_branch(tree):
        return "counter-or-stack sweep"
    if _calls_attr(tree, "count") or _sum_over_comprehension(tree):
        return "count-equality shortcut"
    return "other"


_CLASSIFIERS = {
    "merge_ranges": moderator23._shape_merge_ranges,
    "median": moderator23._shape_median,
    "flatten_once": moderator23._shape_flatten_once,
    "snake_to_camel": _shape_snake_to_camel,
    "balanced": _shape_balanced,
}


def census_shape(task_name, output_text):
    """Classify one persisted output by the shape it reached for."""
    code = evidence.extract_python(output_text)
    try:
        tree = ast.parse(code)
    except SyntaxError:
        return "unrunnable"
    return _CLASSIFIERS[task_name](tree)


def census_table(rows):
    """Shape distribution per (stage, block, task, cell)."""
    table = {}
    for r in rows:
        key = f"{r['stage']}|{r['block']}|{r['task']}|{r['cell']}"
        cell = table.setdefault(
            key, {s: 0 for s in CENSUS_TAXONOMY[r["task"]]})
        cell[r["shape"]] += 1
    return table


def recensus(rows_path, runs_dir=None):
    """Re-run the classifier over the persisted outputs behind a rows
    file and compare to the recorded shapes. The conductor's replay."""
    runs_dir = runs_dir or runner.RUNS
    mismatches = 0
    rows = [json.loads(l) for l in open(rows_path, encoding="utf-8")
            if l.strip()]
    for r in rows:
        spath = os.path.join(runs_dir, f"{r['run_id']}.summary.json")
        with open(spath, encoding="utf-8") as f:
            summary = json.load(f)
        fresh = census_shape(r["task"], summary["output"])
        if fresh != r["shape"]:
            mismatches += 1
            print(f"MISMATCH {r['run_id']}: recorded {r['shape']}, "
                  f"recomputed {fresh}")
    print(f"recensus: {len(rows)} rows, {mismatches} mismatches")
    return mismatches


# ---------------------------------------------------------------------------
# Materials
# ---------------------------------------------------------------------------

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
                             f"carry gen_task {cfg['gen_task']}, "
                             f"expected exactly 1")
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
        if lessons[0]["trail"]["gen_task"] != cfg["gen_task"]:
            raise SystemExit(f"wrong lesson in the {key} store")
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


# ---------------------------------------------------------------------------
# Cells
# ---------------------------------------------------------------------------

def _run_one(t, tools, stage, block, cell, rep):
    r = runner.run_once(t["task"], CRITERIA, _features(t),
                        model=PERFORMER, audience_model=AUDIENCE,
                        landscape=tools or None,
                        evidence_checks=t["checks"])
    checks = {c["call"]: bool(c["ok"]) for c in
              (r["evidence"] or {}).get("results") or []}
    row = {"stage": stage, "block": block, "cell": cell,
           "task": t["name"], "rep": rep, "run_id": r["run_id"],
           "verdict": r["verdict"], "tools": len(tools),
           "tool_concepts": [x["concept"] for x in tools],
           "ev": ev_fraction(r["evidence"]),
           "checks": checks,
           "no_readings": not checks,
           "shape": census_shape(t["name"], r["output"])}
    _row(row)
    _p(f"{stage} {block} {t['name']} {cell} rep {rep}: "
       f"ev={row['ev']:.2f} tools={row['tools']} shape={row['shape']}")
    return row


def pooled_rule(rows, task_name):
    """Canonical accounting (DECISIONS 2026-07-04): every row
    contributes every rule check and a missing reading counts as a
    fail. readings-present rides beside as the diagnostic."""
    rule_checks = set(_TASKS[task_name]["rule_checks"])
    out = {"n": len(rule_checks) * len(rows), "passed": 0,
           "present_n": 0, "present_passed": 0, "unrunnable_rows": 0}
    for r in rows:
        checks = r.get("checks") or {}
        if not checks:
            out["unrunnable_rows"] += 1
        for call, ok in checks.items():
            if call in rule_checks:
                out["present_n"] += 1
                if ok:
                    out["passed"] += 1
                    out["present_passed"] += 1
    return out


def qualify(block, task_name, repeats=R, prior_rows=None):
    """Stage A gate cell: none at R, canonical pooled rule counts,
    mixed at the scaled minimum. Gate only, never a baseline."""
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
       f"passes, {fails} fails of {pooled['n']} canonical "
       f"(unrunnable-as-fail; {pooled['unrunnable_rows']} unrunnable "
       f"rows; diagnostic {pooled['present_passed']}/"
       f"{pooled['present_n']} readings-present); "
       f"{'QUALIFIES' if qualified else 'does not qualify'} "
       f"(mixed means at least {qmin} of each)")
    return {"task": task_name, "rule_checks": rule_n(task_name),
            "pooled": pooled, "fails": fails, "qualify_min": qmin,
            "qualified": qualified}


def sweep(block, repeats=R, prior_rows=None):
    """One class sweep in ranked order, stopping at its first
    qualifier. An exhausted sweep closes its class on the supply
    answer, the third seat's floors said plainly."""
    results = []
    for name in SWEEPS[block]:
        result = qualify(block, name, repeats, prior_rows)
        results.append(result)
        if result["qualified"]:
            _p(f"{block} sweep stops at its first qualifier: {name}")
            return results, name
    _p(f"{block} sweep exhausted with no qualifier: the class closes "
       f"on the supply answer, the third seat's floors on the record")
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


def check_table(rows, task_name, cells):
    """Per-check canonical counts: passed over rows, with the
    readings-present n kept beside as the diagnostic."""
    rule_checks = set(_TASKS[task_name]["rule_checks"])
    n_rows = {c: sum(1 for r in rows if r["cell"] == c) for c in cells}
    table = {}
    for r in rows:
        for call, ok in (r.get("checks") or {}).items():
            cell = (table.setdefault(call,
                                     {"rule_check": call in rule_checks,
                                      "cells": {}})
                    ["cells"].setdefault(r["cell"],
                                         {"rows": n_rows[r["cell"]],
                                          "present_n": 0, "passed": 0}))
            cell["present_n"] += 1
            cell["passed"] += 1 if ok else 0
    for c in table.values():
        for a in c["cells"].values():
            a["rate"] = a["passed"] / a["rows"] if a["rows"] else 0.0
    return table


def main(repeats=R, resume_ts=None):
    prior_rows = []
    if resume_ts:
        _set_ts(resume_ts)
        prior_rows = _load_rows()
        _p(f"RESUME {_TS}: {len(prior_rows)} checkpointed rows found")
    checks = byte_checks()
    stores = load_stores()
    _p(f"SELF-DELIVERY {_TS} (PACKET-024)")
    _p(f"performer={PERFORMER}  audience={AUDIENCE} (v1, production)")
    _p(f"every armed cell is self-delivery: the origin seat receiving "
       f"its own store, no transfer edge, never pooled with the P022 "
       f"llama cells")
    _p(f"sweeps (P022 ranked order): boundary={SWEEPS['boundary']}  "
       f"normalize={SWEEPS['normalize']}  R={repeats}")
    _p(f"qualification at the standing fraction, canonical accounting "
       f"(unrunnable-as-fail, DECISIONS 2026-07-04): at least 2 passes "
       f"AND 2 fails of 12 pooled on one-rule ground, at least 4 AND 4 "
       f"of 24 on two-rule ground")
    _p(f"drift bars, scaled as standing: 2 of 12 pooled one-rule, "
       f"4 of 24 pooled two-rule")
    _p(f"byte checks against the production lines: " +
       " ".join(f"{k}={checks[k]}" for k in sorted(checks)))
    for key in ("armed-B1", "armed-B2", "armed-N1", "armed-N2"):
        les = stores[key][0]
        aw = les["applies_when"]
        _p(f"{key}: gen_task={les['trail']['gen_task']}  "
           f"pins {aw['rule_class']}/{aw['rule_topic']}  "
           f"origin={les['trail']['origin_seat']} (self-delivery)")
    _p("the census taxonomy, stated per task before any run "
       "(deterministic AST classifiers: merge_ranges, median, "
       "flatten_once reused unchanged from moderator23; snake_to_camel "
       "and balanced committed here; re-runnable: py selfdeliv24.py "
       "census <rows-file>):")
    for block in BLOCKS:
        for name in SWEEPS[block]:
            _p(f"  {name}: {', '.join(CENSUS_TAXONOMY[name])}")
    for block in BLOCKS:
        for name in SWEEPS[block]:
            _p(f"rule checks for {name} (the standing annotation): "
               f"{_TASKS[name]['rule_checks']}")

    # Stage A: both sweeps complete before any stage B run.
    stage_a = {}
    grounds = {}
    for block in BLOCKS:
        stage_a[block], grounds[block] = sweep(block, repeats,
                                               prior_rows)

    # Stage B: the boundary block whole before the normalize block.
    stage_b = {}
    for block in BLOCKS:
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
                          "check_table": check_table(
                              rows, grounds[block],
                              BLOCK_CELLS[block]),
                          "pooled_rule_checks": pooled}

    all_rows = _load_rows()
    b_rows = [r for blk in stage_b.values() for r in blk["rows"]]
    audit_ok = all(r["tools"] == EXPECT_TOOLS[r["cell"]] for r in b_rows)
    census = census_table(all_rows)
    divergent = sum(1 for r in all_rows
                    if (r["shape"] == "unrunnable") != r["no_readings"])

    report = {
        "selfdeliv24_id": _TS, "packet": "PACKET-024",
        "performer": PERFORMER, "audience": AUDIENCE, "repeats": repeats,
        "self_delivery_note": "origin seat receiving its own store; no "
                              "transfer edge; never pooled with P022",
        "sweeps": {k: list(v) for k, v in SWEEPS.items()},
        "qualify_rule": "standing fraction, canonical accounting: "
                        "2 of 12 pooled one-rule, 4 of 24 pooled "
                        "two-rule, passes AND fails, unrunnable-as-fail",
        "byte_checks": checks,
        "annotations": {name: _TASKS[name]["rule_checks"]
                        for b in BLOCKS for name in SWEEPS[b]},
        "lessons": {k: {"concept": stores[k][0]["concept"],
                        "rule": stores[k][0]["rule"],
                        "pins": stores[k][0]["applies_when"],
                        "gen_task": stores[k][0]["trail"]["gen_task"],
                        "origin_seat": stores[k][0]["trail"]
                        ["origin_seat"]} for k in stores},
        "census_taxonomy": CENSUS_TAXONOMY,
        "stage_a": stage_a, "grounds": grounds,
        "stage_b": {b: {k: v for k, v in blk.items() if k != "rows"}
                    for b, blk in stage_b.items()},
        "census": census,
        "census_no_readings_divergence": divergent,
        "tool_audit_ok": audit_ok,
        "priors": PRIORS,
        "n_note": ("Stage A gates only. The four signed readings, the "
                   "two-cause HARM sentences for armed-B2 and armed-N2, "
                   "the no-name watch columns, the self-delivery note, "
                   "and the census's descriptive role live in the "
                   "packet and are applied in its RESULTS. Census data "
                   "never flips a signed exit."),
    }
    with open(_REPORT, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    for block, blk in stage_b.items():
        ground = blk["ground"]
        _p(f"== STAGE B {block.upper()} ({ground}) POOLED RULE CHECKS "
           f"(canonical passed/n per cell, bar {blk['drift_bar']}) ==")
        for cell in blk["cells"]:
            p = blk["pooled_rule_checks"][cell]
            _p(f"  {cell}: {p['passed']}/{p['n']} "
               f"(diagnostic {p['present_passed']}/{p['present_n']} "
               f"readings-present; unrunnable rows "
               f"{p['unrunnable_rows']})")
        _p(f"== STAGE B {block.upper()} PER-CHECK canonical "
           f"({' / '.join(blk['cells'])}) ==")
        for call, c in blk["check_table"].items():
            rates = " / ".join(
                f"{c['cells'].get(a, {}).get('rate', 0.0):.2f}"
                for a in blk["cells"])
            mark = "  <-- rule" if c["rule_check"] else "  <-- watch"
            _p(f"  {call}: {rates}{mark}")

    _p("== CENSUS (shape distribution per cell, every cell run, "
       "descriptive only) ==")
    for key in sorted(census):
        dist = "  ".join(f"{s}={n}" for s, n in census[key].items())
        _p(f"  {key}: {dist}")
    _p(f"census unrunnable against zero-readings divergence: "
       f"{divergent} rows")

    counts_ok = all(
        sum(1 for r in stage_b[b]["rows"] if r["cell"] == c) == repeats
        for b in stage_b for c in BLOCK_CELLS[b])
    gate = counts_ok and audit_ok and os.path.exists(_ROWS)
    ran = [f"{b} on {stage_b[b]['ground']}" for b in stage_b]
    closed = [b for b in BLOCKS if not grounds[b]]
    _p(f"GATE: {'PASSED' if gate else 'FAILED'}. both sweeps ran in "
       f"ranked order with the arithmetic printed, stage B "
       f"{', '.join(ran) if ran else 'did not run'}"
       + (f", {', '.join(closed)} closed on the supply answer"
          if closed else "")
       + f", all four byte checks asserted, tool audit "
       f"{'clean' if audit_ok else 'BROKEN'}, census reported for "
       f"every cell, every run checkpointed, report persisted. The "
       f"readings are applied in the packet RESULTS. The seat neither "
       f"taught nor learned.")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "census":
        raise SystemExit(recensus(sys.argv[2]))
    main(repeats=int(sys.argv[1]) if len(sys.argv) > 1 else R,
         resume_ts=sys.argv[2] if len(sys.argv) > 2 else None)
