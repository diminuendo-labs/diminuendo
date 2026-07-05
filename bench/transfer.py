"""PACKET-006: focused transfer arms. The first treatment measurement at
an n that can carry a claim.

Four pairings of performer, class-matched apply tasks, and a lesson
store, each labeled topic_matched: whether the lessons' content addresses
the task's own stated rule or only its class. Two arms per pairing, none
and menu, R=12 per arm per task, the PACKET-004 format the conductor
adopted as doctrine for treatment questions. The five lessons ride
verbatim from packet-local copies of the PACKET-005 probe stores; no
lesson generation, no lesson editing.

Two pre-registered questions in one run: do topic-matched lessons
transfer across seats, and do topic-mismatched lessons of the same class
do anything (prediction: no effect, no harm, the menu safety property).
The reading rules are in the packet and get applied in RESULTS by the
reader. The harness reports, it does not rule.
"""

import json
import os
import sys
import time

import lesson
import menu
import runner
from probe_tasks import APPLY_TASKS, CRITERIA, FEATURES

AUDIENCE = {"llama3.1:8b": "qwen2.5-coder:7b",
            "qwen2.5-coder:7b": "llama3.1:8b"}
ARMS = ("none", "menu")
R = 12

_PACKETS = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        "packets")
STORES = {"A": os.path.join(_PACKETS, "PACKET-006-lessons_A.jsonl"),
          "B": os.path.join(_PACKETS, "PACKET-006-lessons_B.jsonl")}
STORE_SIZES = {"A": 2, "B": 3}

PAIRINGS = [
    {"id": "P1", "performer": "llama3.1:8b", "tasks": ["longest_word"],
     "store": "A", "topic_matched": True},
    {"id": "P2", "performer": "qwen2.5-coder:7b",
     "tasks": ["range_summary"], "store": "B", "topic_matched": True},
    {"id": "P3", "performer": "qwen2.5-coder:7b",
     "tasks": ["snake_to_camel"], "store": "B", "topic_matched": False},
    {"id": "P4", "performer": "llama3.1:8b",
     "tasks": ["snake_to_camel", "balanced"], "store": "A",
     "topic_matched": False},
]

_TASKS = {t["name"]: t for t in APPLY_TASKS}

_TS = time.strftime("%Y%m%d-%H%M%S")
_LOG = os.path.join(runner.RUNS, f"transfer-{_TS}.log")
_ROWS = os.path.join(runner.RUNS, f"transfer-{_TS}.rows.jsonl")
_REPORT = os.path.join(runner.RUNS, f"transfer-{_TS}.report.json")


def _set_ts(ts):
    """Rebind the run id and its file paths. Resume reuses a prior id so
    the checkpoint rows, the log, and the report stay one record."""
    global _TS, _LOG, _ROWS, _REPORT
    _TS = ts
    _LOG = os.path.join(runner.RUNS, f"transfer-{_TS}.log")
    _ROWS = os.path.join(runner.RUNS, f"transfer-{_TS}.rows.jsonl")
    _REPORT = os.path.join(runner.RUNS, f"transfer-{_TS}.report.json")


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
    if "stated_direction" in t:
        f["stated_direction"] = t["stated_direction"]
    return f


def load_store(key):
    """A packet-local store, size-checked, every lesson through the
    gates. The stores ride verbatim; a wrong count means the materials
    were touched, and the harness refuses to run on touched materials."""
    lessons = lesson.load(STORES[key])
    if len(lessons) != STORE_SIZES[key]:
        raise SystemExit(f"store {key} must hold {STORE_SIZES[key]} "
                         f"lessons, found {len(lessons)}")
    for l in lessons:
        lesson.validate(l)
    return lessons


def run_pairing(pairing, repeats=R, prior_rows=None):
    """One pairing, both arms, all its tasks. Runs already checkpointed
    by an interrupted run are counted, not repeated."""
    pid = pairing["id"]
    lessons = load_store(pairing["store"])
    prior = [r for r in prior_rows or [] if r.get("pairing") == pid]
    done = {(r["arm"], r["task"], r["rep"]) for r in prior}
    if prior:
        _p(f"{pid}: resuming past {len(prior)} checkpointed runs")
    rows = list(prior)
    for arm in ARMS:
        for rep in range(repeats):
            for name in pairing["tasks"]:
                if (arm, name, rep) in done:
                    continue
                t = _TASKS[name]
                tools = []
                if arm == "menu":
                    tools = menu.query(lessons, _features(t))
                    if not tools:
                        raise SystemExit(
                            f"{pid}: menu arm delivered no tools on "
                            f"{name}, the instrument is broken")
                r = runner.run_once(t["task"], CRITERIA, _features(t),
                                    model=pairing["performer"],
                                    audience_model=AUDIENCE[
                                        pairing["performer"]],
                                    landscape=tools or None,
                                    evidence_checks=t["checks"])
                row = {"pairing": pid,
                       "topic_matched": pairing["topic_matched"],
                       "performer": pairing["performer"],
                       "store": pairing["store"], "arm": arm,
                       "task": name, "rep": rep, "run_id": r["run_id"],
                       "verdict": r["verdict"], "tools": len(tools),
                       "tool_concepts": [x["concept"] for x in tools],
                       "ev": ev_fraction(r["evidence"]),
                       "checks": {c["call"]: bool(c["ok"]) for c in
                                  (r["evidence"] or {}).get("results")
                                  or []}}
                _row(row)
                rows.append(row)
                _p(f"{pid} {arm} rep {rep} ({name}): "
                   f"ev={row['ev']:.2f} tools={row['tools']}")
    return rows


def check_table(rows):
    """Per pairing, per task, per check: pass rate per arm, rule checks
    marked. The harm column is every non-rule check read armed against
    none."""
    table = {}
    for r in rows:
        rule_checks = set(_TASKS[r["task"]].get("rule_checks", []))
        for call, ok in (r.get("checks") or {}).items():
            cell = (table.setdefault(r["pairing"], {})
                    .setdefault(r["task"], {})
                    .setdefault(call, {"rule_check": call in rule_checks,
                                       "arms": {}})
                    ["arms"].setdefault(r["arm"], {"n": 0, "passed": 0}))
            cell["n"] += 1
            cell["passed"] += 1 if ok else 0
    for p in table.values():
        for t in p.values():
            for c in t.values():
                for a in c["arms"].values():
                    a["rate"] = a["passed"] / a["n"] if a["n"] else 0.0
    return table


def pooled_rule_checks(rows):
    """Per pairing per arm: pooled rule-check passes over all rule-check
    instances, the packet's transfer criterion input."""
    pooled = {}
    for r in rows:
        rule_checks = set(_TASKS[r["task"]].get("rule_checks", []))
        for call, ok in (r.get("checks") or {}).items():
            if call not in rule_checks:
                continue
            cell = (pooled.setdefault(r["pairing"], {})
                    .setdefault(r["arm"], {"n": 0, "passed": 0}))
            cell["n"] += 1
            cell["passed"] += 1 if ok else 0
    for p in pooled.values():
        for a in p.values():
            a["rate"] = a["passed"] / a["n"] if a["n"] else 0.0
    return pooled


def tool_audit(rows):
    """Which lesson concepts rode which tasks, across all armed runs."""
    audit = {}
    for r in rows:
        if r["arm"] != "menu":
            continue
        for concept in r.get("tool_concepts", []):
            audit.setdefault(r["task"], set()).add(concept)
    return {k: sorted(v) for k, v in audit.items()}


def main(repeats=R, resume_ts=None):
    prior_rows = []
    if resume_ts:
        _set_ts(resume_ts)
        prior_rows = _load_rows()
        _p(f"RESUME {_TS}: {len(prior_rows)} checkpointed rows found")
    total = sum(len(p["tasks"]) for p in PAIRINGS) * len(ARMS) * repeats
    _p(f"FOCUSED TRANSFER {_TS} (PACKET-006)")
    _p(f"pairings={len(PAIRINGS)}  arms={ARMS}  R={repeats}  "
       f"total runs={total}")
    all_rows = []
    for pairing in PAIRINGS:
        all_rows.extend(run_pairing(pairing, repeats, prior_rows))

    table = check_table(all_rows)
    pooled = pooled_rule_checks(all_rows)
    audit = tool_audit(all_rows)
    armed = [r for r in all_rows if r["arm"] == "menu"]
    min_tools = min((r["tools"] for r in armed), default=0)

    report = {
        "transfer_id": _TS, "arms": ARMS, "repeats": repeats,
        "pairings": PAIRINGS,
        "stores": {k: [{"concept": l["concept"], "rule": l["rule"],
                        "applies_when": l["applies_when"]}
                       for l in load_store(k)] for k in STORES},
        "check_table": table, "pooled_rule_checks": pooled,
        "tool_audit": audit, "min_tools_armed": min_tools,
        "n_note": (f"R={repeats} per arm per task. Per-check cells are "
                   f"n={repeats}. The reading rules live in the packet "
                   f"and are applied in its RESULTS, not here."),
    }
    with open(_REPORT, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    _p("== POOLED RULE CHECKS (passed/n per arm) ==")
    for pid in sorted(pooled):
        cells = "  ".join(
            f"{a}={pooled[pid][a]['passed']}/{pooled[pid][a]['n']}"
            for a in ARMS if a in pooled[pid])
        _p(f"  {pid}: {cells}")
    _p("== PER-CHECK (none / menu) ==")
    for pid in sorted(table):
        for tname in sorted(table[pid]):
            for call, c in table[pid][tname].items():
                rates = " / ".join(
                    f"{c['arms'].get(a, {}).get('rate', 0.0):.2f}"
                    for a in ARMS)
                mark = "  <-- rule" if c["rule_check"] else ""
                _p(f"  {pid} {call}: {rates}{mark}")

    per_pairing_n = {p["id"]: len(p["tasks"]) * repeats for p in PAIRINGS}
    complete = all(
        sum(1 for r in all_rows
            if r["pairing"] == p["id"] and r["arm"] == a) ==
        per_pairing_n[p["id"]]
        for p in PAIRINGS for a in ARMS)
    gate = complete and min_tools > 0 and os.path.exists(_ROWS)
    _p(f"GATE: {'PASSED' if gate else 'FAILED'}. four pairings, both "
       f"arms complete, every armed run carried tools "
       f"(min={min_tools}), every run checkpointed, report persisted. "
       f"The reading rules are applied in the packet RESULTS.")


if __name__ == "__main__":
    main(repeats=int(sys.argv[1]) if len(sys.argv) > 1 else R,
         resume_ts=sys.argv[2] if len(sys.argv) > 2 else None)
