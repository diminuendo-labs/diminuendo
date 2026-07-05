"""Tests for the catch-better loop: watchlist gates, miss detection, the
teaching sweep with a stub generator, watch injection into the audience
prompt, and the latency mix. No model calls."""

import json
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import hindsight
import watchlist
from runner import _audience_prompt

FEAT = {"operation": "write_code", "language": "python"}


def _watch(**over):
    base = {"watch": "Verify the stated tie-breaking rule is implemented.",
            "applies_when": dict(FEAT), "confidence": 0.5,
            "provenance": "engine", "source_node": "task-x"}
    base.update(over)
    return base


def _summary(**over):
    base = {"node_id": "task-n1", "task": "write f", "verdict": "fail",
            "audience_verdict": "pass", "code_mutated": False,
            "output": "def f(): pass",
            "evidence": {"passed": False, "results": [
                {"call": "f('ab')", "ok": False,
                 "got": "'b'", "expect": "'a'"}], "error": None}}
    base.update(over)
    return base


class TestWatchlist(unittest.TestCase):

    def test_gates(self):
        watchlist.validate(_watch())
        with self.assertRaises(watchlist.WatchError):
            watchlist.validate(_watch(watch="Check it uses fewer tokens."))
        with self.assertRaises(watchlist.WatchError):
            watchlist.validate(_watch(applies_when={}))
        with self.assertRaises(watchlist.WatchError):
            watchlist.validate(_watch(provenance="vibes"))

    def test_commit_query_taught(self):
        with tempfile.TemporaryDirectory() as d:
            p = os.path.join(d, "watch.jsonl")
            watchlist.commit(p, _watch())
            ws = watchlist.query(watchlist.load(p), FEAT)
            self.assertEqual(len(ws), 1)
            self.assertIn("tie-breaking", ws[0])
            self.assertEqual(watchlist.taught_nodes(watchlist.load(p)),
                             {"task-x"})
            # contradiction excluded
            self.assertEqual(watchlist.query(watchlist.load(p),
                                             {"operation": "prose"}), [])


class TestMissDetection(unittest.TestCase):

    def test_natural_miss_shape(self):
        self.assertTrue(hindsight.natural_miss(_summary()))
        self.assertFalse(hindsight.natural_miss(_summary(code_mutated=True)))
        self.assertFalse(hindsight.natural_miss(
            _summary(audience_verdict="fail")))
        self.assertFalse(hindsight.natural_miss(_summary(verdict="pass")))


def _stub_generate(prompt):
    return json.dumps({"watch": "Verify tie handling matches the task rule.",
                       "applies_when": dict(FEAT), "confidence": 0.6})


class TestTeachingSweep(unittest.TestCase):

    def test_scan_teaches_once_and_skips_seeded(self):
        with tempfile.TemporaryDirectory() as d:
            wpath = os.path.join(d, "watch.jsonl")
            for name, s in [
                ("a.summary.json", _summary(node_id="task-a")),
                ("b.summary.json", _summary(node_id="task-b",
                                            code_mutated=True)),
                ("c.summary.json", _summary(node_id="task-c",
                                            verdict="pass",
                                            audience_verdict="pass")),
            ]:
                with open(os.path.join(d, name), "w", encoding="utf-8") as f:
                    json.dump(s, f)
            taught = hindsight.scan_runs(d, wpath, FEAT,
                                         generate_fn=_stub_generate,
                                         log=lambda *a: None)
            self.assertEqual(taught, ["task-a"])  # seeded and clean skipped
            # second sweep teaches nothing: the miss is already on the list
            again = hindsight.scan_runs(d, wpath, FEAT,
                                        generate_fn=_stub_generate,
                                        log=lambda *a: None)
            self.assertEqual(again, [])
            self.assertEqual(len(watchlist.load(wpath)), 1)


class TestInjectionAndMix(unittest.TestCase):

    def test_watches_reach_audience_prompt(self):
        pkt = {"task": "t", "criteria": ["c1"], "output": "o"}
        armed = _audience_prompt(pkt, ["Verify the tie rule."])
        unarmed = _audience_prompt(pkt, [])
        self.assertIn("WATCH-ITEMS", armed)
        self.assertIn("Verify the tie rule.", armed)
        self.assertNotIn("WATCH-ITEMS", unarmed)

    def test_latency_mix_counts(self):
        with tempfile.TemporaryDirectory() as d:
            rows = [
                _summary(node_id="n1"),                          # by evidence
                _summary(node_id="n2", verdict="pass",
                         audience_verdict="pass"),               # clean
                _summary(node_id="n3", audience_verdict="fail"), # live
                _summary(node_id="n4", code_mutated=True),       # seeded
            ]
            for i, s in enumerate(rows):
                with open(os.path.join(d, f"{i}.summary.json"), "w",
                          encoding="utf-8") as f:
                    json.dump(s, f)
            mix = hindsight.latency_mix(d)
            self.assertEqual(mix["caught_by_evidence_after_audience_pass"], 1)
            self.assertEqual(mix["clean_pass"], 1)
            self.assertEqual(mix["caught_live_by_audience"], 1)
            self.assertEqual(mix["seeded"], 1)


if __name__ == "__main__":
    unittest.main()
