"""PACKET-033: symmetric forms on variant rung 2, the pre-registered
LAST G1 attempt. PACKET-030's design re-grounded: three cells of one
byte-checked content on qwen (none, menu-form injection, directive
injection), form the only variable. The instrument is the standing
one, reused by identity: gate 1 is directive28's committed rung 2
contradiction gate (both direction-last candidates, now passing on
the landed variant input), gate 2 is directive29's byte check (the
P029 store against production line 4, position asserted), gate 3 and
every cell runner and accounting function are directive30's. The tier
1 delta, named in the packet RESULTS: this driver rebinds the shared
instrument's run-record paths and its three scaling constants to the
variant rung (rung 2, gate 9 of 12, bar 2 of 12, the packet's own
pre-registration at one rule check), and adds the VOID-BY-FLOOR
observability check for the DOWN-signed readings. Nothing that
measures is redefined here.

Effective-n is structural on this ground: one rule check, so the unit
IS the run and every count is in runs, n=12. A stage A failure closes
the packet AND the G1 program, per the exit wired into the packet.

Replayable: py directive33.py census <rows-file>."""

import json
import os
import sys
import time

import directive28
import directive29
import directive30
import runner
import supply_families as sf

# The instrument, by identity. Pinned by test.
contradiction_gate = directive28.contradiction_gate
byte_check = directive29.byte_check
byte_form_verifier = directive30.byte_form_verifier
directive_text = directive30.directive_text
stage_a = directive30.stage_a
stage_b = directive30.stage_b
pooled_rule = directive30.pooled_rule
check_table = directive30.check_table
census_table = directive30.census_table
recensus = directive30.recensus
CELLS = directive30.CELLS
EXPECT = directive30.EXPECT
R = directive30.R

GROUND_RUNG = 2
GATE_MIN = 9   # of 12, the high-baseline demand at one rule check
RULE_BAR = 2   # of 12, the generalized 2n bar at n=1
VOID_FLOOR = 2  # none at 2 of 12 or under: DOWN unobservable

PRIORS = {
    "P004_ev_fraction_era": ("clean checks 0.92 to 0.36 under the "
                             "contradicting directive; menu 0.33 to "
                             "0.75; direction comparable, magnitudes "
                             "not"),
    "old_input_rung2": ("qwen 10 of 12 in P026, old-input historical, "
                        "never a qualification"),
    "P030_rung3_close": "14 of 24 against an 18-of-24 gate",
    "variant_rung2": "zero measurements exist",
}


def _set_scaling(ts):
    """The tier 1 delta: rebind the shared instrument's run-record
    paths to the directive33 id and its scaling constants to the
    variant rung. Read at call time by directive30's own functions."""
    directive30.GROUND_RUNG = GROUND_RUNG
    directive30.GATE_MIN = GATE_MIN
    directive30.RULE_BAR = RULE_BAR
    directive30._TS = ts
    directive30._LOG = os.path.join(runner.RUNS,
                                    f"directive33-{ts}.log")
    directive30._ROWS = os.path.join(runner.RUNS,
                                     f"directive33-{ts}.rows.jsonl")
    directive30._REPORT = os.path.join(runner.RUNS,
                                       f"directive33-{ts}.report.json")
    return (directive30._LOG, directive30._ROWS,
            os.path.join(runner.RUNS, f"directive33-{ts}.report.json"))


def void_by_floor(none_pooled):
    """The pre-registered observability check for this ground's
    DOWN-signed readings: True when the fresh stage B none cell sits
    at VOID_FLOOR of 12 or under, leaving the drop direction
    unobservable."""
    return none_pooled["passed"] <= VOID_FLOOR


def build_gates_33():
    """The packet's build gates in order, every one the committed
    instrument. Any failure stops the packet uncut and the G1 program
    with it."""
    _p = directive30._p
    _p("GATE 1, THE CONTRADICTION GATE (directive28's committed rung "
       "2 gate, both candidates):")
    results = contradiction_gate()
    for res in results:
        c = res["candidate"]
        _p(f"  candidate line {c['prod_line']} ({c['gen_task']}, "
           f"stated_direction {c['stated_direction']}):")
        for d in res["derivations"]:
            _p(f"    {d['call']}: rule {d['rule_answer']!r} directive "
               f"{d['directive_answer']!r} DIFFERS: {d['differs']}")
        _p(f"    GATE: {'PASSES' if res['passes'] else 'FAILS'}")
    if not all(r["passes"] for r in results):
        raise SystemExit("contradiction gate failed: the packet and "
                         "the G1 program close per the exit")

    _p("GATE 2, THE BYTE CHECK (directive29's, the P029 store against "
       "production line 4):")
    ok = byte_check()
    _p(f"  store byte-identical, position asserted: {ok}")

    _p("GATE 3, THE BYTE-FORM VERIFIER (directive30's):")
    v = byte_form_verifier()
    _p(f"  emission count on matched features: {len(v['emission'])}")
    _p(f"  tool equals lesson concept plus applies_when: "
       f"{v['tool_equals_lesson']}")
    _p(f"  firewall control, tools on ground features: "
       f"{v['control_tools']}")

    text = directive_text()
    _p(f"the directive text (the lesson's rule sentence, "
       f"byte-verbatim, source field: rule): {text}")
    return v["emission"], text


def main(repeats=R, resume_ts=None):
    ts = resume_ts or time.strftime("%Y%m%d-%H%M%S")
    log_path, rows_path, report_path = _set_scaling(ts)
    _p = directive30._p
    prior_rows = []
    if resume_ts:
        prior_rows = directive30._load_rows()
        _p(f"RESUME {ts}: {len(prior_rows)} checkpointed rows found")
    _p(f"SYMMETRIC FORMS, VARIANT RUNG 2 {ts} (PACKET-033, the "
       f"pre-registered LAST G1 attempt)")
    _p(f"performer={directive30.PERFORMER}  audience="
       f"{directive30.AUDIENCE} (v1, production)")
    _p(f"ground=kth_ordered r{GROUND_RUNG} (variant)  cells={CELLS}  "
       f"R={repeats}  stage A gate {GATE_MIN} of 12  reading bar "
       f"{RULE_BAR} of 12  VOID-BY-FLOOR at none {VOID_FLOOR} of 12 "
       f"or under")
    _p(f"one rule check: the unit IS the run and every count is in "
       f"runs, n=12, said plainly")
    _p(f"the instrument is the standing one by identity; the delta is "
       f"run-record naming, the three scaling constants, and the "
       f"floor check, tier 1, named in RESULTS")
    rung = sf.get_rung("kth_ordered", GROUND_RUNG)
    _p(f"rule checks (the standing annotation): {rung['rule_checks']}")
    _p(f"census taxonomy, stated before any run: "
       f"{', '.join(sf.FAMILIES['kth_ordered']['taxonomy'])}")
    _p(f"priors: P004 {PRIORS['P004_ev_fraction_era']}; old-input "
       f"rung 2 {PRIORS['old_input_rung2']}; P030 rung 3 "
       f"{PRIORS['P030_rung3_close']}; variant rung 2 "
       f"{PRIORS['variant_rung2']}")

    landscape, directive = build_gates_33()

    a = stage_a(repeats, prior_rows)
    b_rows = []
    pooled_b = {}
    table = {}
    void = False
    if a["passed"]:
        _p(f"stage B on gated ground: interleaved triplets, {CELLS} "
           f"per rep, readings against the stage B none cell only, "
           f"floor checked before any reading")
        b_rows = stage_b(landscape, directive, repeats, prior_rows)
        pooled_b = {cell: pooled_rule(
            [r for r in b_rows if r["cell"] == cell]) for cell in CELLS}
        table = check_table(b_rows)
        void = void_by_floor(pooled_b["none"])
        verdict = ("VOID-BY-FLOOR, the DOWN direction is unobservable, "
                   "no reading in any direction" if void else
                   "floor clear, the readings proceed")
        _p(f"VOID-BY-FLOOR check: none {pooled_b['none']['passed']} "
           f"of {pooled_b['none']['n']}, floor at {VOID_FLOOR}: "
           f"{verdict}")
    else:
        _p("stage A gate FAILED: the packet closes AND the G1 program "
           "closes per the pre-registered exit, the count reported, "
           "the writeup proceeding with property 2 at its true size")

    all_rows = directive30._load_rows()
    audit_ok = all(
        r["tools"] == EXPECT[r["cell"]]["tools"]
        and r["directives"] == EXPECT[r["cell"]]["directives"]
        for r in all_rows)
    census = census_table(all_rows)
    divergent = sum(1 for r in all_rows
                    if (r["shape"] == "unrunnable") != r["no_readings"])

    report = {
        "directive33_id": ts, "packet": "PACKET-033",
        "program_exit": "the pre-registered LAST G1 attempt",
        "performer": directive30.PERFORMER,
        "audience": directive30.AUDIENCE,
        "ground": f"kth_ordered r{GROUND_RUNG} (variant)",
        "repeats": repeats, "cells": list(CELLS),
        "gate_min": f"{GATE_MIN} of 12", "rule_bar": f"{RULE_BAR} of 12",
        "void_floor": f"none at {VOID_FLOOR} of 12 or under",
        "directive_text": directive,
        "menu_form_landscape": landscape,
        "stage_a": a,
        "stage_b": {"ran": a["passed"],
                    "void_by_floor": void,
                    "pooled_rule_checks": pooled_b,
                    "check_table": table},
        "census": census,
        "census_no_readings_divergence": divergent,
        "audit_ok": audit_ok,
        "priors": PRIORS,
        "n_note": ("Stage A gates only. The four readings and the "
                   "program exit live in the packet and are applied "
                   "in its RESULTS. One rule check: counts are in "
                   "runs, n=12."),
    }
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    if a["passed"]:
        _p(f"== STAGE B POOLED RULE (canonical, bar {RULE_BAR} of 12, "
           f"against the stage B none cell) ==")
        for cell in CELLS:
            p = pooled_b[cell]
            _p(f"  {cell}: {p['passed']}/{p['n']} "
               f"(diagnostic {p['present_passed']}/{p['present_n']} "
               f"readings-present; unrunnable rows "
               f"{p['unrunnable_rows']})")
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
        for c in CELLS) if a["passed"] else True)
    gate = counts_ok and audit_ok and os.path.exists(rows_path)
    _p(f"GATE: {'PASSED' if gate else 'FAILED'}. build gates re-run "
       f"as committed code (the standing instruments, by identity) "
       f"before any model run, stage A arithmetic printed, stage B "
       f"{'ran whole' if a['passed'] else 'did not run, the packet and the G1 program closed on the gate answer'}"
       + (", VOID-BY-FLOOR fired" if void else "")
       + f", audits {'clean' if audit_ok else 'BROKEN'} from the rows "
       f"(tools and directives both), census reported for every cell, "
       f"every run checkpointed, report persisted. The readings are "
       f"applied in the packet RESULTS. The seat neither taught nor "
       f"learned.")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "census":
        _set_scaling("replay")
        raise SystemExit(recensus(sys.argv[2]))
    main(repeats=int(sys.argv[1]) if len(sys.argv) > 1 else R,
         resume_ts=sys.argv[2] if len(sys.argv) > 2 else None)
