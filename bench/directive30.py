"""PACKET-030: the directive replication, symmetric forms. Three
cells of identical byte-checked content on qwen, kth_ordered rung 3:
none, menu-form injection, directive injection. PACKET-029 proved the
production serving path refuses this content (the pin firewall, a
protected surface doing its job), so neither non-none form goes
through serving: both are injected, and form is the only variable
across identical bytes. The menu-form cell measures the model's
response to contradicting content in menu form, never the production
path.

Build gates, all deterministic, all re-run as committed code before
any model run, any failure stopping the packet uncut:
1. The contradiction gate, the PACKET-028/029 instrument imported not
   copied, both derivations printed per rung 3 rule check.
2. The byte check, the PACKET-029 store against production line 4
   with position asserted, imported not copied.
3. The byte-form verifier, new here: menu.query([lesson], matched
   features stating direction last) emits exactly one tool equal to
   the lesson's concept plus applies_when, and that emission IS the
   menu-form cell's landscape by construction; the firewall control
   beside it shows zero tools on the ground's own features. menu.py
   is read, never edited.
4. Audit wiring asserted from the rows: menu-form tools=1
   directives=0, directive tools=0 directives=1, none 0 and 0.

Stage A: 12 bare runs, pooled rule gate at 18 of 24, canonical
unrunnable-as-fail, gate-only rows never a reading baseline. Stage B:
interleaved triplets at R=12 in the fixed order none, menu-form,
directive, 36 runs, census on (supply_families classifiers unchanged,
identity-pinned), all readings against the stage B none cell only.
The four pre-registered readings live in the packet and are applied
in its RESULTS by the reader. The seat neither teaches nor learns.
Replayable: py directive30.py census <rows-file>."""

import json
import os
import sys
import time

import menu
import runner
import supply_families as sf
from directive28 import load_candidate
from directive29 import byte_check as p029_byte_check
from directive29 import derivations as p029_derivations
from directive29 import STORE as P029_STORE
from probe_tasks import CRITERIA, FEATURES

PERFORMER = "qwen2.5-coder:7b"
AUDIENCE = "llama3.1:8b"
R = 12
GROUND_FAMILY = "kth_ordered"
GROUND_RUNG = 3
GATE_MIN = 18   # of 24 pooled, the high-baseline gate
RULE_BAR = 4    # of 24 pooled, the reading bar

CELLS = ("none", "menu-form", "directive")
EXPECT = {"none": {"tools": 0, "directives": 0},
          "menu-form": {"tools": 1, "directives": 0},
          "directive": {"tools": 0, "directives": 1}}

STORE_PROD_LINE = 4
STORE_GEN_TASK = "shortest_word"

_TS = time.strftime("%Y%m%d-%H%M%S")
_LOG = os.path.join(runner.RUNS, f"directive30-{_TS}.log")
_ROWS = os.path.join(runner.RUNS, f"directive30-{_TS}.rows.jsonl")
_REPORT = os.path.join(runner.RUNS, f"directive30-{_TS}.report.json")

PRIORS = {
    "P004_ev_fraction_era": ("clean checks 0.92 to 0.36 under the "
                             "contradicting directive; menu 0.33 to "
                             "0.75; a different counter than pooled "
                             "rule checks, direction comparable, "
                             "magnitudes not"),
    "rung3_qwen": ("no candidacy exists; the P026 sweep kept rung 2 "
                   "at 10 of 12 and stopped; the stage A gate carries "
                   "the risk deliberately"),
    "P029_structural": ("the production serving path refuses this "
                        "content on this ground, on the record"),
}


def _set_ts(ts):
    """Rebind the run id and its file paths. Resume reuses a prior id
    so the checkpoint rows, the log, and the report stay one record."""
    global _TS, _LOG, _ROWS, _REPORT
    _TS = ts
    _LOG = os.path.join(runner.RUNS, f"directive30-{_TS}.log")
    _ROWS = os.path.join(runner.RUNS, f"directive30-{_TS}.rows.jsonl")
    _REPORT = os.path.join(runner.RUNS, f"directive30-{_TS}.report.json")


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


def ground_features():
    return {**FEATURES, **sf.FAMILIES[GROUND_FAMILY]["pins"]}


def matched_features():
    """The features under which the pin firewall serves this lesson:
    the lesson's own stated direction. Used ONLY to obtain the
    production emission for injection, never as the task's features."""
    return {**FEATURES, "rule_class": "tie_break",
            "rule_topic": "direction", "stated_direction": "last"}


def load_lesson():
    with open(P029_STORE, encoding="utf-8") as f:
        lessons = [json.loads(l) for l in f if l.strip()]
    if len(lessons) != 1:
        raise SystemExit(f"store must hold 1 lesson, found "
                         f"{len(lessons)}")
    if lessons[0]["trail"]["gen_task"] != STORE_GEN_TASK:
        raise SystemExit("wrong lesson in the store")
    return lessons[0]


def directive_text():
    """The lesson's rule sentence, byte-verbatim, via the PACKET-028
    instrument, imported not copied."""
    return load_candidate(STORE_PROD_LINE, STORE_GEN_TASK)["rule"]


def byte_form_verifier():
    """Build gate 3: the menu-form landscape is menu.query's own
    emission on matched features, asserted, never a handwritten dict.
    The firewall control beside it confirms the PACKET-029 refusal."""
    lesson = load_lesson()
    emission = menu.query([lesson], matched_features())
    if len(emission) != 1:
        raise SystemExit(f"byte-form verifier: emission count "
                         f"{len(emission)}, expected 1")
    tool = emission[0]
    same = (tool == {"concept": lesson["concept"],
                     "applies_when": lesson["applies_when"]})
    if not same:
        raise SystemExit("byte-form verifier: the emission does not "
                         "equal the lesson's concept plus applies_when")
    control = menu.query([lesson], ground_features())
    if control:
        raise SystemExit(f"firewall control: expected 0 tools on "
                         f"ground features, got {len(control)}")
    return {"emission": emission, "tool_equals_lesson": same,
            "control_tools": len(control)}


def build_gates():
    """All deterministic gates, re-run as committed code before any
    model run. Returns the menu-form landscape (the verified emission)
    and the directive text."""
    _p("GATE 1, THE CONTRADICTION GATE (the P028/P029 instrument, "
       "imported):")
    derivs = p029_derivations()
    for d in derivs:
        _p(f"  {d['call']}:")
        _p(f"    stated rule (reverse-alphabetical among equal "
           f"lengths): order {d['rule_order']} -> {d['rule_answer']!r}")
        _p(f"    directive direction (later-encountered among equal "
           f"lengths): order {d['directive_order']} -> "
           f"{d['directive_answer']!r}")
        _p(f"    DIFFERS: {d['differs']}")
    if not any(d["differs"] for d in derivs):
        raise SystemExit("contradiction gate failed: the packet "
                         "closes uncut")
    _p("  GATE: PASSES")

    _p("GATE 2, THE BYTE CHECK (the P029 store against production "
       "line 4, imported):")
    ok = p029_byte_check()
    _p(f"  store byte-identical, position asserted: {ok}")

    _p("GATE 3, THE BYTE-FORM VERIFIER:")
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


def _run_one(stage, cell, rep, landscape, directives):
    rung_def = sf.get_rung(GROUND_FAMILY, GROUND_RUNG)
    r = runner.run_once(rung_def["task"], CRITERIA, ground_features(),
                        model=PERFORMER, audience_model=AUDIENCE,
                        landscape=landscape or None,
                        evidence_checks=rung_def["checks"],
                        directives=directives or None)
    checks = {c["call"]: bool(c["ok"]) for c in
              (r["evidence"] or {}).get("results") or []}
    row = {"stage": stage, "cell": cell, "rep": rep,
           "run_id": r["run_id"], "verdict": r["verdict"],
           "tools": len(landscape or []),
           "directives": r["directives_used"],
           "ev": ev_fraction(r["evidence"]),
           "checks": checks,
           "no_readings": not checks,
           "shape": sf.census_shape(GROUND_FAMILY, r["output"])}
    _row(row)
    _p(f"{stage} {cell} rep {rep}: ev={row['ev']:.2f} "
       f"tools={row['tools']} directives={row['directives']} "
       f"shape={row['shape']}")
    return row


def pooled_rule(rows):
    """Canonical accounting (DECISIONS 2026-07-04)."""
    rule_checks = set(sf.get_rung(GROUND_FAMILY,
                                  GROUND_RUNG)["rule_checks"])
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


def stage_a(repeats=R, prior_rows=None):
    """The high-baseline gate: 12 bare runs, pooled rule at GATE_MIN
    of 24 or better. Gate only, never a reading baseline."""
    prior = [r for r in prior_rows or [] if r.get("stage") == "A"]
    done = {r["rep"] for r in prior}
    rows = list(prior)
    for rep in range(repeats):
        if rep in done:
            continue
        rows.append(_run_one("A", "none", rep, [], []))
    pooled = pooled_rule(rows)
    n = pooled["n"]
    passed = pooled["passed"] >= GATE_MIN
    _p(f"stage A gate: pooled rule {pooled['passed']} of {n} canonical "
       f"(unrunnable-as-fail; {pooled['unrunnable_rows']} unrunnable "
       f"rows; diagnostic {pooled['present_passed']}/"
       f"{pooled['present_n']} readings-present); "
       f"{'PASSES' if passed else 'FAILS'} (gate at {GATE_MIN} of {n} "
       f"or better)")
    return {"pooled": pooled, "gate_min": GATE_MIN, "passed": passed}


def stage_b(landscape, directive, repeats=R, prior_rows=None):
    """Interleaved triplets, one unit: none, menu-form, directive."""
    prior = [r for r in prior_rows or [] if r.get("stage") == "B"]
    done = {(r["cell"], r["rep"]) for r in prior}
    rows = list(prior)
    for rep in range(repeats):
        for cell in CELLS:
            if (cell, rep) in done:
                continue
            if cell == "menu-form":
                rows.append(_run_one("B", cell, rep, landscape, []))
            elif cell == "directive":
                rows.append(_run_one("B", cell, rep, [], [directive]))
            else:
                rows.append(_run_one("B", cell, rep, [], []))
    return rows


def check_table(rows):
    rule_checks = set(sf.get_rung(GROUND_FAMILY,
                                  GROUND_RUNG)["rule_checks"])
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


def census_table(rows):
    table = {}
    for r in rows:
        key = f"{r['stage']}|{r['cell']}"
        cell = table.setdefault(
            key, {s: 0 for s in sf.FAMILIES[GROUND_FAMILY]["taxonomy"]})
        cell[r["shape"]] += 1
    return table


def recensus(rows_path, runs_dir=None):
    """Re-run the classifier over persisted outputs. The conductor's
    replay."""
    runs_dir = runs_dir or runner.RUNS
    mismatches = 0
    rows = [json.loads(l) for l in open(rows_path, encoding="utf-8")
            if l.strip()]
    for r in rows:
        spath = os.path.join(runs_dir, f"{r['run_id']}.summary.json")
        with open(spath, encoding="utf-8") as f:
            summary = json.load(f)
        fresh = sf.census_shape(GROUND_FAMILY, summary["output"])
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
    _p(f"SYMMETRIC FORMS {_TS} (PACKET-030, gap G1 re-cut)")
    _p(f"performer={PERFORMER}  audience={AUDIENCE} (v1, production)")
    _p(f"ground={GROUND_FAMILY} r{GROUND_RUNG}  cells={CELLS}  "
       f"R={repeats}  stage A gate {GATE_MIN} of 24  reading bar "
       f"{RULE_BAR} of 24  one content, form the only variable")
    rung = sf.get_rung(GROUND_FAMILY, GROUND_RUNG)
    _p(f"rule checks (the standing annotation): {rung['rule_checks']}")
    _p(f"census taxonomy, stated before any run (supply_families "
       f"classifiers unchanged, identity-pinned, re-runnable: "
       f"py directive30.py census <rows-file>): "
       f"{', '.join(sf.FAMILIES[GROUND_FAMILY]['taxonomy'])}")

    landscape, directive = build_gates()

    a = stage_a(repeats, prior_rows)
    b_rows = []
    pooled_b = {}
    table = {}
    if a["passed"]:
        _p(f"stage B on gated ground: interleaved triplets, "
           f"{CELLS} per rep, readings against the stage B none cell "
           f"only")
        b_rows = stage_b(landscape, directive, repeats, prior_rows)
        pooled_b = {cell: pooled_rule(
            [r for r in b_rows if r["cell"] == cell]) for cell in CELLS}
        table = check_table(b_rows)
    else:
        _p("stage A gate FAILED: the packet closes on the answer, no "
           "stage B, no reading fires, the re-cut is a Brad-level "
           "design decision")

    all_rows = _load_rows()
    audit_ok = all(
        r["tools"] == EXPECT[r["cell"]]["tools"]
        and r["directives"] == EXPECT[r["cell"]]["directives"]
        for r in all_rows)
    census = census_table(all_rows)
    divergent = sum(1 for r in all_rows
                    if (r["shape"] == "unrunnable") != r["no_readings"])

    report = {
        "directive30_id": _TS, "packet": "PACKET-030",
        "performer": PERFORMER, "audience": AUDIENCE,
        "ground": f"{GROUND_FAMILY} r{GROUND_RUNG}",
        "repeats": repeats, "cells": list(CELLS),
        "gate_min": f"{GATE_MIN} of 24", "rule_bar": f"{RULE_BAR} of 24",
        "directive_text": directive,
        "menu_form_landscape": landscape,
        "stage_a": a,
        "stage_b": {"ran": a["passed"],
                    "pooled_rule_checks": pooled_b,
                    "check_table": table},
        "census": census,
        "census_no_readings_divergence": divergent,
        "audit_ok": audit_ok,
        "priors": PRIORS,
        "n_note": ("Stage A gates only. The four readings, the "
                   "observability naming, and the census's role live "
                   "in the packet and are applied in its RESULTS. The "
                   "menu-form cell measures the model, never the "
                   "production path."),
    }
    with open(_REPORT, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    if a["passed"]:
        _p(f"== STAGE B POOLED RULE (canonical, bar {RULE_BAR} of 24, "
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
    gate = counts_ok and audit_ok and os.path.exists(_ROWS)
    _p(f"GATE: {'PASSED' if gate else 'FAILED'}. build gates re-run "
       f"as committed code before any model run, stage A arithmetic "
       f"printed, stage B "
       f"{'ran whole' if a['passed'] else 'did not run, closed on the gate answer'}"
       f", audits {'clean' if audit_ok else 'BROKEN'} from the rows "
       f"(tools and directives both), census reported for every cell, "
       f"every run checkpointed, report persisted. The readings are "
       f"applied in the packet RESULTS. The seat neither taught nor "
       f"learned.")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "census":
        raise SystemExit(recensus(sys.argv[2]))
    main(repeats=int(sys.argv[1]) if len(sys.argv) > 1 else R,
         resume_ts=sys.argv[2] if len(sys.argv) > 2 else None)
