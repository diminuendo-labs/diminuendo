"""Tests for the PACKET-022 arm-the-floors harness. Stub runner, temp
runs dir, no model calls."""

import importlib
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import runner


class _ArmFloors22Harness(unittest.TestCase):

    def setUp(self):
        self._real_runs = runner.RUNS
        self._real_run_once = runner.run_once
        self._tmp = tempfile.TemporaryDirectory()
        runner.RUNS = self._tmp.name
        import armfloors22
        self.af = importlib.reload(armfloors22)

    def tearDown(self):
        runner.RUNS = self._real_runs
        runner.run_once = self._real_run_once
        importlib.reload(self.af)
        self._tmp.cleanup()

    def _stub_run(self, rule_ok_fn):
        """Stub whose rule-check outcomes follow rule_ok_fn(task, rep_i);
        non-rule checks always pass."""
        calls = []

        def stub(task, criteria, work_features, **kw):
            name = next(n for n in self.af._TASKS
                        if self.af._TASKS[n]["task"] == task)
            seen = sum(1 for c in calls if c["name"] == name)
            calls.append({"name": name, "kw": kw})
            rule_checks = set(self.af._TASKS[name]["rule_checks"])
            results = []
            for c in self.af._TASKS[name]["checks"]:
                ok = (rule_ok_fn(name, seen) if c["call"] in rule_checks
                      else True)
                results.append({"ok": ok, "call": c["call"],
                                "got": "x", "expect": c["expect"]})
            return {"run_id": f"stub-{len(calls)}", "verdict": "pass",
                    "evidence": {"passed": all(r["ok"] for r in results),
                                 "results": results, "error": None}}

        runner.run_once = stub
        return calls


class TestMaterials(_ArmFloors22Harness):

    def test_annotations_cover_every_candidate(self):
        """Each sweep candidate carries the standing annotation, and the
        qualification arithmetic scales with it: one-rule grounds need
        2 of 12 pooled, two-rule grounds 4 of 24."""
        expected = {"merge_ranges": 1, "median": 2, "flatten_once": 1,
                    "snake_to_camel": 1, "balanced": 2}
        for name, n in expected.items():
            t = self.af._TASKS[name]
            self.assertEqual(len(t["rule_checks"]), n, name)
            calls = {c["call"] for c in t["checks"]}
            self.assertTrue(set(t["rule_checks"]) <= calls, name)
            self.assertEqual(self.af.qualify_min(name), 2 * n, name)
            self.assertEqual(self.af.drift_bar(name), 2 * n, name)

    def test_byte_checks_and_stores(self):
        checks = self.af.byte_checks()
        self.assertEqual(sorted(checks), sorted(self.af.ARMS))
        self.assertTrue(all(checks.values()))
        stores = self.af.load_stores()
        gen = {"armed-B1": "chunk", "armed-B2": "weighted_mean",
               "armed-N1": "split_csvish", "armed-N2": "depth_max"}
        for key, gt in gen.items():
            les = stores[key][0]
            self.assertEqual(les["trail"]["gen_task"], gt)
            self.assertEqual(les["trail"]["origin_seat"], "mistral:7b")
            self.assertEqual(les["provenance"], "engine")
        self.assertEqual(stores["armed-B2"][0]["applies_when"]
                         ["rule_topic"], "*")

    def test_touched_store_refused(self):
        bad = os.path.join(self._tmp.name, "touched.jsonl")
        with open(self.af.ARMS["armed-N2"]["path"], "rb") as f:
            original = f.read()
        with open(bad, "wb") as f:
            f.write(original + b"\n")
        self.af.ARMS = {**self.af.ARMS,
                        "armed-N2": {**self.af.ARMS["armed-N2"],
                                     "path": bad}}
        with self.assertRaises(SystemExit):
            self.af.byte_checks()

    def test_lessons_ride_their_class_grounds_only(self):
        """Boundary lessons serve exactly one tool on every boundary
        candidate (the wildcard topic pin included), normalize lessons
        on every normalize candidate, and never across classes."""
        stores = self.af.load_stores()
        for block, cells in (("boundary", ("armed-B1", "armed-B2")),
                             ("normalize", ("armed-N1", "armed-N2"))):
            for name in self.af.SWEEPS[block]:
                self.assertEqual(
                    self.af.cell_tools("none", stores, name), [])
                for cell in cells:
                    self.assertEqual(
                        len(self.af.cell_tools(cell, stores, name)), 1,
                        f"{cell} on {name}")
        import menu
        for cell, name in (("armed-B1", "snake_to_camel"),
                           ("armed-N1", "merge_ranges")):
            tools = menu.query(stores[cell],
                               self.af._features(self.af._TASKS[name]))
            self.assertEqual(tools, [], f"{cell} on {name}")


class TestStageA(_ArmFloors22Harness):

    def test_one_rule_arithmetic_exactly_two(self):
        # merge_ranges has one rule check: 2 passes and 10 fails of 12
        # qualifies by the letter, 1 pass does not.
        self._stub_run(lambda name, rep: rep < 2)
        result = self.af.qualify("boundary", "merge_ranges", repeats=12)
        self.assertEqual(result["pooled"]["n"], 12)
        self.assertEqual(result["pooled"]["passed"], 2)
        self.assertTrue(result["qualified"])
        self._stub_run(lambda name, rep: rep < 1)
        result = self.af.qualify("boundary", "merge_ranges", repeats=12)
        self.assertEqual(result["pooled"]["passed"], 1)
        self.assertFalse(result["qualified"])

    def test_two_rule_arithmetic_exactly_four(self):
        # median has two rule checks: 2 reps x 2 checks = 4 of 24.
        self._stub_run(lambda name, rep: rep < 2)
        result = self.af.qualify("boundary", "median", repeats=12)
        self.assertEqual(result["pooled"]["n"], 24)
        self.assertEqual(result["pooled"]["passed"], 4)
        self.assertTrue(result["qualified"])

    def test_floor_and_ceiling_do_not_qualify(self):
        self._stub_run(lambda name, rep: False)
        self.assertFalse(
            self.af.qualify("boundary", "merge_ranges",
                            repeats=12)["qualified"])
        self._stub_run(lambda name, rep: True)
        self.assertFalse(
            self.af.qualify("boundary", "merge_ranges",
                            repeats=12)["qualified"])

    def test_sweep_stops_at_first_qualifier(self):
        calls = self._stub_run(lambda name, rep: rep % 2 == 0)
        results, ground = self.af.sweep("boundary", repeats=12)
        self.assertEqual(ground, "merge_ranges")
        self.assertEqual(len(results), 1)
        self.assertEqual({c["name"] for c in calls}, {"merge_ranges"})

    def test_exhausted_sweep_closes_on_supply(self):
        calls = self._stub_run(lambda name, rep: True)
        results, ground = self.af.sweep("normalize", repeats=12)
        self.assertIsNone(ground)
        self.assertEqual([r["task"] for r in results],
                         ["snake_to_camel", "balanced"])
        self.assertEqual({c["name"] for c in calls},
                         {"snake_to_camel", "balanced"})


class TestStageB(_ArmFloors22Harness):

    def test_interleave_and_audit(self):
        calls = self._stub_run(lambda name, rep: rep % 2 == 0)
        stores = self.af.load_stores()
        rows = self.af.run_block("boundary", "merge_ranges", stores,
                                 repeats=2)
        self.assertEqual([r["cell"] for r in rows],
                         ["none", "armed-B1", "armed-B2"] * 2)
        for r in rows:
            self.assertEqual(r["tools"],
                             self.af.EXPECT_TOOLS[r["cell"]])
        armed_calls = [c for c in calls
                       if c["kw"].get("landscape") is not None]
        self.assertEqual(len(armed_calls), 4)

    def test_resume_separates_stages_and_blocks(self):
        self._stub_run(lambda name, rep: True)
        stores = self.af.load_stores()
        self.af.qualify("boundary", "merge_ranges", repeats=2)
        self.af.run_block("boundary", "merge_ranges", stores, repeats=2)
        self.af.run_block("normalize", "snake_to_camel", stores,
                          repeats=2)
        prior = self.af._load_rows()
        calls = self._stub_run(lambda name, rep: True)
        r1 = self.af.qualify("boundary", "merge_ranges", repeats=2,
                             prior_rows=prior)
        r2 = self.af.run_block("boundary", "merge_ranges", stores,
                               repeats=2, prior_rows=prior)
        r3 = self.af.run_block("normalize", "snake_to_camel", stores,
                               repeats=2, prior_rows=prior)
        self.assertEqual(calls, [])
        self.assertEqual(r1["pooled"]["n"], 2)
        self.assertEqual(len(r2), 6)
        self.assertEqual(len(r3), 6)
        self.assertTrue(all(r["block"] == "normalize" for r in r3))


if __name__ == "__main__":
    unittest.main()
