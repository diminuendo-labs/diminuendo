"""PACKET-009: the confirmation arms. The hardened stack measured end to
end on the first fully production-grade supply: the genpass
20260703-053623 lessons, conditional, declarative, topic-pinned,
direction-pinned, riding the production menu with every pin live.

Work item 2 enumerates the matched pairings programmatically from the
pins: a lesson matches an apply task when rule_class matches, rule_topic
matches or the lesson wildcards it, and stated_direction matches or is
unpinned. The full table is reported including structurally empty
lessons, because a lesson whose pins match no apply task is a supply
finding, and the packet ranks empties above everything else.

Work item 3 runs arms (none and menu, R=12 per arm per task) for every
matched pairing where the performer is the other seat from the lesson's
origin, plus a pin regression: deliberate topic-mismatch cells asserted
to deliver zero tools through the production menu, at no model cost.

The pre-registered reading lives in the packet and is applied in RESULTS
by the reader. The harness reports, it does not rule.
"""

import json
import os
import sys
import time

import lesson
import menu
import runner
from probe_tasks import APPLY_TASKS, CRITERIA, FEATURES

MODELS = {"A": "qwen2.5-coder:7b", "B": "llama3.1:8b"}
AUDIENCE = {"qwen2.5-coder:7b": "llama3.1:8b",
            "llama3.1:8b": "qwen2.5-coder:7b"}
ARMS = ("none", "menu")
R = 12

_PACKETS = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        "packets")
STORES = {"A": os.path.join(_PACKETS, "PACKET-009-lessons_A.jsonl"),
          "B": os.path.join(_PACKETS, "PACKET-009-lessons_B.jsonl")}
STORE_SIZES = {"A": 3, "B": 2}

# deliberate topic-mismatch cells, the pin regression: the menu must
# deliver zero tools on every one of these, asserted without model runs
PIN_REGRESSION = [
    {"store": "B", "task": "range_summary"},   # pairs vs values
    {"store": "B", "task": "snake_to_camel"},  # punctuation vs delimiters
    {"store": "A", "task": "balanced"},        # punctuation vs delimiters
    {"store": "A", "task": "most_common_word"},  # last vs alphabetical
]

_TASKS = {t["name"]: t for t in APPLY_TASKS}

_TS = time.strftime("%Y%m%d-%H%M%S")
_LOG = os.path.join(runner.RUNS, f"confirm-{_TS}.log")
_ROWS = os.path.join(runner.RUNS, f"confirm-{_TS}.rows.jsonl")
_REPORT = os.path.join(runner.RUNS, f"confirm-{_TS}.report.json")


def _set_ts(ts):
    """Rebind the run id and its file paths. Resume reuses a prior id so
    the checkpoint rows, the log, and the report stay one record."""
    global _TS, _LOG, _ROWS, _REPORT
    _TS = ts
    _LOG = os.path.join(runner.RUNS, f"confirm-{_TS}.log")
    _ROWS = os.path.join(runner.RUNS, f"confirm-{_TS}.rows.jsonl")
    _REPORT = os.path.join(runner.RUNS, f"confirm-{_TS}.report.json")


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


def load_store(key):
    """A packet-local store, size-checked, every lesson through the full
    gates. These are production-grade lessons; a gate failure here means
    the materials were touched."""
    lessons = lesson.load(STORES[key])
    if len(lessons) != STORE_SIZES[key]:
        raise SystemExit(f"store {key} must hold {STORE_SIZES[key]} "
                         f"lessons, found {len(lessons)}")
    for l in lessons:
        lesson.validate(l)
    return lessons


def lesson_id(key, l):
    trail = l.get("trail", {})
    return f"{key}/{trail.get('gen_task')}/{trail.get('contrast_type')}"


def matched(l, t):
    """The packet's matching rule, from the pins: class matches, topic
    matches or wildcard, direction matches or unpinned."""
    aw = l["applies_when"]
    if aw.get("rule_class") not in (t["rule_class"], "*"):
        return False
    if aw.get("rule_topic", "*") not in (t.get("rule_topic"), "*"):
        return False
    if aw.get("stated_direction", "*") not in (
            t.get("stated_direction"), "*") and \
            aw.get("stated_direction") is not None:
        return False
    return True


def pairing_table():
    """Every lesson against every apply task, from the pins alone."""
    table = []
    for key in ("A", "B"):
        for l in load_store(key):
            hits = [t["name"] for t in APPLY_TASKS if matched(l, t)]
            table.append({"lesson": lesson_id(key, l), "store": key,
                          "pins": {k: l["applies_when"].get(k) for k in
                                   ("rule_class", "rule_topic",
                                    "stated_direction")},
                          "matched_tasks": hits,
                          "structurally_empty": not hits})
    return table


def cross_seat_pairings(table):
    """Matched (performer, task, store) cells where the performer is the
    other seat from the lesson's origin, grouped per task."""
    cells = {}
    for entry in table:
        performer = MODELS["B"] if entry["store"] == "A" else MODELS["A"]
        for name in entry["matched_tasks"]:
            cell = cells.setdefault((performer, name, entry["store"]),
                                    {"performer": performer, "task": name,
                                     "store": entry["store"],
                                     "lessons": []})
            cell["lessons"].append(entry["lesson"])
    return list(cells.values())


def run_pairing(cell, repeats=R, prior_rows=None):
    """Both arms for one matched cross-seat cell. Checkpointed runs are
    counted, not repeated."""
    name = cell["task"]
    t = _TASKS[name]
    lessons = load_store(cell["store"])
    pid = f"{cell['performer'].split(':')[0]}|{name}|{cell['store']}"
    prior = [r for r in prior_rows or [] if r.get("pairing") == pid]
    done = {(r["arm"], r["rep"]) for r in prior}
    if prior:
        _p(f"{pid}: resuming past {len(prior)} checkpointed runs")
    rows = list(prior)
    for arm in ARMS:
        for rep in range(repeats):
            if (arm, rep) in done:
                continue
            tools = []
            if arm == "menu":
                tools = menu.query(lessons, _features(t))
                if not tools:
                    raise SystemExit(f"{pid}: matched armed run delivered "
                                     f"no tools, the instrument is broken")
            r = runner.run_once(t["task"], CRITERIA, _features(t),
                                model=cell["performer"],
                                audience_model=AUDIENCE[cell["performer"]],
                                landscape=tools or None,
                                evidence_checks=t["checks"])
            row = {"pairing": pid, "performer": cell["performer"],
                   "store": cell["store"], "arm": arm, "task": name,
                   "rep": rep, "run_id": r["run_id"],
                   "verdict": r["verdict"], "tools": len(tools),
                   "tool_concepts": [x["concept"] for x in tools],
                   "ev": ev_fraction(r["evidence"]),
                   "checks": {c["call"]: bool(c["ok"]) for c in
                              (r["evidence"] or {}).get("results") or []}}
            _row(row)
            rows.append(row)
            _p(f"{pid} {arm} rep {rep}: ev={row['ev']:.2f} "
               f"tools={row['tools']}")
    return rows


def pin_regression():
    """The deliberate mismatch cells: the production menu must deliver
    zero tools on every one, no model runs needed."""
    results = []
    for cell in PIN_REGRESSION:
        t = _TASKS[cell["task"]]
        tools = menu.query(load_store(cell["store"]), _features(t))
        results.append({**cell, "tools": len(tools),
                        "passed": len(tools) == 0})
    return results


def check_table(rows):
    table = {}
    for r in rows:
        rule_checks = set(_TASKS[r["task"]].get("rule_checks", []))
        for call, ok in (r.get("checks") or {}).items():
            cell = (table.setdefault(r["pairing"], {})
                    .setdefault(call, {"rule_check": call in rule_checks,
                                       "arms": {}})
                    ["arms"].setdefault(r["arm"], {"n": 0, "passed": 0}))
            cell["n"] += 1
            cell["passed"] += 1 if ok else 0
    for p in table.values():
        for c in p.values():
            for a in c["arms"].values():
                a["rate"] = a["passed"] / a["n"] if a["n"] else 0.0
    return table


def main(repeats=R, resume_ts=None):
    prior_rows = []
    if resume_ts:
        _set_ts(resume_ts)
        prior_rows = _load_rows()
        _p(f"RESUME {_TS}: {len(prior_rows)} checkpointed rows found")
    table = pairing_table()
    cells = cross_seat_pairings(table)
    regression = pin_regression()
    _p(f"CONFIRMATION ARMS {_TS} (PACKET-009)")
    _p(f"lessons={sum(STORE_SIZES.values())}  apply tasks={len(APPLY_TASKS)}")
    _p("== PAIRING TABLE (from the pins) ==")
    for entry in table:
        mark = "  <-- STRUCTURALLY EMPTY" if entry["structurally_empty"] \
            else ""
        _p(f"  {entry['lesson']} pins={entry['pins']} -> "
           f"{entry['matched_tasks'] or 'nothing'}{mark}")
    _p(f"cross-seat armed cells: "
       f"{[(c['performer'], c['task'], c['store']) for c in cells]}")
    _p("== PIN REGRESSION (mismatch cells must deliver zero tools) ==")
    for r in regression:
        _p(f"  store {r['store']} on {r['task']}: tools={r['tools']} "
           f"{'ok' if r['passed'] else 'FAILED'}")

    all_rows = []
    for cell in cells:
        all_rows.extend(run_pairing(cell, repeats, prior_rows))

    checks = check_table(all_rows)
    armed = [r for r in all_rows if r["arm"] == "menu"]
    min_tools = min((r["tools"] for r in armed), default=0)

    report = {
        "confirm_id": _TS, "arms": ARMS, "repeats": repeats,
        "pairing_table": table,
        "cross_seat_cells": [{k: c[k] for k in
                              ("performer", "task", "store", "lessons")}
                             for c in cells],
        "pin_regression": regression, "check_table": checks,
        "min_tools_armed": min_tools,
        "n_note": (f"R={repeats} per arm per task on matched cross-seat "
                   f"cells. The reading rules live in the packet and are "
                   f"applied in its RESULTS, not here."),
    }
    with open(_REPORT, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    _p("== PER-CHECK (none / menu) ==")
    for pid in sorted(checks):
        for call, c in checks[pid].items():
            rates = " / ".join(
                f"{c['arms'].get(a, {}).get('rate', 0.0):.2f}"
                for a in ARMS)
            mark = "  <-- rule" if c["rule_check"] else ""
            _p(f"  {pid} {call}: {rates}{mark}")

    expected = len(cells) * len(ARMS) * repeats
    gate = (len(all_rows) == expected
            and all(r["passed"] for r in regression)
            and (not armed or min_tools > 0)
            and os.path.exists(_ROWS))
    _p(f"GATE: {'PASSED' if gate else 'FAILED'}. pairing table complete "
       f"with empties named, {len(cells)} matched cross-seat cell(s) at "
       f"R={repeats} per arm, pin regression clean "
       f"({sum(1 for r in regression if r['passed'])}/{len(regression)}), "
       f"every run checkpointed, report persisted. The reading is applied "
       f"in the packet RESULTS.")


if __name__ == "__main__":
    main(repeats=int(sys.argv[1]) if len(sys.argv) > 1 else R,
         resume_ts=sys.argv[2] if len(sys.argv) > 2 else None)
