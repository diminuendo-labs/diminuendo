"""Tests for judge calibration: corpus selection and rate math. Pure logic,
no model calls."""

import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from judgecal import rates, select_corpus
from runner import _audience_prompt


def _s(node, passed, mutated=False):
    return {"node_id": node, "task": "t", "output": "def f(): pass",
            "code_mutated": mutated,
            "evidence": {"passed": passed, "results": []}}


class TestCorpus(unittest.TestCase):

    def test_selection_rules(self):
        summaries = [
            _s("n1", True), _s("n2", False), _s("n3", True, mutated=True),
            _s("n1", True),                         # duplicate node
            {"node_id": "n4", "task": "t", "output": "x",
             "code_mutated": False, "evidence": {"passed": None}},
            {"node_id": "n5", "output": "x", "code_mutated": False,
             "evidence": {"passed": True}},         # predates the task field
        ]
        corpus = select_corpus(summaries)
        ids = [s["node_id"] for s in corpus]
        self.assertEqual(sorted(ids), ["n1", "n2"])

    def test_caps(self):
        summaries = ([_s(f"b{i}", False) for i in range(10)]
                     + [_s(f"c{i}", True) for i in range(10)])
        corpus = select_corpus(summaries, max_broken=3, max_clean=2)
        self.assertEqual(len(corpus), 5)


class TestRates(unittest.TestCase):

    def test_rate_math_and_unscorable_exclusion(self):
        rows = [
            {"truth_clean": True, "verdict": "pass"},
            {"truth_clean": True, "verdict": "fail"},     # false alarm
            {"truth_clean": False, "verdict": "pass"},    # miss
            {"truth_clean": False, "verdict": "fail"},
            {"truth_clean": True, "verdict": "unscorable"},
        ]
        r = rates(rows)
        self.assertEqual(r["false_alarm_rate"], 0.5)
        self.assertEqual(r["miss_rate"], 0.5)
        self.assertEqual(r["clean_n"], 2)
        self.assertEqual(r["unscorable"], 1)

    def test_empty_class_yields_none(self):
        r = rates([{"truth_clean": True, "verdict": "pass"}])
        self.assertIsNone(r["miss_rate"])


class TestProtocolRouting(unittest.TestCase):

    def test_v2_contains_substantiation_rules(self):
        pkt = {"task": "t", "criteria": ["c"], "output": "o"}
        v1 = _audience_prompt(pkt, [], protocol="v1")
        v2 = _audience_prompt(pkt, [], protocol="v2")
        self.assertIn("JUDGING PROTOCOL", v2)
        self.assertIn("trace the code", v2)
        self.assertIn("Uncertainty is never", v2)
        self.assertNotIn("JUDGING PROTOCOL", v1)

    def test_v2_keeps_watches(self):
        pkt = {"task": "t", "criteria": ["c"], "output": "o"}
        v2 = _audience_prompt(pkt, ["watch this"], protocol="v2")
        self.assertIn("WATCH-ITEMS", v2)
        self.assertIn("watch this", v2)


if __name__ == "__main__":
    unittest.main()
