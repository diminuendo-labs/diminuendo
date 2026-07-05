"""Tests for the PACKET-004 delivery harness and the runner's directive
path. Stub runner, temp runs dir, no model calls. The packet-local lesson
store is committed material and is read as-is; mutations of it are tested
against temp copies only."""

import importlib
import json
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import runner
from contracts import performer_context


class TestDirectivePrompt(unittest.TestCase):

    def test_block_present_and_verbatim(self):
        ctx = performer_context("do the task", ["correct"], None)
        prompt = runner._performer_prompt(ctx, ["rule one", "rule two"])
        self.assertIn("APPLY THESE RULES:", prompt)
        self.assertIn("- rule one", prompt)
        self.assertIn("- rule two", prompt)

    def test_no_block_without_directives(self):
        ctx = performer_context("do the task", ["correct"], None)
        self.assertNotIn("APPLY THESE RULES:", runner._performer_prompt(ctx))


class _DeliveryHarness(unittest.TestCase):

    def setUp(self):
        self._real_runs = runner.RUNS
        self._real_run_once = runner.run_once
        self._tmp = tempfile.TemporaryDirectory()
        runner.RUNS = self._tmp.name
        import delivery
        self.delivery = importlib.reload(delivery)

    def tearDown(self):
        runner.RUNS = self._real_runs
        runner.run_once = self._real_run_once
        importlib.reload(self.delivery)
        self._tmp.cleanup()

    def _stub_run(self, ok=True):
        calls = []

        def stub(task, criteria, work_features, **kw):
            calls.append({"task": task, "kw": kw})
            return {"run_id": f"stub-{len(calls)}", "verdict": "pass",
                    "evidence": {"passed": ok,
                                 "results": [{"ok": ok, "call": "f(1)",
                                              "got": "1", "expect": "1"}],
                                 "error": None}}

        runner.run_once = stub
        return calls


class TestDeliveryArms(_DeliveryHarness):

    def test_materials_are_two_aimed_lessons(self):
        lessons = self.delivery.load_materials()
        self.assertEqual(len(lessons), 2)
        for l in lessons:
            self.assertEqual(l["trail"]["gen_task"], "max_index")
            self.assertEqual(l["applies_when"]["rule_class"], "tie_break")

    def test_misaimed_store_refused(self):
        bad = os.path.join(self._tmp.name, "bad.jsonl")
        lessons = self.delivery.load_materials()
        rogue = dict(lessons[0])
        rogue["trail"] = {**rogue["trail"], "gen_task": "shortest_word"}
        with open(bad, "w", encoding="utf-8") as f:
            f.write(json.dumps(lessons[0]) + "\n")
            f.write(json.dumps(rogue) + "\n")
        self.delivery.LESSON_STORE = bad
        with self.assertRaises(SystemExit):
            self.delivery.load_materials()

    def test_tasks_selected_by_field(self):
        names = {t["name"] for t in self.delivery.tasks()}
        self.assertEqual(names, {"most_common_word", "longest_word"})

    def test_none_arm_is_bare(self):
        calls = self._stub_run()
        lessons = self.delivery.load_materials()
        rows = self.delivery.run_arm("none", lessons, repeats=2)
        self.assertEqual(len(rows), 4)
        for c in calls:
            self.assertIsNone(c["kw"].get("landscape"))
            self.assertIsNone(c["kw"].get("directives"))
        self.assertTrue(all(r["tools"] == 0 and r["directives"] == 0
                            for r in rows))

    def test_menu_arm_delivers_tools(self):
        calls = self._stub_run()
        lessons = self.delivery.load_materials()
        rows = self.delivery.run_arm("menu", lessons, repeats=1)
        for c in calls:
            self.assertEqual(len(c["kw"]["landscape"]), 2)
            self.assertIsNone(c["kw"].get("directives"))
        self.assertTrue(all(r["tools"] == 2 for r in rows))

    def test_directive_arm_delivers_verbatim_text(self):
        calls = self._stub_run()
        lessons = self.delivery.load_materials()
        self.delivery.run_arm("directive", lessons, repeats=1)
        expected = [x for l in lessons
                    for x in (l["concept"], str(l["rule"]))]
        for c in calls:
            self.assertEqual(c["kw"]["directives"], expected)
            self.assertIsNone(c["kw"].get("landscape"))

    def test_resume_skips_checkpointed_runs(self):
        lessons = self.delivery.load_materials()
        for t in self.delivery.tasks():
            self.delivery._row({"arm": "none", "task": t["name"], "rep": 0,
                                "run_id": "prior", "verdict": "fail",
                                "tools": 0, "directives": 0, "ev": 0.5,
                                "checks": {"f(1)": False}})
        calls = self._stub_run()
        prior = self.delivery._load_rows()
        rows = self.delivery.run_arm("none", lessons, repeats=2,
                                     prior_rows=prior)
        self.assertEqual(len(calls), 2)   # only rep 1 ran live
        self.assertEqual(len(rows), 4)    # prior rows counted


class TestCheckTable(unittest.TestCase):

    def test_rates_and_tie_marking(self):
        import delivery
        rows = [
            {"arm": "none", "task": "longest_word",
             "checks": {"longest_word('cat door bird')": False,
                        "longest_word('')": True}},
            {"arm": "none", "task": "longest_word",
             "checks": {"longest_word('cat door bird')": True,
                        "longest_word('')": True}},
            {"arm": "directive", "task": "longest_word",
             "checks": {"longest_word('cat door bird')": True,
                        "longest_word('')": True}},
        ]
        table = delivery.check_table(rows)
        tie = table["longest_word"]["longest_word('cat door bird')"]
        self.assertTrue(tie["tie_rule"])
        self.assertAlmostEqual(tie["arms"]["none"]["rate"], 0.5)
        self.assertEqual(tie["arms"]["none"]["n"], 2)
        self.assertAlmostEqual(tie["arms"]["directive"]["rate"], 1.0)
        boundary = table["longest_word"]["longest_word('')"]
        self.assertFalse(boundary["tie_rule"])


if __name__ == "__main__":
    unittest.main()
