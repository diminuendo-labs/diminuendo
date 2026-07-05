"""Tests for the ledger: signs by category, axes never blended, persistence."""

import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ledger import Ledger


class TestLedger(unittest.TestCase):

    def test_clean_posts_positive(self):
        led = Ledger()
        led.post("n1", "clean", 2.0, 100)
        self.assertEqual(led.totals(), {"time_s": 2.0, "tokens": 100})

    def test_catch_sequence(self):
        led = Ledger()
        led.post("n1", "clean", 2.0, 100)
        led.post_catch("n1", fail_time_s=3.0, fail_tokens=200,
                       fix_time_s=1.0, fix_tokens=50,
                       bonus_time_s=1.5, bonus_tokens=75)
        t = led.totals()
        self.assertAlmostEqual(t["time_s"], 2.0 - 3.0 - 1.0 + 1.5)
        self.assertEqual(t["tokens"], 100 - 200 - 50 + 75)

    def test_axes_stay_separate(self):
        led = Ledger()
        led.post("n1", "clean", 5.0, 10)
        t = led.totals()
        self.assertEqual(sorted(t), ["time_s", "tokens"])
        self.assertFalse(hasattr(led, "combined"))

    def test_bad_inputs_rejected(self):
        led = Ledger()
        with self.assertRaises(ValueError):
            led.post("n1", "vibes", 1.0, 1)
        with self.assertRaises(ValueError):
            led.post("n1", "clean", -1.0, 1)

    def test_persistence_round_trip(self):
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "ledger.jsonl")
            led = Ledger(path=path)
            led.post("n1", "clean", 2.0, 100)
            led.post("n2", "failure", 1.0, 40)
            back = Ledger.load(path)
            self.assertEqual(back.totals(), led.totals())
            self.assertEqual(back.node_totals("n2"),
                             {"time_s": -1.0, "tokens": -40})


if __name__ == "__main__":
    unittest.main()
