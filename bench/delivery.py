"""PACKET-004: the delivery test. Friction theater, measured.

Does a lesson delivered as a menu tool change the performer's output, or
is it merely accepted? Three arms on identical tasks, criteria, and
audience, only the delivery varies: none (the bare production context),
menu (the lessons as landscape tools through the production menu path),
directive (the same lesson text as an explicit APPLY THESE RULES block
in the performer prompt). The lessons are the two correctly aimed
tie_break lessons from probe 20260702-083121, copied into a packet-local
store; the misaimed lesson is excluded by field selection and the loader
enforces that. Performer is llama only, the seat with headroom on this
class. Audience is qwen on the production v1 path, unchanged.

Measurement at two levels: ev_fraction per arm is the coarse level, and
per-check pass rates are the sharp one, because the checks that encode
the stated tie rule are the treatment target. The decision logic is
pre-registered in the packet and gets applied in RESULTS by its reader.
The harness reports, it does not rule.
"""

import json
import os
import sys
import time

import lesson
import menu
import runner
from probe_tasks import APPLY_TASKS, CRITERIA, FEATURES

PERFORMER = "llama3.1:8b"
AUDIENCE = "qwen2.5-coder:7b"
ARMS = ("none", "menu", "directive")
RULE_CLASS = "tie_break"

LESSON_STORE = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            "packets", "PACKET-004-lessons.jsonl")

# The checks that encode each task's stated tie rule, the treatment
# target. Everything else on these tasks measures plain correctness.
TIE_CHECKS = {
    "most_common_word('b a b a c')",  # a and b tie at 2, alphabetical: 'a'
    "longest_word('cat door bird')",  # door and bird tie at 4, last: 'bird'
    "longest_word('a bb cc d')",      # bb and cc tie at 2, last: 'cc'
}

_TS = time.strftime("%Y%m%d-%H%M%S")
_LOG = os.path.join(runner.RUNS, f"delivery-{_TS}.log")
_ROWS = os.path.join(runner.RUNS, f"delivery-{_TS}.rows.jsonl")
_REPORT = os.path.join(runner.RUNS, f"delivery-{_TS}.report.json")


def _set_ts(ts):
    """Rebind the run id and its file paths. Resume reuses a prior id so
    the checkpoint rows, the log, and the report stay one record."""
    global _TS, _LOG, _ROWS, _REPORT
    _TS = ts
    _LOG = os.path.join(runner.RUNS, f"delivery-{_TS}.log")
    _ROWS = os.path.join(runner.RUNS, f"delivery-{_TS}.rows.jsonl")
    _REPORT = os.path.join(runner.RUNS, f"delivery-{_TS}.report.json")


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


def _mean(xs):
    return sum(xs) / len(xs) if xs else 0.0


def tasks():
    """The treatment tasks, selected by field, never by name."""
    return [t for t in APPLY_TASKS if t["rule_class"] == RULE_CLASS]


def _features(t):
    return {**FEATURES, "rule_class": t["rule_class"]}


def load_materials():
    """The packet-local store, validated: exactly two lessons, both from
    the aimed max_index contrasts. The misaimed lesson never rides."""
    lessons = lesson.load(LESSON_STORE)
    if len(lessons) != 2:
        raise SystemExit(f"packet store must hold exactly 2 lessons, "
                         f"found {len(lessons)}")
    for l in lessons:
        lesson.validate(l)
        if l.get("trail", {}).get("gen_task") != "max_index":
            raise SystemExit("misaimed lesson found in packet store")
    return lessons


def directive_lines(lessons):
    """The directive arm's block: concept and rule text verbatim."""
    return [x for l in lessons for x in (l["concept"], str(l["rule"]))]


def run_arm(arm, lessons, repeats, prior_rows=None):
    """One arm across the treatment tasks, repeats passes. Runs already
    checkpointed by an interrupted run are counted, not repeated."""
    prior = [r for r in prior_rows or [] if r.get("arm") == arm]
    done = {(r["task"], r["rep"]) for r in prior}
    if prior:
        _p(f"arm {arm}: resuming past {len(prior)} checkpointed runs")
    rows = list(prior)
    for rep in range(repeats):
        for t in tasks():
            if (t["name"], rep) in done:
                continue
            tools = []
            directives = None
            if arm == "menu":
                tools = menu.query(lessons, _features(t))
                if not tools:
                    raise SystemExit("menu arm delivered no tools, "
                                     "the instrument is broken")
            elif arm == "directive":
                directives = directive_lines(lessons)
            r = runner.run_once(t["task"], CRITERIA, _features(t),
                                model=PERFORMER, audience_model=AUDIENCE,
                                landscape=tools or None,
                                directives=directives,
                                evidence_checks=t["checks"])
            row = {"arm": arm, "task": t["name"], "rep": rep,
                   "run_id": r["run_id"], "verdict": r["verdict"],
                   "tools": len(tools), "directives": len(directives or []),
                   "ev": ev_fraction(r["evidence"]),
                   "checks": {c["call"]: bool(c["ok"]) for c in
                              (r["evidence"] or {}).get("results") or []}}
            _row(row)
            rows.append(row)
            _p(f"arm {arm} rep {rep} ({t['name']}): ev={row['ev']:.2f} "
               f"tools={row['tools']} directives={row['directives']}")
    return rows


def check_table(rows):
    """The sharp level: per task, per evidence check, per arm, the pass
    rate and its n. The tie-rule checks carry the treatment question."""
    table = {}
    for r in rows:
        for call, ok in r["checks"].items():
            cell = (table.setdefault(r["task"], {})
                    .setdefault(call, {"tie_rule": call in TIE_CHECKS,
                                       "arms": {}})
                    ["arms"].setdefault(r["arm"], {"n": 0, "passed": 0}))
            cell["n"] += 1
            cell["passed"] += 1 if ok else 0
    for t in table.values():
        for c in t.values():
            for a in c["arms"].values():
                a["rate"] = a["passed"] / a["n"] if a["n"] else 0.0
    return table


def main(repeats=12, resume_ts=None):
    prior_rows = []
    if resume_ts:
        _set_ts(resume_ts)
        prior_rows = _load_rows()
        _p(f"RESUME {_TS}: {len(prior_rows)} checkpointed rows found")
    lessons = load_materials()
    names = [t["name"] for t in tasks()]
    _p(f"DELIVERY TEST {_TS} (PACKET-004)")
    _p(f"performer={PERFORMER}  audience={AUDIENCE} (v1, production)")
    _p(f"arms={ARMS}  tasks={names}  R={repeats} per arm per task")
    _p(f"lessons: {len(lessons)} aimed tie_break, misaimed excluded by "
       f"loader")

    all_rows = []
    for arm in ARMS:
        all_rows.extend(run_arm(arm, lessons, repeats, prior_rows))

    arms_summary = {}
    for arm in ARMS:
        arm_rows = [r for r in all_rows if r["arm"] == arm]
        arms_summary[arm] = {
            "n": len(arm_rows),
            "ev_mean": _mean([r["ev"] for r in arm_rows]),
            "per_task": {name: _mean([r["ev"] for r in arm_rows
                                      if r["task"] == name])
                         for name in names},
            "min_tools": min([r["tools"] for r in arm_rows], default=0),
        }
    table = check_table(all_rows)

    report = {
        "delivery_id": _TS, "performer": PERFORMER, "audience": AUDIENCE,
        "rule_class": RULE_CLASS, "tasks": names, "repeats": repeats,
        "lessons": [{"concept": l["concept"], "rule": l["rule"],
                     "trail": l["trail"]} for l in lessons],
        "arms": arms_summary, "check_table": table,
        "tie_checks": sorted(TIE_CHECKS),
        "n_note": (f"R={repeats} per arm per task, {len(names)} tasks, "
                   f"three arms. Per-check cells are n={repeats}. "
                   f"Direction at this n, not rates."),
    }
    with open(_REPORT, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    _p("== ARMS (ev_mean, n) ==")
    for arm in ARMS:
        s = arms_summary[arm]
        per_task = "  ".join(f"{k}={v:.2f}" for k, v in s["per_task"].items())
        _p(f"  {arm}: ev={s['ev_mean']:.2f} n={s['n']}  {per_task}")
    _p("== PER-CHECK PASS RATES (none / menu / directive) ==")
    for tname in sorted(table):
        for call in sorted(table[tname]):
            c = table[tname][call]
            rates = " / ".join(
                f"{c['arms'].get(a, {}).get('rate', 0.0):.2f}"
                for a in ARMS)
            mark = "  <-- tie rule" if c["tie_rule"] else ""
            _p(f"  {call}: {rates}{mark}")

    expect = repeats * len(names)
    gate = (all(arms_summary[a]["n"] == expect for a in ARMS)
            and arms_summary["menu"]["min_tools"] > 0
            and os.path.exists(_ROWS) and bool(table))
    _p(f"GATE: {'PASSED' if gate else 'FAILED'}. three arms at "
       f"n={expect} each, every run checkpointed, menu arm delivered "
       f"tools on every run (min={arms_summary['menu']['min_tools']}), "
       f"per-check table persisted. The decision logic is applied in the "
       f"packet RESULTS, not here.")


if __name__ == "__main__":
    main(repeats=int(sys.argv[1]) if len(sys.argv) > 1 else 12,
         resume_ts=sys.argv[2] if len(sys.argv) > 2 else None)
