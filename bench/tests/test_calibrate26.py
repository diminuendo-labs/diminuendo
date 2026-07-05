"""Tests for the PACKET-026 calibration harness. Stub runner, temp
runs dir, no model calls. Rungs are identified by their check sets,
which are unique across all (family, rung) pairs."""

import importlib
import json
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import runner
import supply_families as sf


def _rung_of(evidence_checks):
    for family in sf.FAMILY_ORDER:
        for rung_def in sf.FAMILIES[family]["rungs"]:
            if rung_def["checks"] == evidence_checks:
                return family, rung_def
    raise AssertionError("unknown check set")


class _Calibrate26Harness(unittest.TestCase):

    def setUp(self):
        self._real_runs = runner.RUNS
        self._real_run_once = runner.run_once
        self._tmp = tempfile.TemporaryDirectory()
        runner.RUNS = self._tmp.name
        import calibrate26
        self.cal = importlib.reload(calibrate26)

    def tearDown(self):
        runner.RUNS = self._real_runs
        runner.run_once = self._real_run_once
        importlib.reload(self.cal)
        self._tmp.cleanup()

    def _stub_run(self, rule_ok_fn, output_fn=None):
        """rule_ok_fn(family, rung, rep_i) -> True/False/None (None
        means unrunnable); non-rule checks always pass."""
        calls = []

        def stub(task, criteria, work_features, **kw):
            family, rung_def = _rung_of(kw["evidence_checks"])
            seen = sum(1 for c in calls
                       if c["family"] == family
                       and c["rung"] == rung_def["rung"])
            calls.append({"family": family, "rung": rung_def["rung"],
                          "kw": kw})
            verdict_ok = rule_ok_fn(family, rung_def["rung"], seen)
            output = (output_fn(family, rung_def["rung"], seen)
                      if output_fn
                      else "def f():\n    return 1\n")
            if verdict_ok is None:
                results = []
                output = "def f(:\n"
            else:
                rule_checks = set(rung_def["rule_checks"])
                results = [{"ok": (verdict_ok if c["call"] in rule_checks
                                   else True),
                            "call": c["call"], "got": "x",
                            "expect": c["expect"]}
                           for c in rung_def["checks"]]
            summary = {"run_id": f"stub-{len(calls)}", "verdict": "pass",
                       "output": output,
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


class TestArithmetic(_Calibrate26Harness):

    def test_generalized_fraction(self):
        self.assertEqual(self.cal.qualify_min("chunk_pad", 1), 2)
        self.assertEqual(self.cal.qualify_min("merge_within", 2), 4)
        self.assertEqual(self.cal.qualify_min("safe_stats", 2), 8)
        self.assertEqual(self.cal.qualify_min("safe_stats", 3), 10)
        self.assertEqual(self.cal.qualify_min("collapse_delims", 3), 6)

    def test_exact_boundary_qualifies(self):
        # chunk_pad r1 has one rule check: exactly 2 passes of 12.
        self._stub_run(lambda f, r, i: i < 2)
        result = self.cal.run_rung("seatX", "audY", "chunk_pad", 1,
                                   repeats=12)
        self.assertEqual(result["pooled"]["n"], 12)
        self.assertEqual(result["pooled"]["passed"], 2)
        self.assertTrue(result["qualified"])

    def test_floor_and_ceiling_refuse_with_character(self):
        self._stub_run(lambda f, r, i: False)
        result = self.cal.run_rung("seatX", "audY", "chunk_pad", 1,
                                   repeats=12)
        self.assertFalse(result["qualified"])
        self.assertEqual(result["character"], "floor-leaning")
        self._stub_run(lambda f, r, i: True)
        result = self.cal.run_rung("seatX", "audY", "chunk_pad", 1,
                                   repeats=12)
        self.assertFalse(result["qualified"])
        self.assertEqual(result["character"], "ceiling-leaning")

    def test_unrunnable_counts_as_fail(self):
        def outcomes(f, r, i):
            if i < 2:
                return True
            if i >= 10:
                return None
            return False
        self._stub_run(outcomes)
        result = self.cal.run_rung("seatX", "audY", "chunk_pad", 1,
                                   repeats=12)
        self.assertEqual(result["pooled"]["passed"], 2)
        self.assertEqual(result["pooled"]["unrunnable_rows"], 2)
        self.assertTrue(result["qualified"])

    def test_control_rung_marked(self):
        self._stub_run(lambda f, r, i: i % 2 == 0)
        result = self.cal.run_rung("seatX", "audY", "merge_within", 1,
                                   repeats=12)
        self.assertTrue(result["control"])
        self.assertTrue(result["qualified"])


class TestSweep(_Calibrate26Harness):

    def test_family_stops_at_first_mixed_rung(self):
        calls = self._stub_run(
            lambda f, r, i: (i % 2 == 0) if f == "chunk_pad" and r == 1
            else True)
        results, kept = self.cal.sweep_seat("seatX", "audY", repeats=12)
        ran = {(c["family"], c["rung"]) for c in calls}
        self.assertIn(("chunk_pad", 1), ran)
        self.assertNotIn(("chunk_pad", 2), ran)
        self.assertEqual(kept[0]["family"], "chunk_pad")
        self.assertEqual(kept[0]["rung"], 1)
        # every other family exhausted at ceiling, nothing kept
        self.assertEqual(len(kept), 1)
        for family in sf.FAMILY_ORDER[1:]:
            self.assertIn((family, 3), ran)

    def test_all_ceiling_keeps_nothing(self):
        self._stub_run(lambda f, r, i: True)
        results, kept = self.cal.sweep_seat("seatX", "audY", repeats=12)
        self.assertEqual(kept, [])
        self.assertEqual(len(results), 18)

    def test_resume_no_reruns(self):
        self._stub_run(lambda f, r, i: True)
        self.cal.run_rung("seatX", "audY", "token_case", 1, repeats=2)
        prior = self.cal._load_rows()
        calls = self._stub_run(lambda f, r, i: True)
        result = self.cal.run_rung("seatX", "audY", "token_case", 1,
                                   repeats=2, prior_rows=prior)
        self.assertEqual(calls, [])
        self.assertEqual(result["pooled"]["n"], 2)

    def test_rows_are_bare_none_cells(self):
        calls = self._stub_run(lambda f, r, i: True)
        self.cal.run_rung("seatX", "audY", "kth_ordered", 1, repeats=2)
        rows = self.cal._load_rows()
        self.assertTrue(all(r["tools"] == 0 and r["cell"] == "none"
                            for r in rows))
        self.assertTrue(all(c["kw"]["landscape"] is None
                            for c in calls))


class TestCensus(_Calibrate26Harness):

    def test_census_table_and_moderator_ready(self):
        sweep_code = ("def merge_within(pairs):\n"
                      "    out = []\n"
                      "    for s, e in sorted(pairs):\n"
                      "        if out and s <= out[-1][1] + 1:\n"
                      "            out[-1][1] = max(out[-1][1], e)\n"
                      "        else:\n"
                      "            out.append([s, e])\n"
                      "    return out")
        self._stub_run(lambda f, r, i: i % 2 == 0,
                       output_fn=lambda f, r, i: f"```python\n"
                                                 f"{sweep_code}\n```")
        self.cal.run_rung("seatX", "audY", "merge_within", 2,
                          repeats=12)
        rows = self.cal._load_rows()
        census = self.cal.census_table(rows)
        key = "seatX|merge_within|r2"
        self.assertEqual(census[key]["sort-and-sweep"], 12)
        kept = [{"family": "merge_within", "rung": 2,
                 "pooled": {}, "control": False}]
        ready = self.cal.moderator_ready(kept, census, "seatX")
        self.assertEqual(len(ready), 1)
        self.assertEqual(ready[0]["named_shape"], "sort-and-sweep")
        self.assertEqual(ready[0]["count"], 12)

    def test_below_concentration_not_designated(self):
        census = {"seatX|chunk_pad|r1": {"range-step comprehension": 8,
                                         "explicit loop-with-pad": 4,
                                         "other": 0, "unrunnable": 0}}
        kept = [{"family": "chunk_pad", "rung": 1, "pooled": {},
                 "control": False}]
        self.assertEqual(
            self.cal.moderator_ready(kept, census, "seatX"), [])

    def test_recensus_replays_from_summaries(self):
        self._stub_run(lambda f, r, i: True)
        self.cal.run_rung("seatX", "audY", "safe_stats", 1, repeats=2)
        mismatches = self.cal.recensus(self.cal._ROWS,
                                       runs_dir=runner.RUNS)
        self.assertEqual(mismatches, 0)


if __name__ == "__main__":
    unittest.main()
