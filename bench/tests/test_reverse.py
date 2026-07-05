"""Tests for the PACKET-011 reverse-cell harness. Stub runner, temp runs
dir, no model calls."""

import importlib
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import menu
import runner


class _ReverseHarness(unittest.TestCase):

    def setUp(self):
        self._real_runs = runner.RUNS
        self._real_run_once = runner.run_once
        self._tmp = tempfile.TemporaryDirectory()
        runner.RUNS = self._tmp.name
        import reverse
        self.rv = importlib.reload(reverse)

    def tearDown(self):
        runner.RUNS = self._real_runs
        runner.run_once = self._real_run_once
        importlib.reload(self.rv)
        self._tmp.cleanup()

    def _stub_run(self):
        calls = []

        def stub(task, criteria, work_features, **kw):
            calls.append({"task": task, "kw": kw})
            return {"run_id": f"stub-{len(calls)}", "verdict": "pass",
                    "evidence": {"passed": True,
                                 "results": [{"ok": True, "call": "f(1)",
                                              "got": "1", "expect": "1"}],
                                 "error": None}}

        runner.run_once = stub
        return calls


class TestReverseCell(_ReverseHarness):

    def test_store_is_the_two_llama_origin_lessons(self):
        lessons = self.rv.load_store()
        self.assertEqual(len(lessons), 2)
        for l in lessons:
            aw = l["applies_when"]
            self.assertEqual(aw["rule_class"], "tie_break")
            self.assertEqual(aw["rule_topic"], "direction")
            self.assertEqual(aw["stated_direction"], "last")
        kinds = {l["trail"]["contrast_type"] for l in lessons}
        self.assertEqual(kinds, {"within_task", "sibling"})

    def test_both_lessons_ride_longest_word(self):
        t = self.rv._TASKS[self.rv.TASK]
        tools = menu.query(self.rv.load_store(), self.rv._features(t))
        self.assertEqual(len(tools), 2)

    def test_arms_and_resume(self):
        calls = self._stub_run()
        rows = self.rv.run_arms(repeats=2)
        self.assertEqual(len(rows), 4)
        armed = [r for r in rows if r["arm"] == "menu"]
        self.assertTrue(all(r["tools"] == 2 for r in armed))
        bare = [c for c in calls if c["kw"].get("landscape") is None]
        self.assertEqual(len(bare), 2)
        calls.clear()
        rows2 = self.rv.run_arms(repeats=2,
                                 prior_rows=self.rv._load_rows())
        self.assertEqual(calls, [])
        self.assertEqual(len(rows2), 4)

    def test_tables(self):
        rows = [
            {"arm": "none", "task": "longest_word",
             "checks": {"longest_word('cat door bird')": False,
                        "longest_word('')": True}},
            {"arm": "menu", "task": "longest_word",
             "checks": {"longest_word('cat door bird')": True,
                        "longest_word('')": True}},
        ]
        table = self.rv.check_table(rows)
        rule = table["longest_word('cat door bird')"]
        self.assertTrue(rule["rule_check"])
        self.assertAlmostEqual(rule["arms"]["none"]["rate"], 0.0)
        self.assertAlmostEqual(rule["arms"]["menu"]["rate"], 1.0)
        self.assertFalse(table["longest_word('')"]["rule_check"])
        pooled = self.rv.pooled_rule_checks(rows)
        self.assertEqual(pooled["none"], {"n": 1, "passed": 0, "rate": 0.0})
        self.assertEqual(pooled["menu"], {"n": 1, "passed": 1, "rate": 1.0})


if __name__ == "__main__":
    unittest.main()
