"""PACKET-023: the moderator test. One lesson, one seat, two grounds
classified in opposite directions before the run, so the readings land
on the idiom-conflict moderator and nothing else. Performer
qwen2.5-coder:7b (the amplifier, where the moderator was observed),
audience llama3.1:8b, v1 production path. The classification table is
pre-registration and lives in the packet, never here.

Stage A qualifies ground per side in ranked order (FIGHTS:
flatten_once, merge_ranges; EXTENDS: median), a none cell at R=12 per
candidate, stopping each sweep at its first qualifier. Qualification
at the standing fraction scaled to the ground's rule-check count, on
the canonical accounting: unrunnable outputs count as fails in every
pooled rule count (DECISIONS 2026-07-04), the per-cell unrunnable
count is its own column, and readings-present rides beside as the
diagnostic. A sweep that exhausts its candidates closes that side on
the supply answer.

Stage B, on qualified ground only: two fresh cells at R=12 each,
interleaved per rep in the fixed order none then armed, the FIGHTS
block whole before the EXTENDS block. The armed cell delivers the B1
chunk lesson (production line 8, pins boundary/degenerate, mistral
origin) through the menu path from its single-lesson packet-local
store, byte-checked against its production line before any run. Drift
bars: 2 of 12 pooled one-rule, 4 of 24 pooled two-rule.

The census instrument, pre-registered as descriptive: every output in
every cell, stage A included, is classified by the solution shape it
reached for. The taxonomy prints before any run and the classifier
below is deterministic AST logic over persisted outputs, so the
conductor can re-run it: py moderator23.py census <rows-file>. Census
data interprets a FLAT and contextualizes a landed sign; it never
flips a signed exit.

The three signed readings live in the packet and are applied in its
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
import runner
from probe_tasks import APPLY_TASKS, CRITERIA, FEATURES

PERFORMER = "qwen2.5-coder:7b"
AUDIENCE = "llama3.1:8b"
R = 12

SWEEPS = {"fights": ("flatten_once", "merge_ranges"),
          "extends": ("median",)}
BLOCKS = ("fights", "extends")
CELLS = ("none", "armed")
EXPECT_TOOLS = {"none": 0, "armed": 1}

_BENCH = os.path.dirname(os.path.abspath(__file__))
_PACKETS = os.path.join(_BENCH, "packets")
LESSONS_PROD = os.path.join(_BENCH, "lessons.jsonl")
STORE = os.path.join(_PACKETS, "PACKET-023-lesson_B1.jsonl")
STORE_GEN_TASK = "chunk"

PRIORS = {
    "anchors_calibrated_not_confirming": {
        "longest_word_FIGHTS": ("tie lessons on qwen, three "
                                "same-direction declines, gaps 6/24, "
                                "4/24, 11/24, direction never a rate"),
        "range_summary_EXTENDS": ("lifts on qwen, replicated: none 8/12 "
                                  "to rev 12/12 and hand 12/12 (P15), "
                                  "none 4/12 to rev 11/12 and hand "
                                  "10/12 (P21)")},
    "boundary_class_to_qwen": ("no prior boundary-class delivery cell "
                               "to this seat exists; these are the "
                               "first"),
    "calibration_n1_seatA": {"flatten_once": 0.33, "merge_ranges": 0.75,
                             "median": 1.00},
    "collateral_safety": ("the amplifier's harm columns clean four "
                          "consecutive measurements"),
}

_TASKS = {t["name"]: t for t in APPLY_TASKS}

_TS = time.strftime("%Y%m%d-%H%M%S")
_LOG = os.path.join(runner.RUNS, f"moderator23-{_TS}.log")
_ROWS = os.path.join(runner.RUNS, f"moderator23-{_TS}.rows.jsonl")
_REPORT = os.path.join(runner.RUNS, f"moderator23-{_TS}.report.json")


def _set_ts(ts):
    """Rebind the run id and its file paths. Resume reuses a prior id so
    the checkpoint rows, the log, and the report stay one record."""
    global _TS, _LOG, _ROWS, _REPORT
    _TS = ts
    _LOG = os.path.join(runner.RUNS, f"moderator23-{_TS}.log")
    _ROWS = os.path.join(runner.RUNS, f"moderator23-{_TS}.rows.jsonl")
    _REPORT = os.path.join(runner.RUNS, f"moderator23-{_TS}.report.json")


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
# The census classifier. Deterministic AST logic over the persisted
# output text, committed with the harness per the packet gate. The
# taxonomy is per task and prints before any run. "unrunnable" here
# means the extracted code does not parse; the rule tables' unrunnable
# column counts rows with zero evidence readings (which also covers
# module-level crashes and timeouts), and any divergence between the
# two is reported, never hidden.
# ---------------------------------------------------------------------------

CENSUS_TAXONOMY = {
    "flatten_once": ("comprehension", "loop-with-branch", "other",
                     "unrunnable"),
    "merge_ranges": ("sweep", "other", "unrunnable"),
    "median": ("sort-and-index", "other", "unrunnable"),
}


def _has_sort(tree):
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            f = node.func
            if isinstance(f, ast.Name) and f.id == "sorted":
                return True
            if isinstance(f, ast.Attribute) and f.attr == "sort":
                return True
    return False


def _has_node(tree, types):
    return any(isinstance(n, types) for n in ast.walk(tree))


def _loop_with_branch(tree):
    for node in ast.walk(tree):
        if isinstance(node, (ast.For, ast.While)):
            for sub in ast.walk(node):
                if sub is not node and isinstance(sub, (ast.If,
                                                        ast.IfExp)):
                    return True
    return False


def _shape_flatten_once(tree):
    if _loop_with_branch(tree):
        return "loop-with-branch"
    if _has_node(tree, (ast.ListComp, ast.SetComp, ast.GeneratorExp)):
        return "comprehension"
    return "other"


def _shape_merge_ranges(tree):
    if _has_sort(tree) and _has_node(tree, (ast.For, ast.While)):
        return "sweep"
    return "other"


def _shape_median(tree):
    if _has_sort(tree) and _has_node(tree, ast.Subscript):
        return "sort-and-index"
    return "other"


_CLASSIFIERS = {"flatten_once": _shape_flatten_once,
                "merge_ranges": _shape_merge_ranges,
                "median": _shape_median}


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

def byte_check():
    """The packet-local store byte-identical to its production line,
    asserted before any stage B run. The line is found by its trail
    gen_task, and a duplicate match fails loudly instead of guessing."""
    with open(LESSONS_PROD, "rb") as f:
        prod_lines = [l for l in f.read().split(b"\n") if l.strip()]
    matches = [l for l in prod_lines
               if (json.loads(l).get("trail") or {}).get("gen_task")
               == STORE_GEN_TASK]
    if len(matches) != 1:
        raise SystemExit(f"{len(matches)} production lines carry "
                         f"gen_task {STORE_GEN_TASK}, expected exactly 1")
    with open(STORE, "rb") as f:
        ok = f.read() == matches[0] + b"\n"
    if not ok:
        raise SystemExit("byte check failed, the lesson was touched")
    return ok


def load_store():
    lessons = lesson.load(STORE)
    if len(lessons) != 1:
        raise SystemExit(f"store must hold 1 lesson, "
                         f"found {len(lessons)}")
    lesson.validate(lessons[0])
    if lessons[0]["trail"]["gen_task"] != STORE_GEN_TASK:
        raise SystemExit("wrong lesson in the store")
    return lessons


def cell_tools(cell, store, task_name):
    if cell == "none":
        return []
    tools = menu.query(store, _features(_TASKS[task_name]))
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
    """One side's sweep in ranked order, stopping at its first
    qualifier. An exhausted sweep closes its side on the supply
    answer."""
    results = []
    for name in SWEEPS[block]:
        result = qualify(block, name, repeats, prior_rows)
        results.append(result)
        if result["qualified"]:
            _p(f"{block} sweep stops at its first qualifier: {name}")
            return results, name
    _p(f"{block} sweep exhausted with no qualifier: this side closes "
       f"on the supply answer and the moderator stays untested on it")
    return results, None


def run_block(block, ground, store, repeats=R, prior_rows=None):
    """Stage B: two fresh cells on the qualified ground, interleaved
    per rep, none then armed."""
    t = _TASKS[ground]
    prior = [r for r in prior_rows or []
             if r.get("stage") == "B" and r.get("block") == block]
    done = {(r["cell"], r["rep"]) for r in prior}
    rows = list(prior)
    for rep in range(repeats):
        for cell in CELLS:
            if (cell, rep) in done:
                continue
            tools = cell_tools(cell, store, ground)
            rows.append(_run_one(t, tools, "B", block, cell, rep))
    return rows


def check_table(rows, task_name):
    """Per-check canonical counts: passed over rows, with the
    readings-present n kept beside as the diagnostic."""
    rule_checks = set(_TASKS[task_name]["rule_checks"])
    n_rows = {c: sum(1 for r in rows if r["cell"] == c) for c in CELLS}
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
    ok = byte_check()
    store = load_store()
    les = store[0]
    aw = les["applies_when"]
    _p(f"MODERATOR TEST {_TS} (PACKET-023)")
    _p(f"performer={PERFORMER}  audience={AUDIENCE} (v1, production)")
    _p(f"sweeps (ranked): FIGHTS={SWEEPS['fights']}  "
       f"EXTENDS={SWEEPS['extends']}  R={repeats}")
    _p(f"qualification at the standing fraction, canonical accounting "
       f"(unrunnable-as-fail, DECISIONS 2026-07-04): at least 2 passes "
       f"AND 2 fails of 12 pooled on one-rule ground, at least 4 AND 4 "
       f"of 24 on two-rule ground")
    _p(f"drift bars, scaled as standing: 2 of 12 pooled one-rule, "
       f"4 of 24 pooled two-rule")
    _p(f"byte check against production line: {ok}")
    _p(f"B1: gen_task={les['trail']['gen_task']}  "
       f"pins {aw['rule_class']}/{aw['rule_topic']}  "
       f"origin={les['trail']['origin_seat']}")
    _p("the census taxonomy, stated per task before any run "
       "(deterministic AST classifier, committed with this harness, "
       "re-runnable: py moderator23.py census <rows-file>):")
    for name in ("flatten_once", "merge_ranges", "median"):
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

    # Stage B: the FIGHTS block whole before the EXTENDS block.
    stage_b = {}
    for block in BLOCKS:
        if not grounds[block]:
            continue
        _p(f"stage B {block} block on qualified ground "
           f"{grounds[block]}: fresh interleaved cells, none then "
           f"armed per rep, the stage A cell gates and is never the "
           f"baseline")
        rows = run_block(block, grounds[block], store, repeats,
                         prior_rows)
        pooled = {cell: pooled_rule(
            [r for r in rows if r["cell"] == cell], grounds[block])
            for cell in CELLS}
        stage_b[block] = {"ground": grounds[block],
                          "cells": list(CELLS),
                          "drift_bar": f"{drift_bar(grounds[block])} of "
                                       f"{repeats * rule_n(grounds[block])}"
                                       f" pooled",
                          "rows": rows,
                          "check_table": check_table(rows,
                                                     grounds[block]),
                          "pooled_rule_checks": pooled}

    all_rows = _load_rows()
    b_rows = [r for blk in stage_b.values() for r in blk["rows"]]
    audit_ok = all(r["tools"] == EXPECT_TOOLS[r["cell"]] for r in b_rows)
    census = census_table(all_rows)
    divergent = sum(1 for r in all_rows
                    if (r["shape"] == "unrunnable") != r["no_readings"])

    report = {
        "moderator23_id": _TS, "packet": "PACKET-023",
        "performer": PERFORMER, "audience": AUDIENCE, "repeats": repeats,
        "sweeps": {k: list(v) for k, v in SWEEPS.items()},
        "qualify_rule": "standing fraction, canonical accounting: "
                        "2 of 12 pooled one-rule, 4 of 24 pooled "
                        "two-rule, passes AND fails, unrunnable-as-fail",
        "byte_check": ok,
        "annotations": {name: _TASKS[name]["rule_checks"]
                        for b in BLOCKS for name in SWEEPS[b]},
        "lesson": {"concept": les["concept"], "rule": les["rule"],
                   "pins": aw, "gen_task": les["trail"]["gen_task"],
                   "origin_seat": les["trail"]["origin_seat"]},
        "census_taxonomy": CENSUS_TAXONOMY,
        "stage_a": stage_a, "grounds": grounds,
        "stage_b": {b: {k: v for k, v in blk.items() if k != "rows"}
                    for b, blk in stage_b.items()},
        "census": census,
        "census_no_readings_divergence": divergent,
        "tool_audit_ok": audit_ok,
        "priors": PRIORS,
        "n_note": ("Stage A gates only. The three signed readings, the "
                   "census's pre-registered descriptive role, and the "
                   "no-name watch columns live in the packet and are "
                   "applied in its RESULTS. Census data never flips a "
                   "signed exit."),
    }
    with open(_REPORT, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    for block, blk in stage_b.items():
        ground = blk["ground"]
        _p(f"== STAGE B {block.upper()} ({ground}) POOLED RULE CHECKS "
           f"(canonical passed/n per cell, bar {blk['drift_bar']}) ==")
        for cell in CELLS:
            p = blk["pooled_rule_checks"][cell]
            _p(f"  {cell}: {p['passed']}/{p['n']} "
               f"(diagnostic {p['present_passed']}/{p['present_n']} "
               f"readings-present; unrunnable rows "
               f"{p['unrunnable_rows']})")
        _p(f"== STAGE B {block.upper()} PER-CHECK canonical "
           f"({' / '.join(CELLS)}) ==")
        for call, c in blk["check_table"].items():
            rates = " / ".join(
                f"{c['cells'].get(a, {}).get('rate', 0.0):.2f}"
                for a in CELLS)
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
        for b in stage_b for c in CELLS)
    gate = counts_ok and audit_ok and os.path.exists(_ROWS)
    ran = [f"{b} on {stage_b[b]['ground']}" for b in stage_b]
    closed = [b for b in BLOCKS if not grounds[b]]
    _p(f"GATE: {'PASSED' if gate else 'FAILED'}. both sweeps ran in "
       f"ranked order with the arithmetic printed, stage B "
       f"{', '.join(ran) if ran else 'did not run'}"
       + (f", {', '.join(closed)} closed on the supply answer"
          if closed else "")
       + f", byte check asserted, tool audit "
       f"{'clean' if audit_ok else 'BROKEN'}, census reported for "
       f"every cell, every run checkpointed, report persisted. The "
       f"readings are applied in the packet RESULTS. The seat neither "
       f"taught nor learned.")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "census":
        raise SystemExit(recensus(sys.argv[2]))
    main(repeats=int(sys.argv[1]) if len(sys.argv) > 1 else R,
         resume_ts=sys.argv[2] if len(sys.argv) > 2 else None)
