"""Tests for the PACKET-028 contradiction gate. Pure derivation, no
model calls, no temp dirs needed: the gate is deterministic and these
tests pin it for the conductor's replay."""

import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import directive28 as d28
import supply_families as sf


class TestDerivations(unittest.TestCase):

    def test_rule_order_matches_the_family_reference(self):
        # The stated rule's derivation must agree with the committed
        # family checks: rung 2 (variant input) expects 'bb' at k=2,
        # rung 3 'ba' and 'ab' at k=2 and k=3.
        self.assertEqual(d28.kth(d28.rule_order(['bb', 'ab', 'c']), 2),
                         'bb')
        order3 = d28.rule_order(['ab', 'ba', 'aa', 'c'])
        self.assertEqual(order3, ['c', 'ba', 'ab', 'aa'])
        self.assertEqual(d28.kth(order3, 2), 'ba')
        self.assertEqual(d28.kth(order3, 3), 'ab')

    def test_directive_order_prefers_later_encountered(self):
        self.assertEqual(d28.directive_order(['aa', 'bb', 'c']),
                         ['c', 'bb', 'aa'])
        self.assertEqual(d28.directive_order(['bb', 'aa', 'c']),
                         ['c', 'aa', 'bb'])

    def test_old_rung2_input_coincides(self):
        """The historical fact that walled P028 and motivated the
        variant: on the ORIGINAL rung 2 input the two directions
        produce the same answer, because the tie pair's encounter
        order inverts its alphabetical order. Kept as the
        instrument-level record of why rung 2's input changed."""
        words, k = ['aa', 'bb', 'c'], 2
        self.assertEqual(d28.kth(d28.rule_order(words), k),
                         d28.kth(d28.directive_order(words), k))

    def test_rung2_committed_input_separates(self):
        """The committed rung 2 rule check must separate the two
        directions, or the G1 lane dies again the same way. Derives
        the input from the family definition so this pin follows the
        committed instrument, not a copy of it."""
        call = sf.get_rung("kth_ordered", 2)["rule_checks"][0]
        inside = call[call.index("(") + 1:call.rindex(")")]
        words_txt, k_txt = inside.rsplit(",", 1)
        words, k = eval(words_txt), int(k_txt)
        rule = d28.kth(d28.rule_order(words), k)
        directive = d28.kth(d28.directive_order(words), k)
        self.assertEqual(rule, 'bb')
        self.assertEqual(directive, 'ab')
        self.assertNotEqual(rule, directive)

    def test_gate_logic_can_pass_on_separating_input(self):
        """A synthetic input where the directions separate, proving
        the gate tests the input, not a constant."""
        words, k = ['bb', 'aa', 'c'], 2
        self.assertEqual(d28.kth(d28.rule_order(words), k), 'bb')
        self.assertEqual(d28.kth(d28.directive_order(words), k), 'aa')

    def test_rung3_rule_checks_separate(self):
        """The FINDINGS lead: rung 3's dense-tie rule checks separate
        the two directions on both k values."""
        words = ['ab', 'ba', 'aa', 'c']
        for k, rule_ans in ((2, 'ba'), (3, 'ab')):
            d_ans = d28.kth(d28.directive_order(words), k)
            self.assertEqual(d28.kth(d28.rule_order(words), k),
                             rule_ans)
            self.assertNotEqual(rule_ans, d_ans)


class TestGate(unittest.TestCase):

    def test_derivations_cover_every_rule_check(self):
        derivs = d28.derivations()
        rung = sf.get_rung("kth_ordered", 2)
        self.assertEqual([d["call"] for d in derivs],
                         rung["rule_checks"])

    def test_both_candidates_pass_on_variant_rung2(self):
        """Inverted with the rung 2 variant: on the ORIGINAL input
        both candidates failed the gate (the P028 measured stop, on
        the record); the variant input separates the directions, so
        both direction-last candidates now pass. This pin holds the
        variant to its purpose."""
        results = d28.contradiction_gate()
        self.assertEqual([r["candidate"]["prod_line"] for r in results],
                         [4, 5])
        for r in results:
            self.assertEqual(r["candidate"]["stated_direction"], "last")
            self.assertTrue(r["passes"])

    def test_candidate_rule_sentences_match_production(self):
        c4 = d28.load_candidate(4, "shortest_word")
        c5 = d28.load_candidate(5, "longest_run_char")
        self.assertIn("last such word encountered", c4["rule"])
        self.assertIn("appears in the string last", c5["rule"])

    def test_wrong_line_position_refused(self):
        with self.assertRaises(SystemExit):
            d28.load_candidate(4, "longest_run_char")


if __name__ == "__main__":
    unittest.main()
