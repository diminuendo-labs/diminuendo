"""PACKET-017: third-seat onboarding executed against mistral:7b, the
seat Brad pulled on the conductor's recommendation. PACKET-016's stages
1 and 2, verbatim, staged inside one detached run.

Stage 0 is a presence check, printed before any run. Stage 1 baselines
the seat at R=6 across every task in both v1 candidate pools, evidence
execution as the label: counts, no treatment claims, no rates. The
audience is llama3.1:8b, cross-family from the seat, stated for the
record; the audience is a detector here, evidence is the label. Stage 2
runs only if stage 1 shows range_summary headroom: two interleaved
cells, none and the PACKET-014 llama-origin lesson byte-copied
packet-local, R=12, the signed three-exit reading with the 2-of-12 bar
applied in the packet RESULTS by the reader. The seat neither teaches
nor learns anywhere in this packet: no distillation, no chair memory,
no production store changes."""

import json
import os
import subprocess
import sys
import time

import lesson
import menu
import runner
from probe_tasks import (APPLY_TASKS, CANDIDATE_APPLY_TASKS,
                         CANDIDATE_GEN_TASKS, CRITERIA, FEATURES)

SEAT = "mistral:7b"
AUDIENCE = "llama3.1:8b"
R_BASE = 6
R_TRAIT = 12
TRAIT_TASK = "range_summary"

_PACKETS = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        "packets")
ARMED_STORE = os.path.join(_PACKETS, "PACKET-017-lesson_armed.jsonl")
ARMED_SOURCE = os.path.join(_PACKETS, "PACKET-014-lessons.jsonl")

_ALL = {t["name"]: t for t in CANDIDATE_GEN_TASKS + CANDIDATE_APPLY_TASKS}
_KEPT_APPLY = {t["name"]: t for t in APPLY_TASKS}

_TS = time.strftime("%Y%m%d-%H%M%S")
_LOG = os.path.join(runner.RUNS, f"onboard17-{_TS}.log")
_ROWS = os.path.join(runner.RUNS, f"onboard17-{_TS}.rows.jsonl")
_REPORT = os.path.join(runner.RUNS, f"onboard17-{_TS}.report.json")


def _set_ts(ts):
    """Rebind the run id and its file paths. Resume reuses a prior id so
    the checkpoint rows, the log, and the report stay one record."""
    global _TS, _LOG, _ROWS, _REPORT
    _TS = ts
    _LOG = os.path.join(runner.RUNS, f"onboard17-{_TS}.log")
    _ROWS = os.path.join(runner.RUNS, f"onboard17-{_TS}.rows.jsonl")
    _REPORT = os.path.join(runner.RUNS, f"onboard17-{_TS}.report.json")


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


def seat_installed():
    """Stage 0, the presence check."""
    out = subprocess.run(["ollama", "list"], capture_output=True,
                         text=True, timeout=30)
    return any(line.split()[0] == SEAT
               for line in out.stdout.splitlines()[1:] if line.strip())


def byte_check():
    with open(ARMED_STORE, "rb") as f:
        local = f.read()
    with open(ARMED_SOURCE, "rb") as f:
        ok = f.read() == local
    if not ok:
        raise SystemExit("byte check failed, the armed lesson was touched")
    return ok


def load_armed():
    lessons = lesson.load(ARMED_STORE)
    if len(lessons) != 1:
        raise SystemExit(f"armed store must hold 1 lesson, "
                         f"found {len(lessons)}")
    lesson.validate(lessons[0])
    return lessons


def baseline_tasks():
    """Every task in both v1 candidate pools, generation pool first."""
    return ([{"name": t["name"], "pool": "generation"}
             for t in CANDIDATE_GEN_TASKS]
            + [{"name": t["name"], "pool": "apply"}
               for t in CANDIDATE_APPLY_TASKS])


def run_stage1(repeats=R_BASE, prior_rows=None):
    enum = baseline_tasks()
    prior = [r for r in prior_rows or [] if r.get("stage") == 1]
    done = {(r["task"], r["rep"]) for r in prior}
    if prior:
        _p(f"stage 1: resuming past {len(prior)} checkpointed runs")
    rows = list(prior)
    for entry in enum:
        t = _ALL[entry["name"]]
        for rep in range(repeats):
            if (t["name"], rep) in done:
                continue
            r = runner.run_once(t["task"], CRITERIA, _features(t),
                                model=SEAT, audience_model=AUDIENCE,
                                evidence_checks=t["checks"])
            row = {"stage": 1, "task": t["name"], "pool": entry["pool"],
                   "rep": rep, "run_id": r["run_id"],
                   "verdict": r["verdict"],
                   "ev": ev_fraction(r["evidence"]),
                   "ev_passed": bool((r["evidence"] or {}).get("passed")),
                   "checks": {c["call"]: bool(c["ok"]) for c in
                              (r["evidence"] or {}).get("results") or []}}
            _row(row)
            rows.append(row)
            _p(f"s1 {t['name']} rep {rep}: ev={row['ev']:.2f} "
               f"passed={row['ev_passed']}")
    return rows


def supply_table(rows):
    apply_topics = {t["rule_topic"] for t in APPLY_TASKS}
    table = []
    for entry in baseline_tasks():
        t = _ALL[entry["name"]]
        task_rows = [r for r in rows if r["task"] == t["name"]]
        fails = sum(1 for r in task_rows if not r["ev_passed"])
        table.append({"name": t["name"], "pool": entry["pool"],
                      "rule_class": t["rule_class"],
                      "rule_topic": t["rule_topic"],
                      "runs": len(task_rows), "fails": fails,
                      "passes": len(task_rows) - fails,
                      "case": ("mixed" if 0 < fails < len(task_rows) else
                               "all_pass" if fails == 0 else "all_fail"),
                      "headroom": fails > 0,
                      "conjunction_eligible": (
                          entry["pool"] == "generation" and fails > 0
                          and t["rule_topic"] in apply_topics)})
    return table


def contrast_pairs(table):
    """Standing engine rules over the generation pool: within-task pairs
    first, sibling pairs second, conjunction filter, per-class cap two.
    Enumerated only; the seat does not teach in this packet."""
    gen = [e for e in table if e["pool"] == "generation"]
    by_class = {}
    for e in gen:
        by_class.setdefault(e["rule_class"], []).append(e)
    pairs = []
    for cls, entries in by_class.items():
        cls_pairs = []
        for e in entries:
            if len(cls_pairs) >= 2:
                break
            if e["case"] == "mixed" and e["conjunction_eligible"]:
                cls_pairs.append({"type": "within_task",
                                  "rule_class": cls,
                                  "fail_task": e["name"],
                                  "pass_task": e["name"],
                                  "rule_topic": e["rule_topic"]})
        mined = {p["fail_task"] for p in cls_pairs}
        for e in entries:
            if len(cls_pairs) >= 2:
                break
            if e["name"] in mined or not e["fails"]:
                continue
            if not e["conjunction_eligible"]:
                continue
            partner = next((x for x in entries if x["name"] != e["name"]
                            and x["passes"]), None)
            if partner is None:
                continue
            cls_pairs.append({"type": "sibling", "rule_class": cls,
                              "fail_task": e["name"],
                              "pass_task": partner["name"],
                              "rule_topic": e["rule_topic"]})
            mined.add(e["name"])
        pairs.extend(cls_pairs)
    return pairs


def run_stage2(repeats=R_TRAIT, prior_rows=None):
    armed = load_armed()
    t = _KEPT_APPLY[TRAIT_TASK]
    prior = [r for r in prior_rows or [] if r.get("stage") == 2]
    done = {(r["cell"], r["rep"]) for r in prior}
    if prior:
        _p(f"stage 2: resuming past {len(prior)} checkpointed runs")
    rows = list(prior)
    for rep in range(repeats):
        for cell in ("none", "armed"):
            if (cell, rep) in done:
                continue
            tools = []
            if cell == "armed":
                tools = menu.query(armed, _features(t))
                if len(tools) != 1:
                    raise SystemExit(f"armed cell expected 1 tool, "
                                     f"got {len(tools)}")
            r = runner.run_once(t["task"], CRITERIA, _features(t),
                                model=SEAT, audience_model=AUDIENCE,
                                landscape=tools or None,
                                evidence_checks=t["checks"])
            row = {"stage": 2, "cell": cell, "task": TRAIT_TASK,
                   "rep": rep, "run_id": r["run_id"],
                   "verdict": r["verdict"], "tools": len(tools),
                   "ev": ev_fraction(r["evidence"]),
                   "checks": {c["call"]: bool(c["ok"]) for c in
                              (r["evidence"] or {}).get("results") or []}}
            _row(row)
            rows.append(row)
            _p(f"s2 rep {rep} {cell}: ev={row['ev']:.2f} "
               f"tools={row['tools']}")
    return rows


def stage2_table(rows):
    rule_checks = set(_KEPT_APPLY[TRAIT_TASK].get("rule_checks", []))
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


def main(resume_ts=None):
    prior_rows = []
    if resume_ts:
        _set_ts(resume_ts)
        prior_rows = _load_rows()
        _p(f"RESUME {_TS}: {len(prior_rows)} checkpointed rows found")
    if not seat_installed():
        _p(f"STAGE 0: {SEAT} is NOT installed. Stopping; the pull is "
           f"Brad's surface, not a session's.")
        return
    checks_ok = byte_check()
    _p(f"THIRD-SEAT ONBOARDING {_TS} (PACKET-017)")
    _p(f"STAGE 0: {SEAT} installed, confirmed before any run.")
    _p(f"seat={SEAT}  audience={AUDIENCE} (cross-family, stated)  "
       f"armed-lesson byte check={checks_ok}")
    _p(f"stage 1: {len(baseline_tasks())} tasks x R={R_BASE}")

    s1_rows = run_stage1(R_BASE, prior_rows)
    table = supply_table(s1_rows)
    pairs = contrast_pairs(table)
    _p("== STAGE 1 SUPPLY TABLE ==")
    for e in table:
        marks = []
        if e["headroom"]:
            marks.append("HEADROOM")
        if e["conjunction_eligible"]:
            marks.append("CONJUNCTION")
        _p(f"  {e['name']:24s} [{e['pool']:10s}] {e['case']:9s} "
           f"({e['fails']}/{e['runs']} failed) {' '.join(marks)}")
    _p(f"== ELIGIBLE CONTRAST PAIRS (enumerated, not distilled): "
       f"{len(pairs)} ==")
    for p in pairs:
        _p(f"  {p['rule_class']}/{p['rule_topic']} {p['type']}: "
           f"fail={p['fail_task']} pass={p['pass_task']}")

    range_entry = next(e for e in table if e["name"] == TRAIT_TASK)
    stage2_ran = range_entry["fails"] > 0
    s2_rows = []
    s2 = {}
    if stage2_ran:
        _p(f"stage 2: {TRAIT_TASK} shows headroom "
           f"({range_entry['fails']}/{range_entry['runs']} failed), "
           f"running the trait reading at R={R_TRAIT}")
        s2_rows = run_stage2(R_TRAIT, prior_rows)
        s2 = stage2_table(s2_rows)
        _p("== STAGE 2 PER-CHECK (none / armed) ==")
        for call, c in s2.items():
            rates = " / ".join(
                f"{c['cells'].get(a, {}).get('rate', 0.0):.2f}"
                for a in ("none", "armed"))
            mark = "  <-- rule" if c["rule_check"] else ""
            _p(f"  {call}: {rates}{mark}")
    else:
        _p(f"stage 2 SKIPPED: {TRAIT_TASK} showed no headroom at "
           f"R={R_BASE} (0 fails). The trait probe needs different "
           f"ground; that is the conductor's next cut.")

    report = {
        "onboard17_id": _TS, "seat": SEAT, "audience": AUDIENCE,
        "stage0_installed": True, "armed_byte_check": checks_ok,
        "stage1": {"repeats": R_BASE, "supply_table": table,
                   "eligible_pairs": pairs},
        "stage2": {"ran": stage2_ran, "repeats": R_TRAIT,
                   "drift_bar": "2 of 12", "check_table": s2,
                   "tool_audit_ok": all(
                       r["tools"] == (1 if r["cell"] == "armed" else 0)
                       for r in s2_rows)},
        "n_note": ("Stage 1 is a probe, counts not claims. Stage 2's "
                   "signed three-exit reading and the 2-of-12 bar live "
                   "in the packet and are applied in its RESULTS."),
    }
    with open(_REPORT, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    s1_ok = all(e["runs"] == R_BASE for e in table)
    s2_ok = (not stage2_ran) or all(
        sum(1 for r in s2_rows if r["cell"] == c) == R_TRAIT
        for c in ("none", "armed"))
    gate = s1_ok and s2_ok and os.path.exists(_ROWS)
    _p(f"GATE: {'PASSED' if gate else 'FAILED'}. stage 0 printed first, "
       f"stage 1 complete at R={R_BASE} across both pools, stage 2 "
       f"{'ran at R=' + str(R_TRAIT) if stage2_ran else 'skipped with '
       'the justification stated'}, every run checkpointed, report "
       f"persisted. The seat neither taught nor learned.")


if __name__ == "__main__":
    main(resume_ts=sys.argv[1] if len(sys.argv) > 1 else None)
