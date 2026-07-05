"""PACKET-010, work item 1: the demand table, the shopping list.

Enumerates every (rule_class, rule_topic) pair present in the apply pool,
and per pair, which seats have rule-check headroom, computed from the
unarmed rule-check record already committed in runs/: the PACKET-005
probe's none cells (n=3 per check per seat), the PACKET-007 obedience
none arms (qwen, n=24), and the PACKET-009 confirm none arm (llama,
n=12). A seat has headroom on a pair when any unarmed observation of any
rule check on any task in the pair sits below 1.0. No model calls; this
harness reads the record and reports."""

import json
import os
import time

import runner
from probe_tasks import APPLY_TASKS

SOURCES = {
    "probe-20260702-215407": {"kind": "probe",
                              "cells": {"A|none": "qwen", "B|none": "llama"}},
    "obedience-20260703-043045": {"kind": "arms", "performer": "qwen",
                                  "arm": "none"},
    "confirm-20260703-064149": {"kind": "arms", "performer": "llama",
                                "arm": "none"},
}

_TS = time.strftime("%Y%m%d-%H%M%S")
_REPORT = os.path.join(runner.RUNS, f"demand-{_TS}.report.json")


def _load(name):
    with open(os.path.join(runner.RUNS, f"{name}.report.json"),
              encoding="utf-8") as f:
        return json.load(f)


def observations():
    """Unarmed rule-check observations from the record:
    (task, check, seat) -> list of {rate, n, source}."""
    obs = {}
    rule_checks = {t["name"]: set(t.get("rule_checks", []))
                   for t in APPLY_TASKS}

    def add(task, call, seat, arms, source):
        if call not in rule_checks.get(task, set()):
            return
        obs.setdefault((task, call, seat), []).append(
            {"rate": arms["rate"], "n": arms["n"], "source": source})

    probe = _load("probe-20260702-215407")
    for task, checks in probe["check_table"].items():
        for call, c in checks.items():
            for cell, seat in SOURCES["probe-20260702-215407"]["cells"].items():
                if cell in c["cells"]:
                    add(task, call, seat, c["cells"][cell],
                        "probe-20260702-215407")

    ob = _load("obedience-20260703-043045")
    for task, checks in ob["check_table"].items():
        for call, c in checks.items():
            if "none" in c["arms"]:
                add(task, call, "qwen", c["arms"]["none"],
                    "obedience-20260703-043045")

    cf = _load("confirm-20260703-064149")
    for pairing, checks in cf["check_table"].items():
        task = pairing.split("|")[1]
        for call, c in checks.items():
            if "none" in c["arms"]:
                add(task, call, "llama", c["arms"]["none"],
                    "confirm-20260703-064149")
    return obs


def demand_table():
    obs = observations()
    pairs = {}
    for t in APPLY_TASKS:
        key = (t["rule_class"], t["rule_topic"])
        pairs.setdefault(key, {"rule_class": t["rule_class"],
                               "rule_topic": t["rule_topic"],
                               "tasks": [], "seats": {}})
        pairs[key]["tasks"].append(t["name"])
    for key, pair in pairs.items():
        for seat in ("qwen", "llama"):
            seen = []
            for t in pair["tasks"]:
                for (task, call, s), rows in obs.items():
                    if task == t and s == seat:
                        for r in rows:
                            seen.append({"task": task, "check": call, **r})
            below = [r for r in seen if r["rate"] < 1.0]
            pair["seats"][seat] = {
                "headroom": bool(below),
                "observations": seen,
                "evidence": (min(below, key=lambda r: r["rate"])
                             if below else None)}
    return sorted(pairs.values(),
                  key=lambda p: (p["rule_class"], p["rule_topic"]))


def main():
    table = demand_table()
    report = {"demand_id": _TS,
              "sources": sorted(SOURCES),
              "pairs": table,
              "n_note": ("Headroom is read from unarmed rule-check "
                         "observations in the committed record; the probe "
                         "cells are n=3 and direction only, the arms "
                         "baselines are n=12 to 24.")}
    os.makedirs(runner.RUNS, exist_ok=True)
    with open(_REPORT, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)
    print(f"DEMAND TABLE {_TS} (the shopping list)")
    for p in table:
        seats = "  ".join(
            f"{s}={'HEADROOM' if p['seats'][s]['headroom'] else 'ceiling'}"
            + (f" (min {p['seats'][s]['evidence']['rate']:.2f}"
               f" n={p['seats'][s]['evidence']['n']}"
               f" {p['seats'][s]['evidence']['task']})"
               if p['seats'][s]['evidence'] else "")
            for s in ("qwen", "llama"))
        print(f"  ({p['rule_class']}, {p['rule_topic']}) "
              f"tasks={p['tasks']}: {seats}")
    print(f"report: {os.path.basename(_REPORT)}")


if __name__ == "__main__":
    main()
