"""Tests for the six supply families. Every rung's checks are executed
against a correct reference implementation through the real evidence
harness, so the expected values and their determinism are pinned; every
census classifier is pinned on synthetic exemplars of each taxonomy
shape."""

import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import evidence
import supply_families as sf
from probe_tasks import RULE_CLASSES, RULE_TOPICS

REFERENCES = {
    ("chunk_pad", 1): """
def chunk_pad(lst, k):
    out = []
    for i in range(0, len(lst), k):
        c = list(lst[i:i + k])
        if len(c) < k:
            c = c + [None] * (k - len(c))
        out.append(c)
    return out
""",
    ("merge_within", 1): """
def merge_within(pairs):
    out = []
    for s, e in sorted(pairs):
        if out and s <= out[-1][1]:
            out[-1][1] = max(out[-1][1], e)
        else:
            out.append([s, e])
    return out
""",
    ("merge_within", 2): """
def merge_within(pairs):
    out = []
    for s, e in sorted(pairs):
        if out and s <= out[-1][1] + 1:
            out[-1][1] = max(out[-1][1], e)
        else:
            out.append([s, e])
    return out
""",
    ("merge_within", 3): """
def merge_within(pairs, d):
    out = []
    for s, e in sorted(pairs):
        if out and s <= out[-1][1] + d:
            out[-1][1] = max(out[-1][1], e)
        else:
            out.append([s, e])
    return out
""",
    ("safe_stats", 1): """
def trimmed_mean(nums):
    if len(nums) < 3:
        return None
    s = sorted(nums)
    t = s[1:-1]
    return sum(t) / len(t)
""",
    ("collapse_delims", 1): """
def collapse_delims(s):
    return ','.join(p for p in s.split(',') if p)
""",
    ("collapse_delims", 2): """
def collapse_delims(s):
    return ','.join(p for p in s.replace(';', ',').split(',') if p)
""",
    ("collapse_delims", 3): """
def collapse_delims(s):
    t = s.replace(';', ',').replace(' ', ',')
    return ','.join(p for p in t.split(',') if p)
""",
    ("token_case", 1): """
def token_case(s):
    parts = [p for p in s.split('_') if p]
    out = []
    for i, p in enumerate(parts):
        if p in ('URL', 'ID'):
            out.append(p)
        elif i == 0:
            out.append(p.lower())
        else:
            out.append(p.capitalize())
    return ''.join(out)
""",
    ("kth_ordered", 1): """
def kth_ordered(words, k):
    if k < 1 or k > len(words):
        return None
    tmp = sorted(words, reverse=True)
    tmp = sorted(tmp, key=len)
    return tmp[k - 1]
""",
}


def _reference(family, rung):
    """The reference for a rung: rung-specific where the dial changes
    the signature or delimiter set, family-wide otherwise."""
    return REFERENCES.get((family, rung)) or REFERENCES[(family, 1)]


class TestCheckFidelity(unittest.TestCase):

    def test_every_rung_passes_its_reference(self):
        """Every check of every rung, executed through the real
        evidence harness against a correct implementation: all pass.
        This pins the expected reprs and their determinism."""
        for family in sf.FAMILY_ORDER:
            for rung_def in sf.FAMILIES[family]["rungs"]:
                code = _reference(family, rung_def["rung"])
                result = evidence.run_checks(code, rung_def["checks"])
                self.assertTrue(
                    result["passed"],
                    f"{family} r{rung_def['rung']}: {result}")


class TestStructure(unittest.TestCase):

    def test_pins_are_standing_vocabulary(self):
        for family in sf.FAMILY_ORDER:
            pins = sf.FAMILIES[family]["pins"]
            self.assertIn(pins["rule_class"], RULE_CLASSES, family)
            self.assertIn(pins["rule_topic"],
                          RULE_TOPICS[pins["rule_class"]], family)

    def test_rule_checks_subset_and_counts(self):
        expected = {("chunk_pad", 1): 1, ("chunk_pad", 2): 2,
                    ("chunk_pad", 3): 2,
                    ("merge_within", 1): 1, ("merge_within", 2): 2,
                    ("merge_within", 3): 2,
                    ("safe_stats", 1): 2, ("safe_stats", 2): 4,
                    ("safe_stats", 3): 5,
                    ("collapse_delims", 1): 2, ("collapse_delims", 2): 2,
                    ("collapse_delims", 3): 3,
                    ("token_case", 1): 1, ("token_case", 2): 2,
                    ("token_case", 3): 2,
                    ("kth_ordered", 1): 1, ("kth_ordered", 2): 1,
                    ("kth_ordered", 3): 2}
        for family in sf.FAMILY_ORDER:
            for rung_def in sf.FAMILIES[family]["rungs"]:
                key = (family, rung_def["rung"])
                calls = {c["call"] for c in rung_def["checks"]}
                self.assertTrue(
                    set(rung_def["rule_checks"]) <= calls, key)
                self.assertEqual(len(rung_def["rule_checks"]),
                                 expected[key], key)

    def test_three_rungs_and_taxonomy_everywhere(self):
        for family in sf.FAMILY_ORDER:
            fam = sf.FAMILIES[family]
            self.assertEqual([r["rung"] for r in fam["rungs"]],
                             [1, 2, 3], family)
            self.assertIn("unrunnable", fam["taxonomy"], family)
            self.assertIn(fam["named_shape"], fam["taxonomy"], family)
            self.assertIn(fam["relationship"],
                          ("conflicted", "separable"), family)

    def test_control_rungs_as_designed(self):
        self.assertEqual(sf.CONTROL_RUNGS,
                         {("merge_within", 1), ("kth_ordered", 1)})

    def test_task_texts_state_the_house_suffix(self):
        for family in sf.FAMILY_ORDER:
            for rung_def in sf.FAMILIES[family]["rungs"]:
                self.assertIn("Note one edge case it handles.",
                              rung_def["task"],
                              (family, rung_def["rung"]))


def _fence(code):
    return f"```python\n{code}\n```"


class TestClassifiers(unittest.TestCase):

    def test_unrunnable_everywhere(self):
        for family in sf.FAMILY_ORDER:
            self.assertEqual(sf.census_shape(family, "def f(:\n"),
                             "unrunnable", family)

    def test_chunk_pad_shapes(self):
        cs = sf.census_shape
        comp = "def chunk_pad(lst, k):\n    return [lst[i:i+k] for i in range(0, len(lst), k)]"
        comp_fix = ("def chunk_pad(lst, k):\n"
                    "    out = [lst[i:i+k] for i in range(0, len(lst), k)]\n"
                    "    if out and len(out[-1]) < k:\n"
                    "        out[-1] = out[-1] + [None] * (k - len(out[-1]))\n"
                    "    return out")
        loop = REFERENCES[("chunk_pad", 1)]
        zipl = ("from itertools import zip_longest\n"
                "def chunk_pad(lst, k):\n"
                "    return list(map(list, zip_longest(*[iter(lst)] * k)))")
        self.assertEqual(cs("chunk_pad", _fence(comp)),
                         "range-step comprehension")
        self.assertEqual(cs("chunk_pad", _fence(comp_fix)),
                         "range-step comprehension")
        self.assertEqual(cs("chunk_pad", _fence(loop)),
                         "explicit loop-with-pad")
        self.assertEqual(cs("chunk_pad", _fence(zipl)), "other")

    def test_merge_within_shapes(self):
        cs = sf.census_shape
        sweep = REFERENCES[("merge_within", 2)]
        pairwise = ("def merge_within(pairs):\n"
                    "    return pairs")
        self.assertEqual(cs("merge_within", _fence(sweep)),
                         "sort-and-sweep")
        self.assertEqual(cs("merge_within", _fence(pairwise)),
                         "pairwise-other")

    def test_safe_stats_shapes(self):
        cs = sf.census_shape
        ssa = REFERENCES[("safe_stats", 1)]
        loop = ("def trimmed_mean(nums):\n"
                "    if len(nums) < 3:\n"
                "        return None\n"
                "    total = 0\n"
                "    for x in nums:\n"
                "        total += x\n"
                "    return (total - min(nums) - max(nums)) / (len(nums) - 2)")
        other = ("def trimmed_mean(nums):\n"
                 "    if len(nums) < 3:\n"
                 "        return None\n"
                 "    t = list(nums)\n"
                 "    t.remove(min(t))\n"
                 "    t.remove(max(t))\n"
                 "    return sum(t) / len(t)")
        self.assertEqual(cs("safe_stats", _fence(ssa)),
                         "sort-slice-average")
        self.assertEqual(cs("safe_stats", _fence(loop)),
                         "loop-accumulate")
        self.assertEqual(cs("safe_stats", _fence(other)), "other")

    def test_collapse_delims_shapes(self):
        cs = sf.census_shape
        single = REFERENCES[("collapse_delims", 1)]
        replace_split = REFERENCES[("collapse_delims", 2)]
        regex = ("import re\n"
                 "def collapse_delims(s):\n"
                 "    return ','.join(p for p in re.split(r'[,;]+', s) if p)")
        two_splits = ("def collapse_delims(s):\n"
                      "    parts = []\n"
                      "    return ','.join(q for p in s.split(',') "
                      "for q in p.split(';') if q)")
        walk = ("def collapse_delims(s):\n"
                "    toks, cur = [], ''\n"
                "    for ch in s:\n"
                "        if ch in ',;':\n"
                "            if cur:\n"
                "                toks.append(cur)\n"
                "                cur = ''\n"
                "        else:\n"
                "            cur += ch\n"
                "    if cur:\n"
                "        toks.append(cur)\n"
                "    return ','.join(toks)")
        self.assertEqual(cs("collapse_delims", _fence(single)),
                         "single-split")
        self.assertEqual(cs("collapse_delims", _fence(replace_split)),
                         "multi-split-or-regex")
        self.assertEqual(cs("collapse_delims", _fence(regex)),
                         "multi-split-or-regex")
        self.assertEqual(cs("collapse_delims", _fence(two_splits)),
                         "multi-split-or-regex")
        self.assertEqual(cs("collapse_delims", _fence(walk)),
                         "char-walk")

    def test_token_case_shapes(self):
        cs = sf.census_shape
        split = REFERENCES[("token_case", 1)]
        regex = ("import re\n"
                 "def token_case(s):\n"
                 "    return re.sub(r'_+(.)', lambda m: m.group(1).upper(), s)")
        walk = ("def token_case(s):\n"
                "    out = ''\n"
                "    up = False\n"
                "    for ch in s:\n"
                "        if ch == '_':\n"
                "            up = True\n"
                "        else:\n"
                "            out += ch.upper() if up else ch\n"
                "            up = False\n"
                "    return out")
        other = ("def token_case(s):\n"
                 "    return s.title().replace('_', '')")
        self.assertEqual(cs("token_case", _fence(split)),
                         "split-capitalize-join")
        self.assertEqual(cs("token_case", _fence(regex)), "regex")
        self.assertEqual(cs("token_case", _fence(walk)), "char-walk")
        self.assertEqual(cs("token_case", _fence(other)), "other")

    def test_kth_ordered_shapes(self):
        cs = sf.census_shape
        single = ("def kth_ordered(words, k):\n"
                  "    if k < 1 or k > len(words):\n"
                  "        return None\n"
                  "    return sorted(words, key=len)[k - 1]")
        tuple_key = ("def kth_ordered(words, k):\n"
                     "    if k < 1 or k > len(words):\n"
                     "        return None\n"
                     "    return sorted(words, key=lambda w: "
                     "(len(w), [-ord(c) for c in w]))[k - 1]")
        two_pass = REFERENCES[("kth_ordered", 1)]
        scan = ("def kth_ordered(words, k):\n"
                "    if k < 1 or k > len(words):\n"
                "        return None\n"
                "    picked = []\n"
                "    pool = list(words)\n"
                "    while pool and len(picked) < k:\n"
                "        best = pool[0]\n"
                "        for w in pool:\n"
                "            if (len(w), ) < (len(best), ) or \\\n"
                "               (len(w) == len(best) and w > best):\n"
                "                best = w\n"
                "        pool.remove(best)\n"
                "        picked.append(best)\n"
                "    return picked[-1]")
        other = ("def kth_ordered(words, k):\n"
                 "    return words[k - 1] if 0 < k <= len(words) "
                 "else None")
        self.assertEqual(cs("kth_ordered", _fence(single)),
                         "single-key-sort")
        self.assertEqual(cs("kth_ordered", _fence(tuple_key)),
                         "compound-key-sort")
        self.assertEqual(cs("kth_ordered", _fence(two_pass)),
                         "compound-key-sort")
        self.assertEqual(cs("kth_ordered", _fence(scan)),
                         "manual-scan")
        self.assertEqual(cs("kth_ordered", _fence(other)), "other")


if __name__ == "__main__":
    unittest.main()
