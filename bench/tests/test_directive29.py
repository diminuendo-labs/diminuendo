"""Tests for the PACKET-029 build stage. Pure derivation and
production-path checks, no model calls. The derivation instrument must
be PACKET-028's by identity, and the census pin must be
supply_families' by identity."""

import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import directive28 as d28
import directive29 as d29
import supply_families as sf


class TestInstrumentPins(unittest.TestCase):

    def test_derivation_functions_are_p028s_by_identity(self):
        import directive29
        self.assertIs(directive29.rule_order, d28.rule_order)
        self.assertIs(directive29.directive_order, d28.directive_order)
        self.assertIs(directive29.kth, d28.kth)
        self.assertIs(directive29.load_candidate, d28.load_candidate)

    def test_census_pin_is_supply_families_by_identity(self):
        self.assertIs(d29.CENSUS_SHAPE, sf.census_shape)


class TestContradictionGate(unittest.TestCase):

    def test_rung3_derivations_separate_on_both_rule_checks(self):
        derivs = d29.derivations()
        rung = sf.get_rung("kth_ordered", 3)
        self.assertEqual([d["call"] for d in derivs],
                         rung["rule_checks"])
        expected = {2: ("ba", "aa"), 3: ("ab", "ba")}
        for d in derivs:
            rule_ans, dir_ans = expected[d["k"]]
            self.assertEqual(d["rule_answer"], rule_ans, d["call"])
            self.assertEqual(d["directive_answer"], dir_ans, d["call"])
            self.assertTrue(d["differs"], d["call"])

    def test_gate_passes_line4_and_stops_selection_there(self):
        results = d29.contradiction_gate()
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["candidate"]["prod_line"], 4)
        self.assertTrue(results[0]["passes"])


class TestByteCheckAndDeliveryPath(unittest.TestCase):

    def test_byte_check_passes(self):
        self.assertTrue(d29.byte_check())

    def test_touched_store_refused(self):
        import tempfile
        real = d29.STORE
        try:
            with open(real, "rb") as f:
                original = f.read()
            with tempfile.NamedTemporaryFile(delete=False,
                                             suffix=".jsonl") as f:
                f.write(original + b"\n")
                bad = f.name
            d29.STORE = bad
            with self.assertRaises(SystemExit):
                d29.byte_check()
        finally:
            d29.STORE = real
            os.unlink(bad)

    def test_menu_refuses_on_ground_and_serves_on_control(self):
        """The structural discovery pinned: the production menu's
        contradiction logic refuses the last-direction lesson on
        reverse_alphabetical ground and serves the same lesson on
        matched ground, so the refusal is the pin firewall, not a
        loading defect."""
        chk = d29.menu_delivery_check()
        self.assertEqual(chk["ground_tools"], 0)
        self.assertEqual(chk["control_tools"], 1)
        self.assertEqual(chk["lesson_stated_direction"], "last")
        self.assertEqual(chk["ground_stated_direction"],
                         "reverse_alphabetical")

    def test_build_stage_stops_at_the_menu_check(self):
        self.assertEqual(d29.main.__name__, "main")
        # main prints; exercise it end to end and pin the exit code
        import contextlib
        import io
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            code = d29.main()
        self.assertEqual(code, 2)
        out = buf.getvalue()
        self.assertIn("GATE: PASSES", out)
        self.assertIn("SELECTED: line 4", out)
        self.assertIn("STRUCTURALLY UNREACHABLE", out)


if __name__ == "__main__":
    unittest.main()
