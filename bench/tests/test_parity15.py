"""Tests for the PACKET-015 origin-parity harness. Stub runner, temp
runs dir, no model calls."""

import importlib
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import menu
import runner


class _ParityHarness(unittest.TestCase):

    def setUp(self):
        self._real_runs = runner.RUNS
        self._real_run_once = runner.run_once
        self._tmp = tempfile.TemporaryDirectory()
        runner.RUNS = self._tmp.name
        import parity15
        self.pt = importlib.reload(parity15)

    def tearDown(self):
        runner.RUNS = self._real_runs
        runner.run_once = self._real_run_once
        importlib.reload(self.pt)
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


class TestMaterials(_ParityHarness):

    def test_byte_checks_pass_on_committed_copies(self):
        checks = self.pt.byte_checks()
        self.assertTrue(checks["rev"])
        self.assertTrue(checks["hand"])

    def test_both_lessons_load_and_ride_range_summary(self):
        stores = self.pt.load_stores()
        rev = stores["rev"][0]
        hand = stores["hand"][0]
        self.assertEqual(rev["provenance"], "engine")
        self.assertEqual(rev["trail"]["gen_task"], "sum_distinct")
        self.assertEqual(hand["provenance"], "hand")
        for key in ("rev", "hand"):
            tools = self.pt.cell_tools(key, stores)
            self.assertEqual(len(tools), 1, key)
        self.assertEqual(self.pt.cell_tools("none", stores), [])

    def test_touched_store_refused(self):
        bad = os.path.join(self._tmp.name, "touched.jsonl")
        with open(self.pt.STORES["rev"]["path"], "rb") as f:
            original = f.read()
        with open(bad, "wb") as f:
            f.write(original + b"\n")
        self.pt.STORES = {**self.pt.STORES,
                          "rev": {**self.pt.STORES["rev"], "path": bad}}
        with self.assertRaises(SystemExit):
            self.pt.byte_checks()


class TestCells(_ParityHarness):

    def test_interleaved_order_tools_and_resume(self):
        calls = self._stub_run()
        rows = self.pt.run_cells(repeats=2)
        self.assertEqual(len(rows), 6)
        self.assertEqual([r["cell"] for r in rows],
                         ["none", "rev", "hand"] * 2)
        for r in rows:
            self.assertEqual(r["tools"],
                             self.pt.EXPECT_TOOLS[r["cell"]], r["cell"])
        self.assertIsNone(calls[0]["landscape"])
        self.assertEqual(len(calls[1]["landscape"]), 1)
        self.assertEqual(len(calls[2]["landscape"]), 1)
        calls.clear()
        rows2 = self.pt.run_cells(repeats=2,
                                  prior_rows=self.pt._load_rows())
        self.assertEqual(calls, [])
        self.assertEqual(len(rows2), 6)

    def test_tables(self):
        rows = [
            {"cell": "none", "task": "range_summary",
             "checks": {"range_summary([3, 1, 2, 2])": False,
                        "range_summary([])": True}},
            {"cell": "rev", "task": "range_summary",
             "checks": {"range_summary([3, 1, 2, 2])": True,
                        "range_summary([])": True}},
        ]
        table = self.pt.check_table(rows)
        rule = table["range_summary([3, 1, 2, 2])"]
        self.assertTrue(rule["rule_check"])
        self.assertAlmostEqual(rule["cells"]["none"]["rate"], 0.0)
        self.assertAlmostEqual(rule["cells"]["rev"]["rate"], 1.0)
        self.assertFalse(table["range_summary([])"]["rule_check"])
        pooled = self.pt.pooled_rule_checks(rows)
        self.assertEqual(pooled["none"]["passed"], 0)
        self.assertEqual(pooled["rev"]["passed"], 1)


if __name__ == "__main__":
    unittest.main()
