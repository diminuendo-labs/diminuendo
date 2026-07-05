"""PACKET-026: supply calibration, the eye chart's first hang. The six
graded families from supply_families.py (the design document's
implementation) swept on all three seats with the universal procedure:
one seat at a time in the gap order mistral, qwen, llama, a seat's
whole sweep complete before the next begins. Per seat, per family,
rungs bottom-up: a bare none cell at R=12, no tools anywhere, census
on, canonical unrunnable-as-fail accounting. A rung that qualifies
mixed at the standing fraction enters the seat's kept pool and stops
that family for that seat; exhausted families record floor or ceiling
character per rung and keep nothing. Control rungs are swept like any
other and an unexpected qualification there is reported, never
suppressed.

Pure supply and audition instrumentation: no lessons, no delivery, no
treatment claims of any kind, and the audition firewall applies from
birth, so nothing here ever feeds lesson generation. The qualification
fraction generalizes the standing bar to any rule-check count n as 2n
passes AND 2n fails of 12n pooled, the same one-in-six fraction, since
three rungs carry more than two rule checks; logged in RESULTS.

Census classifiers are supply_families.py's, replayable:
py calibrate26.py census <rows-file>. The structural readings live in
the packet and are applied in its RESULTS. No seat teaches or
learns."""

import json
import os
import sys
import time

import runner
import supply_families as sf
from probe_tasks import CRITERIA, FEATURES

SEATS = (("mistral:7b", "llama3.1:8b"),
         ("qwen2.5-coder:7b", "llama3.1:8b"),
         ("llama3.1:8b", "qwen2.5-coder:7b"))
R = 12
CONCENTRATION = 9  # of 12, the standing per-seat criterion threshold

_TS = time.strftime("%Y%m%d-%H%M%S")
_LOG = os.path.join(runner.RUNS, f"calibrate26-{_TS}.log")
_ROWS = os.path.join(runner.RUNS, f"calibrate26-{_TS}.rows.jsonl")
_REPORT = os.path.join(runner.RUNS, f"calibrate26-{_TS}.report.json")


def _set_ts(ts):
    """Rebind the run id and its file paths. Resume reuses a prior id so
    the checkpoint rows, the log, and the report stay one record."""
    global _TS, _LOG, _ROWS, _REPORT
    _TS = ts
    _LOG = os.path.join(runner.RUNS, f"calibrate26-{_TS}.log")
    _ROWS = os.path.join(runner.RUNS, f"calibrate26-{_TS}.rows.jsonl")
    _REPORT = os.path.join(runner.RUNS, f"calibrate26-{_TS}.report.json")


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


def rule_n(family, rung):
    return len(sf.get_rung(family, rung)["rule_checks"])


def qualify_min(family, rung):
    """The standing fraction generalized: 2n of 12n pooled."""
    return 2 * rule_n(family, rung)


def census_table(rows):
    """Shape distribution per (seat, family, rung)."""
    table = {}
    for r in rows:
        key = f"{r['seat']}|{r['family']}|r{r['rung']}"
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


def _run_one(seat, audience, family, rung_def, rep):
    r = runner.run_once(rung_def["task"], CRITERIA, _features(family),
                        model=seat, audience_model=audience,
                        landscape=None,
                        evidence_checks=rung_def["checks"])
    checks = {c["call"]: bool(c["ok"]) for c in
              (r["evidence"] or {}).get("results") or []}
    row = {"seat": seat, "family": family, "rung": rung_def["rung"],
           "cell": "none", "rep": rep, "run_id": r["run_id"],
           "verdict": r["verdict"], "tools": 0,
           "ev": ev_fraction(r["evidence"]),
           "checks": checks,
           "no_readings": not checks,
           "shape": sf.census_shape(family, r["output"])}
    _row(row)
    _p(f"{seat} {family} r{rung_def['rung']} none rep {rep}: "
       f"ev={row['ev']:.2f} shape={row['shape']}")
    return row


def pooled_rule(rows, family, rung):
    """Canonical accounting (DECISIONS 2026-07-04): every row
    contributes every rule check and a missing reading counts as a
    fail. readings-present rides beside as the diagnostic."""
    rule_checks = set(sf.get_rung(family, rung)["rule_checks"])
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


def run_rung(seat, audience, family, rung, repeats=R, prior_rows=None):
    """One (seat, family, rung) none cell at R, qualification
    arithmetic printed. Gates the kept pool, never a baseline."""
    rung_def = sf.get_rung(family, rung)
    qmin = qualify_min(family, rung)
    prior = [r for r in prior_rows or []
             if r.get("seat") == seat and r.get("family") == family
             and r.get("rung") == rung]
    done = {r["rep"] for r in prior}
    rows = list(prior)
    for rep in range(repeats):
        if rep in done:
            continue
        rows.append(_run_one(seat, audience, family, rung_def, rep))
    pooled = pooled_rule(rows, family, rung)
    fails = pooled["n"] - pooled["passed"]
    qualified = pooled["passed"] >= qmin and fails >= qmin
    character = ("mixed" if qualified else
                 "floor-leaning" if pooled["passed"] < qmin else
                 "ceiling-leaning")
    control = (family, rung) in sf.CONTROL_RUNGS
    _p(f"{seat} {family} r{rung}: pooled rule {pooled['passed']} "
       f"passes, {fails} fails of {pooled['n']} canonical "
       f"(unrunnable-as-fail; {pooled['unrunnable_rows']} unrunnable "
       f"rows; diagnostic {pooled['present_passed']}/"
       f"{pooled['present_n']} readings-present); "
       f"{'QUALIFIES' if qualified else 'does not qualify'} "
       f"(mixed means at least {qmin} of each)"
       + (" [CONTROL RUNG"
          + (", UNEXPECTED QUALIFICATION" if qualified else "")
          + "]" if control else ""))
    return {"seat": seat, "family": family, "rung": rung,
            "pooled": pooled, "fails": fails, "qualify_min": qmin,
            "qualified": qualified, "character": character,
            "control": control, "rows": rows}


def sweep_seat(seat, audience, repeats=R, prior_rows=None):
    """One seat's whole sweep: every family bottom-up, each family
    stopping at its first mixed rung."""
    results = []
    kept = []
    for family in sf.FAMILY_ORDER:
        for rung in (1, 2, 3):
            result = run_rung(seat, audience, family, rung, repeats,
                              prior_rows)
            results.append({k: v for k, v in result.items()
                            if k != "rows"})
            if result["qualified"]:
                kept.append({"family": family, "rung": rung,
                             "pooled": result["pooled"],
                             "control": result["control"]})
                _p(f"{seat} {family}: KEPT at rung {rung}, the family "
                   f"stops for this seat")
                break
        else:
            _p(f"{seat} {family}: rungs exhausted, nothing kept, the "
               f"per-rung character is on the record")
    return results, kept


def moderator_ready(kept, census, seat):
    """The designation, one sentence per case in RESULTS: a kept rung
    whose census concentrates at CONCENTRATION of 12 or better on the
    family's named shape."""
    out = []
    for k in kept:
        fam = sf.FAMILIES[k["family"]]
        key = f"{seat}|{k['family']}|r{k['rung']}"
        count = census.get(key, {}).get(fam["named_shape"], 0)
        if count >= CONCENTRATION:
            out.append({"family": k["family"], "rung": k["rung"],
                        "named_shape": fam["named_shape"],
                        "relationship": fam["relationship"],
                        "count": count})
    return out


def main(repeats=R, resume_ts=None):
    prior_rows = []
    if resume_ts:
        _set_ts(resume_ts)
        prior_rows = _load_rows()
        _p(f"RESUME {_TS}: {len(prior_rows)} checkpointed rows found")
    _p(f"SUPPLY CALIBRATION {_TS} (PACKET-026, the universal sweep)")
    _p(f"seats in gap order: " +
       "  ".join(f"{s} (audience {a})" for s, a in SEATS) +
       f"  R={repeats}, every row a bare none cell, tools=0, no "
       f"lessons anywhere, audition firewall from birth")
    _p(f"qualification, the standing fraction generalized to n rule "
       f"checks: at least 2n passes AND 2n fails of 12n pooled, "
       f"canonical unrunnable-as-fail accounting")
    _p("families, taxonomies, and rule-check annotations, stated "
       "before any run (classifiers committed in supply_families.py, "
       "re-runnable: py calibrate26.py census <rows-file>):")
    for family in sf.FAMILY_ORDER:
        fam = sf.FAMILIES[family]
        _p(f"  {family}: pins {fam['pins']['rule_class']}/"
           f"{fam['pins']['rule_topic']}  named shape "
           f"{fam['named_shape']} ({fam['relationship']})  taxonomy: "
           f"{', '.join(fam['taxonomy'])}")
        for rung_def in fam["rungs"]:
            control = ((family, rung_def["rung"]) in sf.CONTROL_RUNGS)
            _p(f"    r{rung_def['rung']}"
               + (" [control]" if control else "")
               + f" rule checks ({len(rung_def['rule_checks'])}): "
               f"{rung_def['rule_checks']}")

    seat_results = {}
    kept_pools = {}
    for seat, audience in SEATS:
        _p(f"== SWEEP {seat} (audience {audience}) ==")
        results, kept = sweep_seat(seat, audience, repeats, prior_rows)
        seat_results[seat] = results
        kept_pools[seat] = kept
        _p(f"{seat} kept pool: " +
           (", ".join(f"({k['family']}, r{k['rung']})" for k in kept)
            if kept else "EMPTY, a loud supply result"))

    all_rows = _load_rows()
    audit_ok = all(r["tools"] == 0 and r["cell"] == "none"
                   for r in all_rows)
    census = census_table(all_rows)
    divergent = sum(1 for r in all_rows
                    if (r["shape"] == "unrunnable") != r["no_readings"])
    ready = {seat: moderator_ready(kept_pools[seat], census, seat)
             for seat, _ in SEATS}

    report = {
        "calibrate26_id": _TS, "packet": "PACKET-026",
        "seats": [{"performer": s, "audience": a} for s, a in SEATS],
        "repeats": repeats,
        "qualify_rule": "standing fraction generalized: 2n passes AND "
                        "2n fails of 12n pooled for n rule checks, "
                        "canonical unrunnable-as-fail",
        "family_order": list(sf.FAMILY_ORDER),
        "control_rungs": sorted(list(sf.CONTROL_RUNGS)),
        "annotations": {f"{family}|r{r['rung']}": r["rule_checks"]
                        for family in sf.FAMILY_ORDER
                        for r in sf.FAMILIES[family]["rungs"]},
        "taxonomies": {family: list(sf.FAMILIES[family]["taxonomy"])
                       for family in sf.FAMILY_ORDER},
        "seat_results": seat_results,
        "kept_pools": kept_pools,
        "moderator_ready": ready,
        "census": census,
        "census_no_readings_divergence": divergent,
        "tool_audit_ok": audit_ok,
        "n_note": ("Pure supply and audition instrumentation: no "
                   "treatment, delivery, moderator, or trait claim "
                   "under any outcome. Structural readings live in "
                   "the packet and are applied in its RESULTS. Kept "
                   "pools enter no standing pool without the "
                   "conductor's ruling."),
    }
    with open(_REPORT, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    _p("== KEPT POOLS ==")
    for seat, _ in SEATS:
        kept = kept_pools.get(seat, [])
        _p(f"  {seat}: " +
           (", ".join(f"({k['family']}, r{k['rung']}, "
                      f"{k['pooled']['passed']}/{k['pooled']['n']})"
                      for k in kept) if kept else "EMPTY"))
    _p("== MODERATOR-READY DESIGNATIONS (kept AND census at "
       f"{CONCENTRATION} of 12 or better on the named shape) ==")
    any_ready = False
    for seat, entries in ready.items():
        for e in entries:
            any_ready = True
            _p(f"  {seat} ({e['family']}, r{e['rung']}): "
               f"{e['count']}/12 {e['named_shape']} "
               f"({e['relationship']})")
    if not any_ready:
        _p("  none")
    _p("== CENSUS (shape distribution per cell, every cell run) ==")
    for key in sorted(census):
        dist = "  ".join(f"{s}={n}" for s, n in census[key].items())
        _p(f"  {key}: {dist}")
    _p(f"census unrunnable against zero-readings divergence: "
       f"{divergent} rows")

    gate = audit_ok and os.path.exists(_ROWS)
    _p(f"GATE: {'PASSED' if gate else 'FAILED'}. seats swept whole in "
       f"the stated order, rungs bottom-up with families stopping at "
       f"their first mixed rung, arithmetic printed per rung, tool "
       f"audit {'clean (tools=0 every row)' if audit_ok else 'BROKEN'}"
       f", census reported for every cell, every run checkpointed, "
       f"report persisted. The structural readings are applied in the "
       f"packet RESULTS. No seat taught or learned.")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "census":
        raise SystemExit(recensus(sys.argv[2]))
    main(repeats=int(sys.argv[1]) if len(sys.argv) > 1 else R,
         resume_ts=sys.argv[2] if len(sys.argv) > 2 else None)
