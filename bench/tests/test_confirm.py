"""Tests for the PACKET-009 confirmation-arms harness: pairing
enumeration from the pins, agreement with the production menu, the pin
regression, and arm behavior. Stub runner, temp runs dir, no model
calls."""

import importlib
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import menu
import runner


class _ConfirmHarness(unittest.TestCase):

    def setUp(self):
        self._real_runs = runner.RUNS
        self._real_run_once = runner.run_once
        self._tmp = tempfile.TemporaryDirectory()
        runner.RUNS = self._tmp.name
        import confirm
        self.cf = importlib.reload(confirm)

    def tearDown(self):
        runner.RUNS = self._real_runs
        runner.run_once = self._real_run_once
        importlib.reload(self.cf)
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


class TestEnumeration(_ConfirmHarness):

    def test_stores_are_production_grade(self):
        self.assertEqual(len(self.cf.load_store("A")), 3)
        self.assertEqual(len(self.cf.load_store("B")), 2)

    def test_pairing_table_from_the_pins(self):
        table = {e["lesson"]: e for e in self.cf.pairing_table()}
        self.assertEqual(len(table), 5)
        # the two qwen tie lessons match longest_word and nothing else
        self.assertEqual(
            table["A/max_index/within_task"]["matched_tasks"],
            ["longest_word"])
        self.assertEqual(
            table["A/shortest_word/within_task"]["matched_tasks"],
            ["longest_word"])
        # the other three lessons are structurally empty, named as such
        for lid in ("A/count_token/sibling",
                    "B/count_distinct_pairs/within_task",
                    "B/count_token/sibling"):
            self.assertTrue(table[lid]["structurally_empty"], lid)
            self.assertEqual(table[lid]["matched_tasks"], [])

    def test_cross_seat_cells(self):
        cells = self.cf.cross_seat_pairings(self.cf.pairing_table())
        self.assertEqual(len(cells), 1)
        cell = cells[0]
        self.assertEqual(cell["performer"], "llama3.1:8b")
        self.assertEqual(cell["task"], "longest_word")
        self.assertEqual(cell["store"], "A")
        self.assertEqual(len(cell["lessons"]), 2)

    def test_matched_agrees_with_the_production_menu(self):
        lw = self.cf._TASKS["longest_word"]
        rs = self.cf._TASKS["range_summary"]
        a = self.cf.load_store("A")
        b = self.cf.load_store("B")
        self.assertEqual(len(menu.query(a, self.cf._features(lw))), 2)
        self.assertEqual(menu.query(b, self.cf._features(rs)), [])
        for l in a:
            self.assertEqual(self.cf.matched(l, lw),
                             l["applies_when"]["rule_class"] == "tie_break")
        for l in b:
            self.assertFalse(self.cf.matched(l, rs))

    def test_pin_regression_all_clean(self):
        results = self.cf.pin_regression()
        self.assertEqual(len(results), 4)
        for r in results:
            self.assertTrue(r["passed"], r)
            self.assertEqual(r["tools"], 0)


class TestArms(_ConfirmHarness):

    def test_arms_and_resume(self):
        calls = self._stub_run()
        cell = self.cf.cross_seat_pairings(self.cf.pairing_table())[0]
        rows = self.cf.run_pairing(cell, repeats=2)
        self.assertEqual(len(rows), 4)
        armed = [r for r in rows if r["arm"] == "menu"]
        self.assertTrue(all(r["tools"] == 2 for r in armed))
        bare = [c for c in calls if c["kw"].get("landscape") is None]
        self.assertEqual(len(bare), 2)
        # resume: nothing runs twice
        calls.clear()
        prior = self.cf._load_rows()
        rows2 = self.cf.run_pairing(cell, repeats=2, prior_rows=prior)
        self.assertEqual(calls, [])
        self.assertEqual(len(rows2), 4)


if __name__ == "__main__":
    unittest.main()
