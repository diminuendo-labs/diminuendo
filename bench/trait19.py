"""PACKET-019: the trait measurement, staged and qualified. Two trait
cells returned null on ground that lied at R=6, so this packet gates
before it measures, per the amended doctrine: stage A qualifies ground
with a none cell at R=12 (mixed means at least 4 passes AND 4 fails of
the 24 pooled rule readings), ranked second_largest then dedupe,
stopping at the first qualifier or closing on the supply answer. Stage
B, on qualified ground only, runs FRESH interleaved cells, none then
armed per rep, the PACKET-014 llama-origin distinctness lesson riding
byte-verbatim as the instrument. Stage A cells gate; they are never the
treatment baseline.

Performer mistral:7b, audience llama3.1:8b, v1 production path, pins
live. The signed three-exit reading (bar 4 of 24 pooled, the two-cause
sentence pre-registered for HARM) and the no-name boundary-watch live in
the packet and are applied in its RESULTS by the reader. The seat
neither teaches nor learns. The harness reports, it does not rule."""

import json
import os
import sys
import time

import lesson
import menu
import runner
from probe_tasks import CANDIDATE_APPLY_TASKS, CRITERIA, FEATURES

PERFORMER = "mistral:7b"
AUDIENCE = "llama3.1:8b"
CANDIDATES = ("second_largest", "dedupe")  # ranked order
R = 12
QUALIFY_MIN = 4  # at least this many passes AND fails of 24 pooled

_PACKETS = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        "packets")
STORE = os.path.join(_PACKETS, "PACKET-019-lesson_armed.jsonl")
SOURCE = os.path.join(_PACKETS, "PACKET-014-lessons.jsonl")

_TASKS = {t["name"]: t for t in CANDIDATE_APPLY_TASKS}

_TS = time.strftime("%Y%m%d-%H%M%S")
_LOG = os.path.join(runner.RUNS, f"trait19-{_TS}.log")
_ROWS = os.path.join(runner.RUNS, f"trait19-{_TS}.rows.jsonl")
_REPORT = os.path.join(runner.RUNS, f"trait19-{_TS}.report.json")


def _set_ts(ts):
    """Rebind the run id and its file paths. Resume reuses a prior id so
    the checkpoint rows, the log, and the report stay one record."""
    global _TS, _LOG, _ROWS, _REPORT
    _TS = ts
    _LOG = os.path.join(runner.RUNS, f"trait19-{_TS}.log")
    _ROWS = os.path.join(runner.RUNS, f"trait19-{_TS}.rows.jsonl")
    _REPORT = os.path.join(runner.RUNS, f"trait19-{_TS}.report.json")


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


def byte_check():
    with open(STORE, "rb") as f:
        local = f.read()
    with open(SOURCE, "rb") as f:
        ok = f.read() == local
    if not ok:
        raise SystemExit("byte check failed, the lesson was touched")
    return ok


def load_armed():
    lessons = lesson.load(STORE)
    if len(lessons) != 1:
        raise SystemExit(f"armed store must hold 1 lesson, "
                         f"found {len(lessons)}")
    lesson.validate(lessons[0])
    return lessons


def _run_one(t, tools, tag, rep):
    r = runner.run_once(t["task"], CRITERIA, _features(t),
                        model=PERFORMER, audience_model=AUDIENCE,
                        landscape=tools or None,
                        evidence_checks=t["checks"])
    row = {"stage": tag[0], "cell": tag[1], "task": t["name"],
           "rep": rep, "run_id": r["run_id"], "verdict": r["verdict"],
           "tools": len(tools),
           "ev": ev_fraction(r["evidence"]),
           "checks": {c["call"]: bool(c["ok"]) for c in
                      (r["evidence"] or {}).get("results") or []}}
    _row(row)
    _p(f"{tag[0]} {t['name']} {tag[1]} rep {rep}: ev={row['ev']:.2f} "
       f"tools={row['tools']}")
    return row


def pooled_rule(rows, task_name):
    rule_checks = set(_TASKS[task_name].get("rule_checks", []))
    out = {"n": 0, "passed": 0}
    for r in rows:
        for call, ok in (r.get("checks") or {}).items():
            if call in rule_checks:
                out["n"] += 1
                out["passed"] += 1 if ok else 0
    return out


def qualify(task_name, repeats=R, prior_rows=None):
    """Stage A gate cell: none at R, pooled rule readings, mixed means
    at least QUALIFY_MIN passes AND fails. Gate only, never a baseline."""
    t = _TASKS[task_name]
    prior = [r for r in prior_rows or []
             if r.get("stage") == "A" and r.get("task") == task_name]
    done = {r["rep"] for r in prior}
    rows = list(prior)
    for rep in range(repeats):
        if rep in done:
            continue
        rows.append(_run_one(t, [], ("A", "none"), rep))
    pooled = pooled_rule(rows, task_name)
    fails = pooled["n"] - pooled["passed"]
    qualified = (pooled["passed"] >= QUALIFY_MIN
                 and fails >= QUALIFY_MIN)
    _p(f"stage A {task_name}: pooled rule {pooled['passed']} passes, "
       f"{fails} fails of {pooled['n']}; "
       f"{'QUALIFIES' if qualified else 'does not qualify'} "
       f"(mixed means at least {QUALIFY_MIN} of each)")
    return {"task": task_name, "pooled": pooled, "fails": fails,
            "qualified": qualified}


def run_stage_b(task_name, repeats=R, prior_rows=None):
    """Fresh interleaved cells on the qualified ground."""
    armed = load_armed()
    t = _TASKS[task_name]
    prior = [r for r in prior_rows or [] if r.get("stage") == "B"]
    done = {(r["cell"], r["rep"]) for r in prior}
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
            rows.append(_run_one(t, tools, ("B", cell), rep))
    return rows


def stage_b_table(rows, task_name):
    rule_checks = set(_TASKS[task_name].get("rule_checks", []))
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


def main(repeats=R, resume_ts=None):
    prior_rows = []
    if resume_ts:
        _set_ts(resume_ts)
        prior_rows = _load_rows()
        _p(f"RESUME {_TS}: {len(prior_rows)} checkpointed rows found")
    ok = byte_check()
    _p(f"STAGED QUALIFIED TRAIT {_TS} (PACKET-019)")
    _p(f"performer={PERFORMER}  audience={AUDIENCE} (v1, production)")
    _p(f"candidates={CANDIDATES} (ranked)  R={repeats}  "
       f"qualify: at least {QUALIFY_MIN} passes AND {QUALIFY_MIN} fails "
       f"of 24 pooled  byte check={ok}")
    for name in CANDIDATES:
        _p(f"rule checks for {name} (the standing annotation): "
           f"{_TASKS[name]['rule_checks']}")

    stage_a = []
    ground = None
    for name in CANDIDATES:
        result = qualify(name, repeats, prior_rows)
        stage_a.append(result)
        if result["qualified"]:
            ground = name
            break

    stage_b_rows = []
    table = {}
    pooled_b = {}
    if ground:
        _p(f"stage B on qualified ground: {ground}, fresh interleaved "
           f"cells, the stage A cell gates and is never the baseline")
        stage_b_rows = run_stage_b(ground, repeats, prior_rows)
        table = stage_b_table(stage_b_rows, ground)
        for cell in ("none", "armed"):
            pooled_b[cell] = pooled_rule(
                [r for r in stage_b_rows if r["cell"] == cell], ground)
    else:
        _p("no candidate qualified: the packet closes on the supply "
           "answer, the next ground is the conductor's cut")

    audit_ok = all(
        r["tools"] == (1 if r.get("cell") == "armed" else 0)
        for r in stage_b_rows)

    report = {
        "trait19_id": _TS, "performer": PERFORMER, "audience": AUDIENCE,
        "candidates": list(CANDIDATES), "repeats": repeats,
        "qualify_rule": f"at least {QUALIFY_MIN} passes and "
                        f"{QUALIFY_MIN} fails of 24 pooled",
        "byte_check": ok, "stage_a": stage_a, "qualified_ground": ground,
        "stage_b": {"ran": ground is not None,
                    "drift_bar": "4 of 24 pooled",
                    "check_table": table,
                    "pooled_rule_checks": pooled_b,
                    "tool_audit_ok": audit_ok},
        "n_note": ("Stage A gates only. The three-exit reading, the "
                   "two-cause HARM sentence, and the no-name "
                   "boundary-watch live in the packet and are applied "
                   "in its RESULTS, not here."),
    }
    with open(_REPORT, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    if ground:
        _p("== STAGE B POOLED RULE CHECKS (passed/n per cell) ==")
        for cell in ("none", "armed"):
            _p(f"  {cell}: {pooled_b[cell]['passed']}/"
               f"{pooled_b[cell]['n']}")
        _p("== STAGE B PER-CHECK (none / armed) ==")
        for call, c in table.items():
            rates = " / ".join(
                f"{c['cells'].get(a, {}).get('rate', 0.0):.2f}"
                for a in ("none", "armed"))
            mark = "  <-- rule" if c["rule_check"] else "  <-- watch"
            _p(f"  {call}: {rates}{mark}")

    counts_ok = all(
        sum(1 for r in stage_b_rows if r["cell"] == c) == repeats
        for c in ("none", "armed")) if ground else True
    gate = counts_ok and audit_ok and os.path.exists(_ROWS)
    _p(f"GATE: {'PASSED' if gate else 'FAILED'}. stage A ran in ranked "
       f"order with the arithmetic printed, stage B "
       f"{'ran on ' + ground if ground else 'closed on the supply answer'}"
       f", every run checkpointed, report persisted. The reading is "
       f"applied in the packet RESULTS. The seat neither taught nor "
       f"learned.")


if __name__ == "__main__":
    main(repeats=int(sys.argv[1]) if len(sys.argv) > 1 else R,
         resume_ts=sys.argv[2] if len(sys.argv) > 2 else None)
