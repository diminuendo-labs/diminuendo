"""Tests for the probe task pools, rule classes, the probe's repeats
parameter, and the contrastive generation accounting.

The pools are the probe's instrument, so the tests pin what the harness
relies on: well-formed tasks, disjoint pools, one of the four rule
classes on every task, two per class in the generation pool, a kept pool
of the sized band, and every check satisfiable by a correct reference
solution run through the real evidence harness. The probe tests use a
stub runner and a temp runs dir, no model calls."""

import importlib
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import evidence
import probe_tasks

# One reference solution per task, deliberately obeying every stated rule.
# All references share one namespace, so function names must stay unique
# across both pools, which the disjointness test also demands.
REFS = {
    # generation pool v2
    "max_index": (
        "def max_index(nums):\n"
        "    best = 0\n"
        "    for i, v in enumerate(nums):\n"
        "        if v >= nums[best]:\n"
        "            best = i\n"
        "    return best\n"),
    "shortest_word": (
        "def shortest_word(s):\n"
        "    words = s.split()\n"
        "    if not words:\n"
        "        return ''\n"
        "    best = words[0]\n"
        "    for w in words[1:]:\n"
        "        if len(w) <= len(best):\n"
        "            best = w\n"
        "    return best\n"),
    "count_unique": (
        "def count_unique(nums):\n"
        "    return sum(1 for v in set(nums) if nums.count(v) == 1)\n"),
    "sum_distinct": (
        "def sum_distinct(nums):\n"
        "    return sum(set(nums))\n"),
    "average": (
        "def average(nums):\n"
        "    if not nums:\n"
        "        return None\n"
        "    return sum(nums) / len(nums)\n"),
    "chunk": (
        "def chunk(lst, size):\n"
        "    if size <= 0:\n"
        "        return []\n"
        "    return [lst[i:i + size] for i in range(0, len(lst), size)]\n"),
    "count_word": (
        "def count_word(s, w):\n"
        "    return sum(1 for x in s.split() if x.lower() == w.lower())\n"),
    "equal_ignoring_spaces": (
        "def equal_ignoring_spaces(a, b):\n"
        "    return ''.join(a.split()).lower() == ''.join(b.split()).lower()\n"),
    "count_distinct_pairs": (
        "def count_distinct_pairs(nums, target):\n"
        "    pairs = set()\n"
        "    for i in range(len(nums)):\n"
        "        for j in range(i + 1, len(nums)):\n"
        "            if nums[i] + nums[j] == target:\n"
        "                pairs.add(tuple(sorted((nums[i], nums[j]))))\n"
        "    return len(pairs)\n"),
    "sum_of_modes": (
        "def sum_of_modes(nums):\n"
        "    if not nums:\n"
        "        return 0\n"
        "    top = max(nums.count(v) for v in set(nums))\n"
        "    return sum(v for v in set(nums) if nums.count(v) == top)\n"),
    "weighted_mean": (
        "def weighted_mean(values, weights):\n"
        "    if not values or not weights:\n"
        "        return None\n"
        "    total = sum(weights)\n"
        "    if total == 0:\n"
        "        return None\n"
        "    return sum(v * w for v, w in zip(values, weights)) / total\n"),
    "range_step": (
        "def range_step(start, stop, step):\n"
        "    if step <= 0:\n"
        "        return []\n"
        "    out = []\n"
        "    while start < stop:\n"
        "        out.append(start)\n"
        "        start += step\n"
        "    return out\n"),
    "title_words": (
        "def title_words(s):\n"
        "    out = []\n"
        "    for w in s.split():\n"
        "        if w.isupper():\n"
        "            out.append(w)\n"
        "        else:\n"
        "            out.append(w[:1].upper() + w[1:].lower())\n"
        "    return ' '.join(out)\n"),
    "count_token": (
        "def count_token(s, w):\n"
        "    import string\n"
        "    return sum(1 for x in s.split()\n"
        "               if x.strip(string.punctuation).lower() == w.lower())\n"),
    "longest_run_char": (
        "def longest_run_char(s):\n"
        "    best_char, best_len = '', 0\n"
        "    i = 0\n"
        "    while i < len(s):\n"
        "        j = i\n"
        "        while j < len(s) and s[j] == s[i]:\n"
        "            j += 1\n"
        "        if j - i >= best_len:\n"
        "            best_char, best_len = s[i], j - i\n"
        "        i = j\n"
        "    return best_char\n"),
    "least_frequent_word": (
        "def least_frequent_word(s):\n"
        "    words = s.lower().split()\n"
        "    if not words:\n"
        "        return ''\n"
        "    return min(set(words), key=lambda w: (words.count(w), w))\n"),
    "count_distinct_over": (
        "def count_distinct_over(nums, k):\n"
        "    return len({v for v in nums if v > k})\n"),
    "third_largest_distinct": (
        "def third_largest_distinct(nums):\n"
        "    d = sorted(set(nums))\n"
        "    return d[-3] if len(d) >= 3 else None\n"),
    "mode_count": (
        "def mode_count(nums):\n"
        "    if not nums:\n"
        "        return 0\n"
        "    top = max(nums.count(v) for v in set(nums))\n"
        "    return sum(1 for v in set(nums) if nums.count(v) == top)\n"),
    "clamp": (
        "def clamp(value, lo, hi):\n"
        "    if lo > hi:\n"
        "        return None\n"
        "    return max(lo, min(hi, value))\n"),
    "nth_page": (
        "def nth_page(items, size, n):\n"
        "    if size <= 0 or n < 1:\n"
        "        return []\n"
        "    return items[(n - 1) * size:n * size]\n"),
    "split_csvish": (
        "def split_csvish(s):\n"
        "    return [f.strip() for f in s.split(',') if f.strip()]\n"),
    "depth_max": (
        "def depth_max(s):\n"
        "    depth, best = 0, 0\n"
        "    for c in s:\n"
        "        if c == '[':\n"
        "            depth += 1\n"
        "            best = max(best, depth)\n"
        "        elif c == ']':\n"
        "            depth -= 1\n"
        "            if depth < 0:\n"
        "                return -1\n"
        "    return best if depth == 0 else -1\n"),
    # candidate application pool
    "second_largest": (
        "def second_largest(nums):\n"
        "    d = sorted(set(nums))\n"
        "    return d[-2] if len(d) >= 2 else None\n"),
    "most_common_word": (
        "def most_common_word(s):\n"
        "    words = s.lower().split()\n"
        "    if not words:\n"
        "        return ''\n"
        "    return min(set(words), key=lambda w: (-words.count(w), w))\n"),
    "top_k": (
        "def top_k(nums, k):\n"
        "    if k <= 0:\n"
        "        return []\n"
        "    return sorted(nums, reverse=True)[:k]\n"),
    "dedupe": (
        "def dedupe(items):\n"
        "    seen, out = set(), []\n"
        "    for x in items:\n"
        "        if x not in seen:\n"
        "            seen.add(x)\n"
        "            out.append(x)\n"
        "    return out\n"),
    "mode": (
        "def mode(nums):\n"
        "    if not nums:\n"
        "        return None\n"
        "    return min(set(nums), key=lambda v: (-nums.count(v), v))\n"),
    "merge_ranges": (
        "def merge_ranges(pairs):\n"
        "    out = []\n"
        "    for a, b in sorted(pairs):\n"
        "        if out and a <= out[-1][1] + 1:\n"
        "            out[-1][1] = max(out[-1][1], b)\n"
        "        else:\n"
        "            out.append([a, b])\n"
        "    return out\n"),
    "longest_word": (
        "def longest_word(s):\n"
        "    best = ''\n"
        "    for w in s.split():\n"
        "        if len(w) >= len(best):\n"
        "            best = w\n"
        "    return best\n"),
    "median": (
        "def median(nums):\n"
        "    if not nums:\n"
        "        return None\n"
        "    s = sorted(nums)\n"
        "    n = len(s)\n"
        "    if n % 2:\n"
        "        return s[n // 2]\n"
        "    return (s[n // 2 - 1] + s[n // 2]) / 2\n"),
    "range_summary": (
        "def range_summary(nums):\n"
        "    vals = sorted(set(nums))\n"
        "    if not vals:\n"
        "        return ''\n"
        "    pieces, start, prev = [], vals[0], vals[0]\n"
        "    for v in vals[1:] + [None]:\n"
        "        if v is not None and v == prev + 1:\n"
        "            prev = v\n"
        "            continue\n"
        "        pieces.append(str(start) if start == prev\n"
        "                      else str(start) + '-' + str(prev))\n"
        "        if v is not None:\n"
        "            start = prev = v\n"
        "    return ','.join(pieces)\n"),
    "flatten_once": (
        "def flatten_once(lst):\n"
        "    out = []\n"
        "    for x in lst:\n"
        "        if isinstance(x, list):\n"
        "            out.extend(x)\n"
        "        else:\n"
        "            out.append(x)\n"
        "    return out\n"),
    "snake_to_camel": (
        "def snake_to_camel(s):\n"
        "    parts = [p for p in s.split('_') if p]\n"
        "    if not parts:\n"
        "        return ''\n"
        "    return parts[0] + ''.join(p.capitalize() for p in parts[1:])\n"),
    "nth_smallest": (
        "def nth_smallest(nums, n):\n"
        "    d = sorted(set(nums))\n"
        "    if n < 1 or n > len(d):\n"
        "        return None\n"
        "    return d[n - 1]\n"),
    "is_rotation": (
        "def is_rotation(a, b):\n"
        "    return len(a) == len(b) and b in a + a\n"),
    "truncate_words": (
        "def truncate_words(s, n):\n"
        "    if n <= 0:\n"
        "        return ''\n"
        "    return ' '.join(s.split()[:n])\n"),
    "balanced": (
        "def balanced(s):\n"
        "    depth = 0\n"
        "    for c in s:\n"
        "        if c == '(':\n"
        "            depth += 1\n"
        "        elif c == ')':\n"
        "            depth -= 1\n"
        "            if depth < 0:\n"
        "                return False\n"
        "    return depth == 0\n"),
    "interleave": (
        "def interleave(a, b):\n"
        "    out = []\n"
        "    for i in range(max(len(a), len(b))):\n"
        "        if i < len(a):\n"
        "            out.append(a[i])\n"
        "        if i < len(b):\n"
        "            out.append(b[i])\n"
        "    return out\n"),
    "count_pairs": (
        "def count_pairs(nums, target):\n"
        "    n = len(nums)\n"
        "    return sum(1 for i in range(n) for j in range(i + 1, n)\n"
        "               if nums[i] + nums[j] == target)\n"),
}


def _all_tasks():
    return probe_tasks.CANDIDATE_GEN_TASKS + probe_tasks.CANDIDATE_APPLY_TASKS


class TestPools(unittest.TestCase):

    def test_task_format(self):
        for t in _all_tasks():
            self.assertTrue(t["name"])
            self.assertIsInstance(t["task"], str)
            self.assertIn(t["name"] + "(", t["task"])
            self.assertTrue(3 <= len(t["checks"]) <= 5,
                            f"{t['name']}: {len(t['checks'])} checks")
            for c in t["checks"]:
                self.assertIsInstance(c["call"], str)
                self.assertIsInstance(c["expect"], str)
                self.assertTrue(c["call"].startswith(t["name"] + "("),
                                f"{t['name']}: check calls {c['call']}")

    def test_pool_sizes(self):
        self.assertTrue(4 <= len(probe_tasks.GEN_TASKS) <= 12)
        self.assertTrue(14 <= len(probe_tasks.CANDIDATE_GEN_TASKS) <= 24)
        self.assertTrue(14 <= len(probe_tasks.CANDIDATE_APPLY_TASKS) <= 18)

    def test_pools_disjoint(self):
        gen = {t["name"] for t in probe_tasks.CANDIDATE_GEN_TASKS}
        app = {t["name"] for t in probe_tasks.CANDIDATE_APPLY_TASKS}
        self.assertEqual(len(gen), len(probe_tasks.CANDIDATE_GEN_TASKS))
        self.assertEqual(len(app), len(probe_tasks.CANDIDATE_APPLY_TASKS))
        self.assertFalse(gen & app)
        gen_texts = {t["task"] for t in probe_tasks.CANDIDATE_GEN_TASKS}
        app_texts = {t["task"] for t in probe_tasks.CANDIDATE_APPLY_TASKS}
        self.assertFalse(gen_texts & app_texts)

    def test_gen_kept_selected_from_candidates(self):
        names = {t["name"] for t in probe_tasks.CANDIDATE_GEN_TASKS}
        self.assertEqual(len(set(probe_tasks.GEN_KEPT)),
                         len(probe_tasks.GEN_KEPT))
        self.assertTrue(set(probe_tasks.GEN_KEPT) <= names)
        self.assertEqual(len(probe_tasks.GEN_TASKS),
                         len(probe_tasks.GEN_KEPT))

    def test_tie_break_tasks_carry_stated_direction(self):
        """PACKET-005: every tie_break task states its direction, so
        lessons can pin it and the menu can refuse contradictions."""
        for t in _all_tasks():
            if t["rule_class"] == "tie_break":
                self.assertIn(t.get("stated_direction"),
                              ("last", "first", "alphabetical", "smallest"),
                              t["name"])

    def test_every_task_carries_a_rule_topic(self):
        """PACKET-008: the topic vocabulary is fixed per class, and every
        task names the thing its stated rule governs."""
        self.assertEqual(set(probe_tasks.RULE_TOPICS),
                         set(probe_tasks.RULE_CLASSES))
        for t in _all_tasks():
            self.assertIn(t.get("rule_topic"),
                          probe_tasks.RULE_TOPICS[t["rule_class"]],
                          t["name"])

    def test_kept_apply_tasks_carry_rule_checks(self):
        """PACKET-005: the report's sharp level needs to know which checks
        encode each task's stated rule."""
        for t in probe_tasks.APPLY_TASKS:
            calls = {c["call"] for c in t["checks"]}
            self.assertTrue(t.get("rule_checks"), t["name"])
            self.assertTrue(set(t["rule_checks"]) <= calls, t["name"])

    def test_every_task_carries_a_rule_class(self):
        """PACKET-002: exactly four classes, every task carries one."""
        self.assertEqual(set(probe_tasks.RULE_CLASSES),
                         {"tie_break", "distinctness", "boundary",
                          "normalize"})
        for t in _all_tasks():
            self.assertIn(t["rule_class"], probe_tasks.RULE_CLASSES,
                          f"{t['name']}: {t.get('rule_class')}")

    def test_gen_pool_law_topic_coverage(self):
        """PACKET-010: the conjunction filter replaces the two-per-class
        law. Every kept generation task's (rule_class, rule_topic) pair
        exists in the apply pool, so no committed lesson can pin to an
        orphan topic. The breakage half of the conjunction lives in the
        calibration record in the module docstring."""
        apply_pairs = {(t["rule_class"], t["rule_topic"])
                       for t in probe_tasks.APPLY_TASKS}
        for t in probe_tasks.GEN_TASKS:
            self.assertIn((t["rule_class"], t["rule_topic"]), apply_pairs,
                          t["name"])

    def test_kept_pool_covers_every_class(self):
        classes = {t["rule_class"] for t in probe_tasks.APPLY_TASKS}
        self.assertEqual(classes, set(probe_tasks.RULE_CLASSES))

    def test_kept_pool_selected_from_candidates(self):
        names = {t["name"] for t in probe_tasks.CANDIDATE_APPLY_TASKS}
        self.assertTrue(8 <= len(probe_tasks.KEPT) <= 12)
        self.assertEqual(len(set(probe_tasks.KEPT)), len(probe_tasks.KEPT))
        self.assertTrue(set(probe_tasks.KEPT) <= names)
        self.assertEqual(len(probe_tasks.APPLY_TASKS),
                         len(probe_tasks.KEPT))

    def test_every_check_satisfiable_by_reference(self):
        """All references in one blob, all checks in one subprocess run of
        the real evidence harness. A check no correct solution can pass is
        a broken instrument, and this is the tripwire for it."""
        tasks = _all_tasks()
        missing = [t["name"] for t in tasks if t["name"] not in REFS]
        self.assertFalse(missing, f"tasks without a reference: {missing}")
        code = "\n".join(REFS[t["name"]] for t in tasks)
        checks = [c for t in tasks for c in t["checks"]]
        res = evidence.run_checks(code, checks)
        bad = [r for r in res.get("results", []) if not r["ok"]]
        self.assertTrue(res["passed"],
                        f"error={res['error']} failing={bad}")


class _ProbeHarness(unittest.TestCase):
    """Shared setup: temp runs dir, reloaded probe, stubbed model calls.
    Tests never write into the real runs/ record."""

    def setUp(self):
        import lesson
        import runner
        self._lesson = lesson
        self._runner = runner
        self._real_runs = runner.RUNS
        self._real_run_once = runner.run_once
        self._real_contrastive = lesson.generate_contrastive
        self._real_sibling = lesson.generate_sibling_contrast
        self._tmp = tempfile.TemporaryDirectory()
        runner.RUNS = self._tmp.name
        import probe
        # reload so the probe's module-level log paths land in the temp dir
        self.probe = importlib.reload(probe)

    def tearDown(self):
        self._runner.RUNS = self._real_runs
        self._runner.run_once = self._real_run_once
        self._lesson.generate_contrastive = self._real_contrastive
        self._lesson.generate_sibling_contrast = self._real_sibling
        importlib.reload(self.probe)
        self._tmp.cleanup()

    def _pattern(self, patterns):
        """ev_passed_fn from per-task pass patterns, for gen-phase stubs.
        Call order in the gen phase is GEN_TASKS order, R_G reps each."""
        def fn(i):
            t = probe_tasks.GEN_TASKS[i // self.probe.R_G]
            return patterns.get(t["name"], [True] * self.probe.R_G)[
                i % self.probe.R_G]
        return fn

    def _stub_run(self, ev_passed_fn):
        """run_once stub: ev_passed_fn(call_index) decides evidence."""
        calls = []

        def stub(task, criteria, work_features, **kw):
            ok = ev_passed_fn(len(calls))
            calls.append(task)
            return {"run_id": f"stub-{len(calls)}",
                    "node_id": f"node-{len(calls)}",
                    "verdict": "pass" if ok else "fail",
                    "output": "def f(): pass",
                    "evidence": {"passed": ok,
                                 "results": [{"ok": ok, "call": "f()",
                                              "got": "1", "expect": "1"}],
                                 "error": None}}

        self._runner.run_once = stub
        return calls

    def _stub_contrastive(self):
        made = []

        def stub(task_text, work_features, fail_s, pass_s, model=None):
            made.append(task_text)
            return {"concept": "Honor the stated tie direction when the "
                               "task names one.",
                    "rule": "on ties return the last occurrence",
                    "applies_when": dict(work_features),
                    "confidence": 0.5, "provenance": "engine",
                    "trail": {"node_id": fail_s["node_id"],
                              "contrast_node_id": pass_s["node_id"],
                              "work_features": work_features}}

        self._lesson.generate_contrastive = stub
        return made

    def _stub_sibling(self):
        made = []

        def stub(fail_task_text, pass_task_text, rule_class, work_features,
                 fail_s, pass_s, model=None):
            made.append(rule_class)
            return {"concept": "Find the stated rule of the class in the "
                               "task text and honor it in the code path "
                               "it governs.",
                    "rule": f"the stated {rule_class} rule, honored in "
                            f"the sibling task",
                    "applies_when": dict(work_features),
                    "confidence": 0.5, "provenance": "engine",
                    "trail": {"node_id": fail_s["node_id"],
                              "contrast_node_id": pass_s["node_id"],
                              "contrast_type": "sibling",
                              "work_features": work_features}}

        self._lesson.generate_sibling_contrast = stub
        return made


class TestProbeRepeats(_ProbeHarness):

    def test_repeats_multiplies_runs_and_reports_n(self):
        calls = self._stub_run(lambda i: True)
        out = self.probe.run_cell("A", None, repeats=3)
        expect = len(probe_tasks.APPLY_TASKS) * 3
        self.assertEqual(len(calls), expect)
        self.assertEqual(out["n"], expect)
        self.assertEqual(out["ev_mean"], 1.0)
        self.assertEqual(out["pass_rate"], 1.0)
        # every run checkpointed as its own row
        with open(self.probe._ROWS, encoding="utf-8") as f:
            rows = [l for l in f if l.strip()]
        self.assertEqual(len(rows), expect)

    def test_per_class_breakdown_covers_all_runs(self):
        self._stub_run(lambda i: True)
        out = self.probe.run_cell("A", None, repeats=2)
        self.assertEqual(sum(v["n"] for v in out["per_class"].values()),
                         out["n"])
        expected = {t["rule_class"] for t in probe_tasks.APPLY_TASKS}
        self.assertEqual(set(out["per_class"]), expected)


class TestContrastAccounting(_ProbeHarness):

    def test_all_mixed_respects_the_per_class_cap(self):
        # first attempt of each task fails evidence, the rest pass
        self._stub_run(lambda i: i % self.probe.R_G != 0)
        made = self._stub_contrastive()
        made_sib = self._stub_sibling()
        accounting = self.probe.gen_lessons("A")
        classes = {t["rule_class"] for t in probe_tasks.GEN_TASKS}
        self.assertEqual({e["rule_class"] for e in accounting}, classes)
        self.assertEqual(made_sib, [])  # within-task covered every class
        expected_total = 0
        for e in accounting:
            in_class = sum(1 for t in probe_tasks.GEN_TASKS
                           if t["rule_class"] == e["rule_class"])
            self.assertEqual(len(e["lessons"]), min(2, in_class))
            expected_total += min(2, in_class)
            self.assertTrue(all(l["type"] == "within_task" and l["committed"]
                                for l in e["lessons"]))
        self.assertEqual(len(made), expected_total)
        store = self._lesson.load(self.probe.store("A"))
        self.assertEqual(len(store), expected_total)
        # the committed lesson carries its class in applies_when
        self.assertIn("rule_class", store[0]["applies_when"])

    def test_no_contrast_yields_no_lesson(self):
        self._stub_run(lambda i: True)  # every attempt passes
        made = self._stub_contrastive()
        made_sib = self._stub_sibling()
        accounting = self.probe.gen_lessons("A")
        self.assertEqual(made, [])
        self.assertEqual(made_sib, [])
        for e in accounting:
            self.assertEqual(e["lessons"], [])
            self.assertEqual(e["reason"],
                             "both siblings all_pass, nothing broke")
        self.assertEqual(self._lesson.load(self.probe.store("A")), [])

    def test_within_task_takes_precedence_over_sibling(self):
        # max_index mixed, its tie_break sibling all_pass: the class gets
        # its lesson from the cleaner within-task pair, sibling never fires
        self._stub_run(self._pattern({"max_index": [False, True, True]}))
        made = self._stub_contrastive()
        made_sib = self._stub_sibling()
        accounting = self.probe.gen_lessons("A")
        tie = next(e for e in accounting if e["rule_class"] == "tie_break")
        self.assertEqual(len(made), 1)
        self.assertEqual(made_sib, [])
        self.assertEqual([l["type"] for l in tie["lessons"]],
                         ["within_task"])
        self.assertTrue(tie["lessons"][0]["committed"])

    def test_sibling_fires_when_one_sibling_all_fails(self):
        # max_index all_fail, shortest_word all_pass: the PACKET-002
        # starvation case, now teachable through the sibling pair
        self._stub_run(self._pattern({"max_index": [False, False, False]}))
        made = self._stub_contrastive()
        made_sib = self._stub_sibling()
        accounting = self.probe.gen_lessons("A")
        tie = next(e for e in accounting if e["rule_class"] == "tie_break")
        self.assertEqual(made, [])
        self.assertEqual(made_sib, ["tie_break"])
        self.assertEqual(tie["cases"]["max_index"], "all_fail")
        self.assertEqual(tie["cases"]["shortest_word"], "all_pass")
        lesson_entry = tie["lessons"][0]
        self.assertEqual(lesson_entry["type"], "sibling")
        self.assertEqual(lesson_entry["task"], "max_index")
        self.assertEqual(lesson_entry["sibling"], "shortest_word")
        self.assertTrue(lesson_entry["committed"])
        store = self._lesson.load(self.probe.store("A"))
        self.assertEqual(len(store), 1)
        self.assertEqual(store[0]["trail"]["contrast_type"], "sibling")

    def test_all_fail_class_yields_no_lesson(self):
        self._stub_run(self._pattern(
            {"max_index": [False] * 3, "shortest_word": [False] * 3,
             "longest_run_char": [False] * 3,
             "least_frequent_word": [False] * 3}))
        made = self._stub_contrastive()
        made_sib = self._stub_sibling()
        accounting = self.probe.gen_lessons("A")
        tie = next(e for e in accounting if e["rule_class"] == "tie_break")
        self.assertEqual(made, [])
        self.assertEqual(made_sib, [])
        self.assertEqual(tie["lessons"], [])
        self.assertEqual(tie["reason"], "all_fail with no passing sibling")
        self.assertEqual(self._lesson.load(self.probe.store("A")), [])

    def test_cap_mines_all_fail_sibling_next_to_mined_task(self):
        """PACKET-005, conductor-approved: the per-class cap replaces the
        has-a-lesson trigger. PACKET-003's unmined shape, max_index mixed
        and shortest_word all_fail, now yields both lessons."""
        self._stub_run(self._pattern({"max_index": [False, True, True],
                                      "shortest_word": [False] * 3}))
        made = self._stub_contrastive()
        made_sib = self._stub_sibling()
        accounting = self.probe.gen_lessons("A")
        tie = next(e for e in accounting if e["rule_class"] == "tie_break")
        self.assertEqual(len(made), 1)
        self.assertEqual(made_sib, ["tie_break"])
        entries = {(l["type"], l["task"], l["committed"])
                   for l in tie["lessons"]}
        self.assertIn(("within_task", "max_index", True), entries)
        self.assertIn(("sibling", "shortest_word", True), entries)
        self.assertEqual(len(self._lesson.load(self.probe.store("A"))), 2)


class TestCheckTable(unittest.TestCase):

    def test_rates_and_rule_marking(self):
        import probe
        rows = [
            {"phase": "apply", "cell": "B|none", "task": "longest_word",
             "checks": {"longest_word('cat door bird')": False,
                        "longest_word('')": True}},
            {"phase": "apply", "cell": "B|none", "task": "longest_word",
             "checks": {"longest_word('cat door bird')": True,
                        "longest_word('')": True}},
            {"phase": "gen", "task": "max_index",
             "checks": {"max_index([1, 3, 3])": True}},
        ]
        table = probe.check_table(rows)
        tie = table["longest_word"]["longest_word('cat door bird')"]
        self.assertTrue(tie["rule_check"])
        self.assertEqual(tie["cells"]["B|none"]["n"], 2)
        self.assertAlmostEqual(tie["cells"]["B|none"]["rate"], 0.5)
        self.assertFalse(
            table["longest_word"]["longest_word('')"]["rule_check"])
        self.assertNotIn("max_index", table)  # gen rows never enter


class TestProbeResume(_ProbeHarness):
    """A killed run resumes from its own checkpoint rows and summaries.
    Paid for twice: the environment stopped a multi-hour probe mid-run."""

    def test_resume_skips_checkpointed_apply_runs(self):
        for i, t in enumerate(probe_tasks.APPLY_TASKS):
            self.probe._row({"phase": "apply", "cell": "A|none",
                             "task": t["name"],
                             "rule_class": t["rule_class"], "rep": 0,
                             "run_id": f"prior-{i}", "tools": 0,
                             "verdict": "fail", "ev": 0.5})
        calls = self._stub_run(lambda i: True)
        prior = self.probe._load_rows()
        out = self.probe.run_cell("A", None, repeats=2, prior_rows=prior)
        # only the second rep ran live, the first was counted from disk
        self.assertEqual(len(calls), len(probe_tasks.APPLY_TASKS))
        self.assertEqual(out["n"], len(probe_tasks.APPLY_TASKS) * 2)
        # prior rows are in the aggregate: 8 at 0.5 and 8 at 1.0
        self.assertAlmostEqual(out["ev_mean"], 0.75)

    def test_resume_gen_reloads_summaries_and_skips_committed_lesson(self):
        import json as _json
        target = probe_tasks.GEN_TASKS[0]
        for rep, ok in enumerate((False, True, True)):
            rid = f"g{rep}"
            self.probe._row({"phase": "gen", "model": "A",
                             "task": target["name"],
                             "rule_class": target["rule_class"],
                             "rep": rep, "run_id": rid,
                             "verdict": "pass" if ok else "fail",
                             "ev": 1.0 if ok else 0.0, "ev_passed": ok})
            with open(os.path.join(self._runner.RUNS,
                                   f"{rid}.summary.json"), "w",
                      encoding="utf-8") as f:
                _json.dump({"run_id": rid, "node_id": f"task-{rid}",
                            "verdict": "pass" if ok else "fail",
                            "output": "def f(): pass",
                            "evidence": {"passed": ok,
                                         "results": [{"ok": ok,
                                                      "call": "f()",
                                                      "got": "1",
                                                      "expect": "1"}],
                                         "error": None}}, f)
        calls = self._stub_run(lambda i: True)  # live reruns all pass
        made = self._stub_contrastive()
        self._stub_sibling()
        prior = self.probe._load_rows()
        acc = self.probe.gen_lessons("A", prior_rows=prior)
        # the checkpointed task never re-ran, the other tasks ran live
        self.assertEqual(len(calls),
                         (len(probe_tasks.GEN_TASKS) - 1) * self.probe.R_G)
        self.assertEqual(len(made), 1)
        cls_entry = next(e for e in acc
                         if e["rule_class"] == target["rule_class"])
        self.assertEqual(cls_entry["cases"][target["name"]], "mixed")
        self.assertTrue(cls_entry["lessons"][0]["committed"])
        # a second resume does not distill the same contrast twice
        acc2 = self.probe.gen_lessons("A", prior_rows=prior)
        self.assertEqual(len(made), 1)
        cls_entry2 = next(e for e in acc2
                          if e["rule_class"] == target["rule_class"])
        self.assertTrue(cls_entry2["lessons"][0]["committed"])


if __name__ == "__main__":
    unittest.main()
