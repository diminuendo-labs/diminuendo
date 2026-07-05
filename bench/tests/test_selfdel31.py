"""Tests for the PACKET-031 self-delivery harness. Stub runner, temp
runs dir, no model calls. The store must be a raw byte copy of
production line 8 at the desk-check md5, served through the
production path, and the effective-n instrument must count within-row
rule-check disagreement."""

import importlib
import json
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import runner
import supply_families as sf

SSA = ("```python\n"
       "def trimmed_mean(nums):\n"
       "    if len(nums) < 3:\n"
       "        return None\n"
       "    s = sorted(nums)\n"
       "    t = s[1:-1]\n"
       "    return sum(t) / len(t)\n"
       "```")


class _SelfDel31Harness(unittest.TestCase):

    def setUp(self):
        self._real_runs = runner.RUNS
        self._real_run_once = runner.run_once
        self._tmp = tempfile.TemporaryDirectory()
        runner.RUNS = self._tmp.name
        import selfdel31
        self.sd = importlib.reload(selfdel31)

    def tearDown(self):
        runner.RUNS = self._real_runs
        runner.run_once = self._real_run_once
        importlib.reload(self.sd)
        self._tmp.cleanup()

    def _stub_run(self, rule_ok_fn, output_fn=None):
        """rule_ok_fn(call_index) -> True/False/None/dict; a dict maps
        rule-check call to ok for within-row disagreement tests."""
        calls = []

        def stub(task, criteria, work_features, **kw):
            seen = len(calls)
            calls.append({"kw": kw})
            verdict = rule_ok_fn(seen)
            output = output_fn(seen) if output_fn else SSA
            rung = sf.get_rung("safe_stats", 1)
            if verdict is None:
                results = []
                output = "def f(:\n"
            else:
                rule_checks = set(rung["rule_checks"])
                results = []
                for c in rung["checks"]:
                    if c["call"] in rule_checks:
                        ok = (verdict[c["call"]]
                              if isinstance(verdict, dict) else verdict)
                    else:
                        ok = True
                    results.append({"ok": ok, "call": c["call"],
                                    "got": "x", "expect": c["expect"]})
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


class TestBuildGates(_SelfDel31Harness):

    def test_byte_check_and_md5_tie_to_desk_check(self):
        b = self.sd.byte_check()
        self.assertTrue(b["ok"])
        self.assertEqual(b["md5"], self.sd.DESK_CHECK_MD5)

    def test_touched_store_refused(self):
        real = self.sd.STORE
        try:
            with open(real, "rb") as f:
                original = f.read()
            with tempfile.NamedTemporaryFile(delete=False,
                                             suffix=".jsonl") as f:
                f.write(original + b"\n")
                bad = f.name
            self.sd.STORE = bad
            with self.assertRaises(SystemExit):
                self.sd.byte_check()
        finally:
            self.sd.STORE = real
            os.unlink(bad)

    def test_delivery_path_serves_the_production_emission(self):
        import menu
        tools = self.sd.delivery_path_check()
        store = self.sd.load_store()
        self.assertEqual(len(tools), 1)
        self.assertEqual(tools[0],
                         {"concept": store[0]["concept"],
                          "applies_when": store[0]["applies_when"]})
        self.assertEqual(tools,
                         menu.query(store, self.sd.ground_features()))
        self.assertEqual(sorted(tools[0].keys()),
                         ["applies_when", "concept"])

    def test_instrument_is_self_origin(self):
        store = self.sd.load_store()
        self.assertEqual(store[0]["trail"]["origin_seat"],
                         self.sd.PERFORMER)
        self.assertEqual(store[0]["trail"]["gen_task"], "chunk")

    def test_census_pin_is_supply_families_by_identity(self):
        self.assertIs(self.sd.sf.census_shape, sf.census_shape)


class TestStageA(_SelfDel31Harness):

    def test_mixed_boundary_exactly_four(self):
        # two rule checks per run: 2 passing reps = 4 of 24 passes
        self._stub_run(lambda i: i < 2)
        a = self.sd.stage_a(repeats=12)
        self.assertEqual(a["pooled"]["passed"], 4)
        self.assertTrue(a["qualified"])
        self._stub_run(lambda i: i < 1)
        a = self.sd.stage_a(repeats=12)
        self.assertEqual(a["pooled"]["passed"], 2)
        self.assertFalse(a["qualified"])

    def test_floor_and_ceiling_refuse(self):
        self._stub_run(lambda i: False)
        self.assertFalse(self.sd.stage_a(repeats=12)["qualified"])
        self._stub_run(lambda i: True)
        self.assertFalse(self.sd.stage_a(repeats=12)["qualified"])


class TestStageB(_SelfDel31Harness):

    def test_interleave_and_audits(self):
        calls = self._stub_run(lambda i: True)
        tools = self.sd.delivery_path_check()
        rows = self.sd.stage_b(tools, repeats=2)
        self.assertEqual([r["cell"] for r in rows],
                         ["none", "armed"] * 2)
        for r in rows:
            exp = self.sd.EXPECT[r["cell"]]
            self.assertEqual(r["tools"], exp["tools"], r["cell"])
            self.assertEqual(r["directives"], exp["directives"])
        armed_calls = [c for c in calls
                       if c["kw"].get("landscape") is not None]
        self.assertEqual(len(armed_calls), 2)
        self.assertEqual(armed_calls[0]["kw"]["landscape"], tools)

    def test_effective_n_counts_within_row_disagreement(self):
        rc = sf.get_rung("safe_stats", 1)["rule_checks"]
        # reps alternate: agree-pass, disagree, agree-fail
        def outcomes(i):
            if i % 3 == 0:
                return True
            if i % 3 == 1:
                return {rc[0]: True, rc[1]: False}
            return False
        self._stub_run(outcomes)
        tools = self.sd.delivery_path_check()
        rows = self.sd.stage_b(tools, repeats=3)
        eff = self.sd.rule_disagreement(
            [r for r in rows if r["cell"] == "none"])
        self.assertEqual(eff["rows"], 3)
        self.assertEqual(eff["disagreeing_rows"], 1)

    def test_no_readings_row_counts_as_agreeing(self):
        self._stub_run(lambda i: None)
        tools = self.sd.delivery_path_check()
        rows = self.sd.stage_b(tools, repeats=1)
        eff = self.sd.rule_disagreement(rows)
        self.assertEqual(eff["disagreeing_rows"], 0)

    def test_resume_no_reruns(self):
        self._stub_run(lambda i: True)
        tools = self.sd.delivery_path_check()
        self.sd.stage_a(repeats=2)
        self.sd.stage_b(tools, repeats=2)
        prior = self.sd._load_rows()
        calls = self._stub_run(lambda i: True)
        a = self.sd.stage_a(repeats=2, prior_rows=prior)
        rows = self.sd.stage_b(tools, repeats=2, prior_rows=prior)
        self.assertEqual(calls, [])
        self.assertEqual(a["pooled"]["n"], 4)
        self.assertEqual(len(rows), 4)

    def test_recensus_replays_from_summaries(self):
        self._stub_run(lambda i: True)
        self.sd.stage_a(repeats=2)
        mismatches = self.sd.recensus(self.sd._ROWS,
                                      runs_dir=runner.RUNS)
        self.assertEqual(mismatches, 0)


if __name__ == "__main__":
    unittest.main()
