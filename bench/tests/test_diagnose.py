"""Tests for the PACKET-012 residue-diagnosis harness. Stub runner, temp
runs dir, no model calls. The hand lesson rides exactly as printed in
the packet; the tests pin both what the production gates say about it
and the injection mechanism the packet pre-authorizes."""

import importlib
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import lesson
import menu
import runner


class _DiagnoseHarness(unittest.TestCase):

    def setUp(self):
        self._real_runs = runner.RUNS
        self._real_run_once = runner.run_once
        self._tmp = tempfile.TemporaryDirectory()
        runner.RUNS = self._tmp.name
        import diagnose
        self.dg = importlib.reload(diagnose)

    def tearDown(self):
        runner.RUNS = self._real_runs
        runner.run_once = self._real_run_once
        importlib.reload(self.dg)
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


class TestMaterials(_DiagnoseHarness):

    def test_prod_store_is_packet011_menu_arm(self):
        prod = self.dg.load_prod()
        self.assertEqual(len(prod), 2)
        for l in prod:
            self.assertEqual(l["applies_when"]["stated_direction"], "last")

    def test_hand_lesson_text_is_residue_free_and_verbatim(self):
        hand = self.dg.load_hand()
        text = (hand["concept"] + " " + hand["rule"]).lower()
        for noun in ("run", "character", "occurrence", "word"):
            self.assertNotIn(noun, text, noun)
        self.assertEqual(hand["trail"]["gen_task"], "hand_authored")
        self.assertEqual(hand["applies_when"]["stated_direction"], "last")

    def test_hand_lesson_dies_at_the_production_gates(self):
        """The packet's pre-authorized contingency: the printed lesson
        lacks confidence and provenance, so validate rejects it. At
        PACKET-012's run time the menu also raised KeyError on it; the
        PACKET-013 conductor-ruled fix makes the menu DECLINE such a
        lesson instead, so the pin here follows the current gates: the
        lesson is refused by validate and silently shelved by the menu."""
        hand = self.dg.load_hand()
        with self.assertRaises(lesson.LessonError):
            lesson.validate(dict(hand))
        t = self.dg._TASKS[self.dg.TASK]
        self.assertEqual(menu.query([dict(hand)], self.dg._features(t)),
                         [])
        validate_error, query_error = self.dg.hand_gate_check(hand)
        self.assertIn("missing fields", validate_error)
        self.assertIsNone(query_error)

    def test_hand_injection_matches_menu_surface(self):
        """The injection mechanism emits exactly what the menu emits for
        a matched lesson: concept plus applies_when, match confirmed by
        the public matcher."""
        hand = self.dg.load_hand()
        tools = self.dg.hand_tools(hand)
        self.assertEqual(len(tools), 1)
        self.assertEqual(sorted(tools[0]), ["applies_when", "concept"])
        self.assertEqual(tools[0]["concept"], hand["concept"])


class TestArms(_DiagnoseHarness):

    def test_arm_tools_and_resume(self):
        calls = self._stub_run()
        rows = self.dg.run_arms(repeats=2)
        self.assertEqual(len(rows), 6)
        by_arm = {}
        for r in rows:
            by_arm.setdefault(r["arm"], []).append(r)
        self.assertTrue(all(r["tools"] == 0 for r in by_arm["none"]))
        self.assertTrue(all(r["tools"] == 2 for r in by_arm["prod"]))
        self.assertTrue(all(r["tools"] == 1 for r in by_arm["hand"]))
        bare = [c for c in calls if c["kw"].get("landscape") is None]
        self.assertEqual(len(bare), 2)
        calls.clear()
        rows2 = self.dg.run_arms(repeats=2,
                                 prior_rows=self.dg._load_rows())
        self.assertEqual(calls, [])
        self.assertEqual(len(rows2), 6)

    def test_tables(self):
        rows = [
            {"arm": "none", "task": "longest_word",
             "checks": {"longest_word('cat door bird')": True,
                        "longest_word('')": True}},
            {"arm": "hand", "task": "longest_word",
             "checks": {"longest_word('cat door bird')": False,
                        "longest_word('')": True}},
        ]
        table = self.dg.check_table(rows)
        rule = table["longest_word('cat door bird')"]
        self.assertTrue(rule["rule_check"])
        self.assertAlmostEqual(rule["arms"]["none"]["rate"], 1.0)
        self.assertAlmostEqual(rule["arms"]["hand"]["rate"], 0.0)
        pooled = self.dg.pooled_rule_checks(rows)
        self.assertEqual(pooled["none"]["passed"], 1)
        self.assertEqual(pooled["hand"]["passed"], 0)


if __name__ == "__main__":
    unittest.main()
