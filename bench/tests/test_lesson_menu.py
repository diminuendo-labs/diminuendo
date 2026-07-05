"""Tests for the lesson engine's rules and the menu's matching. The live
generation path is exercised by the loop itself, these test the gates."""

import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import lesson
import menu


def _lesson(**over):
    base = {
        "concept": "State the empty-input convention before writing the body.",
        "rule": "an empty list returns None, never zero",
        "applies_when": {"operation": "write_code", "language": "python"},
        "confidence": 0.5, "provenance": "engine",
        "trail": {"node_id": "task-x", "work_features": {}},
    }
    base.update(over)
    return base


class TestLessonGates(unittest.TestCase):

    def test_good_lesson_commits(self):
        with tempfile.TemporaryDirectory() as d:
            p = os.path.join(d, "lessons.jsonl")
            lesson.commit(p, _lesson())
            self.assertEqual(len(lesson.load(p)), 1)

    def test_metric_key_rejected(self):
        bad = _lesson(applies_when={"tokens": "many"})
        with self.assertRaises(Exception):
            lesson.validate(bad)

    def test_metric_prose_rejected(self):
        bad = _lesson(concept="Use fewer tokens by keeping answers short.")
        with self.assertRaises(lesson.LessonError):
            lesson.validate(bad)

    def test_bad_shapes_rejected(self):
        with self.assertRaises(lesson.LessonError):
            lesson.validate(_lesson(applies_when={}))
        with self.assertRaises(lesson.LessonError):
            lesson.validate(_lesson(confidence=1.5))
        with self.assertRaises(lesson.LessonError):
            lesson.validate(_lesson(provenance="vibes"))


class TestContentGate(unittest.TestCase):
    """PACKET-002: a lesson names a specific rule or it does not commit."""

    def test_missing_rule_rejected(self):
        bad = _lesson()
        del bad["rule"]
        with self.assertRaises(lesson.LessonError):
            lesson.validate(bad)

    def test_empty_rule_rejected(self):
        with self.assertRaises(lesson.LessonError):
            lesson.validate(_lesson(rule="   "))

    def test_platitude_concept_rejected(self):
        with self.assertRaises(lesson.LessonError):
            lesson.validate(_lesson(
                concept="Always consider edge cases when writing code."))

    def test_platitude_rule_rejected(self):
        for phrase in ("use built-in methods where possible",
                       "prioritize readability", "aim for efficiency",
                       "follow best practices", "write clean code"):
            with self.assertRaises(lesson.LessonError, msg=phrase):
                lesson.validate(_lesson(rule=phrase))

    def test_metric_term_in_rule_rejected(self):
        with self.assertRaises(lesson.LessonError):
            lesson.validate(_lesson(rule="keep the runtime short"))

    def test_specific_rule_passes(self):
        good = _lesson(rule="on ties return the last such word, not the first")
        self.assertEqual(lesson.validate(good), good)


class TestShapeScreen(unittest.TestCase):
    """PACKET-007, conductor-approved: the rule field is declarative
    about what the task states, never imperative about what code to
    write. The spec's own definition, enforced."""

    def test_packet006_harm_lesson_rejected(self):
        # the PACKET-006 harm lesson's rule, verbatim: the fixture
        with self.assertRaises(lesson.LessonError):
            lesson.validate(_lesson(
                rule="Convert potential pairs to tuples and sort them "
                     "before adding to a set to maintain uniqueness "
                     "regardless of order."))

    def test_packet005_lessons_pass(self):
        # the two pass fixtures, verbatim from probe 20260702-215407
        tie = _lesson(rule="follow the direction the task states")
        self.assertEqual(lesson.validate(tie), tie)
        upper = _lesson(rule="Follow the direction the task states, "
                             "specifically ensuring words already in all "
                             "uppercase remain unchanged.")
        self.assertEqual(lesson.validate(upper), upper)

    def test_listed_imperatives_rejected(self):
        for phrase in ("use a dictionary keyed by word",
                       "store in a set for lookup",
                       "loop over the indices in reverse",
                       "iterate from the end",
                       "call sorted on the values first",
                       "append to a result list",
                       "create a counter for each value",
                       "initialize the best index at zero"):
            with self.assertRaises(lesson.LessonError, msg=phrase):
                lesson.validate(_lesson(rule=phrase))

    def test_packet006_harm_concept_rejected(self):
        """PACKET-008: the imperative screen extends to the concept, the
        field that rides the menu. Fixture: the PACKET-006 harm lesson's
        concept text, verbatim."""
        with self.assertRaises(lesson.LessonError):
            lesson.validate(_lesson(
                concept="When the task states that each distinct pair "
                        "should be counted once no matter how many times "
                        "its values repeat, ensure that pairs are stored "
                        "in a way that disregards order."))

    def test_packet005_concepts_pass(self):
        tie = _lesson(concept="When the task states that if the largest "
                              "value appears more than once, return the "
                              "index of its last occurrence, ensure your "
                              "code follows this directive.")
        self.assertEqual(lesson.validate(tie), tie)
        upper = _lesson(concept="When the task states that words already "
                                "entirely uppercase stay exactly as they "
                                "are, respect that rule by not applying "
                                "title casing to those words.")
        self.assertEqual(lesson.validate(upper), upper)

    def test_prompts_carry_the_shape_instruction(self):
        """Both distiller prompts tell the generator what the screen
        enforces, so rejection is the backstop, not the teacher."""
        captured = []
        real = lesson.ollama_client.generate

        def capture(model, prompt, **kw):
            captured.append(prompt)
            return {"text": '{"concept": "When the task states a tie '
                            'direction, honor it.", '
                            '"rule": "follow the tie direction the task '
                            'states", '
                            '"applies_when": {"operation": "write_code"}, '
                            '"confidence": 0.5}',
                    "prompt_tokens": 0, "output_tokens": 0, "time_s": 0}

        lesson.ollama_client.generate = capture
        try:
            fail_summary = {"node_id": "n-fail",
                            "evidence": {"passed": False,
                                         "results": [{"ok": False,
                                                      "call": "max_index([1, 3, 3])",
                                                      "got": "1",
                                                      "expect": "2"}],
                                         "error": None}}
            pass_summary = {"node_id": "n-pass", "output": "def f(): pass"}
            features = {"operation": "write_code",
                        "rule_class": "tie_break",
                        "stated_direction": "last"}
            lesson.generate_contrastive("task text", features,
                                        fail_summary, pass_summary)
            lesson.generate_sibling_contrast(
                "fail task", "pass task", "tie_break", features,
                fail_summary, pass_summary)
        finally:
            lesson.ollama_client.generate = real
        self.assertEqual(len(captured), 2)
        for prompt in captured:
            self.assertIn("never how to code it", prompt)
            self.assertIn("The concept states what the task requires",
                          prompt)
            self.assertIn("pin rule_topic", prompt)
        # PACKET-009: both prompts demand class-level phrasing, the
        # within-task prompt aligned to the sibling's requirement
        self.assertIn("stated rule of the CLASS", captured[0])
        self.assertIn("stated rule of the class", captured[1])


class TestAimScreen(unittest.TestCase):
    """PACKET-005, conductor-approved: the rule text must share ground
    with the failing check that produced it."""

    # the failing check of the run that produced PACKET-003's misaimed
    # lesson: a shortest_word tie break
    FAIL_CHECKS = [{"call": "shortest_word('bb a cc d')",
                    "got": "'a'", "expect": "'d'"}]

    def _ground(self):
        return lesson.aim_ground(self.FAIL_CHECKS, "tie_break", "last")

    def test_misaimed_rule_rejected(self):
        # PACKET-003's misaimed lesson, verbatim: the wrong stated rule
        misaimed = "An empty string returns ''. Note one edge case it handles."
        with self.assertRaises(lesson.LessonError):
            lesson.screen_aim(misaimed, self._ground())

    def test_aimed_rule_passes(self):
        aimed = "On ties return the last such word, not the first."
        self.assertTrue(lesson.screen_aim(aimed, self._ground()))

    def test_conditional_phrasing_passes(self):
        conditional = "Follow the tie direction the task states."
        self.assertTrue(lesson.screen_aim(conditional, self._ground()))

    def test_generators_run_the_screen(self):
        """The screen is wired into the contrast path: a canned generator
        response carrying a misaimed rule dies before it becomes a
        candidate."""
        real = lesson.ollama_client.generate
        canned = {"text": '{"concept": "State the empty convention.", '
                          '"rule": "An empty string returns nothing.", '
                          '"applies_when": {"operation": "write_code"}, '
                          '"confidence": 0.5}',
                  "prompt_tokens": 0, "output_tokens": 0, "time_s": 0}
        lesson.ollama_client.generate = lambda *a, **k: canned
        try:
            fail_summary = {"node_id": "n-fail",
                            "evidence": {"passed": False,
                                         "results": [dict(self.FAIL_CHECKS[0],
                                                          ok=False)],
                                         "error": None}}
            pass_summary = {"node_id": "n-pass", "output": "def f(): pass"}
            features = {"operation": "write_code",
                        "rule_class": "tie_break",
                        "stated_direction": "last"}
            with self.assertRaises(lesson.LessonError):
                lesson.generate_contrastive("task text", features,
                                            fail_summary, pass_summary)
            with self.assertRaises(lesson.LessonError):
                lesson.generate_sibling_contrast(
                    "fail task", "pass task", "tie_break", features,
                    fail_summary, pass_summary)
        finally:
            lesson.ollama_client.generate = real


class TestMenu(unittest.TestCase):

    def test_matching_and_contradiction(self):
        lessons = [
            _lesson(concept="python one", confidence=0.4),
            _lesson(concept="rust only",
                    applies_when={"operation": "write_code",
                                  "language": "rust"}),
            _lesson(concept="wildcard", confidence=0.9,
                    applies_when={"operation": "*"}),
        ]
        tools = menu.query(lessons, {"operation": "write_code",
                                     "language": "python"})
        concepts = [t["concept"] for t in tools]
        self.assertIn("python one", concepts)
        self.assertIn("wildcard", concepts)
        self.assertNotIn("rust only", concepts)  # contradiction excluded
        # two matched conditions beat one, even at lower confidence
        self.assertEqual(concepts[0], "python one")

    def test_no_confidence_crosses_to_performer(self):
        tools = menu.query([_lesson()], {"operation": "write_code"})
        self.assertEqual(sorted(tools[0]), ["applies_when", "concept"])

    def test_rule_class_matching(self):
        """PACKET-002: a lesson pinned to a rule class surfaces for tasks
        of that class and is a contradiction for every other class."""
        pinned = _lesson(concept="tie lesson",
                         applies_when={"operation": "write_code",
                                       "rule_class": "tie_break"})
        base = {"operation": "write_code", "language": "python"}
        hits = menu.query([pinned], {**base, "rule_class": "tie_break"})
        self.assertEqual([t["concept"] for t in hits], ["tie lesson"])
        misses = menu.query([pinned], {**base, "rule_class": "boundary"})
        self.assertEqual(misses, [])

    def test_direction_mismatched_lesson_never_surfaces(self):
        """PACKET-005: a direction-specific lesson pins stated_direction
        in applies_when, and the menu never serves it to a task whose
        stated direction contradicts it."""
        pinned = _lesson(concept="last lesson",
                         rule="when the task states ties break toward the "
                              "last occurrence, return the last",
                         applies_when={"operation": "write_code",
                                       "rule_class": "tie_break",
                                       "stated_direction": "last"})
        base = {"operation": "write_code", "rule_class": "tie_break"}
        hits = menu.query([pinned], {**base, "stated_direction": "last"})
        self.assertEqual([t["concept"] for t in hits], ["last lesson"])
        misses = menu.query([pinned],
                            {**base, "stated_direction": "alphabetical"})
        self.assertEqual(misses, [])
        # a conditionally phrased lesson wildcards the direction and rides
        wild = _lesson(concept="conditional lesson",
                       applies_when={"operation": "write_code",
                                     "rule_class": "tie_break",
                                     "stated_direction": "*"})
        hits = menu.query([wild],
                          {**base, "stated_direction": "alphabetical"})
        self.assertEqual([t["concept"] for t in hits],
                         ["conditional lesson"])

    def test_malformed_lesson_declined_not_crashed(self):
        """PACKET-013 tier 1, conductor-ruled: a lesson missing the
        fields the menu consumes is declined, and the well-formed lesson
        beside it still rides."""
        good = _lesson(concept="good lesson")
        bad = {"concept": "no confidence field",
               "applies_when": {"operation": "write_code"}}
        tools = menu.query([bad, good], {"operation": "write_code"})
        self.assertEqual([t["concept"] for t in tools], ["good lesson"])
        self.assertEqual(menu.query([bad], {"operation": "write_code"}), [])

    def test_rule_topic_mismatch_never_surfaces(self):
        """PACKET-008: a topic-specific lesson pins rule_topic, and the
        menu never serves it to a task whose stated rule governs a
        different thing, even inside the same class."""
        punct = _lesson(concept="punctuation lesson",
                        applies_when={"operation": "write_code",
                                      "rule_class": "normalize",
                                      "rule_topic": "punctuation"})
        base = {"operation": "write_code", "rule_class": "normalize"}
        hits = menu.query([punct], {**base, "rule_topic": "punctuation"})
        self.assertEqual([t["concept"] for t in hits],
                         ["punctuation lesson"])
        misses = menu.query([punct], {**base, "rule_topic": "delimiters"})
        self.assertEqual(misses, [])
        # a genuinely general lesson wildcards the topic and rides the class
        wild = _lesson(concept="class lesson",
                       applies_when={"operation": "write_code",
                                     "rule_class": "normalize",
                                     "rule_topic": "*"})
        for topic in ("case", "whitespace", "punctuation", "delimiters"):
            hits = menu.query([wild], {**base, "rule_topic": topic})
            self.assertEqual([t["concept"] for t in hits],
                             ["class lesson"], topic)


if __name__ == "__main__":
    unittest.main()
