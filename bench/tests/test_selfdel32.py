"""Tests for the PACKET-032 replication driver. The instrument must
be selfdel31's by identity, the path rebinding must carry the
selfdel32 id, and the VOID-BY-CEILING boundary must sit exactly at
none 20 of 24."""

import importlib
import json
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import runner
import selfdel31
import supply_families as sf


class _SelfDel32Harness(unittest.TestCase):

    def setUp(self):
        self._real_runs = runner.RUNS
        self._real_run_once = runner.run_once
        self._real_paths = (selfdel31._TS, selfdel31._LOG,
                            selfdel31._ROWS, selfdel31._REPORT)
        self._tmp = tempfile.TemporaryDirectory()
        runner.RUNS = self._tmp.name
        import selfdel32
        self.rep = importlib.reload(selfdel32)

    def tearDown(self):
        runner.RUNS = self._real_runs
        runner.run_once = self._real_run_once
        (selfdel31._TS, selfdel31._LOG,
         selfdel31._ROWS, selfdel31._REPORT) = self._real_paths
        self._tmp.cleanup()

    def _stub_run(self, rule_ok_fn):
        calls = []

        def stub(task, criteria, work_features, **kw):
            seen = len(calls)
            calls.append({"kw": kw})
            verdict = rule_ok_fn(seen)
            rung = sf.get_rung("safe_stats", 1)
            rule_checks = set(rung["rule_checks"])
            results = [{"ok": (verdict if c["call"] in rule_checks
                               else True),
                        "call": c["call"], "got": "x",
                        "expect": c["expect"]}
                       for c in rung["checks"]]
            summary = {"run_id": f"stub-{len(calls)}", "verdict": "pass",
                       "output": "def trimmed_mean(n):\n    return 1\n",
                       "directives_used": 0,
                       "evidence": {"passed": all(r["ok"]
                                                  for r in results),
                                    "results": results, "error": None}}
            with open(os.path.join(runner.RUNS,
                                   f"stub-{len(calls)}.summary.json"),
                      "w", encoding="utf-8") as f:
                json.dump(summary, f)
            return summary

        runner.run_once = stub
        return calls


class TestIdentity(_SelfDel32Harness):

    def test_the_instrument_is_selfdel31_by_identity(self):
        pairs = (("build_gates", selfdel31.build_gates),
                 ("stage_a", selfdel31.stage_a),
                 ("stage_b", selfdel31.stage_b),
                 ("pooled_rule", selfdel31.pooled_rule),
                 ("rule_disagreement", selfdel31.rule_disagreement),
                 ("check_table", selfdel31.check_table),
                 ("census_table", selfdel31.census_table),
                 ("recensus", selfdel31.recensus),
                 ("byte_check", selfdel31.byte_check))
        for name, fn in pairs:
            self.assertIs(getattr(self.rep, name), fn, name)
        self.assertIs(self.rep.CELLS, selfdel31.CELLS)
        self.assertIs(self.rep.EXPECT, selfdel31.EXPECT)

    def test_paths_rebind_to_selfdel32_id(self):
        log, rows, report = self.rep._set_paths("19990101-000000")
        for path in (log, rows, report):
            self.assertIn("selfdel32-19990101-000000",
                          os.path.basename(path))
        self.assertEqual(selfdel31._ROWS, rows)
        self.assertEqual(selfdel31._LOG, log)

    def test_rows_land_under_the_replication_id(self):
        self.rep._set_paths("19990101-000001")
        self._stub_run(lambda i: i % 2 == 0)
        selfdel31.stage_a(repeats=2)
        self.assertTrue(os.path.exists(selfdel31._ROWS))
        self.assertIn("selfdel32-19990101-000001",
                      os.path.basename(selfdel31._ROWS))


class TestVoidByCeiling(_SelfDel32Harness):

    def test_boundary_exactly_twenty(self):
        self.assertTrue(self.rep.void_by_ceiling(
            {"passed": 20, "n": 24}))
        self.assertTrue(self.rep.void_by_ceiling(
            {"passed": 24, "n": 24}))
        self.assertFalse(self.rep.void_by_ceiling(
            {"passed": 19, "n": 24}))

    def test_p031_baseline_would_not_void(self):
        # P031's fresh none cell read 15 of 24: headroom existed.
        self.assertFalse(self.rep.void_by_ceiling(
            {"passed": 15, "n": 24}))


class TestGatesStillHold(_SelfDel32Harness):

    def test_byte_check_and_md5(self):
        b = self.rep.byte_check()
        self.assertTrue(b["ok"])
        self.assertEqual(b["md5"], selfdel31.DESK_CHECK_MD5)

    def test_delivery_path_serves_one_tool(self):
        tools = selfdel31.delivery_path_check()
        self.assertEqual(len(tools), 1)


if __name__ == "__main__":
    unittest.main()
