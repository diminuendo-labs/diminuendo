"""PACKET-025: the shape-steering replication, the trigger. One cell
in PACKET-022 produced the record's first mechanism-shaped
observation: under the depth_max lesson, llama's balanced census moved
4 to 8 sweeps of 12 beside a rule direction up at exactly the bar,
post-hoc, unregistered, a lead. This packet is the pre-registered
replication that alone can move canon, and only through the conductor:
this harness reports, it does not rule, and no exit here touches any
canonical document.

Performer llama3.1:8b, audience qwen2.5-coder:7b, v1 production path.
Stage A qualifies balanced, the ground where the lead was born, none
at R=12, canonical unrunnable-as-fail accounting, two-rule ground so
mixed means at least 4 passes AND 4 fails of 24 pooled. If it refuses,
the packet closes on the supply answer and the replication is
unmeasured, the lead keeping a failed-to-ground attempt on its record.

Stage B, on qualified ground only: two fresh cells at R=12,
interleaved per rep in the fixed order none then armed-N2, the
depth_max lesson riding byte-verbatim from its single-lesson
packet-local store through the production menu path, byte-check
asserted against production line 11 before any run.

The census is the primary instrument here, not a side table: reading 1
lives on the armed-against-none sweep count at a 2-of-12 bar, reading
2 on the pooled rule checks at the standing 4-of-24 bar, the two
independent by pre-registration, and both are applied in the packet
RESULTS by the reader. The balanced classifier is selfdeliv24's,
imported unchanged and pinned by identity test, taxonomy printed
before any run, replayable: py shapesteer25.py census <rows-file>.
The seat neither teaches nor learns."""

import json
import os
import sys
import time

import lesson
import menu
import runner
import selfdeliv24
from probe_tasks import APPLY_TASKS, CRITERIA, FEATURES

PERFORMER = "llama3.1:8b"
AUDIENCE = "qwen2.5-coder:7b"
R = 12
TASK = "balanced"
CELLS = ("none", "armed-N2")
EXPECT_TOOLS = {"none": 0, "armed-N2": 1}
SWEEP_SHAPE = "counter-or-stack sweep"

_BENCH = os.path.dirname(os.path.abspath(__file__))
_PACKETS = os.path.join(_BENCH, "packets")
LESSONS_PROD = os.path.join(_BENCH, "lessons.jsonl")
STORE = os.path.join(_PACKETS, "PACKET-025-lesson_N2.jsonl")
STORE_GEN_TASK = "depth_max"
STORE_PROD_LINE = 11  # 1-indexed position in the production store

# The committed selfdeliv24 balanced classifier, unchanged. The
# identity is pinned by test; the taxonomy is printed before any run.
_BALANCED_CLASSIFIER = selfdeliv24._shape_balanced
TAXONOMY = selfdeliv24.CENSUS_TAXONOMY["balanced"]

PRIORS = {
    "origin_lead_P022_armed_N2_on_balanced": (
        "census 4 to 8 sweep of 12, pooled rule 16 to 20 of 24, "
        "post-hoc, unregistered, the observation this packet exists "
        "to test, never pooled with these cells"),
    "P022_stage_a_balanced": "19 passes 5 fails of 24, qualified",
    "P022_llama_none_census_balanced": "8 shortcut, 4 sweep of 12",
}

_TASKS = {t["name"]: t for t in APPLY_TASKS}
RULE_N = len(_TASKS[TASK]["rule_checks"])
QUALIFY_MIN = 2 * RULE_N   # 4 of 24 pooled, the standing fraction
RULE_BAR = 2 * RULE_N      # reading 2, the standing drift bar
CENSUS_BAR = 2             # reading 1, of 12 rows, stated in the packet

_TS = time.strftime("%Y%m%d-%H%M%S")
_LOG = os.path.join(runner.RUNS, f"shapesteer25-{_TS}.log")
_ROWS = os.path.join(runner.RUNS, f"shapesteer25-{_TS}.rows.jsonl")
_REPORT = os.path.join(runner.RUNS, f"shapesteer25-{_TS}.report.json")


def _set_ts(ts):
    """Rebind the run id and its file paths. Resume reuses a prior id so
    the checkpoint rows, the log, and the report stay one record."""
    global _TS, _LOG, _ROWS, _REPORT
    _TS = ts
    _LOG = os.path.join(runner.RUNS, f"shapesteer25-{_TS}.log")
    _ROWS = os.path.join(runner.RUNS, f"shapesteer25-{_TS}.rows.jsonl")
    _REPORT = os.path.join(runner.RUNS, f"shapesteer25-{_TS}.report.json")


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


def census_shape(output_text):
    """The selfdeliv24 balanced classifier, unchanged, whole path."""
    return selfdeliv24.census_shape(TASK, output_text)


def census_table(rows):
    """Shape distribution per (stage, cell)."""
    table = {}
    for r in rows:
        key = f"{r['stage']}|{r['cell']}"
        cell = table.setdefault(key, {s: 0 for s in TAXONOMY})
        cell[r["shape"]] += 1
    return table


def sweep_counts(rows):
    """Reading 1's numbers: sweep-shape rows per stage B cell."""
    out = {}
    for cell in CELLS:
        out[cell] = sum(1 for r in rows
                        if r["stage"] == "B" and r["cell"] == cell
                        and r["shape"] == SWEEP_SHAPE)
    return out


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
        fresh = census_shape(summary["output"])
        if fresh != r["shape"]:
            mismatches += 1
            print(f"MISMATCH {r['run_id']}: recorded {r['shape']}, "
                  f"recomputed {fresh}")
    print(f"recensus: {len(rows)} rows, {mismatches} mismatches")
    return mismatches


def byte_check():
    """The packet-local store byte-identical to production line 11,
    asserted before any stage B run. Found by trail gen_task, position
    asserted, a duplicate match fails loudly."""
    with open(LESSONS_PROD, "rb") as f:
        prod_lines = [l for l in f.read().split(b"\n") if l.strip()]
    matches = [(i, l) for i, l in enumerate(prod_lines, start=1)
               if (json.loads(l).get("trail") or {}).get("gen_task")
               == STORE_GEN_TASK]
    if len(matches) != 1:
        raise SystemExit(f"{len(matches)} production lines carry "
                         f"gen_task {STORE_GEN_TASK}, expected exactly 1")
    line_no, src = matches[0]
    if line_no != STORE_PROD_LINE:
        raise SystemExit(f"{STORE_GEN_TASK} sits at production line "
                         f"{line_no}, the packet names line "
                         f"{STORE_PROD_LINE}")
    with open(STORE, "rb") as f:
        ok = f.read() == src + b"\n"
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


def cell_tools(cell, store):
    if cell == "none":
        return []
    tools = menu.query(store, _features(_TASKS[TASK]))
    if len(tools) != EXPECT_TOOLS[cell]:
        raise SystemExit(f"{cell}: expected {EXPECT_TOOLS[cell]} "
                         f"tools, got {len(tools)}")
    return tools


def _run_one(t, tools, stage, cell, rep):
    r = runner.run_once(t["task"], CRITERIA, _features(t),
                        model=PERFORMER, audience_model=AUDIENCE,
                        landscape=tools or None,
                        evidence_checks=t["checks"])
    checks = {c["call"]: bool(c["ok"]) for c in
              (r["evidence"] or {}).get("results") or []}
    row = {"stage": stage, "cell": cell, "task": t["name"],
           "rep": rep, "run_id": r["run_id"], "verdict": r["verdict"],
           "tools": len(tools),
           "tool_concepts": [x["concept"] for x in tools],
           "ev": ev_fraction(r["evidence"]),
           "checks": checks,
           "no_readings": not checks,
           "shape": census_shape(r["output"])}
    _row(row)
    _p(f"{stage} {t['name']} {cell} rep {rep}: ev={row['ev']:.2f} "
       f"tools={row['tools']} shape={row['shape']}")
    return row


def pooled_rule(rows):
    """Canonical accounting (DECISIONS 2026-07-04): every row
    contributes every rule check and a missing reading counts as a
    fail. readings-present rides beside as the diagnostic."""
    rule_checks = set(_TASKS[TASK]["rule_checks"])
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


def qualify(repeats=R, prior_rows=None):
    """Stage A gate cell on the one candidate, balanced. Gate only,
    never a baseline."""
    t = _TASKS[TASK]
    prior = [r for r in prior_rows or [] if r.get("stage") == "A"]
    done = {r["rep"] for r in prior}
    rows = list(prior)
    for rep in range(repeats):
        if rep in done:
            continue
        rows.append(_run_one(t, [], "A", "none", rep))
    pooled = pooled_rule(rows)
    fails = pooled["n"] - pooled["passed"]
    qualified = (pooled["passed"] >= QUALIFY_MIN
                 and fails >= QUALIFY_MIN)
    _p(f"stage A {TASK}: pooled rule {pooled['passed']} passes, "
       f"{fails} fails of {pooled['n']} canonical "
       f"(unrunnable-as-fail; {pooled['unrunnable_rows']} unrunnable "
       f"rows; diagnostic {pooled['present_passed']}/"
       f"{pooled['present_n']} readings-present); "
       f"{'QUALIFIES' if qualified else 'does not qualify'} "
       f"(mixed means at least {QUALIFY_MIN} of each)")
    return {"task": TASK, "pooled": pooled, "fails": fails,
            "qualify_min": QUALIFY_MIN, "qualified": qualified}


def run_block(store, repeats=R, prior_rows=None):
    """Stage B: the two replication cells, interleaved per rep, none
    then armed-N2, one unit."""
    t = _TASKS[TASK]
    prior = [r for r in prior_rows or [] if r.get("stage") == "B"]
    done = {(r["cell"], r["rep"]) for r in prior}
    rows = list(prior)
    for rep in range(repeats):
        for cell in CELLS:
            if (cell, rep) in done:
                continue
            tools = cell_tools(cell, store)
            rows.append(_run_one(t, tools, "B", cell, rep))
    return rows


def check_table(rows):
    """Per-check canonical counts with the readings-present n beside."""
    rule_checks = set(_TASKS[TASK]["rule_checks"])
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
    _p(f"SHAPE-STEERING REPLICATION {_TS} (PACKET-025, the trigger)")
    _p(f"performer={PERFORMER}  audience={AUDIENCE} (v1, production)")
    _p(f"ground={TASK} (the one candidate, where the lead was born)  "
       f"R={repeats}")
    _p(f"qualification, canonical accounting: at least {QUALIFY_MIN} "
       f"passes AND {QUALIFY_MIN} fails of {RULE_N * repeats} pooled")
    _p(f"reading 1 PRIMARY, the census: armed sweep count against "
       f"none, both of {repeats} rows, bar {CENSUS_BAR} of {repeats}")
    _p(f"reading 2 SECONDARY, pooled rule: standing bar {RULE_BAR} of "
       f"{RULE_N * repeats}; the two readings independent, neither "
       f"flips the other")
    _p(f"byte check against production line {STORE_PROD_LINE}: {ok}")
    _p(f"armed-N2: gen_task={les['trail']['gen_task']}  "
       f"pins {aw['rule_class']}/{aw['rule_topic']}  "
       f"origin={les['trail']['origin_seat']}  carries the flagged "
       f"cross-topic residue, its delivery cell is its watch")
    _p(f"the census taxonomy, stated before any run (the selfdeliv24 "
       f"balanced classifier, unchanged, identity-pinned by test, "
       f"re-runnable: py shapesteer25.py census <rows-file>): "
       f"{', '.join(TAXONOMY)}")
    _p(f"rule checks for {TASK} (the standing annotation): "
       f"{_TASKS[TASK]['rule_checks']}")

    stage_a = qualify(repeats, prior_rows)

    stage_b_rows = []
    pooled_b = {}
    table = {}
    sweeps = {}
    if stage_a["qualified"]:
        _p(f"stage B on qualified ground: fresh interleaved cells, "
           f"{CELLS} per rep, the stage A cell gates and is never the "
           f"baseline")
        stage_b_rows = run_block(store, repeats, prior_rows)
        pooled_b = {cell: pooled_rule(
            [r for r in stage_b_rows if r["cell"] == cell])
            for cell in CELLS}
        table = check_table(stage_b_rows)
        sweeps = sweep_counts(stage_b_rows)
    else:
        _p("balanced does not qualify: the packet closes on the "
           "supply answer, the replication is unmeasured, and the "
           "lead keeps a failed-to-ground attempt on its record")

    all_rows = _load_rows()
    audit_ok = all(r["tools"] == EXPECT_TOOLS[r["cell"]]
                   for r in stage_b_rows)
    census = census_table(all_rows)
    divergent = sum(1 for r in all_rows
                    if (r["shape"] == "unrunnable") != r["no_readings"])

    report = {
        "shapesteer25_id": _TS, "packet": "PACKET-025",
        "performer": PERFORMER, "audience": AUDIENCE,
        "task": TASK, "repeats": repeats,
        "byte_check": ok, "store_prod_line": STORE_PROD_LINE,
        "annotations": _TASKS[TASK]["rule_checks"],
        "lesson": {"concept": les["concept"], "rule": les["rule"],
                   "pins": aw, "gen_task": les["trail"]["gen_task"],
                   "origin_seat": les["trail"]["origin_seat"]},
        "census_taxonomy": list(TAXONOMY),
        "stage_a": stage_a,
        "stage_b": {"ran": stage_a["qualified"],
                    "cells": list(CELLS),
                    "census_bar": f"{CENSUS_BAR} of {repeats}",
                    "rule_bar": f"{RULE_BAR} of {RULE_N * repeats}",
                    "sweep_counts": sweeps,
                    "pooled_rule_checks": pooled_b,
                    "check_table": table},
        "census": census,
        "census_no_readings_divergence": divergent,
        "tool_audit_ok": audit_ok,
        "priors": PRIORS,
        "n_note": ("Stage A gates only. Reading 1 lives on the census "
                   "sweep counts, reading 2 on the pooled rule, "
                   "independent by pre-registration; both are applied "
                   "in the packet RESULTS by the reader. No exit here "
                   "touches canon; a PASS unlocks conductor work "
                   "only."),
    }
    with open(_REPORT, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    if stage_a["qualified"]:
        _p(f"== READING 1 PRIMARY, census sweep counts (of "
           f"{repeats} rows, bar {CENSUS_BAR} of {repeats}) ==")
        for cell in CELLS:
            _p(f"  {cell}: {sweeps[cell]}/{repeats} {SWEEP_SHAPE}")
        _p(f"== READING 2 SECONDARY, pooled rule (canonical, bar "
           f"{RULE_BAR} of {RULE_N * repeats}) ==")
        for cell in CELLS:
            p = pooled_b[cell]
            _p(f"  {cell}: {p['passed']}/{p['n']} "
               f"(diagnostic {p['present_passed']}/{p['present_n']} "
               f"readings-present; unrunnable rows "
               f"{p['unrunnable_rows']})")
        _p(f"== STAGE B PER-CHECK canonical ({' / '.join(CELLS)}) ==")
        for call, c in table.items():
            rates = " / ".join(
                f"{c['cells'].get(a, {}).get('rate', 0.0):.2f}"
                for a in CELLS)
            mark = "  <-- rule" if c["rule_check"] else "  <-- watch"
            _p(f"  {call}: {rates}{mark}")

    _p("== CENSUS (shape distribution per cell, every cell run, the "
       "primary instrument) ==")
    for key in sorted(census):
        dist = "  ".join(f"{s}={n}" for s, n in census[key].items())
        _p(f"  {key}: {dist}")
    _p(f"census unrunnable against zero-readings divergence: "
       f"{divergent} rows")

    counts_ok = (all(
        sum(1 for r in stage_b_rows if r["cell"] == c) == repeats
        for c in CELLS) if stage_a["qualified"] else True)
    gate = counts_ok and audit_ok and os.path.exists(_ROWS)
    _p(f"GATE: {'PASSED' if gate else 'FAILED'}. stage A arithmetic "
       f"printed, stage B "
       f"{'ran on qualified ground' if stage_a['qualified'] else 'did not run, closed on the supply answer'}"
       f", byte check asserted, tool audit "
       f"{'clean' if audit_ok else 'BROKEN'}, census reported for "
       f"every cell, every run checkpointed, report persisted. Both "
       f"readings are applied in the packet RESULTS; canon is "
       f"untouched by this session regardless of exit.")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "census":
        raise SystemExit(recensus(sys.argv[2]))
    main(repeats=int(sys.argv[1]) if len(sys.argv) > 1 else R,
         resume_ts=sys.argv[2] if len(sys.argv) > 2 else None)
