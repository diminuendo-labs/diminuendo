"""Tests for the PACKET-027 moderator retest harness. Stub runner,
temp runs dir, no model calls. The census classifiers must be
supply_families' by identity, and stage A must enforce both gates."""

import importlib
import json
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import runner
import supply_families as sf

SWEEP_CODE = ("```python\n"
              "def chunk_pad(lst, k):\n"
              "    return [lst[i:i+k] for i in range(0, len(lst), k)]\n"
              "```")
SPLIT_CODE = ("```python\n"
              "def token_case(s):\n"
              "    parts = [p for p in s.split('_') if p]\n"
              "    return parts[0].lower() + ''.join(p.capitalize() "
              "for p in parts[1:]) if parts else ''\n"
              "```")
LOOP_CODE = ("```python\n"
             "def chunk_pad(lst, k):\n"
             "    out = []\n"
             "    for i in range(0, len(lst), k):\n"
             "        out.append(lst[i:i+k])\n"
             "    return out\n"
             "```")


class _ModRetest27Harness(unittest.TestCase):

    def setUp(self):
        self._real_runs = runner.RUNS
        self._real_run_once = runner.run_once
        self._tmp = tempfile.TemporaryDirectory()
        runner.RUNS = self._tmp.name
        import modretest27
        self.mr = importlib.reload(modretest27)

    def tearDown(self):
        runner.RUNS = self._real_runs
        runner.run_once = self._real_run_once
        importlib.reload(self.mr)
        self._tmp.cleanup()

    def _stub_run(self, rule_ok_fn, output_fn=None):
        """rule_ok_fn(side_family, rep_i) -> True/False/None; non-rule
        checks always pass. output_fn(side_family, rep_i) -> text."""
        calls = []

        def stub(task, criteria, work_features, **kw):
            family = next(
                f for f in ("chunk_pad", "token_case")
                if any(sf.get_rung(f, r)["checks"] ==
                       kw["evidence_checks"] for r in (1, 2, 3)))
            rung_def = next(
                sf.get_rung(family, r) for r in (1, 2, 3)
                if sf.get_rung(family, r)["checks"] ==
                kw["evidence_checks"])
            seen = sum(1 for c in calls if c["family"] == family)
            calls.append({"family": family, "kw": kw})
            verdict_ok = rule_ok_fn(family, seen)
            output = (output_fn(family, seen) if output_fn
                      else (SWEEP_CODE if family == "chunk_pad"
                            else SPLIT_CODE))
            if verdict_ok is None:
                results = []
                output = "def f(:\n"
            else:
                rule_checks = set(rung_def["rule_checks"])
                results = [{"ok": (verdict_ok if c["call"] in
                                   rule_checks else True),
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


class TestMaterials(_ModRetest27Harness):

    def test_byte_checks_and_stores(self):
        checks = self.mr.byte_checks()
        self.assertTrue(all(checks.values()))
        stores = self.mr.load_stores()
        b1 = stores["armed-B1"][0]
        n1 = stores["armed-N1"][0]
        self.assertEqual(b1["trail"]["gen_task"], "chunk")
        self.assertEqual(n1["trail"]["gen_task"], "split_csvish")
        for les in (b1, n1):
            self.assertEqual(les["trail"]["origin_seat"], "mistral:7b")

    def test_touched_store_refused(self):
        bad = os.path.join(self._tmp.name, "touched.jsonl")
        with open(self.mr.ARMS["armed-N1"]["path"], "rb") as f:
            original = f.read()
        with open(bad, "wb") as f:
            f.write(original + b"\n")
        self.mr.ARMS = {**self.mr.ARMS,
                        "armed-N1": {**self.mr.ARMS["armed-N1"],
                                     "path": bad}}
        with self.assertRaises(SystemExit):
            self.mr.byte_checks()

    def test_lessons_ride_their_sides_only(self):
        import menu
        stores = self.mr.load_stores()
        self.assertEqual(
            len(self.mr.cell_tools("armed-B1", stores, "chunk_pad")), 1)
        self.assertEqual(
            len(self.mr.cell_tools("armed-N1", stores, "token_case")), 1)
        self.assertEqual(
            self.mr.cell_tools("none", stores, "chunk_pad"), [])
        # structural separation: B1 never rides token_case ground and
        # N1 never rides chunk_pad ground, the pins contradict
        self.assertEqual(
            menu.query(stores["armed-B1"],
                       self.mr._features("token_case")), [])
        self.assertEqual(
            menu.query(stores["armed-N1"],
                       self.mr._features("chunk_pad")), [])

    def test_classifiers_identity_pinned(self):
        self.assertIs(self.mr.sf.census_shape, sf.census_shape)
        self.assertIs(self.mr.sf._CLASSIFIERS["chunk_pad"],
                      sf._shape_chunk_pad)
        self.assertIs(self.mr.sf._CLASSIFIERS["token_case"],
                      sf._shape_token_case)

    def test_bars_and_named_shapes(self):
        self.assertEqual(self.mr.rule_n("fights"), 2)
        self.assertEqual(self.mr.drift_bar("fights"), 4)
        self.assertEqual(self.mr.rule_n("extends"), 1)
        self.assertEqual(self.mr.drift_bar("extends"), 2)
        self.assertEqual(self.mr.named_shape("fights"),
                         "range-step comprehension")
        self.assertEqual(self.mr.named_shape("extends"),
                         "split-capitalize-join")


class TestStageA(_ModRetest27Harness):

    def test_both_gates_pass_survives(self):
        self._stub_run(lambda f, i: i % 2 == 0)
        result = self.mr.gate_side("fights", repeats=12)
        self.assertTrue(result["qualified"])
        self.assertEqual(result["concentration"], 12)
        self.assertTrue(result["concentrated"])
        self.assertTrue(result["survives"])

    def test_qualification_fails_closes(self):
        self._stub_run(lambda f, i: True)
        result = self.mr.gate_side("fights", repeats=12)
        self.assertFalse(result["qualified"])
        self.assertTrue(result["concentrated"])
        self.assertFalse(result["survives"])

    def test_concentration_fails_voids_prediction(self):
        # mixed rule outcomes but the census sits on the wrong shape
        self._stub_run(lambda f, i: i % 2 == 0,
                       output_fn=lambda f, i: LOOP_CODE)
        result = self.mr.gate_side("fights", repeats=12)
        self.assertTrue(result["qualified"])
        self.assertEqual(result["concentration"], 0)
        self.assertFalse(result["concentrated"])
        self.assertFalse(result["survives"])

    def test_concentration_boundary_exactly_nine(self):
        self._stub_run(lambda f, i: i % 2 == 0,
                       output_fn=lambda f, i: (SWEEP_CODE if i < 9
                                               else LOOP_CODE))
        result = self.mr.gate_side("fights", repeats=12)
        self.assertEqual(result["concentration"], 9)
        self.assertTrue(result["concentrated"])
        self._stub_run(lambda f, i: i % 2 == 0,
                       output_fn=lambda f, i: (SWEEP_CODE if i < 8
                                               else LOOP_CODE))
        result = self.mr.gate_side("fights", repeats=12)
        self.assertEqual(result["concentration"], 8)
        self.assertFalse(result["concentrated"])

    def test_extends_gate_arithmetic(self):
        self._stub_run(lambda f, i: i < 2)
        result = self.mr.gate_side("extends", repeats=12)
        self.assertEqual(result["pooled"]["n"], 12)
        self.assertEqual(result["pooled"]["passed"], 2)
        self.assertTrue(result["qualified"])
        self.assertTrue(result["survives"])


class TestStageB(_ModRetest27Harness):

    def test_interleave_audit_and_resume(self):
        self._stub_run(lambda f, i: i % 2 == 0)
        stores = self.mr.load_stores()
        rows = self.mr.run_block("fights", stores, repeats=2)
        self.assertEqual([r["cell"] for r in rows],
                         ["none", "armed-B1"] * 2)
        for r in rows:
            self.assertEqual(r["tools"],
                             self.mr.EXPECT_TOOLS[r["cell"]])
        prior = self.mr._load_rows()
        calls = self._stub_run(lambda f, i: True)
        rows2 = self.mr.run_block("fights", stores, repeats=2,
                                  prior_rows=prior)
        self.assertEqual(calls, [])
        self.assertEqual(len(rows2), 4)

    def test_sides_separate_in_rows(self):
        self._stub_run(lambda f, i: True)
        stores = self.mr.load_stores()
        self.mr.run_block("fights", stores, repeats=2)
        self.mr.run_block("extends", stores, repeats=2)
        rows = self.mr._load_rows()
        fights = [r for r in rows if r["side"] == "fights"]
        extends = [r for r in rows if r["side"] == "extends"]
        self.assertEqual(len(fights), 4)
        self.assertEqual(len(extends), 4)
        self.assertTrue(all(r["family"] == "chunk_pad" for r in fights))
        self.assertTrue(all(r["family"] == "token_case"
                            for r in extends))

    def test_recensus_replays_from_summaries(self):
        self._stub_run(lambda f, i: True)
        self.mr.gate_side("extends", repeats=2)
        mismatches = self.mr.recensus(self.mr._ROWS,
                                      runs_dir=runner.RUNS)
        self.assertEqual(mismatches, 0)


if __name__ == "__main__":
    unittest.main()
