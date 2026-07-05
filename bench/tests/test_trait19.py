"""Tests for the PACKET-019 staged qualified trait harness. Stub runner,
temp runs dir, no model calls."""

import importlib
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import probe_tasks
import runner


class _Trait19Harness(unittest.TestCase):

    def setUp(self):
        self._real_runs = runner.RUNS
        self._real_run_once = runner.run_once
        self._tmp = tempfile.TemporaryDirectory()
        runner.RUNS = self._tmp.name
        import trait19
        self.tr = importlib.reload(trait19)

    def tearDown(self):
        runner.RUNS = self._real_runs
        runner.run_once = self._real_run_once
        importlib.reload(self.tr)
        self._tmp.cleanup()

    def _stub_run(self, rule_ok_fn):
        """Stub whose rule-check outcomes follow rule_ok_fn(task, rep_i);
        non-rule checks always pass."""
        calls = []

        def stub(task, criteria, work_features, **kw):
            name = next(n for n in self.tr._TASKS
                        if self.tr._TASKS[n]["task"] == task)
            seen = sum(1 for c in calls if c["name"] == name)
            calls.append({"name": name, "kw": kw})
            rule_checks = set(self.tr._TASKS[name].get("rule_checks", []))
            results = []
            for c in self.tr._TASKS[name]["checks"]:
                ok = (rule_ok_fn(name, seen) if c["call"] in rule_checks
                      else True)
                results.append({"ok": ok, "call": c["call"],
                                "got": "x", "expect": c["expect"]})
            return {"run_id": f"stub-{len(calls)}", "verdict": "pass",
                    "evidence": {"passed": all(r["ok"] for r in results),
                                 "results": results, "error": None}}

        runner.run_once = stub
        return calls


class TestAnnotations(_Trait19Harness):

    def test_candidates_carry_two_rule_checks(self):
        """PACKET-019 tier 1: the standing annotation now covers the
        stage A candidates, checks that encode each task's stated rule."""
        for name in self.tr.CANDIDATES:
            t = self.tr._TASKS[name]
            calls = {c["call"] for c in t["checks"]}
            self.assertEqual(len(t["rule_checks"]), 2, name)
            self.assertTrue(set(t["rule_checks"]) <= calls, name)

    def test_byte_check_and_armed_lesson_matches_grounds(self):
        import menu
        self.assertTrue(self.tr.byte_check())
        armed = self.tr.load_armed()
        for name in self.tr.CANDIDATES:
            t = self.tr._TASKS[name]
            tools = menu.query(armed, self.tr._features(t))
            self.assertEqual(len(tools), 1, name)


class TestStageA(_Trait19Harness):

    def test_mixed_ground_qualifies_and_stops_the_sweep(self):
        # second_largest: 6 rule passes, 6 rule fails per check -> mixed
        self._stub_run(lambda name, rep: rep % 2 == 0)
        result = self.tr.qualify("second_largest", repeats=12)
        self.assertTrue(result["qualified"])
        self.assertEqual(result["pooled"]["n"], 24)
        self.assertEqual(result["pooled"]["passed"], 12)

    def test_floor_ground_does_not_qualify(self):
        self._stub_run(lambda name, rep: False)
        result = self.tr.qualify("second_largest", repeats=12)
        self.assertFalse(result["qualified"])
        self.assertEqual(result["pooled"]["passed"], 0)

    def test_ceiling_ground_does_not_qualify(self):
        self._stub_run(lambda name, rep: True)
        result = self.tr.qualify("second_largest", repeats=12)
        self.assertFalse(result["qualified"])

    def test_boundary_arithmetic_exactly_four(self):
        # exactly 4 passes and 20 fails qualifies by the letter
        self._stub_run(lambda name, rep: rep < 2)  # 2 reps x 2 checks = 4
        result = self.tr.qualify("second_largest", repeats=12)
        self.assertEqual(result["pooled"]["passed"], 4)
        self.assertTrue(result["qualified"])


class TestStageB(_Trait19Harness):

    def test_fresh_interleaved_cells_and_audit(self):
        calls = self._stub_run(lambda name, rep: rep % 2 == 0)
        rows = self.tr.run_stage_b("second_largest", repeats=2)
        self.assertEqual([(r["cell"]) for r in rows],
                         ["none", "armed", "none", "armed"])
        self.assertTrue(all(
            r["tools"] == (1 if r["cell"] == "armed" else 0)
            for r in rows))
        armed_calls = [c for c in calls
                       if c["kw"].get("landscape") is not None]
        self.assertEqual(len(armed_calls), 2)

    def test_resume_separates_stages(self):
        self._stub_run(lambda name, rep: True)
        self.tr.qualify("second_largest", repeats=2)
        self.tr.run_stage_b("second_largest", repeats=2)
        prior = self.tr._load_rows()
        calls = self._stub_run(lambda name, rep: True)
        # both stages resume from their own rows, nothing re-runs
        r1 = self.tr.qualify("second_largest", repeats=2,
                             prior_rows=prior)
        r2 = self.tr.run_stage_b("second_largest", repeats=2,
                                 prior_rows=prior)
        self.assertEqual(calls, [])
        self.assertEqual(r1["pooled"]["n"], 4)
        self.assertEqual(len(r2), 4)


if __name__ == "__main__":
    unittest.main()
