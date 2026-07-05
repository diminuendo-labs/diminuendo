"""Tests for executable evidence: correct code passes, wrong code is caught,
broken code is caught, a hang is contained by the timeout."""

import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import evidence

CHECKS = [
    {"call": "add(2, 3)", "expect": "5"},
    {"call": "add(-1, 1)", "expect": "0"},
]


class TestEvidence(unittest.TestCase):

    def test_correct_code_passes(self):
        out = evidence.run_checks("def add(a, b):\n    return a + b", CHECKS)
        self.assertTrue(out["passed"])
        self.assertIsNone(out["error"])

    def test_wrong_code_caught(self):
        out = evidence.run_checks("def add(a, b):\n    return a - b", CHECKS)
        self.assertFalse(out["passed"])
        self.assertFalse(out["results"][0]["ok"])

    def test_broken_code_caught(self):
        out = evidence.run_checks("def add(a, b) return a + b", CHECKS)
        self.assertFalse(out["passed"])
        self.assertIsNotNone(out["error"])

    def test_hang_contained(self):
        out = evidence.run_checks(
            "def add(a, b):\n    while True:\n        pass", CHECKS,
            timeout_s=3)
        self.assertFalse(out["passed"])
        self.assertIn("timeout", out["error"])

    def test_extract_fenced_block(self):
        text = "here\n```python\ndef f():\n    return 1\n```\ntail"
        self.assertEqual(evidence.extract_python(text),
                         "def f():\n    return 1")


if __name__ == "__main__":
    unittest.main()
