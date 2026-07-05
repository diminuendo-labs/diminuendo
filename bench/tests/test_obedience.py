"""Tests for the PACKET-007 obedience decomposition harness. Stub runner,
temp runs dir, no model calls. The packet-local variants are committed
material, deliberately outside the lesson gates, and the loader's
structure checks are what these tests pin."""

import importlib
import json
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import runner


class _ObedienceHarness(unittest.TestCase):

    def setUp(self):
        self._real_runs = runner.RUNS
        self._real_run_once = runner.run_once
        self._tmp = tempfile.TemporaryDirectory()
        runner.RUNS = self._tmp.name
        import obedience
        self.ob = importlib.reload(obedience)

    def tearDown(self):
        runner.RUNS = self._real_runs
        runner.run_once = self._real_run_once
        importlib.reload(self.ob)
        self._tmp.cleanup()

    def _stub_run(self):
        calls = []

        def stub(task, criteria, work_features, **kw):
            calls.append({"task": task, "kw": kw})
            return {"run_id": f"stub-{len(calls)}", "verdict": "pass",
                    "evidence": {"passed": True,
                                 "results": [{"ok": True, "call": "f(1)",
                                              "got": "1", "expect": "1"}],
                                 "error": None}}

        runner.run_once = stub
        return calls


class TestMaterials(_ObedienceHarness):

    def test_variants_load_with_labels_and_stripped_pins(self):
        v = self.ob.load_materials()
        self.assertEqual(len(v), 4)
        for topic in ("distinctness", "tie"):
            for shape in ("concept", "recipe"):
                self.assertIn((topic, shape), v)
        for key, l in v.items():
            self.assertEqual(l["provenance"], "hand")
        self.assertEqual(
            v[("tie", "concept")]["applies_when"]["stated_direction"], "*")
        self.assertTrue(v[("tie", "recipe")]["deliberately_mismatched"])
        # the recipe concept is the PACKET-006 harm text, verbatim
        self.assertIn("stored in a way that disregards order",
                      v[("distinctness", "recipe")]["concept"])

    def test_recipe_variants_fail_the_production_gates(self):
        """The instruments are deliberately gate-violating: the shape
        screen refuses both recipe variants, which is why the loader does
        not validate. Pinned so nobody promotes these into a probe store."""
        import lesson
        v = self.ob.load_materials()
        with self.assertRaises(lesson.LessonError):
            lesson.validate(v[("distinctness", "recipe")])

    def test_touched_store_refused(self):
        bad = os.path.join(self._tmp.name, "bad.jsonl")
        v = self.ob.load_materials()
        with open(bad, "w", encoding="utf-8") as f:
            f.write(json.dumps(v[("tie", "concept")]) + "\n")
        self.ob.STORE = bad
        with self.assertRaises(SystemExit):
            self.ob.load_materials()


class TestArms(_ObedienceHarness):

    def test_arms_deliver_the_right_shape(self):
        calls = self._stub_run()
        v = self.ob.load_materials()
        self.ob.R_NONE, self.ob.R_MENU = 2, 1
        rows = self.ob.run_task("most_common_word", v)
        self.assertEqual(len(rows), 4)  # 2 none + 1 concept + 1 recipe
        armed = [r for r in rows if r["arm"] != "none"]
        by_arm = {r["arm"]: r for r in armed}
        self.assertEqual(by_arm["menu_concept"]["tool_concepts"],
                         [v[("tie", "concept")]["concept"]])
        self.assertEqual(by_arm["menu_recipe"]["tool_concepts"],
                         [v[("tie", "recipe")]["concept"]])
        # the stripped pin lets the tie variants ride the alphabetical task
        self.assertTrue(all(r["tools"] == 1 for r in armed))
        bare = [c for c in calls if c["kw"].get("landscape") is None]
        self.assertEqual(len(bare), 2)

    def test_resume_skips_checkpointed_runs(self):
        v = self.ob.load_materials()
        self.ob.R_NONE, self.ob.R_MENU = 2, 1
        for rep in range(2):
            self.ob._row({"task": "range_summary", "topic": "distinctness",
                          "arm": "none", "rep": rep, "mismatched": None,
                          "run_id": "prior", "verdict": "fail", "tools": 0,
                          "tool_concepts": [], "ev": 0.5,
                          "checks": {"f(1)": False}})
        calls = self._stub_run()
        prior = self.ob._load_rows()
        rows = self.ob.run_task("range_summary", v, prior_rows=prior)
        self.assertEqual(len(calls), 2)  # only the two menu arms ran live
        self.assertEqual(len(rows), 4)


class TestTables(unittest.TestCase):

    def test_check_table_and_pooled(self):
        import obedience
        rows = [
            {"task": "range_summary", "arm": "none",
             "checks": {"range_summary([3, 1, 2, 2])": True,
                        "range_summary([])": True}},
            {"task": "range_summary", "arm": "menu_recipe",
             "checks": {"range_summary([3, 1, 2, 2])": False,
                        "range_summary([])": True}},
        ]
        table = obedience.check_table(rows)
        rule = table["range_summary"]["range_summary([3, 1, 2, 2])"]
        self.assertTrue(rule["rule_check"])
        self.assertAlmostEqual(rule["arms"]["none"]["rate"], 1.0)
        self.assertAlmostEqual(rule["arms"]["menu_recipe"]["rate"], 0.0)
        pooled = obedience.pooled_rule_checks(rows)
        self.assertEqual(pooled["range_summary"]["menu_recipe"]["passed"], 0)


if __name__ == "__main__":
    unittest.main()
