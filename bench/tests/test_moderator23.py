"""Tests for the PACKET-023 moderator-test harness. Stub runner, temp
runs dir, no model calls. The census classifier is tested on
hand-written code shapes so the conductor's replay has a pinned
meaning."""

import importlib
import json
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import runner


class _Moderator23Harness(unittest.TestCase):

    def setUp(self):
        self._real_runs = runner.RUNS
        self._real_run_once = runner.run_once
        self._tmp = tempfile.TemporaryDirectory()
        runner.RUNS = self._tmp.name
        import moderator23
        self.md = importlib.reload(moderator23)

    def tearDown(self):
        runner.RUNS = self._real_runs
        runner.run_once = self._real_run_once
        importlib.reload(self.md)
        self._tmp.cleanup()

    def _stub_run(self, rule_ok_fn, output_fn=None):
        """Stub whose rule-check outcomes follow rule_ok_fn(task, rep_i)
        and whose output text follows output_fn(task, rep_i); non-rule
        checks always pass. rule_ok_fn returning None means the run is
        unrunnable: no readings at all and a broken output."""
        calls = []

        def stub(task, criteria, work_features, **kw):
            name = next(n for n in self.md._TASKS
                        if self.md._TASKS[n]["task"] == task)
            seen = sum(1 for c in calls if c["name"] == name)
            calls.append({"name": name, "kw": kw})
            verdict_ok = rule_ok_fn(name, seen)
            output = (output_fn(name, seen) if output_fn
                      else "def f():\n    return sorted([1])[0]\n")
            if verdict_ok is None:
                results = []
                output = "def f(:\n"
            else:
                rule_checks = set(self.md._TASKS[name]["rule_checks"])
                results = []
                for c in self.md._TASKS[name]["checks"]:
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


FLAT_COMPREHENSION = """```python
def flatten_once(lst):
    return [item for sub in lst for item in sub]
```"""

FLAT_COMPREHENSION_IFEXP = """```python
def flatten_once(lst):
    return [i for x in lst for i in (x if isinstance(x, list) else [x])]
```"""

FLAT_LOOP_BRANCH = """```python
def flatten_once(lst):
    out = []
    for x in lst:
        if isinstance(x, list):
            out.extend(x)
        else:
            out.append(x)
    return out
```"""

FLAT_LOOP_IFEXP = """```python
def flatten_once(lst):
    out = []
    for x in lst:
        out.extend(x if isinstance(x, list) else [x])
    return out
```"""

FLAT_ILLEGAL = """```python
def flatten_once(lst):
    return [x for x in lst if not isinstance(x, list) else x]
```"""

FLAT_CHAIN = """```python
from itertools import chain
def flatten_once(lst):
    return list(chain.from_iterable(lst))
```"""

MERGE_SWEEP = """```python
def merge_ranges(pairs):
    out = []
    for start, end in sorted(pairs):
        if out and start <= out[-1][1]:
            out[-1][1] = max(out[-1][1], end)
        else:
            out.append([start, end])
    return out
```"""

MERGE_NO_SORT = """```python
def merge_ranges(pairs):
    return pairs
```"""

MEDIAN_SORT_INDEX = """```python
def median(nums):
    if not nums:
        return None
    s = sorted(nums)
    m = len(s) // 2
    return s[m] if len(s) % 2 else (s[m - 1] + s[m]) / 2
```"""

MEDIAN_STATISTICS = """```python
import statistics
def median(nums):
    return statistics.median(nums) if nums else None
```"""


class TestCensusClassifier(_Moderator23Harness):

    def test_flatten_once_shapes(self):
        cs = self.md.census_shape
        self.assertEqual(cs("flatten_once", FLAT_COMPREHENSION),
                         "comprehension")
        self.assertEqual(cs("flatten_once", FLAT_COMPREHENSION_IFEXP),
                         "comprehension")
        self.assertEqual(cs("flatten_once", FLAT_LOOP_BRANCH),
                         "loop-with-branch")
        self.assertEqual(cs("flatten_once", FLAT_LOOP_IFEXP),
                         "loop-with-branch")
        self.assertEqual(cs("flatten_once", FLAT_ILLEGAL), "unrunnable")
        self.assertEqual(cs("flatten_once", FLAT_CHAIN), "other")

    def test_merge_ranges_shapes(self):
        cs = self.md.census_shape
        self.assertEqual(cs("merge_ranges", MERGE_SWEEP), "sweep")
        self.assertEqual(cs("merge_ranges", MERGE_NO_SORT), "other")

    def test_median_shapes(self):
        cs = self.md.census_shape
        self.assertEqual(cs("median", MEDIAN_SORT_INDEX),
                         "sort-and-index")
        self.assertEqual(cs("median", MEDIAN_STATISTICS), "other")

    def test_taxonomy_covers_all_grounds(self):
        for block in self.md.BLOCKS:
            for name in self.md.SWEEPS[block]:
                self.assertIn(name, self.md.CENSUS_TAXONOMY)


class TestMaterials(_Moderator23Harness):

    def test_byte_check_and_store(self):
        self.assertTrue(self.md.byte_check())
        store = self.md.load_store()
        les = store[0]
        self.assertEqual(les["trail"]["gen_task"], "chunk")
        self.assertEqual(les["trail"]["origin_seat"], "mistral:7b")
        self.assertEqual(les["applies_when"]["rule_class"], "boundary")
        self.assertEqual(les["applies_when"]["rule_topic"], "degenerate")

    def test_wildcard_lesson_structurally_absent(self):
        """The weighted_mean wildcard lesson is blocked to qwen by
        standing rule; the single-lesson store makes the block
        structural."""
        store = self.md.load_store()
        self.assertEqual(len(store), 1)
        self.assertNotEqual(store[0]["trail"]["gen_task"],
                            "weighted_mean")

    def test_touched_store_refused(self):
        bad = os.path.join(self._tmp.name, "touched.jsonl")
        with open(self.md.STORE, "rb") as f:
            original = f.read()
        with open(bad, "wb") as f:
            f.write(original + b"\n")
        self.md.STORE = bad
        with self.assertRaises(SystemExit):
            self.md.byte_check()

    def test_lesson_rides_all_three_grounds(self):
        store = self.md.load_store()
        for name in ("flatten_once", "merge_ranges", "median"):
            self.assertEqual(
                len(self.md.cell_tools("armed", store, name)), 1, name)
            self.assertEqual(
                self.md.cell_tools("none", store, name), [])

    def test_annotations_and_scaling(self):
        expected = {"flatten_once": 1, "merge_ranges": 1, "median": 2}
        for name, n in expected.items():
            t = self.md._TASKS[name]
            self.assertEqual(len(t["rule_checks"]), n, name)
            self.assertEqual(self.md.qualify_min(name), 2 * n, name)
            self.assertEqual(self.md.drift_bar(name), 2 * n, name)


class TestAccounting(_Moderator23Harness):

    def test_unrunnable_counts_as_fail_in_pooled(self):
        """DECISIONS 2026-07-04: canonical pooled counts hold n at
        rows x rule checks, missing readings count as fails, and the
        diagnostic keeps the readings-present view."""
        rows = [{"cell": "none", "checks":
                 {"flatten_once([1, [2, [3, 4]]])": True,
                  "flatten_once([])": True}},
                {"cell": "none", "checks": {}},
                {"cell": "none", "checks":
                 {"flatten_once([1, [2, [3, 4]]])": False,
                  "flatten_once([])": True}}]
        p = self.md.pooled_rule(rows, "flatten_once")
        self.assertEqual(p["n"], 3)
        self.assertEqual(p["passed"], 1)
        self.assertEqual(p["present_n"], 2)
        self.assertEqual(p["present_passed"], 1)
        self.assertEqual(p["unrunnable_rows"], 1)

    def test_qualification_with_unrunnable_rows(self):
        # 2 rule passes, 8 rule fails, 2 unrunnable of 12: canonical
        # counts 2 passes 10 fails, qualifies on one-rule ground.
        def outcomes(name, rep):
            if rep < 2:
                return True
            if rep >= 10:
                return None
            return False
        self._stub_run(outcomes)
        result = self.md.qualify("fights", "flatten_once", repeats=12)
        self.assertEqual(result["pooled"]["n"], 12)
        self.assertEqual(result["pooled"]["passed"], 2)
        self.assertEqual(result["pooled"]["unrunnable_rows"], 2)
        self.assertTrue(result["qualified"])

    def test_floor_and_ceiling_do_not_qualify(self):
        self._stub_run(lambda name, rep: False)
        self.assertFalse(
            self.md.qualify("fights", "flatten_once",
                            repeats=12)["qualified"])
        self._stub_run(lambda name, rep: True)
        self.assertFalse(
            self.md.qualify("fights", "flatten_once",
                            repeats=12)["qualified"])


class TestSweepsAndStageB(_Moderator23Harness):

    def test_sweep_stops_at_first_qualifier(self):
        calls = self._stub_run(lambda name, rep: rep % 2 == 0)
        results, ground = self.md.sweep("fights", repeats=12)
        self.assertEqual(ground, "flatten_once")
        self.assertEqual({c["name"] for c in calls}, {"flatten_once"})

    def test_exhausted_sweep_closes_on_supply(self):
        calls = self._stub_run(lambda name, rep: True)
        results, ground = self.md.sweep("extends", repeats=12)
        self.assertIsNone(ground)
        self.assertEqual([r["task"] for r in results], ["median"])

    def test_interleave_audit_and_census_rows(self):
        self._stub_run(lambda name, rep: rep % 2 == 0,
                       output_fn=lambda name, rep: FLAT_LOOP_BRANCH)
        store = self.md.load_store()
        rows = self.md.run_block("fights", "flatten_once", store,
                                 repeats=2)
        self.assertEqual([r["cell"] for r in rows],
                         ["none", "armed"] * 2)
        for r in rows:
            self.assertEqual(r["tools"],
                             self.md.EXPECT_TOOLS[r["cell"]])
            self.assertEqual(r["shape"], "loop-with-branch")
            self.assertFalse(r["no_readings"])

    def test_census_table_and_resume(self):
        self._stub_run(lambda name, rep: True,
                       output_fn=lambda name, rep: FLAT_COMPREHENSION)
        store = self.md.load_store()
        self.md.qualify("fights", "flatten_once", repeats=2)
        self.md.run_block("fights", "flatten_once", store, repeats=2)
        rows = self.md._load_rows()
        table = self.md.census_table(rows)
        self.assertEqual(
            table["A|fights|flatten_once|none"]["comprehension"], 2)
        self.assertEqual(
            table["B|fights|flatten_once|armed"]["comprehension"], 2)
        calls = self._stub_run(lambda name, rep: True)
        r1 = self.md.qualify("fights", "flatten_once", repeats=2,
                             prior_rows=rows)
        r2 = self.md.run_block("fights", "flatten_once", store,
                               repeats=2, prior_rows=rows)
        self.assertEqual(calls, [])
        self.assertEqual(r1["pooled"]["n"], 2)
        self.assertEqual(len(r2), 4)

    def test_recensus_replays_from_summaries(self):
        self._stub_run(lambda name, rep: True,
                       output_fn=lambda name, rep: FLAT_COMPREHENSION)
        self.md.qualify("fights", "flatten_once", repeats=2)
        mismatches = self.md.recensus(self.md._ROWS,
                                      runs_dir=runner.RUNS)
        self.assertEqual(mismatches, 0)


if __name__ == "__main__":
    unittest.main()
