"""Tests for the control's classifier: every cell of the table, both the win
column and the cost column. Pure logic, no model calls."""

import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from control import classify


class TestClassifier(unittest.TestCase):

    def test_win_column_broken_outputs(self):
        self.assertEqual(classify(False, "pass", "fail"),
                         "miss_converted_to_catch")
        self.assertEqual(classify(False, "fail", "fail"),
                         "caught_without_watch")
        self.assertEqual(classify(False, "fail", "pass"),
                         "caught_without_watch")
        self.assertEqual(classify(False, "pass", "pass"),
                         "missed_even_armed")

    def test_cost_column_clean_outputs(self):
        self.assertEqual(classify(True, "pass", "fail"),
                         "false_alarm_induced")
        self.assertEqual(classify(True, "pass", "pass"), "clean_no_harm")
        self.assertEqual(classify(True, "fail", "fail"),
                         "unarmed_false_alarm")
        self.assertEqual(classify(True, "fail", "pass"),
                         "unarmed_false_alarm")

    def test_no_ground_truth(self):
        self.assertEqual(classify(None, "pass", "fail"), "no_ground_truth")


if __name__ == "__main__":
    unittest.main()
