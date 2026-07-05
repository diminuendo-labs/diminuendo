"""Tests for the Score. The gate: releases obey dependencies, cycles are
rejected, dynamic downstream growth works, and the missing-edge write (the
backward pass) changes future ordering."""

import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from score import Score, CycleError, UnknownNodeError


class TestScore(unittest.TestCase):

    def test_release_gating(self):
        s = Score()
        s.add_node("a")
        s.add_node("b", depends_on=["a"])
        s.add_node("c", depends_on=["a", "b"])
        self.assertEqual(s.ready_nodes(), ["a"])
        s.mark_complete("a")
        self.assertEqual(s.ready_nodes(), ["b"])
        self.assertEqual(s.blocked_by("c"), ["b"])
        s.mark_complete("b")
        self.assertEqual(s.ready_nodes(), ["c"])
        s.mark_complete("c")
        self.assertTrue(s.is_done())

    def test_cycle_rejected(self):
        s = Score()
        s.add_node("a")
        s.add_node("b", depends_on=["a"])
        with self.assertRaises(CycleError):
            s.add_edge("b", "a")
        with self.assertRaises(CycleError):
            s.add_edge("a", "a")
        # the rejected edge left no trace
        self.assertEqual(s.blocked_by("a"), [])

    def test_unknown_node_rejected(self):
        s = Score()
        s.add_node("a")
        with self.assertRaises(UnknownNodeError):
            s.add_edge("a", "ghost")
        with self.assertRaises(UnknownNodeError):
            s.blocked_by("ghost")

    def test_dynamic_downstream_growth(self):
        # a running node spawns a child mid-run: strictly later, always safe
        s = Score()
        s.add_node("parent")
        s.mark_complete("parent")
        s.add_node("child", depends_on=["parent"])
        self.assertEqual(s.ready_nodes(), ["child"])

    def test_missing_edge_written_by_break(self):
        # the backward pass: a break reveals a dependency, the edge is written
        # with source "missing", and the next run's ordering obeys it
        s = Score()
        s.add_node("upstream")
        s.add_node("worker")
        self.assertIn("worker", s.ready_nodes())  # released too early, the break
        s.add_edge("upstream", "worker", source="missing")
        self.assertNotIn("worker", s.ready_nodes())  # next time, gated
        self.assertEqual(s.edge_source("upstream", "worker"), "missing")

    def test_edge_sources_recorded(self):
        s = Score()
        s.add_node("a")
        s.add_node("b")
        s.add_edge("a", "b", source="structural")
        self.assertEqual(s.edge_source("a", "b"), "structural")
        with self.assertRaises(ValueError):
            s.add_node("c", depends_on=["a"], source="vibes")

    def test_snapshot_is_plain_data(self):
        s = Score()
        s.add_node("a")
        s.add_node("b", depends_on=["a"], source="structural")
        snap = s.to_dict()
        self.assertEqual(snap["state"], {"a": "pending", "b": "pending"})
        self.assertEqual(snap["edges"],
                         [{"parent": "a", "child": "b", "source": "structural"}])


if __name__ == "__main__":
    unittest.main()
