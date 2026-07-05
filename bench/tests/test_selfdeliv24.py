"""Tests for the PACKET-024 self-delivery harness. Stub runner, temp
runs dir, no model calls. The two new census classifiers are pinned on
hand-written shapes; the three reused ones are asserted identical to
moderator23's, imported not copied."""

import importlib
import json
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import runner


class _SelfDeliv24Harness(unittest.TestCase):

    def setUp(self):
        self._real_runs = runner.RUNS
        self._real_run_once = runner.run_once
        self._tmp = tempfile.TemporaryDirectory()
        runner.RUNS = self._tmp.name
        import selfdeliv24
        self.sd = importlib.reload(selfdeliv24)

    def tearDown(self):
        runner.RUNS = self._real_runs
        runner.run_once = self._real_run_once
        importlib.reload(self.sd)
        self._tmp.cleanup()

    def _stub_run(self, rule_ok_fn, output_fn=None):
        """Stub whose rule-check outcomes follow rule_ok_fn(task, rep_i)
        and whose output follows output_fn(task, rep_i); non-rule checks
        always pass. rule_ok_fn returning None means unrunnable."""
        calls = []

        def stub(task, criteria, work_features, **kw):
            name = next(n for n in self.sd._TASKS
                        if self.sd._TASKS[n]["task"] == task)
            seen = sum(1 for c in calls if c["name"] == name)
            calls.append({"name": name, "kw": kw})
            verdict_ok = rule_ok_fn(name, seen)
            output = (output_fn(name, seen) if output_fn
                      else "def f():\n    return sorted([1])[0]\n")
            if verdict_ok is None:
                results = []
                output = "def f(:\n"
            else:
                rule_checks = set(self.sd._TASKS[name]["rule_checks"])
                results = []
                for c in self.sd._TASKS[name]["checks"]:
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


CAMEL_SPLIT_JOIN = """```python
def snake_to_camel(s):
    parts = [p for p in s.split('_') if p]
    if not parts:
        return ''
    return parts[0] + ''.join(p.capitalize() for p in parts[1:])
```"""

CAMEL_SPLIT_LOOP = """```python
def snake_to_camel(s):
    parts = s.split('_')
    out = ''
    for p in parts:
        if p:
            out += p.capitalize() if out else p
    return out
```"""

CAMEL_REGEX = """```python
import re
def snake_to_camel(s):
    s = re.sub(r'_+', '_', s).strip('_')
    parts = s.split('_')
    return parts[0] + ''.join(p.title() for p in parts[1:]) if parts else ''
```"""

CAMEL_CHAR_WALK = """```python
def snake_to_camel(s):
    out = []
    up = False
    for ch in s:
        if ch == '_':
            up = bool(out)
        else:
            out.append(ch.upper() if up else ch)
            up = False
    return ''.join(out)
```"""

CAMEL_OTHER = """```python
def snake_to_camel(s):
    return s.title().replace('_', '')
```"""

BALANCED_COUNTER_SWEEP = """```python
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

BALANCED_STACK_SWEEP = """```python
def balanced(s):
    stack = []
    for ch in s:
        if ch == '(':
            stack.append(ch)
        elif ch == ')':
            if not stack:
                return False
            stack.pop()
    return not stack
```"""

BALANCED_COUNT_SHORTCUT = """```python
def balanced(s):
    return s.count('(') == s.count(')')
```"""

BALANCED_SUM_SHORTCUT = """```python
def balanced(s):
    return sum(1 for c in s if c == '(') == sum(1 for c in s if c == ')')
```"""

BALANCED_HYBRID = """```python
def balanced(s):
    if s.count('(') != s.count(')'):
        return False
    depth = 0
    for ch in s:
        if ch == '(':
            depth += 1
        elif ch == ')':
            depth -= 1
        if depth < 0:
            return False
    return True
```"""

BALANCED_REPLACE_OTHER = """```python
def balanced(s):
    t = ''.join(c for c in s if c in '()')
    while '()' in t:
        t = t.replace('()', '')
    return not t
```"""


class TestNewClassifiers(_SelfDeliv24Harness):

    def test_snake_to_camel_shapes(self):
        cs = self.sd.census_shape
        self.assertEqual(cs("snake_to_camel", CAMEL_SPLIT_JOIN),
                         "split-and-join")
        self.assertEqual(cs("snake_to_camel", CAMEL_SPLIT_LOOP),
                         "split-and-join")
        self.assertEqual(cs("snake_to_camel", CAMEL_REGEX), "regex")
        self.assertEqual(cs("snake_to_camel", CAMEL_CHAR_WALK),
                         "char-walk")
        self.assertEqual(cs("snake_to_camel", CAMEL_OTHER), "other")
        self.assertEqual(cs("snake_to_camel", "def f(:\n"),
                         "unrunnable")

    def test_balanced_shapes(self):
        cs = self.sd.census_shape
        self.assertEqual(cs("balanced", BALANCED_COUNTER_SWEEP),
                         "counter-or-stack sweep")
        self.assertEqual(cs("balanced", BALANCED_STACK_SWEEP),
                         "counter-or-stack sweep")
        self.assertEqual(cs("balanced", BALANCED_HYBRID),
                         "counter-or-stack sweep")
        self.assertEqual(cs("balanced", BALANCED_COUNT_SHORTCUT),
                         "count-equality shortcut")
        self.assertEqual(cs("balanced", BALANCED_SUM_SHORTCUT),
                         "count-equality shortcut")
        self.assertEqual(cs("balanced", BALANCED_REPLACE_OTHER),
                         "other")

    def test_moderator23_classifiers_reused_unchanged(self):
        """The packet requires the three moderator23 classifiers reused
        unchanged: identity, not a copy."""
        import moderator23
        for name, fn in (("merge_ranges",
                          moderator23._shape_merge_ranges),
                         ("median", moderator23._shape_median),
                         ("flatten_once",
                          moderator23._shape_flatten_once)):
            self.assertIs(self.sd._CLASSIFIERS[name], fn, name)
            self.assertEqual(self.sd.CENSUS_TAXONOMY[name],
                             moderator23.CENSUS_TAXONOMY[name], name)

    def test_taxonomy_covers_all_grounds(self):
        for block in self.sd.BLOCKS:
            for name in self.sd.SWEEPS[block]:
                self.assertIn(name, self.sd.CENSUS_TAXONOMY)


class TestMaterials(_SelfDeliv24Harness):

    def test_byte_checks_and_stores(self):
        checks = self.sd.byte_checks()
        self.assertEqual(sorted(checks), sorted(self.sd.ARMS))
        self.assertTrue(all(checks.values()))
        stores = self.sd.load_stores()
        gen = {"armed-B1": "chunk", "armed-B2": "weighted_mean",
               "armed-N1": "split_csvish", "armed-N2": "depth_max"}
        for key, gt in gen.items():
            les = stores[key][0]
            self.assertEqual(les["trail"]["gen_task"], gt)
            self.assertEqual(les["trail"]["origin_seat"], "mistral:7b")

    def test_touched_store_refused(self):
        bad = os.path.join(self._tmp.name, "touched.jsonl")
        with open(self.sd.ARMS["armed-B2"]["path"], "rb") as f:
            original = f.read()
        with open(bad, "wb") as f:
            f.write(original + b"\n")
        self.sd.ARMS = {**self.sd.ARMS,
                        "armed-B2": {**self.sd.ARMS["armed-B2"],
                                     "path": bad}}
        with self.assertRaises(SystemExit):
            self.sd.byte_checks()

    def test_lessons_ride_their_class_grounds_only(self):
        stores = self.sd.load_stores()
        for block, cells in (("boundary", ("armed-B1", "armed-B2")),
                             ("normalize", ("armed-N1", "armed-N2"))):
            for name in self.sd.SWEEPS[block]:
                self.assertEqual(
                    self.sd.cell_tools("none", stores, name), [])
                for cell in cells:
                    self.assertEqual(
                        len(self.sd.cell_tools(cell, stores, name)), 1,
                        f"{cell} on {name}")
        import menu
        for cell, name in (("armed-B1", "snake_to_camel"),
                           ("armed-N1", "merge_ranges")):
            tools = menu.query(stores[cell],
                               self.sd._features(self.sd._TASKS[name]))
            self.assertEqual(tools, [], f"{cell} on {name}")

    def test_annotations_and_scaling(self):
        expected = {"merge_ranges": 1, "median": 2, "flatten_once": 1,
                    "snake_to_camel": 1, "balanced": 2}
        for name, n in expected.items():
            t = self.sd._TASKS[name]
            self.assertEqual(len(t["rule_checks"]), n, name)
            self.assertEqual(self.sd.qualify_min(name), 2 * n, name)
            self.assertEqual(self.sd.drift_bar(name), 2 * n, name)


class TestAccountingAndSweeps(_SelfDeliv24Harness):

    def test_unrunnable_counts_as_fail_in_pooled(self):
        rows = [{"cell": "none", "checks":
                 {"snake_to_camel('__a__b_')": True,
                  "snake_to_camel('')": True}},
                {"cell": "none", "checks": {}},
                {"cell": "none", "checks":
                 {"snake_to_camel('__a__b_')": False,
                  "snake_to_camel('')": True}}]
        p = self.sd.pooled_rule(rows, "snake_to_camel")
        self.assertEqual(p["n"], 3)
        self.assertEqual(p["passed"], 1)
        self.assertEqual(p["present_n"], 2)
        self.assertEqual(p["unrunnable_rows"], 1)

    def test_qualification_with_unrunnable_rows(self):
        # 2 rule passes, 8 fails, 2 unrunnable of 12: canonical 2
        # passes 10 fails, qualifies on one-rule ground.
        def outcomes(name, rep):
            if rep < 2:
                return True
            if rep >= 10:
                return None
            return False
        self._stub_run(outcomes)
        result = self.sd.qualify("boundary", "merge_ranges", repeats=12)
        self.assertEqual(result["pooled"]["n"], 12)
        self.assertEqual(result["pooled"]["passed"], 2)
        self.assertEqual(result["pooled"]["unrunnable_rows"], 2)
        self.assertTrue(result["qualified"])

    def test_two_rule_arithmetic_exactly_four(self):
        self._stub_run(lambda name, rep: rep < 2)
        result = self.sd.qualify("normalize", "balanced", repeats=12)
        self.assertEqual(result["pooled"]["n"], 24)
        self.assertEqual(result["pooled"]["passed"], 4)
        self.assertTrue(result["qualified"])

    def test_floor_and_ceiling_do_not_qualify(self):
        self._stub_run(lambda name, rep: False)
        self.assertFalse(
            self.sd.qualify("boundary", "merge_ranges",
                            repeats=12)["qualified"])
        self._stub_run(lambda name, rep: True)
        self.assertFalse(
            self.sd.qualify("boundary", "merge_ranges",
                            repeats=12)["qualified"])

    def test_sweep_stops_at_first_qualifier(self):
        calls = self._stub_run(lambda name, rep: rep % 2 == 0)
        results, ground = self.sd.sweep("boundary", repeats=12)
        self.assertEqual(ground, "merge_ranges")
        self.assertEqual({c["name"] for c in calls}, {"merge_ranges"})

    def test_exhausted_sweep_closes_on_supply(self):
        calls = self._stub_run(lambda name, rep: True)
        results, ground = self.sd.sweep("normalize", repeats=12)
        self.assertIsNone(ground)
        self.assertEqual([r["task"] for r in results],
                         ["snake_to_camel", "balanced"])


class TestStageB(_SelfDeliv24Harness):

    def test_interleave_audit_and_census(self):
        calls = self._stub_run(
            lambda name, rep: rep % 2 == 0,
            output_fn=lambda name, rep: BALANCED_STACK_SWEEP)
        stores = self.sd.load_stores()
        rows = self.sd.run_block("normalize", "balanced", stores,
                                 repeats=2)
        self.assertEqual([r["cell"] for r in rows],
                         ["none", "armed-N1", "armed-N2"] * 2)
        for r in rows:
            self.assertEqual(r["tools"],
                             self.sd.EXPECT_TOOLS[r["cell"]])
            self.assertEqual(r["shape"], "counter-or-stack sweep")
        armed_calls = [c for c in calls
                       if c["kw"].get("landscape") is not None]
        self.assertEqual(len(armed_calls), 4)

    def test_resume_separates_stages_and_blocks(self):
        self._stub_run(lambda name, rep: True)
        stores = self.sd.load_stores()
        self.sd.qualify("boundary", "merge_ranges", repeats=2)
        self.sd.run_block("boundary", "merge_ranges", stores, repeats=2)
        self.sd.run_block("normalize", "balanced", stores, repeats=2)
        prior = self.sd._load_rows()
        calls = self._stub_run(lambda name, rep: True)
        r1 = self.sd.qualify("boundary", "merge_ranges", repeats=2,
                             prior_rows=prior)
        r2 = self.sd.run_block("boundary", "merge_ranges", stores,
                               repeats=2, prior_rows=prior)
        r3 = self.sd.run_block("normalize", "balanced", stores,
                               repeats=2, prior_rows=prior)
        self.assertEqual(calls, [])
        self.assertEqual(r1["pooled"]["n"], 2)
        self.assertEqual(len(r2), 6)
        self.assertEqual(len(r3), 6)

    def test_recensus_replays_from_summaries(self):
        self._stub_run(lambda name, rep: True,
                       output_fn=lambda name, rep: CAMEL_SPLIT_JOIN)
        self.sd.qualify("normalize", "snake_to_camel", repeats=2)
        mismatches = self.sd.recensus(self.sd._ROWS,
                                      runs_dir=runner.RUNS)
        self.assertEqual(mismatches, 0)


if __name__ == "__main__":
    unittest.main()
