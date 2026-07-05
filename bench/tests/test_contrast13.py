"""Tests for the PACKET-013 task-and-topic contrast harness. Stub
runner, temp runs dir, no model calls."""

import importlib
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import runner


class _ContrastHarness(unittest.TestCase):

    def setUp(self):
        self._real_runs = runner.RUNS
        self._real_run_once = runner.run_once
        self._tmp = tempfile.TemporaryDirectory()
        runner.RUNS = self._tmp.name
        import contrast13
        self.ct = importlib.reload(contrast13)

    def tearDown(self):
        runner.RUNS = self._real_runs
        runner.run_once = self._real_run_once
        importlib.reload(self.ct)
        self._tmp.cleanup()

    def _stub_run(self):
        calls = []

        def stub(task, criteria, work_features, **kw):
            calls.append({"task": task,
                          "landscape": kw.get("landscape")})
            return {"run_id": f"stub-{len(calls)}", "verdict": "pass",
                    "evidence": {"passed": True,
                                 "results": [{"ok": True, "call": "f(1)",
                                              "got": "1", "expect": "1"}],
                                 "error": None}}

        runner.run_once = stub
        return calls


class TestMaterials(_ContrastHarness):

    def test_byte_checks_pass_on_the_committed_copies(self):
        checks = self.ct.byte_checks()
        self.assertTrue(checks["prod_byte_identical"])
        self.assertTrue(checks["hand_line_byte_identical"])

    def test_stores_load_through_production_gates(self):
        stores = self.ct.load_stores()
        self.assertEqual(len(stores["prod"]), 2)
        self.assertEqual(len(stores["hand"]), 1)
        hand = stores["hand"][0]
        self.assertEqual(hand["provenance"], "hand")
        self.assertIn("confidence", hand)
        self.assertEqual(hand["applies_when"]["rule_class"],
                         "distinctness")

    def test_hand_lesson_rides_range_summary_through_the_menu(self):
        stores = self.ct.load_stores()
        cell = next(c for c in self.ct.CELLS if c["id"] == "R-hand")
        tools = self.ct.cell_tools(cell, stores)
        self.assertEqual(len(tools), 1)
        self.assertIn("distinct pair counts once", tools[0]["concept"])

    def test_touched_store_refused(self):
        # a byte-different prod copy must refuse to run
        with open(self.ct.PROD_STORE, "rb") as f:
            original = f.read()
        bad = os.path.join(self._tmp.name, "touched.jsonl")
        with open(bad, "wb") as f:
            f.write(original + b"\n")
        self.ct.PROD_STORE = bad
        with self.assertRaises(SystemExit):
            self.ct.byte_checks()


class TestCells(_ContrastHarness):

    def test_interleaved_order_and_tools(self):
        calls = self._stub_run()
        rows = self.ct.run_cells(repeats=2)
        self.assertEqual(len(rows), 8)
        # fixed order within each rep: L-none, L-prod, R-none, R-hand
        order = [r["cell"] for r in rows]
        self.assertEqual(order, ["L-none", "L-prod", "R-none", "R-hand"] * 2)
        by_cell = {}
        for r in rows:
            by_cell.setdefault(r["cell"], []).append(r)
        for cid, expect in self.ct.EXPECT_TOOLS.items():
            self.assertTrue(all(r["tools"] == expect
                                for r in by_cell[cid]), cid)
        # landscape absent on none cells, present on armed cells
        self.assertIsNone(calls[0]["landscape"])
        self.assertEqual(len(calls[1]["landscape"]), 2)
        self.assertIsNone(calls[2]["landscape"])
        self.assertEqual(len(calls[3]["landscape"]), 1)

    def test_resume_skips_checkpointed_runs(self):
        self._stub_run()
        self.ct.run_cells(repeats=1)
        calls2 = self._stub_run()
        rows = self.ct.run_cells(repeats=1,
                                 prior_rows=self.ct._load_rows())
        self.assertEqual(calls2, [])
        self.assertEqual(len(rows), 4)

    def test_tables_read_per_task(self):
        rows = [
            {"cell": "R-none", "task": "range_summary",
             "checks": {"range_summary([3, 1, 2, 2])": False}},
            {"cell": "R-hand", "task": "range_summary",
             "checks": {"range_summary([3, 1, 2, 2])": True}},
            {"cell": "L-none", "task": "longest_word",
             "checks": {"longest_word('cat door bird')": True}},
        ]
        table = self.ct.check_table(rows)
        self.assertIn("range_summary", table)
        self.assertIn("longest_word", table)
        rule = table["range_summary"]["range_summary([3, 1, 2, 2])"]
        self.assertTrue(rule["rule_check"])
        self.assertAlmostEqual(rule["cells"]["R-hand"]["rate"], 1.0)
        pooled = self.ct.pooled_rule_checks(rows)
        self.assertEqual(pooled["R-none"]["passed"], 0)
        self.assertEqual(pooled["R-hand"]["passed"], 1)
        self.assertEqual(pooled["L-none"]["passed"], 1)


if __name__ == "__main__":
    unittest.main()
