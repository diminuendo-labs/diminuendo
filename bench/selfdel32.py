"""PACKET-032: the self-delivery replication, P031's design executed
again on fresh cells. The instrument is selfdel31.py REUSED BY
IDENTITY: every build gate, cell runner, accounting function, and the
census replay below are selfdel31's own functions, imported and
re-exported, never copied, pinned by identity test. The unavoidable
delta, tier 1 and named in the packet RESULTS: this driver rebinds the
shared instrument's run-record paths so the replication's artifacts
carry their own id (selfdel32-<ts>), prints the replication's priors,
and computes the VOID-BY-CEILING pre-registration. Nothing that
measures is redefined here.

The replication-specific pre-registrations, applied in the packet
RESULTS: the two packets' cells are never pooled, the reading is
qualitative exit against exit, a FLAT or HARM downgrades the P031
GAIN where it was made, and VOID-BY-CEILING closes with no reading if
the fresh stage B none cell sits at 20 of 24 or above, leaving less
than bar-plus-one upward headroom for the predicted GAIN direction.

Replayable: py selfdel32.py census <rows-file>."""

import json
import os
import sys
import time

import runner
import selfdel31
import supply_families as sf

# The instrument, by identity. These names exist so the identity is
# visible and pinned by test; they are selfdel31's objects.
build_gates = selfdel31.build_gates
stage_a = selfdel31.stage_a
stage_b = selfdel31.stage_b
pooled_rule = selfdel31.pooled_rule
rule_disagreement = selfdel31.rule_disagreement
check_table = selfdel31.check_table
census_table = selfdel31.census_table
recensus = selfdel31.recensus
byte_check = selfdel31.byte_check
CELLS = selfdel31.CELLS
EXPECT = selfdel31.EXPECT
R = selfdel31.R
RULE_BAR = selfdel31.RULE_BAR

VOID_CEILING = 20  # none at 20 of 24 or above: GAIN unobservable

PRIORS = {
    "P031_cells_verbatim": ("none 15 of 24, armed 20 of 24, GAIN at "
                            "gap 5; never pooled with this packet's "
                            "cells"),
    "P019_trait_cell": "FLAT, none 12/24, armed 13/24, cross-origin",
    "candidacy_history": ("14 of 24 (P026), 19 of 24 (P031 stage A), "
                          "15 of 24 (P031 stage B none, same-run)"),
    "P031_texture": ("movement concentrated on the trim check the "
                     "concept does not address; description only, no "
                     "per-check prediction is pre-registered here"),
}


def _set_paths(ts):
    """The tier 1 delta: rebind the shared instrument's run-record
    paths so this replication's checkpoints, log, and report carry the
    selfdel32 id. The functions that write them are selfdel31's own."""
    selfdel31._TS = ts
    selfdel31._LOG = os.path.join(runner.RUNS, f"selfdel32-{ts}.log")
    selfdel31._ROWS = os.path.join(runner.RUNS,
                                   f"selfdel32-{ts}.rows.jsonl")
    selfdel31._REPORT = os.path.join(runner.RUNS,
                                     f"selfdel32-{ts}.report.json")
    return (selfdel31._LOG, selfdel31._ROWS,
            os.path.join(runner.RUNS, f"selfdel32-{ts}.report.json"))


def void_by_ceiling(none_pooled):
    """The pre-registered observability close: True when the fresh
    stage B none cell leaves less than bar-plus-one upward headroom."""
    return none_pooled["passed"] >= VOID_CEILING


def main(repeats=R, resume_ts=None):
    ts = resume_ts or time.strftime("%Y%m%d-%H%M%S")
    log_path, rows_path, report_path = _set_paths(ts)
    _p = selfdel31._p
    prior_rows = []
    if resume_ts:
        prior_rows = selfdel31._load_rows()
        _p(f"RESUME {ts}: {len(prior_rows)} checkpointed rows found")
    _p(f"SELF-DELIVERY REPLICATION {ts} (PACKET-032, P031's design on "
       f"fresh cells)")
    _p(f"performer={selfdel31.PERFORMER}  audience="
       f"{selfdel31.AUDIENCE} (v1, production)")
    _p(f"ground={selfdel31.GROUND_FAMILY} r{selfdel31.GROUND_RUNG}  "
       f"cells={CELLS}  R={repeats}  stage A mixed gate "
       f"{selfdel31.QUALIFY_MIN} AND {selfdel31.QUALIFY_MIN} of 24  "
       f"drift bar {RULE_BAR} of 24  VOID-BY-CEILING at none "
       f"{VOID_CEILING} of 24 or above")
    _p(f"the harness is selfdel31 by identity; the delta is run-record "
       f"naming and this replication scaffolding, tier 1, named in "
       f"RESULTS")
    _p(f"the two-cause caveat rides every non-FLAT exit; the two "
       f"packets' cells are never pooled, the reading is exit against "
       f"exit")
    _p(f"priors: P031 {PRIORS['P031_cells_verbatim']}; P019 "
       f"{PRIORS['P019_trait_cell']}; candidacy "
       f"{PRIORS['candidacy_history']}")

    tools = build_gates()

    a = stage_a(repeats, prior_rows)
    b_rows = []
    pooled_b = {}
    table = {}
    eff_n = {}
    void = False
    if a["qualified"]:
        _p(f"stage B on qualified ground: fresh interleaved cells, "
           f"{CELLS} per rep, readings against the stage B none cell "
           f"only, headroom checked before any reading")
        b_rows = stage_b(tools, repeats, prior_rows)
        pooled_b = {cell: pooled_rule(
            [r for r in b_rows if r["cell"] == cell]) for cell in CELLS}
        table = check_table(b_rows)
        eff_n = {cell: rule_disagreement(
            [r for r in b_rows if r["cell"] == cell]) for cell in CELLS}
        void = void_by_ceiling(pooled_b["none"])
        verdict = ("VOID, the predicted direction is unobservable, no "
                   "reading in any direction" if void else
                   "headroom present, the reading proceeds")
        _p(f"VOID-BY-CEILING check: none {pooled_b['none']['passed']} "
           f"of {pooled_b['none']['n']}, ceiling at {VOID_CEILING}: "
           f"{verdict}")
    else:
        _p("stage A gate FAILED: the packet closes on the supply "
           "answer with its count, no stage B, no reading")

    all_rows = selfdel31._load_rows()
    audit_ok = all(
        r["tools"] == EXPECT[r["cell"]]["tools"]
        and r["directives"] == EXPECT[r["cell"]]["directives"]
        for r in all_rows)
    census = census_table(all_rows)
    divergent = sum(1 for r in all_rows
                    if (r["shape"] == "unrunnable") != r["no_readings"])

    report = {
        "selfdel32_id": ts, "packet": "PACKET-032",
        "replicates": "PACKET-031, cells never pooled",
        "performer": selfdel31.PERFORMER,
        "audience": selfdel31.AUDIENCE,
        "ground": f"{selfdel31.GROUND_FAMILY} r{selfdel31.GROUND_RUNG}",
        "repeats": repeats, "cells": list(CELLS),
        "qualify_min": selfdel31.QUALIFY_MIN,
        "rule_bar": f"{RULE_BAR} of 24",
        "void_ceiling": f"none at {VOID_CEILING} of 24 or above",
        "store_md5": selfdel31.DESK_CHECK_MD5,
        "stage_a": a,
        "stage_b": {"ran": a["qualified"],
                    "void_by_ceiling": void,
                    "pooled_rule_checks": pooled_b,
                    "check_table": table,
                    "rule_disagreement": eff_n},
        "census": census,
        "census_no_readings_divergence": divergent,
        "audit_ok": audit_ok,
        "priors": PRIORS,
        "n_note": ("Stage A gates only. The exit-against-exit reading, "
                   "the two-cause caveat, observability naming, and "
                   "effective-n sizing live in the packet and are "
                   "applied in its RESULTS. Cells are never pooled "
                   "across packets."),
    }
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    if a["qualified"]:
        _p(f"== STAGE B POOLED RULE (canonical, bar {RULE_BAR} of 24, "
           f"against the stage B none cell) ==")
        for cell in CELLS:
            p = pooled_b[cell]
            _p(f"  {cell}: {p['passed']}/{p['n']} "
               f"(diagnostic {p['present_passed']}/{p['present_n']} "
               f"readings-present; unrunnable rows "
               f"{p['unrunnable_rows']})")
        _p(f"== EFFECTIVE-N (within-row rule-check disagreement) ==")
        for cell in CELLS:
            e = eff_n[cell]
            _p(f"  {cell}: {e['disagreeing_rows']} of {e['rows']} rows "
               f"disagree across the two rule checks")
        _p(f"== STAGE B PER-CHECK canonical ({' / '.join(CELLS)}) ==")
        for call, c in table.items():
            rates = " / ".join(
                f"{c['cells'].get(x, {}).get('rate', 0.0):.2f}"
                for x in CELLS)
            mark = "  <-- rule" if c["rule_check"] else "  <-- watch"
            _p(f"  {call}: {rates}{mark}")

    _p("== CENSUS (shape distribution per cell, every cell run) ==")
    for key in sorted(census):
        dist = "  ".join(f"{s}={n}" for s, n in census[key].items())
        _p(f"  {key}: {dist}")
    _p(f"census unrunnable against zero-readings divergence: "
       f"{divergent} rows")

    counts_ok = (all(
        sum(1 for r in b_rows if r["cell"] == c) == repeats
        for c in CELLS) if a["qualified"] else True)
    gate = counts_ok and audit_ok and os.path.exists(rows_path)
    _p(f"GATE: {'PASSED' if gate else 'FAILED'}. build gates re-run "
       f"as committed code (selfdel31's, by identity) before any "
       f"model run, stage A arithmetic printed, stage B "
       f"{'ran whole' if a['qualified'] else 'did not run'}"
       + (", VOID-BY-CEILING fired" if void else "")
       + f", audits {'clean' if audit_ok else 'BROKEN'} from the "
       f"rows, census reported for every cell, every run "
       f"checkpointed, report persisted. The reading is applied in "
       f"the packet RESULTS, exit against exit, never pooled. The "
       f"seat neither taught nor learned.")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "census":
        raise SystemExit(recensus(sys.argv[2]))
    main(repeats=int(sys.argv[1]) if len(sys.argv) > 1 else R,
         resume_ts=sys.argv[2] if len(sys.argv) > 2 else None)
