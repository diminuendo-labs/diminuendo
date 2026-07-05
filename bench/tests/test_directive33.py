"""Tests for the PACKET-033 variant-rung-2 driver. The instrument
must be the standing one by identity (directive28's rung 2 gate,
directive29's byte check, directive30's cells and accounting), the
scaling rebind must land on rung 2 at gate 9 of 12 and bar 2 of 12,
and the VOID-BY-FLOOR boundary must sit exactly at none 2 of 12."""

import importlib
import json
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import runner
import supply_families as sf


class _Directive33Harness(unittest.TestCase):

    def setUp(self):
        self._real_runs = runner.RUNS
        self._real_run_once = runner.run_once
        self._tmp = tempfile.TemporaryDirectory()
        runner.RUNS = self._tmp.name
        import directive30
        import directive33
        self.d30 = importlib.reload(directive30)
        self.d33 = importlib.reload(directive33)

    def tearDown(self):
        runner.RUNS = self._real_runs
        runner.run_once = self._real_run_once
        importlib.reload(self.d30)
        importlib.reload(self.d33)
        self._tmp.cleanup()

    def _stub_run(self, rule_ok_fn):
        calls = []

        def stub(task, criteria, work_features, **kw):
            seen = len(calls)
            calls.append({"kw": kw})
            verdict = rule_ok_fn(seen)
            rung = sf.get_rung("kth_ordered", 2)
            if verdict is None:
                results = []
                output = "def f(:\n"
            else:
                output = ("def kth_ordered(words, k):\n"
                          "    return sorted(words, key=len)[k - 1] "
                          "if 0 < k <= len(words) else None\n")
                rule_checks = set(rung["rule_checks"])
                results = [{"ok": (verdict if c["call"] in rule_checks
                                   else True),
                            "call": c["call"], "got": "x",
                            "expect": c["expect"]}
                           for c in rung["checks"]]
            summary = {"run_id": f"stub-{len(calls)}", "verdict": "pass",
                       "output": output,
                       "directives_used": len(kw.get("directives")
                                              or []),
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


class TestIdentityAndScaling(_Directive33Harness):

    def test_the_instrument_is_the_standing_one_by_identity(self):
        import directive28
        import directive29
        self.assertIs(self.d33.contradiction_gate,
                      directive28.contradiction_gate)
        self.assertIs(self.d33.byte_check, directive29.byte_check)
        for name in ("byte_form_verifier", "directive_text", "stage_a",
                     "stage_b", "pooled_rule", "check_table",
                     "census_table", "recensus"):
            self.assertIs(getattr(self.d33, name),
                          getattr(self.d30, name), name)

    def test_scaling_rebinds_to_variant_rung(self):
        log, rows, report = self.d33._set_scaling("19990101-000000")
        self.assertEqual(self.d30.GROUND_RUNG, 2)
        self.assertEqual(self.d30.GATE_MIN, 9)
        self.assertEqual(self.d30.RULE_BAR, 2)
        for path in (log, rows, report):
            self.assertIn("directive33-19990101-000000",
                          os.path.basename(path))

    def test_variant_gate_passes_both_candidates(self):
        results = self.d33.contradiction_gate()
        self.assertEqual([r["candidate"]["prod_line"] for r in results],
                         [4, 5])
        self.assertTrue(all(r["passes"] for r in results))


class TestVoidByFloor(_Directive33Harness):

    def test_boundary_exactly_two(self):
        self.assertTrue(self.d33.void_by_floor({"passed": 2, "n": 12}))
        self.assertTrue(self.d33.void_by_floor({"passed": 0, "n": 12}))
        self.assertFalse(self.d33.void_by_floor({"passed": 3, "n": 12}))


class TestStageAScaled(_Directive33Harness):

    def test_gate_boundary_exactly_nine_of_twelve(self):
        self.d33._set_scaling("19990101-000001")
        self._stub_run(lambda i: i < 9)
        a = self.d30.stage_a(repeats=12)
        self.assertEqual(a["pooled"]["n"], 12)
        self.assertEqual(a["pooled"]["passed"], 9)
        self.assertTrue(a["passed"])
        self.d33._set_scaling("19990101-000002")
        self._stub_run(lambda i: i < 8)
        a = self.d30.stage_a(repeats=12)
        self.assertEqual(a["pooled"]["passed"], 8)
        self.assertFalse(a["passed"])

    def test_stage_a_runs_the_variant_rung_checks(self):
        self.d33._set_scaling("19990101-000003")
        calls = self._stub_run(lambda i: True)
        self.d30.stage_a(repeats=1)
        rung = sf.get_rung("kth_ordered", 2)
        self.assertEqual(calls[0]["kw"]["evidence_checks"],
                         rung["checks"])


class TestStageBScaled(_Directive33Harness):

    def test_interleave_audits_and_rows_id(self):
        self.d33._set_scaling("19990101-000004")
        calls = self._stub_run(lambda i: True)
        landscape = self.d33.byte_form_verifier()["emission"]
        directive = self.d33.directive_text()
        rows = self.d30.stage_b(landscape, directive, repeats=2)
        self.assertEqual([r["cell"] for r in rows],
                         ["none", "menu-form", "directive"] * 2)
        for r in rows:
            exp = self.d33.EXPECT[r["cell"]]
            self.assertEqual(r["tools"], exp["tools"], r["cell"])
            self.assertEqual(r["directives"], exp["directives"],
                             r["cell"])
        self.assertIn("directive33-19990101-000004",
                      os.path.basename(self.d30._ROWS))
        dir_calls = [c for c in calls if c["kw"].get("directives")]
        self.assertEqual(dir_calls[0]["kw"]["directives"], [directive])

    def test_recensus_replays_from_summaries(self):
        self.d33._set_scaling("19990101-000005")
        self._stub_run(lambda i: True)
        self.d30.stage_a(repeats=2)
        mismatches = self.d33.recensus(self.d30._ROWS,
                                       runs_dir=runner.RUNS)
        self.assertEqual(mismatches, 0)


if __name__ == "__main__":
    unittest.main()
