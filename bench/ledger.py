"""The Scoring Ledger. Tech Spec Section 4.

Two axes, time and tokens, recorded separately for every node and never combined
into one number. A clean run posts positive. A caught problem posts the cost of
the failure plus its correction as a minus, then a catch bonus as a plus, so
catching stays net-rational instead of hidden.

The ledger IS the metric. It lives on the audience side of the firewall. Nothing
here may be handed to a performer context, and contracts.py enforces that.
"""

import json
import time as _time

# category -> sign. The magnitudes are always recorded positive, the sign is
# the category's, so an entry can never lie about its direction.
CATEGORIES = {
    "clean": 1,
    "failure": -1,
    "correction": -1,
    "catch_bonus": 1,
}


class Ledger:
    def __init__(self, path=None):
        """path: optional JSONL file. Every post appends a line if set."""
        self._entries = []
        self._path = path

    def post(self, node_id, category, time_s, tokens, note=""):
        """Record one signed entry. Magnitudes must be non-negative."""
        if category not in CATEGORIES:
            raise ValueError(f"unknown ledger category: {category}")
        if time_s < 0 or tokens < 0:
            raise ValueError("magnitudes are recorded positive, sign is the category's")
        sign = CATEGORIES[category]
        entry = {
            "ts": _time.time(),
            "node_id": node_id,
            "category": category,
            "time_s": sign * float(time_s),
            "tokens": sign * int(tokens),
            "note": note,
        }
        self._entries.append(entry)
        if self._path:
            with open(self._path, "a", encoding="utf-8") as f:
                f.write(json.dumps(entry) + "\n")
        return entry

    def post_catch(self, node_id, fail_time_s, fail_tokens,
                   fix_time_s, fix_tokens, bonus_time_s, bonus_tokens, note=""):
        """The catch sequence in one call: failure, correction, bonus.
        The bonus number is unknown and gameable per the spec, so it is a
        caller-supplied parameter, never a hidden constant."""
        self.post(node_id, "failure", fail_time_s, fail_tokens, note)
        self.post(node_id, "correction", fix_time_s, fix_tokens, note)
        self.post(node_id, "catch_bonus", bonus_time_s, bonus_tokens, note)

    def totals(self):
        """Two axes, two numbers, never one. There is deliberately no method
        that blends time and tokens."""
        return {
            "time_s": sum(e["time_s"] for e in self._entries),
            "tokens": sum(e["tokens"] for e in self._entries),
        }

    def node_totals(self, node_id):
        rows = [e for e in self._entries if e["node_id"] == node_id]
        return {
            "time_s": sum(e["time_s"] for e in rows),
            "tokens": sum(e["tokens"] for e in rows),
        }

    def entries(self):
        return list(self._entries)

    @classmethod
    def load(cls, path):
        led = cls(path=None)
        with open(path, encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    led._entries.append(json.loads(line))
        led._path = path
        return led
