"""PACKET-031: mistral self-delivery on registry ground, G2
re-scoped. One cell, two pre-registered questions: the seat's
response to its own lesson (the measurement PACKET-024 designed and
its gate refused) and mistral's second trait-series cell beside
PACKET-019's FLAT. The two-cause caveat rides every non-FLAT exit in
the packet RESULTS: the seat's tool-response trait and self-origin
effects, neither chosen at this n.

Performer mistral:7b, audience llama3.1:8b, v1 production path.
Ground: safe_stats rung 1, the seat's strongest registry candidacy,
re-qualified fresh in stage A at the standing mixed fraction (4 AND 4
of 24 pooled, canonical unrunnable-as-fail). Instrument: a fresh raw
byte copy of production line 8 (chunk lesson, boundary/degenerate,
mistral origin), byte check asserted with position and md5 printed to
tie to the desk check, served through menu.query with the ground's
own features, the production serving path with a genuine pin match,
never injected, never edited.

Build gates re-run as committed code before any model run: the byte
check, the delivery-path check (one tool, equal to the lesson's
concept plus applies_when), the rule-checks annotation printed, and
the audit wiring pinned from the rows (armed tools=1 directives=0,
none 0 and 0). Stage B: two fresh cells at R=12 interleaved none then
armed, census on (supply_families classifier unchanged, identity-
pinned), the three-exit reading at the 4-of-24 bar applied in the
packet RESULTS with observability named and effective-n reported from
the within-row correlation of the two rule checks. The seat neither
teaches nor learns. Replayable: py selfdel31.py census <rows-file>."""

import hashlib
import json
import os
import sys
import time

import lesson as lesson_mod
import menu
import runner
import supply_families as sf
from probe_tasks import CRITERIA, FEATURES

PERFORMER = "mistral:7b"
AUDIENCE = "llama3.1:8b"
R = 12
GROUND_FAMILY = "safe_stats"
GROUND_RUNG = 1
QUALIFY_MIN = 4   # passes AND fails of 24 pooled, the standing fraction
RULE_BAR = 4      # of 24 pooled, the drift bar

CELLS = ("none", "armed")
EXPECT = {"none": {"tools": 0, "directives": 0},
          "armed": {"tools": 1, "directives": 0}}

_BENCH = os.path.dirname(os.path.abspath(__file__))
LESSONS_PROD = os.path.join(_BENCH, "lessons.jsonl")
STORE = os.path.join(_BENCH, "packets", "PACKET-031-lesson_B1.jsonl")
STORE_PROD_LINE = 8
STORE_GEN_TASK = "chunk"
DESK_CHECK_MD5 = "588e6eaf31f77559556d15b2d44e040f"

PRIORS = {
    "P019_trait_cell": ("FLAT, none 12/24, armed 13/24, cross-origin "
                        "instrument"),
    "P026_candidacy_this_ground": ("14 of 24, census 12 of 12 "
                                   "sort-slice-average; candidacy is "
                                   "not qualification"),
    "self_delivery": ("zero measurements exist; P024 was refused by "
                      "qualification"),
}

_TS = time.strftime("%Y%m%d-%H%M%S")
_LOG = os.path.join(runner.RUNS, f"selfdel31-{_TS}.log")
_ROWS = os.path.join(runner.RUNS, f"selfdel31-{_TS}.rows.jsonl")
_REPORT = os.path.join(runner.RUNS, f"selfdel31-{_TS}.report.json")


def _set_ts(ts):
    """Rebind the run id and its file paths. Resume reuses a prior id
    so the checkpoint rows, the log, and the report stay one record."""
    global _TS, _LOG, _ROWS, _REPORT
    _TS = ts
    _LOG = os.path.join(runner.RUNS, f"selfdel31-{_TS}.log")
    _ROWS = os.path.join(runner.RUNS, f"selfdel31-{_TS}.rows.jsonl")
    _REPORT = os.path.join(runner.RUNS, f"selfdel31-{_TS}.report.json")


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


def byte_check():
    """Build gate 1: the store byte-identical to production line 8,
    position asserted, md5 printed to tie to the desk check."""
    with open(LESSONS_PROD, "rb") as f:
        lines = [l for l in f.read().split(b"\n") if l.strip()]
    src = lines[STORE_PROD_LINE - 1]
    obj = json.loads(src)
    if (obj.get("trail") or {}).get("gen_task") != STORE_GEN_TASK:
        raise SystemExit(f"line {STORE_PROD_LINE} is not the "
                         f"{STORE_GEN_TASK} lesson")
    with open(STORE, "rb") as f:
        ok = f.read() == src + b"\n"
    if not ok:
        raise SystemExit("byte check failed, the lesson was touched")
    return {"ok": ok, "md5": hashlib.md5(src).hexdigest()}


def load_store():
    lessons = lesson_mod.load(STORE)
    if len(lessons) != 1:
        raise SystemExit(f"store must hold 1 lesson, found "
                         f"{len(lessons)}")
    lesson_mod.validate(lessons[0])
    if lessons[0]["trail"]["origin_seat"] != PERFORMER:
        raise SystemExit("the instrument is not self-origin")
    return lessons


def delivery_path_check():
    """Build gate 2: the production serving path serves exactly one
    tool on the ground's own features, equal to the lesson's concept
    plus applies_when. A genuine pin match, nothing injected."""
    store = load_store()
    tools = menu.query(store, ground_features())
    if len(tools) != 1:
        raise SystemExit(f"delivery-path check: {len(tools)} tools, "
                         f"expected 1")
    same = (tools[0] == {"concept": store[0]["concept"],
                         "applies_when": store[0]["applies_when"]})
    if not same:
        raise SystemExit("delivery-path check: the served tool does "
                         "not equal the lesson's concept plus "
                         "applies_when")
    return tools


def build_gates():
    """All deterministic gates, re-run as committed code before any
    model run. Returns the served tools for the armed cell."""
    _p("GATE 1, THE BYTE CHECK:")
    b = byte_check()
    _p(f"  store byte-identical to production line {STORE_PROD_LINE}, "
       f"position asserted: {b['ok']}")
    _p(f"  line {STORE_PROD_LINE} md5: {b['md5']}")
    if b["md5"] != DESK_CHECK_MD5:
        raise SystemExit("md5 differs from the desk check: the "
                         "production line moved since the cut")
    _p("GATE 2, THE DELIVERY-PATH CHECK (production serving, genuine "
       "pin match):")
    tools = delivery_path_check()
    _p(f"  menu serves the single-lesson store on ground features: "
       f"{len(tools)} tool")
    _p(f"  tool equals lesson concept plus applies_when: True")
    rung = sf.get_rung(GROUND_FAMILY, GROUND_RUNG)
    _p(f"GATE 3, THE ANNOTATION: rule checks for {GROUND_FAMILY} "
       f"r{GROUND_RUNG} (the standing annotation): "
       f"{rung['rule_checks']}")
    return tools


def _run_one(stage, cell, rep, tools):
    rung_def = sf.get_rung(GROUND_FAMILY, GROUND_RUNG)
    r = runner.run_once(rung_def["task"], CRITERIA, ground_features(),
                        model=PERFORMER, audience_model=AUDIENCE,
                        landscape=tools or None,
                        evidence_checks=rung_def["checks"])
    checks = {c["call"]: bool(c["ok"]) for c in
              (r["evidence"] or {}).get("results") or []}
    row = {"stage": stage, "cell": cell, "rep": rep,
           "run_id": r["run_id"], "verdict": r["verdict"],
           "tools": len(tools), "directives": r["directives_used"],
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


def rule_disagreement(rows):
    """Effective-n sizing (the standing addendum): rows where the two
    rule checks disagree inside the row. Rows with no readings count
    as agreeing (both fail under canon)."""
    rule_checks = list(sf.get_rung(GROUND_FAMILY,
                                   GROUND_RUNG)["rule_checks"])
    disagree = 0
    counted = 0
    for r in rows:
        checks = r.get("checks") or {}
        vals = [bool(checks.get(c, False)) for c in rule_checks]
        counted += 1
        if len(set(vals)) > 1:
            disagree += 1
    return {"rows": counted, "disagreeing_rows": disagree}


def stage_a(repeats=R, prior_rows=None):
    """Fresh qualification: 12 bare runs, mixed at the standing
    fraction. Gate only, never a baseline."""
    prior = [r for r in prior_rows or [] if r.get("stage") == "A"]
    done = {r["rep"] for r in prior}
    rows = list(prior)
    for rep in range(repeats):
        if rep in done:
            continue
        rows.append(_run_one("A", "none", rep, []))
    pooled = pooled_rule(rows)
    fails = pooled["n"] - pooled["passed"]
    qualified = (pooled["passed"] >= QUALIFY_MIN
                 and fails >= QUALIFY_MIN)
    _p(f"stage A gate: pooled rule {pooled['passed']} passes, {fails} "
       f"fails of {pooled['n']} canonical (unrunnable-as-fail; "
       f"{pooled['unrunnable_rows']} unrunnable rows; diagnostic "
       f"{pooled['present_passed']}/{pooled['present_n']} readings-"
       f"present); {'QUALIFIES' if qualified else 'FAILS'} (mixed "
       f"means at least {QUALIFY_MIN} of each)")
    return {"pooled": pooled, "fails": fails,
            "qualify_min": QUALIFY_MIN, "qualified": qualified}


def stage_b(tools, repeats=R, prior_rows=None):
    """The reading cells: none then armed per rep, interleaved."""
    prior = [r for r in prior_rows or [] if r.get("stage") == "B"]
    done = {(r["cell"], r["rep"]) for r in prior}
    rows = list(prior)
    for rep in range(repeats):
        for cell in CELLS:
            if (cell, rep) in done:
                continue
            rows.append(_run_one("B", cell, rep,
                                 tools if cell == "armed" else []))
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
    _p(f"MISTRAL SELF-DELIVERY {_TS} (PACKET-031, G2 re-scoped)")
    _p(f"performer={PERFORMER}  audience={AUDIENCE} (v1, production)")
    _p(f"ground={GROUND_FAMILY} r{GROUND_RUNG}  cells={CELLS}  "
       f"R={repeats}  stage A mixed gate {QUALIFY_MIN} AND "
       f"{QUALIFY_MIN} of 24  drift bar {RULE_BAR} of 24")
    _p(f"the instrument is mistral-origin delivered to mistral: the "
       f"two-cause caveat rides every non-FLAT exit in the packet "
       f"RESULTS")
    _p(f"census taxonomy, stated before any run (supply_families "
       f"classifier unchanged, identity-pinned, re-runnable: "
       f"py selfdel31.py census <rows-file>): "
       f"{', '.join(sf.FAMILIES[GROUND_FAMILY]['taxonomy'])}")
    _p(f"priors: P019 trait cell {PRIORS['P019_trait_cell']}; this "
       f"ground's candidacy {PRIORS['P026_candidacy_this_ground']}; "
       f"self-delivery {PRIORS['self_delivery']}")

    tools = build_gates()

    a = stage_a(repeats, prior_rows)
    b_rows = []
    pooled_b = {}
    table = {}
    eff_n = {}
    if a["qualified"]:
        _p(f"stage B on qualified ground: fresh interleaved cells, "
           f"{CELLS} per rep, readings against the stage B none cell "
           f"only")
        b_rows = stage_b(tools, repeats, prior_rows)
        pooled_b = {cell: pooled_rule(
            [r for r in b_rows if r["cell"] == cell]) for cell in CELLS}
        table = check_table(b_rows)
        eff_n = {cell: rule_disagreement(
            [r for r in b_rows if r["cell"] == cell]) for cell in CELLS}
    else:
        _p("stage A gate FAILED: the packet closes on the supply "
           "answer, registry candidacy moved under fresh measurement, "
           "no stage B, no reading fires")

    all_rows = _load_rows()
    audit_ok = all(
        r["tools"] == EXPECT[r["cell"]]["tools"]
        and r["directives"] == EXPECT[r["cell"]]["directives"]
        for r in all_rows)
    census = census_table(all_rows)
    divergent = sum(1 for r in all_rows
                    if (r["shape"] == "unrunnable") != r["no_readings"])

    report = {
        "selfdel31_id": _TS, "packet": "PACKET-031",
        "performer": PERFORMER, "audience": AUDIENCE,
        "ground": f"{GROUND_FAMILY} r{GROUND_RUNG}",
        "repeats": repeats, "cells": list(CELLS),
        "qualify_min": QUALIFY_MIN, "rule_bar": f"{RULE_BAR} of 24",
        "store_md5": DESK_CHECK_MD5,
        "stage_a": a,
        "stage_b": {"ran": a["qualified"],
                    "pooled_rule_checks": pooled_b,
                    "check_table": table,
                    "rule_disagreement": eff_n},
        "census": census,
        "census_no_readings_divergence": divergent,
        "audit_ok": audit_ok,
        "priors": PRIORS,
        "n_note": ("Stage A gates only. The three-exit reading, the "
                   "two-cause caveat, observability naming, and "
                   "effective-n sizing live in the packet and are "
                   "applied in its RESULTS."),
    }
    with open(_REPORT, "w", encoding="utf-8") as f:
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
    gate = counts_ok and audit_ok and os.path.exists(_ROWS)
    _p(f"GATE: {'PASSED' if gate else 'FAILED'}. build gates re-run "
       f"as committed code before any model run, stage A arithmetic "
       f"printed, stage B "
       f"{'ran whole' if a['qualified'] else 'did not run, closed on the supply answer'}"
       f", audits {'clean' if audit_ok else 'BROKEN'} from the rows, "
       f"census reported for every cell, every run checkpointed, "
       f"report persisted. The reading is applied in the packet "
       f"RESULTS. The seat neither taught nor learned.")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "census":
        raise SystemExit(recensus(sys.argv[2]))
    main(repeats=int(sys.argv[1]) if len(sys.argv) > 1 else R,
         resume_ts=sys.argv[2] if len(sys.argv) > 2 else None)
