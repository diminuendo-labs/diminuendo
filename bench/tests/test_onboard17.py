"""Tests for the PACKET-017 onboarding harness. Stub runner, temp runs
dir, no model calls, no ollama calls."""

import importlib
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import probe_tasks
import runner


class _OnboardHarness(unittest.TestCase):

    def setUp(self):
        self._real_runs = runner.RUNS
        self._real_run_once = runner.run_once
        self._tmp = tempfile.TemporaryDirectory()
        runner.RUNS = self._tmp.name
        import onboard17
        self.ob = importlib.reload(onboard17)

    def tearDown(self):
        runner.RUNS = self._real_runs
        runner.run_once = self._real_run_once
        importlib.reload(self.ob)
        self._tmp.cleanup()

    def _stub_run(self, fail_map=None):
        calls = []
        fail_map = fail_map or {}

        def stub(task, criteria, work_features, **kw):
            name = next((n for n in self.ob._ALL
                         if self.ob._ALL[n]["task"] == task), None)
            seen = sum(1 for c in calls if c["name"] == name)
            fails = fail_map.get(name, 0)
            ok = seen >= fails
            calls.append({"name": name, "kw": kw})
            return {"run_id": f"stub-{len(calls)}", "verdict": "pass",
                    "evidence": {"passed": ok,
                                 "results": [{"ok": ok, "call": "f(1)",
                                              "got": "1", "expect": "1"}],
                                 "error": None}}

        runner.run_once = stub
        return calls


class TestMaterials(_OnboardHarness):

    def test_byte_check_and_armed_lesson(self):
        self.assertTrue(self.ob.byte_check())
        armed = self.ob.load_armed()
        self.assertEqual(len(armed), 1)
        self.assertEqual(armed[0]["trail"]["gen_task"], "sum_distinct")
        self.assertEqual(armed[0]["applies_when"]["rule_topic"], "values")

    def test_baseline_covers_both_pools(self):
        enum = self.ob.baseline_tasks()
        self.assertEqual(len(enum),
                         len(probe_tasks.CANDIDATE_GEN_TASKS)
                         + len(probe_tasks.CANDIDATE_APPLY_TASKS))
        pools = {e["pool"] for e in enum}
        self.assertEqual(pools, {"generation", "apply"})


class TestSupplyAndPairs(_OnboardHarness):

    def _table(self, fail_map):
        enum = self.ob.baseline_tasks()
        rows = []
        for e in enum:
            fails = fail_map.get(e["name"], 0)
            for i in range(6):
                rows.append({"task": e["name"], "rep": i,
                             "ev_passed": i >= fails})
        return self.ob.supply_table(rows)

    def test_headroom_and_conjunction_marks(self):
        table = self._table({"mode_count": 2, "range_summary": 1,
                             "count_distinct_pairs": 3})
        by = {e["name"]: e for e in table}
        self.assertTrue(by["mode_count"]["conjunction_eligible"])
        self.assertTrue(by["range_summary"]["headroom"])
        self.assertFalse(by["range_summary"]["conjunction_eligible"])
        self.assertFalse(by["count_distinct_pairs"]
                         ["conjunction_eligible"])  # orphan topic

    def test_pairs_within_task_first_and_cap(self):
        table = self._table({"mode_count": 2, "sum_distinct": 2,
                             "count_unique": 2})
        pairs = self.ob.contrast_pairs(table)
        dist = [p for p in pairs if p["rule_class"] == "distinctness"]
        self.assertEqual(len(dist), 2)  # the per-class cap
        self.assertTrue(all(p["type"] == "within_task" for p in dist))

    def test_sibling_pair_for_all_fail(self):
        table = self._table({"max_index": 6})
        pairs = self.ob.contrast_pairs(table)
        tie = [p for p in pairs if p["rule_class"] == "tie_break"]
        self.assertEqual(len(tie), 1)
        self.assertEqual(tie[0]["type"], "sibling")
        self.assertEqual(tie[0]["fail_task"], "max_index")


class TestStages(_OnboardHarness):

    def test_stage1_runs_and_resumes(self):
        calls = self._stub_run()
        rows = self.ob.run_stage1(repeats=1)
        self.assertEqual(len(rows), len(self.ob.baseline_tasks()))
        calls.clear()
        rows2 = self.ob.run_stage1(repeats=1,
                                   prior_rows=self.ob._load_rows())
        self.assertEqual(calls, [])
        self.assertEqual(len(rows2), len(self.ob.baseline_tasks()))

    def test_stage2_interleaves_and_audits_tools(self):
        calls = self._stub_run()
        rows = self.ob.run_stage2(repeats=2)
        self.assertEqual([r["cell"] for r in rows],
                         ["none", "armed"] * 2)
        self.assertTrue(all(
            r["tools"] == (1 if r["cell"] == "armed" else 0)
            for r in rows))
        armed_calls = [c for c in calls
                       if c["kw"].get("landscape") is not None]
        self.assertEqual(len(armed_calls), 2)


if __name__ == "__main__":
    unittest.main()
