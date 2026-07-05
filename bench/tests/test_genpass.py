"""Tests for the PACKET-008 generation-pass harness: rejection accounting
by reason, commit-after-retry, no model calls."""

import importlib
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import lesson
import runner


class TestReasonKey(unittest.TestCase):

    def test_buckets(self):
        import genpass
        self.assertEqual(genpass._reason_key(
            "aim screen: rule text shares no ground"), "aim_screen")
        self.assertEqual(genpass._reason_key(
            "imperative shape in concept text: 'stored in'"),
            "imperative_shape")
        self.assertEqual(genpass._reason_key(
            "platitude in lesson text: 'clean code'"), "platitude")
        self.assertEqual(genpass._reason_key(
            "metric-shaped term in lesson text: 'tokens'"), "metric_term")
        self.assertEqual(genpass._reason_key(
            "generator returned no parseable JSON"), "no_json")
        self.assertEqual(genpass._reason_key("anything else"), "other")


class TestGenPass(unittest.TestCase):

    def setUp(self):
        self._real_runs = runner.RUNS
        self._real_run_once = runner.run_once
        self._real_contrastive = lesson.generate_contrastive
        self._real_sibling = lesson.generate_sibling_contrast
        self._tmp = tempfile.TemporaryDirectory()
        runner.RUNS = self._tmp.name
        import genpass
        self.gp = importlib.reload(genpass)

    def tearDown(self):
        runner.RUNS = self._real_runs
        runner.run_once = self._real_run_once
        lesson.generate_contrastive = self._real_contrastive
        lesson.generate_sibling_contrast = self._real_sibling
        importlib.reload(self.gp)
        self._tmp.cleanup()

    def test_rejection_recorded_then_commit_on_retry(self):
        import probe_tasks
        calls = []

        def stub_run(task, criteria, work_features, **kw):
            # first attempt of the first task fails, everything else passes
            ok = len(calls) != 0
            calls.append(task)
            return {"run_id": f"stub-{len(calls)}",
                    "node_id": f"node-{len(calls)}",
                    "verdict": "pass" if ok else "fail",
                    "output": "def f(): pass",
                    "evidence": {"passed": ok,
                                 "results": [{"ok": ok, "call": "f()",
                                              "got": "1", "expect": "1"}],
                                 "error": None}}

        attempts = []

        def stub_contrastive(task_text, work_features, fail_s, pass_s,
                             model=None):
            attempts.append(task_text)
            bad = len(attempts) == 1
            return {"concept": ("Store in a set to keep values unique."
                                if bad else
                                "When the task states a tie direction, "
                                "honor the direction it states."),
                    "rule": "follow the direction the task states",
                    "applies_when": dict(work_features),
                    "confidence": 0.5, "provenance": "engine",
                    "trail": {"node_id": fail_s["node_id"],
                              "contrast_node_id": pass_s["node_id"],
                              "work_features": work_features}}

        runner.run_once = stub_run
        lesson.generate_contrastive = stub_contrastive
        lesson.generate_sibling_contrast = stub_contrastive
        rejections = []
        accounting = self.gp.gen_seat("A", rejections)
        classes = {t["rule_class"] for t in probe_tasks.GEN_TASKS}
        self.assertEqual(len(accounting), len(classes))
        # the imperative concept died at the gate, the retry committed
        self.assertEqual(len(rejections), 1)
        self.assertEqual(rejections[0]["reason"], "imperative_shape")
        self.assertEqual(rejections[0]["attempt"], 1)
        store = lesson.load(self.gp.store("A"))
        self.assertEqual(len(store), 1)
        self.assertIn("rule_topic", store[0]["applies_when"])


if __name__ == "__main__":
    unittest.main()
