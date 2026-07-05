"""Tests for the PACKET-014 supply probe. Stub runner, temp runs dir,
no model calls. A probe measures supply and structure; these tests pin
the enumeration, the conjunction filter, the standing contrast rules,
and the packet-local store discipline."""

import importlib
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import runner


class _Probe14Harness(unittest.TestCase):

    def setUp(self):
        self._real_runs = runner.RUNS
        self._real_run_once = runner.run_once
        self._tmp = tempfile.TemporaryDirectory()
        runner.RUNS = self._tmp.name
        import probe14
        self.pb = importlib.reload(probe14)
        # the packet-local store never collides with the committed one
        self.pb.STORE = os.path.join(self._tmp.name, "store.jsonl")

    def tearDown(self):
        runner.RUNS = self._real_runs
        runner.run_once = self._real_run_once
        importlib.reload(self.pb)
        self._tmp.cleanup()


class TestEnumeration(_Probe14Harness):

    def test_every_distinctness_task_in_both_pools(self):
        enum = self.pb.enumerate_tasks()
        names = {e["name"] for e in enum}
        self.assertIn("count_distinct_pairs", names)   # gen, pairs
        self.assertIn("mode_count", names)             # gen, values
        self.assertIn("range_summary", names)          # apply target
        self.assertIn("dedupe", names)                 # apply candidate
        gen = [e for e in enum if e["pool"] == "generation"]
        app = [e for e in enum if e["pool"] == "apply"]
        self.assertTrue(all(e["generation_eligible"] for e in gen))
        self.assertTrue(all(not e["generation_eligible"] for e in app))

    def test_conjunction_marks_orphan_topics(self):
        enum = self.pb.enumerate_tasks()
        by_name = {e["name"]: e for e in enum}
        # pairs has no apply-pool carrier, values has range_summary
        self.assertFalse(by_name["count_distinct_pairs"]
                         ["topic_in_apply_pool"])
        self.assertTrue(by_name["mode_count"]["topic_in_apply_pool"])


class TestSupplyAndPairs(_Probe14Harness):

    def _table(self, cases):
        """Build a supply table from fabricated per-task cases."""
        enum = self.pb.enumerate_tasks()
        rows = []
        for e in enum:
            fails, passes = cases.get(e["name"], (0, 6))
            for i in range(fails):
                rows.append({"task": e["name"], "rep": i,
                             "ev_passed": False})
            for i in range(passes):
                rows.append({"task": e["name"], "rep": fails + i,
                             "ev_passed": True})
        return self.pb.supply_table(enum, rows)

    def test_within_task_pair_from_mixed_conjunction_task(self):
        table = self._table({"mode_count": (2, 4)})
        pairs = self.pb.contrast_pairs(table)
        self.assertEqual(len(pairs), 1)
        self.assertEqual(pairs[0]["type"], "within_task")
        self.assertEqual(pairs[0]["fail_task"], "mode_count")

    def test_orphan_topic_never_pairs_even_when_it_breaks(self):
        table = self._table({"count_distinct_pairs": (2, 4)})
        pairs = self.pb.contrast_pairs(table)
        self.assertEqual(pairs, [])

    def test_sibling_pair_for_all_fail_with_passing_partner(self):
        table = self._table({"mode_count": (6, 0)})
        pairs = self.pb.contrast_pairs(table)
        self.assertEqual(len(pairs), 1)
        self.assertEqual(pairs[0]["type"], "sibling")
        self.assertEqual(pairs[0]["fail_task"], "mode_count")
        self.assertNotEqual(pairs[0]["pass_task"], "mode_count")

    def test_apply_pool_breaks_never_become_pairs(self):
        table = self._table({"range_summary": (3, 3),
                             "dedupe": (6, 0)})
        pairs = self.pb.contrast_pairs(table)
        self.assertEqual(pairs, [])

    def test_cap_two_pairs(self):
        table = self._table({"mode_count": (2, 4),
                             "count_unique": (2, 4),
                             "sum_distinct": (2, 4)})
        pairs = self.pb.contrast_pairs(table)
        self.assertEqual(len(pairs), 2)


class TestProbeRuns(_Probe14Harness):

    def test_runs_and_resume(self):
        calls = []

        def stub(task, criteria, work_features, **kw):
            calls.append(task)
            return {"run_id": f"stub-{len(calls)}", "verdict": "pass",
                    "evidence": {"passed": True,
                                 "results": [{"ok": True, "call": "f()",
                                              "got": "1", "expect": "1"}],
                                 "error": None}}

        runner.run_once = stub
        enum = self.pb.enumerate_tasks()
        rows = self.pb.run_probe(enum, repeats=1)
        self.assertEqual(len(rows), len(enum))
        calls.clear()
        rows2 = self.pb.run_probe(enum, repeats=1,
                                  prior_rows=self.pb._load_rows())
        self.assertEqual(calls, [])
        self.assertEqual(len(rows2), len(enum))


if __name__ == "__main__":
    unittest.main()
