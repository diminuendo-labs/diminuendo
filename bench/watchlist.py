"""The Audience Watchlist: criteria the audience learned from its own misses.

The catch-better half of the two coupled loops (Spec Section 5). When
hindsight finds a break the audience passed and a slower detector caught, the
miss becomes a watch item: an instruction about WHAT TO VERIFY in outputs of
that kind, so the same class of break is caught live next time. This is the
loop that lowers the detection floor.

Watch items live on the audience side of the firewall. The performer never
sees them. They must stay criteria-shaped, what to check, never how to solve,
and never metric-shaped, enforced by the same gates the lesson engine uses.
"""

import json
import re
import time as _time

import menu
from lesson import _METRIC_TERMS

REQUIRED = ("watch", "applies_when", "confidence", "provenance", "source_node")


class WatchError(Exception):
    """The candidate watch item breaks a rule and is not committed."""


def validate(item):
    missing = [k for k in REQUIRED if k not in item]
    if missing:
        raise WatchError(f"watch item missing fields: {missing}")
    if item["provenance"] not in ("engine", "hand"):
        raise WatchError(f"unknown provenance: {item['provenance']}")
    if not isinstance(item["applies_when"], dict) or not item["applies_when"]:
        raise WatchError("applies_when must be a non-empty dict")
    if not (0.0 <= float(item["confidence"]) <= 1.0):
        raise WatchError("confidence must be in [0, 1]")
    text = item["watch"] + " " + json.dumps(item["applies_when"])
    hit = _METRIC_TERMS.search(text)
    if hit:
        raise WatchError(f"metric-shaped term in watch item: '{hit.group(0)}'")
    return item


def commit(path, item):
    validate(item)
    row = dict(item)
    row["ts"] = _time.time()
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(row) + "\n")
    return row


def load(path):
    out = []
    try:
        with open(path, encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    out.append(json.loads(line))
    except FileNotFoundError:
        pass
    return out


def query(items, work_features, limit=5):
    """Watch items whose conditions match the task, confidence-sorted.
    Returns the watch text only: instructions for the evaluator's eye."""
    scored = []
    for it in items:
        s = menu.matches(it["applies_when"], work_features)
        if s >= 1:
            scored.append((s, float(it["confidence"]), it))
    scored.sort(key=lambda t: (-t[0], -t[1]))
    return [it["watch"] for _, _, it in scored[:limit]]


def taught_nodes(items):
    return {it["source_node"] for it in items}
