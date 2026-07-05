"""PACKET-027: the moderator retest, on ground the eye chart built.
PACKET-023 pre-registered the test and never got its ground; the
registry now holds designated ground on the amplifier, and this
harness runs the two signed cells: B1 (chunk lesson, production line
8) on chunk_pad rung 3 where the classification predicts DOWN, N1
(split_csvish lesson, production line 10) on token_case rung 1 where
it predicts UP. Two lessons because the pins force it; the
attribution caveat is pre-registered in the packet and rides every
split outcome. Every armed row is also mistral-origin content
received by qwen, a transfer edge with no readings anywhere.

Performer qwen2.5-coder:7b, audience llama3.1:8b, v1 production path.
Stage A re-proves each ground fresh with TWO gates, both required,
both arithmetics printed: qualification at the standing fraction
(chunk_pad r3 two rule checks, 4 AND 4 of 24; token_case r1 one, 2
AND 2 of 12) and concentration, the fresh none-cell census at 9 of 12
or better on the design document's named shape. Registry entries are
candidacy, never pre-qualification. A side failing either gate closes
on the supply-or-drift answer and its prediction is VOID.

Stage B, per surviving side, the FIGHTS block whole before EXTENDS:
two fresh cells at R=12, interleaved none then armed, the lesson
riding byte-verbatim through the production menu path. Census on in
every cell, classifiers from supply_families.py unchanged, pinned by
identity test, replayable: py modretest27.py census <rows-file>.

The four signed readings live in the packet and are applied in its
RESULTS by the reader. The seat neither teaches nor learns. The
harness reports, it does not rule."""

import json
import os
import sys
import time

import lesson
import menu
import runner
import supply_families as sf
from probe_tasks import CRITERIA, FEATURES

PERFORMER = "qwen2.5-coder:7b"
AUDIENCE = "llama3.1:8b"
R = 12
CONCENTRATION = 9  # of 12, the per-seat criterion threshold

SIDES = ("fights", "extends")
SIDE_DEF = {
    "fights": {"family": "chunk_pad", "rung": 3,
               "armed_cell": "armed-B1", "prediction": "DOWN"},
    "extends": {"family": "token_case", "rung": 1,
                "armed_cell": "armed-N1", "prediction": "UP"},
}
EXPECT_TOOLS = {"none": 0, "armed-B1": 1, "armed-N1": 1}

_BENCH = os.path.dirname(os.path.abspath(__file__))
_PACKETS = os.path.join(_BENCH, "packets")
LESSONS_PROD = os.path.join(_BENCH, "lessons.jsonl")
ARMS = {"armed-B1": {"gen_task": "chunk", "prod_line": 8,
                     "path": os.path.join(_PACKETS,
                                          "PACKET-027-lesson_B1.jsonl")},
        "armed-N1": {"gen_task": "split_csvish", "prod_line": 10,
                     "path": os.path.join(_PACKETS,
                                          "PACKET-027-lesson_N1.jsonl")}}

PRIORS = {
    "P023_refusals_old_ground": ("flatten_once 11p/1f, merge_ranges "
                                 "1p/11f, median 24/24: the first "
                                 "moderator test never got its ground"),
    "P026_registry_candidacy": {
        "chunk_pad_r3_qwen": ("qualified 20/24, census 12/12 "
                              "range-step comprehension; candidacy "
                              "only, re-proven here"),
        "token_case_r1_qwen": ("qualified 7/12, census 12/12 "
                               "split-capitalize-join; candidacy "
                               "only, re-proven here")},
    "anchors_calibrated_not_confirming": {
        "longest_word_FIGHTS": ("tie lessons on qwen, three "
                                "same-direction declines, gaps 6/24, "
                                "4/24, 11/24"),
        "range_summary_EXTENDS": ("lifts on qwen, replicated: 8/12 to "
                                  "12/12 (P15), 4/12 to 11/12 (P21)")},
    "transfer_edge": ("mistral-origin to qwen has no readings "
                      "anywhere; every armed row here is its first "
                      "exposure"),
}

_TS = time.strftime("%Y%m%d-%H%M%S")
_LOG = os.path.join(runner.RUNS, f"modretest27-{_TS}.log")
_ROWS = os.path.join(runner.RUNS, f"modretest27-{_TS}.rows.jsonl")
_REPORT = os.path.join(runner.RUNS, f"modretest27-{_TS}.report.json")


def _set_ts(ts):
    """Rebind the run id and its file paths. Resume reuses a prior id so
    the checkpoint rows, the log, and the report stay one record."""
    global _TS, _LOG, _ROWS, _REPORT
    _TS = ts
    _LOG = os.path.join(runner.RUNS, f"modretest27-{_TS}.log")
    _ROWS = os.path.join(runner.RUNS, f"modretest27-{_TS}.rows.jsonl")
    _REPORT = os.path.join(runner.RUNS, f"modretest27-{_TS}.report.json")


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


def _features(family):
    return {**FEATURES, **sf.FAMILIES[family]["pins"]}


def rule_n(side):
    d = SIDE_DEF[side]
    return len(sf.get_rung(d["family"], d["rung"])["rule_checks"])


def qualify_min(side):
    return 2 * rule_n(side)


def drift_bar(side):
    return 2 * rule_n(side)


def named_shape(side):
    return sf.FAMILIES[SIDE_DEF[side]["family"]]["named_shape"]


def byte_checks():
    """Both packet-local stores byte-identical to their production
    lines, positions asserted, before any stage B run."""
    with open(LESSONS_PROD, "rb") as f:
        prod_lines = [l for l in f.read().split(b"\n") if l.strip()]
    out = {}
    for key, cfg in ARMS.items():
        matches = [(i, l) for i, l in enumerate(prod_lines, start=1)
                   if (json.loads(l).get("trail") or {}).get("gen_task")
                   == cfg["gen_task"]]
        if len(matches) != 1:
            raise SystemExit(f"{key}: {len(matches)} production lines "
                             f"carry gen_task {cfg['gen_task']}")
        line_no, src = matches[0]
        if line_no != cfg["prod_line"]:
            raise SystemExit(f"{key}: {cfg['gen_task']} sits at line "
                             f"{line_no}, the packet names "
                             f"{cfg['prod_line']}")
        with open(cfg["path"], "rb") as f:
            out[key] = f.read() == src + b"\n"
    if not all(out.values()):
        raise SystemExit(f"byte check failed: {out}, the materials "
                         f"were touched")
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


def cell_tools(cell, stores, family):
    if cell == "none":
        return []
    tools = menu.query(stores[cell], _features(family))
    if len(tools) != EXPECT_TOOLS[cell]:
        raise SystemExit(f"{cell} on {family}: expected "
                         f"{EXPECT_TOOLS[cell]} tools, got {len(tools)}")
    return tools


def _run_one(side, tools, stage, cell, rep):
    d = SIDE_DEF[side]
    rung_def = sf.get_rung(d["family"], d["rung"])
    r = runner.run_once(rung_def["task"], CRITERIA,
                        _features(d["family"]),
                        model=PERFORMER, audience_model=AUDIENCE,
                        landscape=tools or None,
                        evidence_checks=rung_def["checks"])
    checks = {c["call"]: bool(c["ok"]) for c in
              (r["evidence"] or {}).get("results") or []}
    row = {"side": side, "stage": stage, "cell": cell,
           "family": d["family"], "rung": d["rung"], "rep": rep,
           "run_id": r["run_id"], "verdict": r["verdict"],
           "tools": len(tools),
           "tool_concepts": [x["concept"] for x in tools],
           "ev": ev_fraction(r["evidence"]),
           "checks": checks,
           "no_readings": not checks,
           "shape": sf.census_shape(d["family"], r["output"])}
    _row(row)
    _p(f"{stage} {side} {d['family']} r{d['rung']} {cell} rep {rep}: "
       f"ev={row['ev']:.2f} tools={row['tools']} shape={row['shape']}")
    return row


def pooled_rule(rows, side):
    """Canonical accounting (DECISIONS 2026-07-04)."""
    d = SIDE_DEF[side]
    rule_checks = set(sf.get_rung(d["family"], d["rung"])["rule_checks"])
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


def gate_side(side, repeats=R, prior_rows=None):
    """Stage A: the fresh none cell, then BOTH gates, qualification
    and concentration, arithmetic printed for each. Gates only, never
    a baseline."""
    d = SIDE_DEF[side]
    qmin = qualify_min(side)
    prior = [r for r in prior_rows or []
             if r.get("stage") == "A" and r.get("side") == side]
    done = {r["rep"] for r in prior}
    rows = list(prior)
    for rep in range(repeats):
        if rep in done:
            continue
        rows.append(_run_one(side, [], "A", "none", rep))
    pooled = pooled_rule(rows, side)
    fails = pooled["n"] - pooled["passed"]
    qualified = pooled["passed"] >= qmin and fails >= qmin
    shape = named_shape(side)
    conc = sum(1 for r in rows if r["shape"] == shape)
    concentrated = conc >= CONCENTRATION
    survives = qualified and concentrated
    _p(f"stage A {side} ({d['family']} r{d['rung']}) gate 1, "
       f"qualification: pooled rule {pooled['passed']} passes, "
       f"{fails} fails of {pooled['n']} canonical (unrunnable-as-fail;"
       f" {pooled['unrunnable_rows']} unrunnable rows; diagnostic "
       f"{pooled['present_passed']}/{pooled['present_n']} readings-"
       f"present); {'QUALIFIES' if qualified else 'does not qualify'} "
       f"(mixed means at least {qmin} of each)")
    _p(f"stage A {side} gate 2, concentration: {conc}/{repeats} on "
       f"the named shape ({shape}); "
       f"{'CONCENTRATES' if concentrated else 'DOES NOT CONCENTRATE'} "
       f"(at least {CONCENTRATION} of {repeats})")
    if not survives:
        reason = []
        if not qualified:
            reason.append("qualification failed: supply")
        if not concentrated:
            reason.append("concentration failed: census drift against "
                          "the P026 designation, the prediction is "
                          "VOID")
        _p(f"stage A {side}: the side CLOSES ({'; '.join(reason)}), "
           f"no reading fires on it")
    return {"side": side, "family": d["family"], "rung": d["rung"],
            "pooled": pooled, "fails": fails, "qualify_min": qmin,
            "qualified": qualified, "named_shape": shape,
            "concentration": conc, "concentrated": concentrated,
            "survives": survives}


def run_block(side, stores, repeats=R, prior_rows=None):
    """Stage B: two fresh cells on the surviving side, interleaved
    per rep, none then armed."""
    d = SIDE_DEF[side]
    cells = ("none", d["armed_cell"])
    prior = [r for r in prior_rows or []
             if r.get("stage") == "B" and r.get("side") == side]
    done = {(r["cell"], r["rep"]) for r in prior}
    rows = list(prior)
    for rep in range(repeats):
        for cell in cells:
            if (cell, rep) in done:
                continue
            tools = cell_tools(cell, stores, d["family"])
            rows.append(_run_one(side, tools, "B", cell, rep))
    return rows


def check_table(rows, side, cells):
    """Per-check canonical counts with readings-present beside."""
    d = SIDE_DEF[side]
    rule_checks = set(sf.get_rung(d["family"], d["rung"])["rule_checks"])
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


def census_table(rows):
    """Shape distribution per (stage, side, cell)."""
    table = {}
    for r in rows:
        key = f"{r['stage']}|{r['side']}|{r['cell']}"
        cell = table.setdefault(
            key, {s: 0 for s in sf.FAMILIES[r["family"]]["taxonomy"]})
        cell[r["shape"]] += 1
    return table


def recensus(rows_path, runs_dir=None):
    """Re-run the classifiers over the persisted outputs behind a rows
    file and compare to the recorded shapes. The conductor's replay."""
    runs_dir = runs_dir or runner.RUNS
    mismatches = 0
    rows = [json.loads(l) for l in open(rows_path, encoding="utf-8")
            if l.strip()]
    for r in rows:
        spath = os.path.join(runs_dir, f"{r['run_id']}.summary.json")
        with open(spath, encoding="utf-8") as f:
            summary = json.load(f)
        fresh = sf.census_shape(r["family"], summary["output"])
        if fresh != r["shape"]:
            mismatches += 1
            print(f"MISMATCH {r['run_id']}: recorded {r['shape']}, "
                  f"recomputed {fresh}")
    print(f"recensus: {len(rows)} rows, {mismatches} mismatches")
    return mismatches


def main(repeats=R, resume_ts=None):
    prior_rows = []
    if resume_ts:
        _set_ts(resume_ts)
        prior_rows = _load_rows()
        _p(f"RESUME {_TS}: {len(prior_rows)} checkpointed rows found")
    checks = byte_checks()
    stores = load_stores()
    _p(f"MODERATOR RETEST {_TS} (PACKET-027, on registry ground)")
    _p(f"performer={PERFORMER}  audience={AUDIENCE} (v1, production)")
    _p(f"cells: FIGHTS = B1 (chunk lesson) on chunk_pad r3, predicts "
       f"DOWN, bar {drift_bar('fights')} of "
       f"{rule_n('fights') * repeats} pooled; EXTENDS = N1 "
       f"(split_csvish lesson) on token_case r1, predicts UP, bar "
       f"{drift_bar('extends')} of {rule_n('extends') * repeats} "
       f"pooled  R={repeats}")
    _p(f"stage A carries TWO gates per ground, qualification at the "
       f"standing fraction and concentration at {CONCENTRATION} of "
       f"{repeats} on the named shape; registry entries are candidacy,"
       f" never pre-qualification")
    _p(f"byte checks against production lines 8 and 10: " +
       " ".join(f"{k}={checks[k]}" for k in sorted(checks)))
    for key in ("armed-B1", "armed-N1"):
        les = stores[key][0]
        aw = les["applies_when"]
        _p(f"{key}: gen_task={les['trail']['gen_task']}  "
           f"pins {aw['rule_class']}/{aw['rule_topic']}  "
           f"origin={les['trail']['origin_seat']} (first "
           f"mistral-to-qwen exposure)")
    _p("census taxonomies, stated before any run (classifiers from "
       "supply_families.py unchanged, identity-pinned by test, "
       "re-runnable: py modretest27.py census <rows-file>):")
    for side in SIDES:
        d = SIDE_DEF[side]
        fam = sf.FAMILIES[d["family"]]
        _p(f"  {d['family']}: {', '.join(fam['taxonomy'])}  named "
           f"shape: {fam['named_shape']} ({fam['relationship']})")
        _p(f"  rule checks for {d['family']} r{d['rung']} (the "
           f"standing annotation): "
           f"{sf.get_rung(d['family'], d['rung'])['rule_checks']}")

    # Stage A: both gates on both grounds before any stage B run.
    stage_a = {side: gate_side(side, repeats, prior_rows)
               for side in SIDES}

    # Stage B: FIGHTS whole before EXTENDS, surviving sides only.
    stage_b = {}
    for side in SIDES:
        if not stage_a[side]["survives"]:
            continue
        d = SIDE_DEF[side]
        cells = ("none", d["armed_cell"])
        _p(f"stage B {side} block on surviving ground {d['family']} "
           f"r{d['rung']}: fresh interleaved cells {cells} per rep, "
           f"the stage A cell gates and is never the baseline")
        rows = run_block(side, stores, repeats, prior_rows)
        pooled = {cell: pooled_rule(
            [r for r in rows if r["cell"] == cell], side)
            for cell in cells}
        stage_b[side] = {"cells": list(cells),
                         "drift_bar": f"{drift_bar(side)} of "
                                      f"{rule_n(side) * repeats} pooled",
                         "rows": rows,
                         "check_table": check_table(rows, side, cells),
                         "pooled_rule_checks": pooled}

    all_rows = _load_rows()
    b_rows = [r for blk in stage_b.values() for r in blk["rows"]]
    audit_ok = all(r["tools"] == EXPECT_TOOLS[r["cell"]] for r in b_rows)
    census = census_table(all_rows)
    divergent = sum(1 for r in all_rows
                    if (r["shape"] == "unrunnable") != r["no_readings"])

    report = {
        "modretest27_id": _TS, "packet": "PACKET-027",
        "performer": PERFORMER, "audience": AUDIENCE, "repeats": repeats,
        "sides": {s: {k: v for k, v in SIDE_DEF[s].items()}
                  for s in SIDES},
        "byte_checks": checks,
        "lessons": {k: {"concept": stores[k][0]["concept"],
                        "rule": stores[k][0]["rule"],
                        "pins": stores[k][0]["applies_when"],
                        "gen_task": stores[k][0]["trail"]["gen_task"],
                        "origin_seat": stores[k][0]["trail"]
                        ["origin_seat"]} for k in stores},
        "stage_a": stage_a,
        "stage_b": {s: {k: v for k, v in blk.items() if k != "rows"}
                    for s, blk in stage_b.items()},
        "census": census,
        "census_no_readings_divergence": divergent,
        "tool_audit_ok": audit_ok,
        "priors": PRIORS,
        "n_note": ("Stage A gates only, both gates required. The four "
                   "signed readings, the attribution caveat, the "
                   "no-name watch columns, and the harm "
                   "reconciliation live in the packet and are applied "
                   "in its RESULTS. Census never flips a signed "
                   "exit."),
    }
    with open(_REPORT, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    for side, blk in stage_b.items():
        d = SIDE_DEF[side]
        _p(f"== STAGE B {side.upper()} ({d['family']} r{d['rung']}, "
           f"prediction {d['prediction']}) POOLED RULE (canonical, "
           f"bar {blk['drift_bar']}) ==")
        for cell in blk["cells"]:
            p = blk["pooled_rule_checks"][cell]
            _p(f"  {cell}: {p['passed']}/{p['n']} "
               f"(diagnostic {p['present_passed']}/{p['present_n']} "
               f"readings-present; unrunnable rows "
               f"{p['unrunnable_rows']})")
        _p(f"== STAGE B {side.upper()} PER-CHECK canonical "
           f"({' / '.join(blk['cells'])}) ==")
        for call, c in blk["check_table"].items():
            rates = " / ".join(
                f"{c['cells'].get(a, {}).get('rate', 0.0):.2f}"
                for a in blk["cells"])
            mark = "  <-- rule" if c["rule_check"] else "  <-- watch"
            _p(f"  {call}: {rates}{mark}")

    _p("== CENSUS (shape distribution per cell, every cell run) ==")
    for key in sorted(census):
        dist = "  ".join(f"{s}={n}" for s, n in census[key].items())
        _p(f"  {key}: {dist}")
    _p(f"census unrunnable against zero-readings divergence: "
       f"{divergent} rows")

    counts_ok = all(
        sum(1 for r in stage_b[s]["rows"] if r["cell"] == c) == repeats
        for s in stage_b for c in stage_b[s]["cells"])
    gate = counts_ok and audit_ok and os.path.exists(_ROWS)
    ran = [s for s in stage_b]
    closed = [s for s in SIDES if not stage_a[s]["survives"]]
    _p(f"GATE: {'PASSED' if gate else 'FAILED'}. both stage A gates "
       f"printed per ground, stage B "
       f"{'ran on ' + ', '.join(ran) if ran else 'did not run'}"
       + (f", {', '.join(closed)} closed at stage A" if closed else "")
       + f", both byte checks asserted, tool audit "
       f"{'clean' if audit_ok else 'BROKEN'}, census reported for "
       f"every cell, every run checkpointed, report persisted. The "
       f"readings are applied in the packet RESULTS. The seat neither "
       f"taught nor learned.")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "census":
        raise SystemExit(recensus(sys.argv[2]))
    main(repeats=int(sys.argv[1]) if len(sys.argv) > 1 else R,
         resume_ts=sys.argv[2] if len(sys.argv) > 2 else None)
