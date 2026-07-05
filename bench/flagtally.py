"""The Flagging Tally: its own system, every level feeds it. Spec Section 10.

A break raises a flag, a flag is a raised hand, not a bell. It appends to a
per-concept tally the upper level watches on its own cadence. It never
initiates a pull, never forces anything. Weight is blast radius times
credibility times surprise, floored above zero so the slow flood inside a
baseline can never discount itself to silence. The flag is a claim, never a
verdict: the reader re-judges against the record before believing it.
"""

import json
import time as _time

FLOOR = 0.01


def raise_flag(path, concept, node_id, level, blast_radius, credibility,
               surprise, note=""):
    weight = max(float(blast_radius) * float(credibility) * float(surprise),
                 FLOOR)
    row = {"ts": _time.time(), "concept": concept, "node_id": node_id,
           "level": level, "blast_radius": blast_radius,
           "credibility": credibility, "surprise": surprise,
           "weight": weight, "note": note}
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(row) + "\n")
    return row


def read_tally(path):
    """Per-concept aggregation. Reading is read-only and side-effect free."""
    tally = {}
    try:
        with open(path, encoding="utf-8") as f:
            rows = [json.loads(l) for l in f if l.strip()]
    except FileNotFoundError:
        return {}
    for r in rows:
        agg = tally.setdefault(r["concept"],
                               {"total_weight": 0.0, "count": 0, "nodes": []})
        agg["total_weight"] += r["weight"]
        agg["count"] += 1
        agg["nodes"].append(r["node_id"])
    return tally
