"""Tests for the breadcrumb store: forward write, hindsight amendment,
back-fill merge, field enforcement."""

import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import breadcrumb


def _record(**over):
    base = {
        "node_id": "n1", "model": "qwen2.5-coder:7b", "role": "musician",
        "work_features": {"operation": "write", "target": "function"},
        "cost_time": 2.0, "cost_tokens": 150, "outcome": "provisional_pass",
    }
    base.update(over)
    return base


class TestBreadcrumb(unittest.TestCase):

    def test_write_and_load(self):
        with tempfile.TemporaryDirectory() as d:
            p = os.path.join(d, "crumbs.jsonl")
            breadcrumb.write(p, _record())
            got = breadcrumb.load(p)["n1"]
            self.assertEqual(got["role"], "musician")
            self.assertEqual(got["work_features"]["operation"], "write")

    def test_amend_overrides_and_backfills(self):
        with tempfile.TemporaryDirectory() as d:
            p = os.path.join(d, "crumbs.jsonl")
            breadcrumb.write(p, _record())
            breadcrumb.amend(p, "n1", outcome="miss_found",
                             error_class="missing_dependency",
                             work_features={"input_size": "large"})
            got = breadcrumb.load(p)["n1"]
            # hindsight corrected the outcome
            self.assertEqual(got["outcome"], "miss_found")
            self.assertEqual(got["error_class"], "missing_dependency")
            # back-fill added a feature without erasing the forward ones
            self.assertEqual(got["work_features"]["operation"], "write")
            self.assertEqual(got["work_features"]["input_size"], "large")

    def test_history_is_append_only(self):
        with tempfile.TemporaryDirectory() as d:
            p = os.path.join(d, "crumbs.jsonl")
            breadcrumb.write(p, _record())
            breadcrumb.amend(p, "n1", outcome="miss_found")
            with open(p, encoding="utf-8") as f:
                lines = [l for l in f if l.strip()]
            self.assertEqual(len(lines), 2)  # nothing rewritten, only appended

    def test_field_enforcement(self):
        with tempfile.TemporaryDirectory() as d:
            p = os.path.join(d, "crumbs.jsonl")
            with self.assertRaises(ValueError):
                breadcrumb.write(p, {"node_id": "n1"})
            with self.assertRaises(ValueError):
                breadcrumb.write(p, _record(surprise_field=1))
            with self.assertRaises(ValueError):
                breadcrumb.amend(p, "n1", surprise_field=1)


if __name__ == "__main__":
    unittest.main()
