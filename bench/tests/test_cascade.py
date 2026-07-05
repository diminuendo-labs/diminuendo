"""Tests for the flag tally and the cascade mechanics. No model calls: the
cascade test injects a stub runner, so the structural claims (each node
released once, flags land, review is read-only, termination) are checked
deterministically."""

import json
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import cascade
import flagtally


class TestFlagTally(unittest.TestCase):

    def test_weight_and_floor(self):
        with tempfile.TemporaryDirectory() as d:
            p = os.path.join(d, "flags.jsonl")
            r = flagtally.raise_flag(p, "c1", "n1", "musician", 2.0, 0.5, 3.0)
            self.assertAlmostEqual(r["weight"], 3.0)
            r2 = flagtally.raise_flag(p, "c1", "n2", "musician", 0.0, 1.0, 1.0)
            self.assertEqual(r2["weight"], flagtally.FLOOR)  # never zero

    def test_aggregation_reads_clean(self):
        with tempfile.TemporaryDirectory() as d:
            p = os.path.join(d, "flags.jsonl")
            flagtally.raise_flag(p, "c1", "n1", "musician", 1, 1, 1)
            flagtally.raise_flag(p, "c1", "n2", "principal", 1, 1, 2)
            t = flagtally.read_tally(p)
            self.assertEqual(t["c1"]["count"], 2)
            self.assertAlmostEqual(t["c1"]["total_weight"], 3.0)
            self.assertEqual(flagtally.read_tally(p + ".missing"), {})


def _stub_run(task, criteria, work_features, evidence_checks=None,
              audience_model=None, flag_path=None, parent_concept=None,
              blast_radius=1.0, mutate_code=None):
    """Mimics run_once's contract: fails when the fault is seeded, and on a
    fail raises exactly one flag, exactly as the run layer does."""
    fails = mutate_code is not None
    node_id = f"task-stub-{task[:12]}"
    if fails and flag_path:
        flagtally.raise_flag(flag_path, parent_concept, node_id, "musician",
                             blast_radius, 1.0, 1.0, note="seeded")
    return {"node_id": node_id,
            "verdict": "fail" if fails else "pass",
            "evidence": {"passed": not fails, "results": [], "error": None}}


def _tasks():
    return [
        {"name": "m_a", "parent_concept": "c", "task": "task alpha work",
         "criteria": ["ok"], "work_features": {"operation": "x"},
         "evidence_checks": [{"call": "f()", "expect": "1"}]},
        {"name": "m_b", "parent_concept": "c", "task": "task beta work",
         "criteria": ["ok"], "work_features": {"operation": "x"},
         "evidence_checks": [{"call": "f()", "expect": "1"}]},
    ]


class TestCascade(unittest.TestCase):

    def setUp(self):
        # tests never write into the real runs/ record
        import runner
        self._runner = runner
        self._real_runs = runner.RUNS
        self._tmp = tempfile.TemporaryDirectory()
        runner.RUNS = self._tmp.name

    def tearDown(self):
        self._runner.RUNS = self._real_runs
        self._tmp.cleanup()

    def test_terminates_and_flags_land(self):
        logs = []
        out = cascade.run_section(_tasks(), seed_fault_in="m_b",
                                  log=logs.append, run_task=_stub_run)
        # each node released exactly once, review included
        self.assertEqual(out["iterations"], out["nodes"])
        self.assertEqual(out["nodes"], 3)
        # exactly one flag: the seeded break, no echo, no amplification
        self.assertEqual(out["flag_count"], 1)
        v = out["review"]["verified"][0]
        self.assertTrue(v["claim_upheld"])
        self.assertTrue(v["evidence_confirms"])
        self.assertFalse(out["review"]["section_pass"])

    def test_clean_section_raises_nothing(self):
        out = cascade.run_section(_tasks(), seed_fault_in=None,
                                  log=lambda *a: None, run_task=_stub_run)
        self.assertEqual(out["flag_count"], 0)
        self.assertTrue(out["review"]["section_pass"])
        self.assertEqual(out["review"]["verified"], [])

    def test_review_is_read_only(self):
        out = cascade.run_section(_tasks(), seed_fault_in="m_b",
                                  log=lambda *a: None, run_task=_stub_run)
        flags = os.path.join(self._runner.RUNS, out["flags_file"])
        with open(flags, encoding="utf-8") as f:
            lines = [l for l in f if l.strip()]
        # the principal's read added nothing: still only the one raised hand
        self.assertEqual(len(lines), 1)

    def test_seeded_fault_is_deterministic(self):
        code = "def add(a, b):\n    return a + b"
        broken = cascade.seeded_fault(code)
        self.assertIn("seeded fault", broken)
        self.assertIn("def add", broken)


if __name__ == "__main__":
    unittest.main()
