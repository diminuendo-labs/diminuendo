"""PACKET-010, work item 5: the before-and-after enumeration.

Runs the PACKET-009 pairing enumeration (confirm.matched, the pins alone)
against the 053623 stores by themselves (before) and against 053623 plus
the PACKET-010 genpass stores (after). Reports matched cross-seat
pairings, the structural-empty rate both sides, and whether a
reverse-direction cell now exists: a llama-origin lesson matched to an
apply task where qwen has headroom per the demand table. No model calls;
this reads stores and the record."""

import json
import os
import time

import lesson
import runner
from confirm import matched
from probe_tasks import APPLY_TASKS

BEFORE = {"A": "genpass-20260703-053623-lessons_A.jsonl",
          "B": "genpass-20260703-053623-lessons_B.jsonl"}
NEW = {"A": "genpass-20260703-081801-lessons_A.jsonl",
       "B": "genpass-20260703-081801-lessons_B.jsonl"}
DEMAND = "demand-20260703-071812.report.json"

_TS = time.strftime("%Y%m%d-%H%M%S")
_REPORT = os.path.join(runner.RUNS, f"coverage-{_TS}.report.json")


def _load_lessons(files):
    out = []
    for seat, name in files.items():
        for l in lesson.load(os.path.join(runner.RUNS, name)):
            trail = l.get("trail", {})
            out.append({"seat": seat, "store": name,
                        "id": f"{seat}/{trail.get('gen_task')}/"
                              f"{trail.get('contrast_type')}",
                        "lesson": l})
    return out


def _qwen_headroom_tasks():
    with open(os.path.join(runner.RUNS, DEMAND), encoding="utf-8") as f:
        demand = json.load(f)
    tasks = set()
    for pair in demand["pairs"]:
        if pair["seats"]["qwen"]["headroom"]:
            tasks.update(pair["tasks"])
    return tasks


def enumerate_stores(entries):
    table = []
    for e in entries:
        hits = [t["name"] for t in APPLY_TASKS if matched(e["lesson"], t)]
        table.append({"lesson": e["id"], "seat": e["seat"],
                      "store": e["store"],
                      "pins": {k: e["lesson"]["applies_when"].get(k) for k
                               in ("rule_class", "rule_topic",
                                   "stated_direction")},
                      "matched_tasks": hits,
                      "structurally_empty": not hits})
    return table


def summarize(table, qwen_headroom):
    empties = [e["lesson"] for e in table if e["structurally_empty"]]
    cross = {}
    reverse = []
    for e in table:
        performer = "llama" if e["seat"] == "A" else "qwen"
        for name in e["matched_tasks"]:
            cross.setdefault((performer, name), []).append(e["lesson"])
            if e["seat"] == "B" and name in qwen_headroom:
                reverse.append({"lesson": e["lesson"], "task": name})
    return {"lessons": len(table), "empties": empties,
            "empty_rate": (f"{len(empties)}/{len(table)}"),
            "cross_seat_cells": [
                {"performer": p, "task": t, "lessons": ls}
                for (p, t), ls in sorted(cross.items())],
            "reverse_direction_cells": reverse}


def main():
    qwen_headroom = _qwen_headroom_tasks()
    before_entries = _load_lessons(BEFORE)
    after_entries = before_entries + _load_lessons(NEW)
    before_table = enumerate_stores(before_entries)
    after_table = enumerate_stores(after_entries)
    report = {
        "coverage_id": _TS, "demand_source": DEMAND,
        "qwen_headroom_tasks": sorted(qwen_headroom),
        "before": {"stores": sorted(BEFORE.values()),
                   "table": before_table,
                   "summary": summarize(before_table, qwen_headroom)},
        "after": {"stores": sorted(BEFORE.values()) + sorted(NEW.values()),
                  "table": after_table,
                  "summary": summarize(after_table, qwen_headroom)},
    }
    os.makedirs(runner.RUNS, exist_ok=True)
    with open(_REPORT, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)
    for label in ("before", "after"):
        s = report[label]["summary"]
        print(f"== {label.upper()} ==")
        print(f"  lessons={s['lessons']}  empty={s['empty_rate']}  "
              f"empties={s['empties']}")
        for c in s["cross_seat_cells"]:
            print(f"  cross-seat: {c['performer']} on {c['task']} "
                  f"<- {c['lessons']}")
        print(f"  reverse-direction cells: "
              f"{s['reverse_direction_cells'] or 'none'}")
    print(f"report: {os.path.basename(_REPORT)}")


if __name__ == "__main__":
    main()
