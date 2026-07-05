"""The Lesson Engine, minimal form. Tech Spec Section 5.

A lesson is a guiding concept plus the conditions on when it applies. Never a
metric. The engine here does the common case: an LLM distills a committed
lesson from the run's criteria-shaped feedback and the trace. The raw numbers
(time, tokens) never enter the generation prompt, which is the firewall's
relocation of the Goodhart risk made literal: the translation is blind.

Every lesson carries provenance: "engine" if the generator produced it,
"hand" if a human shaped it. The run log states which, every time.

The metric screen on lesson text is crude by design: a banned-term scan. It
cannot catch metric advice laundered into clever prose. That limit is stated
in the spec and stays stated here.

The content gate (PACKET-002) is crude the same way: a committed lesson must
carry a non-empty "rule" field naming the specific stated rule at the
failure's boundary, and the concept plus rule text is screened against a
platitude list. A word scan cannot catch an empty thought phrased freshly.
It catches the recorded failure mode: one-task procedures and generic advice
that name no rule.
"""

import json
import re
import time as _time

import ollama_client
from contracts import guard_no_metric

REQUIRED = ("concept", "rule", "applies_when", "confidence", "provenance",
            "trail")

_METRIC_TERMS = re.compile(
    r"\b(tokens?|token count|runtime|wall.?time|milliseconds|"
    r"faster|cheaper|score|per.?second)\b", re.IGNORECASE)

_PLATITUDES = re.compile(
    r"(consider\s+(?:all\s+|the\s+|every\s+)?(?:possible\s+)?edge\s+cases?|"
    r"handle\s+(?:all\s+|the\s+|every\s+)?(?:possible\s+)?edge\s+cases?|"
    r"account\s+for\s+(?:all\s+|the\s+)?edge\s+cases?|"
    r"built.?in\s+methods?|readability|efficiency|"
    r"best\s+practices?|clean\s+code)", re.IGNORECASE)

# ---------------------------------------------------------------------------
# The aim screen (PACKET-005, conductor-approved gate addition). A lesson's
# rule text must share ground with the failing check that produced it, so a
# rule quoting the wrong sentence of the task (the recorded PACKET-003
# failure) dies before commit. The ground is the failing checks' text plus
# the task's rule-class vocabulary, because the approved phrasing is
# conditional ("follow the tie direction the task states"), which names the
# class, not the function under test. Token overlap after stopword removal,
# crude and documented like the other screens: it cannot judge meaning, and
# a wrong sentence that happens to share class vocabulary slips through.
# It runs inside the contrast generators, the only place the failing check
# is in hand.
# ---------------------------------------------------------------------------

_AIM_STOPWORDS = {
    "the", "and", "for", "with", "are", "was", "its", "not", "never",
    "always", "when", "where", "which", "that", "this", "these", "those",
    "returns", "return", "returning", "function", "should", "must",
    "instead", "than", "then", "them", "they", "from", "into",
}

_CLASS_VOCAB = {
    "tie_break": {"tie", "ties", "break", "breaking", "breaks", "direction",
                  "last", "first", "alphabetical", "alphabetically",
                  "smallest", "largest", "occurrence"},
    "distinctness": {"distinct", "distinctness", "unique", "duplicate",
                     "duplicates", "once", "repeat", "repeats", "repeated"},
    "boundary": {"empty", "none", "zero", "boundary", "degenerate",
                 "float", "negative", "convention"},
    "normalize": {"normalize", "normalization", "case", "lowercase",
                  "uppercase", "whitespace", "punctuation", "collapse",
                  "collapsing", "ordering", "insensitive", "insensitively"},
}


def _aim_tokens(text):
    return {t for t in re.findall(r"[a-z0-9]+", str(text).lower())
            if len(t) >= 3 and t not in _AIM_STOPWORDS}


def aim_ground(fail_checks, rule_class=None, stated_direction=None):
    """The tokens an aimed rule must touch: the failing checks plus the
    rule-class vocabulary plus the task's stated direction if any."""
    ground = set()
    for c in fail_checks or []:
        for part in (c.get("call", ""), c.get("got", ""),
                     c.get("expect", "")):
            ground |= _aim_tokens(part)
    ground |= _CLASS_VOCAB.get(rule_class, set())
    if stated_direction:
        ground |= _aim_tokens(stated_direction)
    return ground


def screen_aim(rule_text, ground):
    """Raise when the rule text shares no ground with the failure. The
    committed lesson must be about the break that produced it."""
    hits = _aim_tokens(rule_text) & set(ground)
    if not hits:
        raise LessonError(
            "aim screen: rule text shares no ground with the failing check")
    return hits


# ---------------------------------------------------------------------------
# The declarative-shape screen (PACKET-007, extended to the concept field
# by PACKET-008, both conductor-approved). The spec's definition,
# enforced: a lesson is a concept plus conditions, never a procedure.
# PACKET-006 measured the one recipe-shaped lesson as the one that harmed
# the obedient seat, and PACKET-007 found the concept is the field that
# rides the menu, so both fields must state what the task requires, never
# how to code it. A pattern scan, crude and documented like the other
# screens: it catches the listed implementation imperatives and misses a
# procedure phrased around them.
# ---------------------------------------------------------------------------

_IMPERATIVE = re.compile(
    r"\b(convert(?:ing)?|use\s+a|stor(?:e|ed|ing)\s+in|sort(?:ing)?\s+them|"
    r"add(?:ing)?\s+to\s+a|loop(?:ing)?|iterat(?:e|ing)|call(?:ing)?|"
    r"append(?:ing)?\s+to|creat(?:e|ing)\s+a|initializ(?:e|ing))\b",
    re.IGNORECASE)


class LessonError(Exception):
    """The candidate lesson breaks a rule and is not committed."""


def validate(lesson):
    missing = [k for k in REQUIRED if k not in lesson]
    if missing:
        raise LessonError(f"lesson missing fields: {missing}")
    if lesson["provenance"] not in ("engine", "hand"):
        raise LessonError(f"unknown provenance: {lesson['provenance']}")
    if not isinstance(lesson["applies_when"], dict) or not lesson["applies_when"]:
        raise LessonError("applies_when must be a non-empty dict of conditions")
    if not (0.0 <= float(lesson["confidence"]) <= 1.0):
        raise LessonError("confidence must be in [0, 1]")
    if not str(lesson["rule"]).strip():
        raise LessonError("rule must name the specific stated rule, non-empty")
    guard_no_metric({"concept": lesson["concept"],
                     "rule": lesson["rule"],
                     "applies_when": lesson["applies_when"]})
    text = (lesson["concept"] + " " + str(lesson["rule"]) + " "
            + json.dumps(lesson["applies_when"]))
    hit = _METRIC_TERMS.search(text)
    if hit:
        raise LessonError(f"metric-shaped term in lesson text: '{hit.group(0)}'")
    content = lesson["concept"] + " " + str(lesson["rule"])
    hit = _PLATITUDES.search(content)
    if hit:
        raise LessonError(f"platitude in lesson text: '{hit.group(0)}'")
    hit = _IMPERATIVE.search(str(lesson["rule"]))
    if hit:
        raise LessonError(
            f"imperative shape in rule text: '{hit.group(0)}'. The rule "
            f"states what the task requires, never how to code it")
    hit = _IMPERATIVE.search(str(lesson["concept"]))
    if hit:
        raise LessonError(
            f"imperative shape in concept text: '{hit.group(0)}'. The "
            f"concept states what the task requires, never how to code it")
    return lesson


def commit(path, lesson):
    """Validate, stamp, append. A lesson that fails validation never lands."""
    validate(lesson)
    row = dict(lesson)
    row["ts"] = _time.time()
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(row) + "\n")
    return row


def load(path):
    out = []
    try:
        with open(path, encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    out.append(json.loads(line))
    except FileNotFoundError:
        pass
    return out


def generate(run_summary, work_features, model="qwen2.5-coder:7b"):
    """Distill one lesson from a run. Sees criteria-shaped feedback and the
    trace. Never sees time or tokens. Returns a candidate dict, unvalidated,
    so the caller watches validation pass or fail explicitly."""
    ev = run_summary.get("evidence") or {}
    ev_lines = []
    for r in ev.get("results", []):
        mark = "passed" if r["ok"] else "FAILED"
        ev_lines.append(f"- {r['call']} {mark}: got {r['got']}, expected {r['expect']}")
    prompt = "\n".join([
        "You distill one reusable craft lesson from a completed work episode.",
        f"TASK GIVEN: {run_summary.get('task_text', '(see trace)')}",
        f"VERDICT: {run_summary['verdict']}",
        f"EVALUATOR REASON: {run_summary.get('reason', '')}",
        "EXECUTION CHECKS:" if ev_lines else "",
        *ev_lines,
        "WORKER'S OWN APPROACH NOTES:",
        run_summary.get("trace", ""),
        "",
        "Write ONE lesson about the craft of doing this kind of work. Rules:",
        "- It is a guiding concept plus when it applies, never a step-by-step recipe.",
        "- Never mention speed, cost, length of output, or any quantity of effort.",
        "- If the work passed, capture the approach that earned the pass.",
        "- If it failed, capture the boundary: what context separates this",
        "  failure from times the approach works.",
        "- applies_when rules: for each key, the value MUST be either the exact",
        "  value shown in WORK FEATURES below, or \"*\" to mean any. No other",
        "  values are allowed.",
        f"WORK FEATURES: {json.dumps(work_features)}",
        "Respond with JSON only, in this exact shape:",
        json.dumps({"concept": "<one or two sentences>",
                    "applies_when": dict(work_features),
                    "confidence": 0.5}),
    ])
    resp = ollama_client.generate(model, prompt)
    m = re.search(r"\{.*\}", resp["text"], re.DOTALL)
    if not m:
        raise LessonError("generator returned no parseable JSON")
    cand = json.loads(m.group(0))
    cand["provenance"] = "engine"
    cand["trail"] = {"node_id": run_summary["node_id"],
                     "work_features": work_features}
    return cand


def generate_contrastive(task_text, work_features, fail_summary, pass_summary,
                         model="qwen2.5-coder:7b"):
    """The Section 5 mechanism (PACKET-002): distill one lesson from a
    contrast, a failing and a passing attempt at the same task. The prompt
    shows the failing run's failing checks and the passing run's output,
    and demands the specific stated rule that separates them. Never sees
    time or tokens. Returns a candidate dict, unvalidated, so the caller
    watches validation pass or fail explicitly."""
    ev = fail_summary.get("evidence") or {}
    fail_checks = [r for r in ev.get("results", []) if not r["ok"]]
    fail_lines = [f"- {r['call']} got {r['got']}, expected {r['expect']}"
                  for r in fail_checks]
    prompt = "\n".join([
        "You distill one reusable craft lesson from a contrast: the same",
        "task was attempted more than once. One attempt failed execution",
        "checks, another passed.",
        f"TASK GIVEN: {task_text}",
        "THE FAILING ATTEMPT missed these checks:",
        *fail_lines,
        "THE PASSING ATTEMPT'S OUTPUT:",
        pass_summary.get("output", ""),
        "",
        "The task text states a specific rule that the failing attempt",
        "ignored and the passing attempt honored. Write ONE lesson. Rules:",
        "- The \"rule\" field names the stated rule of the CLASS of rule",
        "  this task states, conditionally, in words that fit any task",
        "  stating a rule of this class, never a retelling of this one",
        "  task's instance: the shape is \"when the task states X, do X\"",
        "  or \"follow the direction the task states\", not \"always do X\".",
        "- If the rule text names one specific direction anyway, then",
        "  applies_when MUST pin stated_direction to exactly that",
        "  direction. A conditionally phrased rule sets stated_direction",
        "  to \"*\".",
        "- The concept says how to honor that kind of stated rule when it",
        "  appears in a task, one or two sentences, never a recipe.",
        "- Generic advice is worthless. Name the rule.",
        "- The rule states what the task requires, never how to code it.",
        "  No implementation steps, no data structures, no function names.",
        "- The concept states what the task requires, never how to code",
        "  it, the same discipline as the rule.",
        "- If the lesson is about one specific topic (the thing the rule",
        "  governs), applies_when MUST pin rule_topic to the exact value",
        "  shown in WORK FEATURES. A lesson that genuinely applies to the",
        "  whole class sets rule_topic to \"*\".",
        "- Never mention speed, cost, length of output, or any quantity of",
        "  effort.",
        "- applies_when rules: for each key, the value MUST be either the",
        "  exact value shown in WORK FEATURES below, or \"*\" to mean any.",
        f"WORK FEATURES: {json.dumps(work_features)}",
        "Respond with JSON only, in this exact shape:",
        json.dumps({"concept": "<one or two sentences>",
                    "rule": "<conditional on the task's stated rule>",
                    "applies_when": dict(work_features),
                    "confidence": 0.5}),
    ])
    resp = ollama_client.generate(model, prompt)
    m = re.search(r"\{.*\}", resp["text"], re.DOTALL)
    if not m:
        raise LessonError("generator returned no parseable JSON")
    cand = json.loads(m.group(0))
    screen_aim(str(cand.get("rule", "")),
               aim_ground(fail_checks, work_features.get("rule_class"),
                          work_features.get("stated_direction")))
    cand["provenance"] = "engine"
    cand["trail"] = {"node_id": fail_summary["node_id"],
                     "contrast_node_id": pass_summary["node_id"],
                     "work_features": work_features}
    return cand


_CLASS_GLOSS = {
    "tie_break": "a stated tie-breaking direction",
    "distinctness": "distinct-values semantics, each value counted once "
                    "no matter how often it repeats",
    "boundary": "an empty or degenerate input convention",
    "normalize": "a stated normalization step, such as case, whitespace, "
                 "or ordering, before comparing",
}


def generate_sibling_contrast(fail_task_text, pass_task_text, rule_class,
                              work_features, fail_summary, pass_summary,
                              model="qwen2.5-coder:7b"):
    """The widened contrast (PACKET-003): same seat, same rule class, two
    sibling tasks, one failed and one passed. The within-task contrast is
    the cleaner comparison and takes precedence; this is the fallback that
    turns all-fail-on-one-sibling into teachable material. The lesson must
    name the stated rule of the CLASS, not a retelling of the failed task.
    Never sees time or tokens. Returns a candidate dict, unvalidated."""
    ev = fail_summary.get("evidence") or {}
    fail_checks = [r for r in ev.get("results", []) if not r["ok"]]
    fail_lines = [f"- {r['call']} got {r['got']}, expected {r['expect']}"
                  for r in fail_checks]
    gloss = _CLASS_GLOSS.get(rule_class, rule_class)
    prompt = "\n".join([
        "You distill one reusable craft lesson from a contrast between two",
        "sibling tasks that state the same class of rule. The same worker",
        "failed one task and passed the other.",
        f"THE SHARED RULE CLASS: {rule_class}, {gloss}.",
        f"TASK THE WORKER FAILED: {fail_task_text}",
        "THE FAILING ATTEMPT missed these checks:",
        *fail_lines,
        f"TASK THE WORKER PASSED: {pass_task_text}",
        "THE PASSING ATTEMPT'S OUTPUT:",
        pass_summary.get("output", ""),
        "",
        "Both tasks state a rule of the same class. The worker honored it",
        "in one task and ignored it in the other. Write ONE lesson. Rules:",
        "- The \"rule\" field names the stated rule of the class in words",
        "  that fit both tasks, never a retelling of the failed task alone.",
        "- The rule must be conditional on what a task states, never",
        "  absolutized from these two tasks: the shape is \"when the task",
        "  states X, do X\" or \"follow the direction the task states\",",
        "  not \"always do X\".",
        "- If the rule text names one specific direction anyway, then",
        "  applies_when MUST pin stated_direction to exactly that",
        "  direction. A conditionally phrased rule sets stated_direction",
        "  to \"*\".",
        "- The concept says how to honor that class of stated rule whenever",
        "  a task names one, one or two sentences, never a recipe.",
        "- Generic advice is worthless. Name the rule.",
        "- The rule states what the task requires, never how to code it.",
        "  No implementation steps, no data structures, no function names.",
        "- The concept states what the task requires, never how to code",
        "  it, the same discipline as the rule.",
        "- If the lesson is about one specific topic (the thing the rule",
        "  governs), applies_when MUST pin rule_topic to the exact value",
        "  shown in WORK FEATURES. A lesson that genuinely applies to the",
        "  whole class sets rule_topic to \"*\".",
        "- Never mention speed, cost, length of output, or any quantity of",
        "  effort.",
        "- applies_when rules: for each key, the value MUST be either the",
        "  exact value shown in WORK FEATURES below, or \"*\" to mean any.",
        f"WORK FEATURES: {json.dumps(work_features)}",
        "Respond with JSON only, in this exact shape:",
        json.dumps({"concept": "<one or two sentences>",
                    "rule": "<conditional on the task's stated rule>",
                    "applies_when": dict(work_features),
                    "confidence": 0.5}),
    ])
    resp = ollama_client.generate(model, prompt)
    m = re.search(r"\{.*\}", resp["text"], re.DOTALL)
    if not m:
        raise LessonError("generator returned no parseable JSON")
    cand = json.loads(m.group(0))
    screen_aim(str(cand.get("rule", "")),
               aim_ground(fail_checks, rule_class,
                          work_features.get("stated_direction")))
    cand["provenance"] = "engine"
    cand["trail"] = {"node_id": fail_summary["node_id"],
                     "contrast_node_id": pass_summary["node_id"],
                     "contrast_type": "sibling",
                     "work_features": work_features}
    return cand
