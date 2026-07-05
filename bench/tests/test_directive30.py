"""Tests for the PACKET-030 symmetric-forms harness. Stub runner,
temp runs dir, no model calls. The build-gate instruments must be the
P028/P029 ones and supply_families' by identity, and the byte-form
verifier must bind the menu-form landscape to menu.query's own
emission."""

import importlib
import json
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import runner
import supply_families as sf

SINGLE_KEY = ("```python\n"
              "def kth_ordered(words, k):\n"
              "    if k < 1 or k > len(words):\n"
              "        return None\n"
              "    return sorted(words, key=len)[k - 1]\n"
              "```")


class _Directive30Harness(unittest.TestCase):

    def setUp(self):
        self._real_runs = runner.RUNS
        self._real_run_once = runner.run_once
        self._tmp = tempfile.TemporaryDirectory()
        runner.RUNS = self._tmp.name
        import directive30
        self.d30 = importlib.reload(directive30)

    def tearDown(self):
        runner.RUNS = self._real_runs
        runner.run_once = self._real_run_once
        importlib.reload(self.d30)
        self._tmp.cleanup()

    def _stub_run(self, rule_ok_fn, output_fn=None):
        """rule_ok_fn(cell_call_index) -> True/False/None; non-rule
        checks always pass. The stub honors the directives kwarg."""
        calls = []

        def stub(task, criteria, work_features, **kw):
            seen = len(calls)
            calls.append({"kw": kw})
            verdict_ok = rule_ok_fn(seen)
            output = output_fn(seen) if output_fn else SINGLE_KEY
            rung = sf.get_rung("kth_ordered", 3)
            if verdict_ok is None:
                results = []
                output = "def f(:\n"
            else:
                rule_checks = set(rung["rule_checks"])
                results = [{"ok": (verdict_ok if c["call"] in
                                   rule_checks else True),
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


class TestBuildGates(_Directive30Harness):

    def test_instruments_are_imported_by_identity(self):
        import directive28 as d28
        import directive29 as d29
        import directive30
        self.assertIs(directive30.p029_derivations, d29.derivations)
        self.assertIs(directive30.p029_byte_check, d29.byte_check)
        self.assertIs(directive30.load_candidate, d28.load_candidate)
        self.assertIs(directive30.sf.census_shape, sf.census_shape)

    def test_byte_form_verifier_binds_the_emission(self):
        import menu
        v = self.d30.byte_form_verifier()
        lesson = self.d30.load_lesson()
        self.assertEqual(len(v["emission"]), 1)
        self.assertEqual(v["emission"][0],
                         {"concept": lesson["concept"],
                          "applies_when": lesson["applies_when"]})
        self.assertEqual(v["emission"],
                         menu.query([lesson],
                                    self.d30.matched_features()))
        self.assertEqual(v["control_tools"], 0)

    def test_emission_carries_no_metric_shaped_data(self):
        v = self.d30.byte_form_verifier()
        self.assertEqual(sorted(v["emission"][0].keys()),
                         ["applies_when", "concept"])

    def test_directive_text_is_the_rule_sentence(self):
        text = self.d30.directive_text()
        lesson = self.d30.load_lesson()
        self.assertEqual(text, lesson["rule"])

    def test_contradiction_gate_still_separates(self):
        derivs = self.d30.p029_derivations()
        self.assertTrue(all(d["differs"] for d in derivs))
        self.assertEqual(len(derivs), 2)

    def test_byte_check_passes(self):
        self.assertTrue(self.d30.p029_byte_check())


class TestStageA(_Directive30Harness):

    def test_gate_boundary_exactly_eighteen(self):
        # two rule checks per run: 9 passing reps = 18 of 24 passes
        self._stub_run(lambda i: i < 9)
        a = self.d30.stage_a(repeats=12)
        self.assertEqual(a["pooled"]["passed"], 18)
        self.assertTrue(a["passed"])
        self._stub_run(lambda i: i < 8)
        a = self.d30.stage_a(repeats=12)
        self.assertEqual(a["pooled"]["passed"], 16)
        self.assertFalse(a["passed"])

    def test_unrunnable_counts_as_fail(self):
        def outcomes(i):
            return None if i >= 10 else True
        self._stub_run(outcomes)
        a = self.d30.stage_a(repeats=12)
        self.assertEqual(a["pooled"]["passed"], 20)
        self.assertEqual(a["pooled"]["unrunnable_rows"], 2)
        self.assertTrue(a["passed"])


class TestStageB(_Directive30Harness):

    def test_interleave_and_audits(self):
        calls = self._stub_run(lambda i: True)
        landscape = self.d30.byte_form_verifier()["emission"]
        directive = self.d30.directive_text()
        rows = self.d30.stage_b(landscape, directive, repeats=2)
        self.assertEqual([r["cell"] for r in rows],
                         ["none", "menu-form", "directive"] * 2)
        for r in rows:
            exp = self.d30.EXPECT[r["cell"]]
            self.assertEqual(r["tools"], exp["tools"], r["cell"])
            self.assertEqual(r["directives"], exp["directives"],
                             r["cell"])
        menu_calls = [c for c in calls
                      if c["kw"].get("landscape") is not None]
        dir_calls = [c for c in calls if c["kw"].get("directives")]
        self.assertEqual(len(menu_calls), 2)
        self.assertEqual(len(dir_calls), 2)
        self.assertEqual(dir_calls[0]["kw"]["directives"], [directive])
        self.assertEqual(menu_calls[0]["kw"]["landscape"], landscape)

    def test_resume_no_reruns(self):
        self._stub_run(lambda i: True)
        landscape = self.d30.byte_form_verifier()["emission"]
        directive = self.d30.directive_text()
        self.d30.stage_a(repeats=2)
        self.d30.stage_b(landscape, directive, repeats=2)
        prior = self.d30._load_rows()
        calls = self._stub_run(lambda i: True)
        a = self.d30.stage_a(repeats=2, prior_rows=prior)
        rows = self.d30.stage_b(landscape, directive, repeats=2,
                                prior_rows=prior)
        self.assertEqual(calls, [])
        self.assertEqual(a["pooled"]["n"], 4)
        self.assertEqual(len(rows), 6)

    def test_recensus_replays_from_summaries(self):
        self._stub_run(lambda i: True)
        self.d30.stage_a(repeats=2)
        mismatches = self.d30.recensus(self.d30._ROWS,
                                       runs_dir=runner.RUNS)
        self.assertEqual(mismatches, 0)


if __name__ == "__main__":
    unittest.main()
