"""Tests for the PACKET-025 shape-steering replication harness. Stub
runner, temp runs dir, no model calls. The balanced classifier must be
selfdeliv24's by identity, unchanged."""

import importlib
import json
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import runner


class _ShapeSteer25Harness(unittest.TestCase):

    def setUp(self):
        self._real_runs = runner.RUNS
        self._real_run_once = runner.run_once
        self._tmp = tempfile.TemporaryDirectory()
        runner.RUNS = self._tmp.name
        import shapesteer25
        self.ss = importlib.reload(shapesteer25)

    def tearDown(self):
        runner.RUNS = self._real_runs
        runner.run_once = self._real_run_once
        importlib.reload(self.ss)
        self._tmp.cleanup()

    def _stub_run(self, rule_ok_fn, output_fn=None):
        """Stub whose rule-check outcomes follow rule_ok_fn(rep_i) per
        cell-call order and whose output follows output_fn; non-rule
        checks always pass. None means unrunnable."""
        calls = []

        def stub(task, criteria, work_features, **kw):
            seen = len(calls)
            calls.append({"kw": kw})
            verdict_ok = rule_ok_fn(seen)
            output = (output_fn(seen) if output_fn
                      else "def f():\n    return 1\n")
            if verdict_ok is None:
                results = []
                output = "def f(:\n"
            else:
                rule_checks = set(
                    self.ss._TASKS[self.ss.TASK]["rule_checks"])
                results = []
                for c in self.ss._TASKS[self.ss.TASK]["checks"]:
                    ok = (verdict_ok if c["call"] in rule_checks
                          else True)
                    results.append({"ok": ok, "call": c["call"],
                                    "got": "x", "expect": c["expect"]})
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


SWEEP = """```python
def balanced(s):
    depth = 0
    for ch in s:
        if ch == '(':
            depth += 1
        elif ch == ')':
            depth -= 1
            if depth < 0:
                return False
    return depth == 0
```"""

SHORTCUT = """```python
def balanced(s):
    return s.count('(') == s.count(')')
```"""


class TestClassifierPin(_ShapeSteer25Harness):

    def test_classifier_is_selfdeliv24s_by_identity(self):
        import selfdeliv24
        self.assertIs(self.ss._BALANCED_CLASSIFIER,
                      selfdeliv24._shape_balanced)
        self.assertEqual(self.ss.TAXONOMY,
                         selfdeliv24.CENSUS_TAXONOMY["balanced"])

    def test_census_shape_matches_selfdeliv24_whole_path(self):
        import selfdeliv24
        for sample in (SWEEP, SHORTCUT, "def f(:\n"):
            self.assertEqual(self.ss.census_shape(sample),
                             selfdeliv24.census_shape("balanced",
                                                      sample))

    def test_shapes(self):
        self.assertEqual(self.ss.census_shape(SWEEP),
                         "counter-or-stack sweep")
        self.assertEqual(self.ss.census_shape(SHORTCUT),
                         "count-equality shortcut")
        self.assertEqual(self.ss.census_shape("def f(:\n"),
                         "unrunnable")


class TestMaterials(_ShapeSteer25Harness):

    def test_byte_check_and_store(self):
        self.assertTrue(self.ss.byte_check())
        store = self.ss.load_store()
        les = store[0]
        self.assertEqual(les["trail"]["gen_task"], "depth_max")
        self.assertEqual(les["trail"]["origin_seat"], "mistral:7b")
        self.assertEqual(les["applies_when"]["rule_class"], "normalize")
        self.assertEqual(les["applies_when"]["rule_topic"],
                         "delimiters")

    def test_touched_store_refused(self):
        bad = os.path.join(self._tmp.name, "touched.jsonl")
        with open(self.ss.STORE, "rb") as f:
            original = f.read()
        with open(bad, "wb") as f:
            f.write(original + b"\n")
        self.ss.STORE = bad
        with self.assertRaises(SystemExit):
            self.ss.byte_check()

    def test_lesson_rides_balanced_only_when_armed(self):
        store = self.ss.load_store()
        self.assertEqual(
            len(self.ss.cell_tools("armed-N2", store)), 1)
        self.assertEqual(self.ss.cell_tools("none", store), [])

    def test_bars_and_annotation(self):
        self.assertEqual(self.ss.RULE_N, 2)
        self.assertEqual(self.ss.QUALIFY_MIN, 4)
        self.assertEqual(self.ss.RULE_BAR, 4)
        self.assertEqual(self.ss.CENSUS_BAR, 2)
        t = self.ss._TASKS[self.ss.TASK]
        self.assertEqual(len(t["rule_checks"]), 2)


class TestStageA(_ShapeSteer25Harness):

    def test_exact_four_of_24_qualifies(self):
        self._stub_run(lambda i: i < 2)
        result = self.ss.qualify(repeats=12)
        self.assertEqual(result["pooled"]["n"], 24)
        self.assertEqual(result["pooled"]["passed"], 4)
        self.assertTrue(result["qualified"])

    def test_floor_and_ceiling_refuse(self):
        self._stub_run(lambda i: False)
        self.assertFalse(self.ss.qualify(repeats=12)["qualified"])
        self._stub_run(lambda i: True)
        self.assertFalse(self.ss.qualify(repeats=12)["qualified"])

    def test_unrunnable_counts_as_fail(self):
        # 2 passing reps, 8 failing, 2 unrunnable: canonical 4 passes
        # 20 fails of 24, qualifies.
        def outcomes(i):
            if i < 2:
                return True
            if i >= 10:
                return None
            return False
        self._stub_run(outcomes)
        result = self.ss.qualify(repeats=12)
        self.assertEqual(result["pooled"]["passed"], 4)
        self.assertEqual(result["pooled"]["unrunnable_rows"], 2)
        self.assertTrue(result["qualified"])


class TestStageB(_ShapeSteer25Harness):

    def test_interleave_audit_and_sweep_counts(self):
        self._stub_run(lambda i: i % 2 == 0,
                       output_fn=lambda i: SWEEP)
        store = self.ss.load_store()
        self.ss.qualify(repeats=2)
        rows = self.ss.run_block(store, repeats=2)
        self.assertEqual([r["cell"] for r in rows],
                         ["none", "armed-N2"] * 2)
        for r in rows:
            self.assertEqual(r["tools"],
                             self.ss.EXPECT_TOOLS[r["cell"]])
        # sweep_counts reads stage B only: 2 per cell here, and the
        # stage A rows never enter it.
        counts = self.ss.sweep_counts(self.ss._load_rows())
        self.assertEqual(counts, {"none": 2, "armed-N2": 2})

    def test_census_distinguishes_cells(self):
        self._stub_run(
            lambda i: True,
            output_fn=lambda i: SHORTCUT if i % 2 == 0 else SWEEP)
        store = self.ss.load_store()
        rows = self.ss.run_block(store, repeats=2)
        counts = self.ss.sweep_counts(rows)
        self.assertEqual(counts, {"none": 0, "armed-N2": 2})

    def test_resume_no_reruns(self):
        self._stub_run(lambda i: True)
        store = self.ss.load_store()
        self.ss.qualify(repeats=2)
        self.ss.run_block(store, repeats=2)
        prior = self.ss._load_rows()
        calls = self._stub_run(lambda i: True)
        r1 = self.ss.qualify(repeats=2, prior_rows=prior)
        r2 = self.ss.run_block(store, repeats=2, prior_rows=prior)
        self.assertEqual(calls, [])
        self.assertEqual(r1["pooled"]["n"], 4)
        self.assertEqual(len(r2), 4)

    def test_recensus_replays_from_summaries(self):
        self._stub_run(lambda i: True, output_fn=lambda i: SWEEP)
        self.ss.qualify(repeats=2)
        mismatches = self.ss.recensus(self.ss._ROWS,
                                      runs_dir=runner.RUNS)
        self.assertEqual(mismatches, 0)


if __name__ == "__main__":
    unittest.main()
