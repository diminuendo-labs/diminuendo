"""Tests for the PACKET-020 mining harness. Stub generators, temp runs
dir, fabricated source artifacts, no model calls."""

import importlib
import json
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import lesson
import runner


class _Mine20Harness(unittest.TestCase):

    def setUp(self):
        self._real_runs = runner.RUNS
        self._real_contrastive = lesson.generate_contrastive
        self._real_sibling = lesson.generate_sibling_contrast
        self._tmp = tempfile.TemporaryDirectory()
        runner.RUNS = self._tmp.name
        import mine20
        self.mn = importlib.reload(mine20)
        self.mn.STORE = os.path.join(self._tmp.name, "store.jsonl")

    def tearDown(self):
        runner.RUNS = self._real_runs
        lesson.generate_contrastive = self._real_contrastive
        lesson.generate_sibling_contrast = self._real_sibling
        importlib.reload(self.mn)
        self._tmp.cleanup()

    def _fabricate_source(self, tasks_with_fails):
        """Write stage 1 rows and summaries for the named tasks: one
        fail, one pass each; other pair tasks get pass-only rows."""
        rows_path = os.path.join(self._tmp.name,
                                 f"{self.mn.SOURCE_RUN}.rows.jsonl")
        names = {p["fail_task"] for p in self.mn.PAIRS} | \
                {p["pass_task"] for p in self.mn.PAIRS}
        with open(rows_path, "w", encoding="utf-8") as f:
            for name in sorted(names):
                reps = ([(0, False), (1, True)]
                        if name in tasks_with_fails else [(0, True)])
                for rep, ok in reps:
                    rid = f"{name}-r{rep}"
                    f.write(json.dumps(
                        {"stage": 1, "task": name, "rep": rep,
                         "run_id": rid, "ev_passed": ok}) + "\n")
                    with open(os.path.join(self._tmp.name,
                                           f"{rid}.summary.json"), "w",
                              encoding="utf-8") as sf:
                        json.dump({"run_id": rid,
                                   "node_id": f"task-{rid}",
                                   "output": "def f(): pass",
                                   "evidence": {"passed": ok,
                                                "results": [
                                                    {"ok": ok,
                                                     "call": "f()",
                                                     "got": "1",
                                                     "expect": "1"}],
                                                "error": None}}, sf)

    def _stub_generators(self, reject_first_for=()):
        made = []

        def gen(task_text, work_features, fail_s, pass_s, model=None):
            name = next(n for n in self.mn._TASKS
                        if self.mn._TASKS[n]["task"] == task_text)
            made.append(name)
            if name in reject_first_for and made.count(name) == 1:
                return {"concept": "Store in a set for speed.",
                        "rule": "use a set",
                        "applies_when": dict(work_features),
                        "confidence": 0.5, "provenance": "engine",
                        "trail": {"node_id": fail_s["node_id"],
                                  "work_features": work_features}}
            return {"concept": "When the task states a rule of this "
                               "class, honor the stated convention.",
                    "rule": "follow the direction the task states",
                    "applies_when": dict(work_features),
                    "confidence": 0.5, "provenance": "engine",
                    "trail": {"node_id": fail_s["node_id"],
                              "contrast_node_id": pass_s["node_id"],
                              "work_features": work_features}}

        def gen_sib(fail_text, pass_text, rule_class, work_features,
                    fail_s, pass_s, model=None):
            return gen(fail_text, work_features, fail_s, pass_s)

        lesson.generate_contrastive = gen
        lesson.generate_sibling_contrast = gen_sib
        return made


class TestPairs(_Mine20Harness):

    def test_pairs_verbatim_from_packet017(self):
        self.assertEqual(len(self.mn.PAIRS), 8)
        classes = [p["rule_class"] for p in self.mn.PAIRS]
        self.assertEqual(classes,
                         ["tie_break"] * 2 + ["distinctness"] * 2
                         + ["boundary"] * 2 + ["normalize"] * 2)
        sib = self.mn.PAIRS[-1]
        self.assertEqual(sib["type"], "sibling")
        self.assertEqual((sib["fail_task"], sib["pass_task"]),
                         ("depth_max", "count_word"))

    def test_all_pairs_mine_and_store_is_packet_local(self):
        all_tasks = {p["fail_task"] for p in self.mn.PAIRS}
        self._fabricate_source(all_tasks)
        self._stub_generators()
        self.mn.main()
        store = lesson.load(self.mn.STORE)
        self.assertEqual(len(store), 8)
        classes = {l["applies_when"]["rule_class"] for l in store}
        self.assertEqual(classes, {"tie_break", "distinctness",
                                   "boundary", "normalize"})
        self.assertTrue(all(l["trail"]["origin_seat"] == "mistral:7b"
                            for l in store))

    def test_reject_recorded_with_screen_then_retry_commits(self):
        self._fabricate_source({"chunk"})
        made = self._stub_generators(reject_first_for={"chunk"})
        rows = self.mn.source_rows()
        outcome = self.mn.mine_pair(self.mn.PAIRS[4], rows, set())
        self.assertTrue(outcome["committed"])
        self.assertEqual(len(outcome["rejects"]), 1)
        self.assertEqual(outcome["rejects"][0]["screen"],
                         "imperative_shape")
        self.assertEqual(made.count("chunk"), 2)

    def test_insufficient_artifacts_reported_not_rerun(self):
        self._fabricate_source(set())  # nobody fails
        self._stub_generators()
        rows = self.mn.source_rows()
        outcome = self.mn.mine_pair(self.mn.PAIRS[0], rows, set())
        self.assertFalse(outcome["attempted"])
        self.assertIn("artifacts insufficient", outcome["outcome"])

    def test_resume_skips_decided_pairs(self):
        all_tasks = {p["fail_task"] for p in self.mn.PAIRS}
        self._fabricate_source(all_tasks)
        made = self._stub_generators()
        self.mn.main()
        first_count = len(made)
        self.mn.main(resume_ts=self.mn._TS)
        self.assertEqual(len(made), first_count)  # nothing re-mined


if __name__ == "__main__":
    unittest.main()
