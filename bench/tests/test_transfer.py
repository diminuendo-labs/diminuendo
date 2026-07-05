"""Tests for the PACKET-006 focused transfer harness. Stub runner, temp
runs dir, no model calls. The packet-local stores are committed material,
read as-is; refusal behavior is tested on temp copies."""

import importlib
import json
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import runner


class _TransferHarness(unittest.TestCase):

    def setUp(self):
        self._real_runs = runner.RUNS
        self._real_run_once = runner.run_once
        self._tmp = tempfile.TemporaryDirectory()
        runner.RUNS = self._tmp.name
        import transfer
        self.transfer = importlib.reload(transfer)

    def tearDown(self):
        runner.RUNS = self._real_runs
        runner.run_once = self._real_run_once
        importlib.reload(self.transfer)
        self._tmp.cleanup()

    def _stub_run(self, ok=True):
        calls = []

        def stub(task, criteria, work_features, **kw):
            calls.append({"task": task, "features": work_features,
                          "kw": kw})
            return {"run_id": f"stub-{len(calls)}", "verdict": "pass",
                    "evidence": {"passed": ok,
                                 "results": [{"ok": ok, "call": "f(1)",
                                              "got": "1", "expect": "1"}],
                                 "error": None}}

        runner.run_once = stub
        return calls


class TestMaterials(_TransferHarness):

    def test_stores_load_with_expected_sizes(self):
        a = self.transfer.load_store("A")
        self.assertEqual(len(a), 2)
        # the direction-specific tie lesson is in A and pinned
        tie = [l for l in a
               if l["applies_when"].get("rule_class") == "tie_break"]
        self.assertEqual(len(tie), 1)
        self.assertEqual(tie[0]["applies_when"]["stated_direction"],
                         "last")

    def test_store_b_dies_at_the_current_gates(self):
        """PACKET-007's shape screen rejects the recipe lesson that store
        B carries, so the PACKET-006 harness can no longer run its B
        pairings. The record stands; the instrument is superseded, which
        is the gate doing its job on historical material."""
        import lesson
        with self.assertRaises(lesson.LessonError):
            self.transfer.load_store("B")

    def test_touched_store_refused(self):
        bad = os.path.join(self._tmp.name, "bad.jsonl")
        a = self.transfer.load_store("A")
        with open(bad, "w", encoding="utf-8") as f:
            f.write(json.dumps(a[0]) + "\n")  # one lesson, not two
        self.transfer.STORES = dict(self.transfer.STORES, A=bad)
        with self.assertRaises(SystemExit):
            self.transfer.load_store("A")

    def test_pairing_tasks_exist_with_rule_checks(self):
        for p in self.transfer.PAIRINGS:
            for name in p["tasks"]:
                t = self.transfer._TASKS[name]
                self.assertTrue(t.get("rule_checks"), name)


class TestArms(_TransferHarness):

    def test_none_arm_is_bare_and_menu_arm_delivers(self):
        calls = self._stub_run()
        p1 = self.transfer.PAIRINGS[0]  # llama, longest_word, store A
        rows = self.transfer.run_pairing(p1, repeats=2)
        self.assertEqual(len(rows), 4)  # 1 task x 2 arms x 2 reps
        none_calls = [c for c in calls if c["kw"].get("landscape") is None]
        menu_calls = [c for c in calls
                      if c["kw"].get("landscape") is not None]
        self.assertEqual(len(none_calls), 2)
        self.assertEqual(len(menu_calls), 2)
        # the tie lesson is the only store-A lesson matching longest_word
        for c in menu_calls:
            self.assertEqual(len(c["kw"]["landscape"]), 1)

    def test_tie_lesson_never_rides_a_mismatched_task(self):
        self._stub_run()
        p4 = self.transfer.PAIRINGS[3]  # llama, snake+balanced, store A
        rows = self.transfer.run_pairing(p4, repeats=1)
        tie_concepts = [l["concept"] for l in self.transfer.load_store("A")
                        if l["applies_when"].get("rule_class")
                        == "tie_break"]
        for r in rows:
            if r["arm"] != "menu":
                continue
            self.assertGreater(r["tools"], 0)  # class-matched normalize
            for concept in tie_concepts:
                self.assertNotIn(concept, r["tool_concepts"], r["task"])

    def test_resume_skips_checkpointed_runs(self):
        p1 = self.transfer.PAIRINGS[0]  # llama, longest_word, store A
        for rep in range(2):
            self.transfer._row({"pairing": "P1", "topic_matched": True,
                                "performer": p1["performer"],
                                "store": "A", "arm": "none",
                                "task": "longest_word", "rep": rep,
                                "run_id": "prior", "verdict": "fail",
                                "tools": 0, "tool_concepts": [],
                                "ev": 0.5, "checks": {"f(1)": False}})
        calls = self._stub_run()
        prior = self.transfer._load_rows()
        rows = self.transfer.run_pairing(p1, repeats=2, prior_rows=prior)
        # both none reps came from disk, both menu reps ran live
        self.assertEqual(len(calls), 2)
        self.assertEqual(len(rows), 4)


class TestTables(unittest.TestCase):

    def test_check_table_pooled_and_audit(self):
        import transfer
        rows = [
            {"pairing": "P1", "arm": "none", "task": "longest_word",
             "tools": 0, "tool_concepts": [],
             "checks": {"longest_word('cat door bird')": False,
                        "longest_word('')": True}},
            {"pairing": "P1", "arm": "menu", "task": "longest_word",
             "tools": 1, "tool_concepts": ["tie concept"],
             "checks": {"longest_word('cat door bird')": True,
                        "longest_word('')": True}},
        ]
        table = transfer.check_table(rows)
        rule = table["P1"]["longest_word"]["longest_word('cat door bird')"]
        self.assertTrue(rule["rule_check"])
        self.assertAlmostEqual(rule["arms"]["none"]["rate"], 0.0)
        self.assertAlmostEqual(rule["arms"]["menu"]["rate"], 1.0)
        self.assertFalse(
            table["P1"]["longest_word"]["longest_word('')"]["rule_check"])
        pooled = transfer.pooled_rule_checks(rows)
        self.assertEqual(pooled["P1"]["none"], {"n": 1, "passed": 0,
                                                "rate": 0.0})
        self.assertEqual(pooled["P1"]["menu"], {"n": 1, "passed": 1,
                                                "rate": 1.0})
        audit = transfer.tool_audit(rows)
        self.assertEqual(audit, {"longest_word": ["tie concept"]})


if __name__ == "__main__":
    unittest.main()
