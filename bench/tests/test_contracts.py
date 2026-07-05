"""Tests for the contracts and the firewall. The one that matters: no metric
key crosses into a performer context, however deeply it is buried."""

import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from contracts import (FirewallError, audience_packet, guard_no_metric,
                       performer_context, validate_performer_output)


class TestFirewall(unittest.TestCase):

    def test_clean_context_passes(self):
        ctx = performer_context(
            task="reverse the words in a sentence",
            criteria=["correct", "concise"],
            landscape=[{"concept": "test edge cases first",
                        "applies_when": "string manipulation"}],
        )
        self.assertEqual(ctx["criteria"], ["correct", "concise"])

    def test_metric_key_blocked_at_top(self):
        with self.assertRaises(FirewallError):
            guard_no_metric({"task": "x", "score": 9})

    def test_metric_key_blocked_when_buried(self):
        landscape = [{"concept": "be careful",
                      "history": {"runs": [{"tokens": 512}]}}]
        with self.assertRaises(FirewallError):
            performer_context("t", ["c"], landscape)

    def test_case_variants_blocked(self):
        with self.assertRaises(FirewallError):
            guard_no_metric({"Tokens": 100})
        with self.assertRaises(FirewallError):
            guard_no_metric([{"nested": {"RAW_SCORE": 1}}])

    def test_performer_output_contract(self):
        good = {"output": "def f(): pass", "tools_chosen": ["direct"],
                "work_features": {"operation": "write"}, "trace": "did x then y"}
        validate_performer_output(good)
        with self.assertRaises(ValueError):
            validate_performer_output({"output": "only this"})

    def test_audience_packet_shape(self):
        pkt = audience_packet("t", ["c1"], "the artifact")
        self.assertEqual(sorted(pkt), ["criteria", "output", "task"])
        # the audience packet carries no performer trace and no chair memory
        self.assertNotIn("trace", pkt)
        self.assertNotIn("landscape", pkt)


if __name__ == "__main__":
    unittest.main()
