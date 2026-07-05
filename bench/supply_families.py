"""The six graded supply families, implemented faithfully from
bench/design/SUPPLY_FAMILIES_v0.md (the authority for pins, stated
rules, dials, taxonomies; never edited from here). Separate from
probe_tasks.py by the packet: nothing here enters any standing pool
without the conductor's ruling, and the audition firewall applies from
birth, so these families never feed lesson generation.

Each family carries pins, the named canonical shape and its
relationship to the rule (the moderator criterion's input), a census
taxonomy with a deterministic AST classifier, and three rungs. Each
rung is a concrete task: text stating the rule, checks with expected
reprs, and the rule-check annotation fixed at build time. Where the
design document leaves an implementation choice open, the smallest
faithful choice was made and is logged in the packet RESULTS.

Census classifiers are replayable by the conductor over persisted
outputs through calibrate26.py. "unrunnable" means the extracted code
does not parse."""

import ast

import evidence

FAMILY_ORDER = ("chunk_pad", "merge_within", "safe_stats",
                "collapse_delims", "token_case", "kth_ordered")

# Rungs the design document names as controls, expected not to qualify;
# their job is anchoring the dial, and a qualification there is
# reported, never suppressed.
CONTROL_RUNGS = {("merge_within", 1), ("kth_ordered", 1)}


# ---------------------------------------------------------------------------
# Classifier helpers, deterministic AST logic
# ---------------------------------------------------------------------------

def _has_node(tree, types):
    return any(isinstance(n, types) for n in ast.walk(tree))


def _has_loop(tree):
    return _has_node(tree, (ast.For, ast.While))


def _sort_calls(tree):
    out = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            f = node.func
            if isinstance(f, ast.Name) and f.id == "sorted":
                out.append(node)
            elif isinstance(f, ast.Attribute) and f.attr == "sort":
                out.append(node)
    return out


def _has_sort(tree):
    return bool(_sort_calls(tree))


def _uses_re(tree):
    for node in ast.walk(tree):
        if isinstance(node, ast.Attribute):
            if isinstance(node.value, ast.Name) and node.value.id == "re":
                return True
        if isinstance(node, ast.ImportFrom) and node.module == "re":
            return True
    return False


def _count_attr_calls(tree, attr):
    return sum(1 for n in ast.walk(tree)
               if isinstance(n, ast.Call)
               and isinstance(n.func, ast.Attribute)
               and n.func.attr == attr)


def _tuple_key(call):
    for kw in call.keywords:
        if (kw.arg == "key" and isinstance(kw.value, ast.Lambda)
                and isinstance(kw.value.body, ast.Tuple)):
            return True
    return False


# ---------------------------------------------------------------------------
# Family classifiers. Precedence per family is stated in each function
# and pinned by test.
# ---------------------------------------------------------------------------

def _shape_chunk_pad(tree):
    """range-step comprehension beats loop: a comprehension calling
    range anywhere inside it is the conflicted idiom whether or not a
    pad fix-up follows it."""
    for node in ast.walk(tree):
        if isinstance(node, (ast.ListComp, ast.GeneratorExp)):
            if any(isinstance(n, ast.Call)
                   and isinstance(n.func, ast.Name)
                   and n.func.id == "range" for n in ast.walk(node)):
                return "range-step comprehension"
    if _has_loop(tree):
        return "explicit loop-with-pad"
    return "other"


def _shape_merge_within(tree):
    """sort plus a loop is the sweep; everything else runnable is
    pairwise-other, per the design taxonomy's two-way split."""
    if _has_sort(tree) and _has_loop(tree):
        return "sort-and-sweep"
    return "pairwise-other"


def _shape_safe_stats(tree):
    """sort plus subscript is the canonical shape; a loop without it
    is the accumulator; the rest is other."""
    if _has_sort(tree) and _has_node(tree, ast.Subscript):
        return "sort-slice-average"
    if _has_loop(tree):
        return "loop-accumulate"
    return "other"


def _shape_collapse_delims(tree):
    """regex or any normalize-then-split (replace+split, or several
    splits) is the multi family; exactly one split call is the
    conflicted single-split; a loop without split is the char walk."""
    if _uses_re(tree):
        return "multi-split-or-regex"
    splits = _count_attr_calls(tree, "split")
    if splits >= 1 and _count_attr_calls(tree, "replace") >= 1:
        return "multi-split-or-regex"
    if splits >= 2:
        return "multi-split-or-regex"
    if splits == 1:
        return "single-split"
    if _has_loop(tree):
        return "char-walk"
    return "other"


def _shape_token_case(tree):
    """regex beats split beats char walk, the selfdeliv24
    snake_to_camel precedence with this family's labels."""
    if _uses_re(tree):
        return "regex"
    if _count_attr_calls(tree, "split") >= 1:
        return "split-capitalize-join"
    if _has_loop(tree):
        return "char-walk"
    return "other"


def _shape_kth_ordered(tree):
    """two sort passes or a tuple-returning key lambda is the compound
    strategy; one plain sort call is the conflicted single key; a loop
    without sorting is the manual scan."""
    sorts = _sort_calls(tree)
    if sorts:
        if len(sorts) >= 2 or any(_tuple_key(c) for c in sorts):
            return "compound-key-sort"
        return "single-key-sort"
    if _has_loop(tree):
        return "manual-scan"
    return "other"


# ---------------------------------------------------------------------------
# The families. Text states the rule exactly as the design document
# gives it; the dial lives in the checks (and, where the design says
# so, in the text: merge_within's d, token_case's rung 3 resolution).
# ---------------------------------------------------------------------------

_CHUNK_PAD_TEXT = (
    "Write a Python function chunk_pad(lst, k) that splits a list into "
    "consecutive chunks of size k, in order. When the final chunk "
    "comes up short, pad it with None so that every chunk has exactly "
    "k elements. An empty list returns []. Note one edge case it "
    "handles.")

_KTH_ORDERED_TEXT = (
    "Write a Python function kth_ordered(words, k) returning the k-th "
    "word, counting from 1, when the words are ordered by increasing "
    "length, and words of equal length are ordered "
    "reverse-alphabetically among themselves. Return None when k is "
    "out of range. Note one edge case it handles.")

_TOKEN_CASE_BASE = (
    "Write a Python function token_case(s) taking an "
    "underscore_delimited identifier and returning it in camel case: "
    "the first token lowercased, every later token capitalized, and "
    "the tokens joined with no separator. Tokens that appear in the "
    "exception list ['URL', 'ID'] keep their exact given form "
    "wherever they appear.")

FAMILIES = {
    "chunk_pad": {
        "pins": {"rule_class": "boundary", "rule_topic": "degenerate"},
        "relationship": "conflicted",
        "named_shape": "range-step comprehension",
        "taxonomy": ("range-step comprehension", "explicit loop-with-pad",
                     "other", "unrunnable"),
        "rungs": [
            {"rung": 1,
             "task": _CHUNK_PAD_TEXT,
             "checks": [
                 {"call": "chunk_pad([1, 2, 3, 4, 5], 2)",
                  "expect": "[[1, 2], [3, 4], [5, None]]"},
                 {"call": "chunk_pad([1, 2, 3, 4], 2)",
                  "expect": "[[1, 2], [3, 4]]"},
                 {"call": "chunk_pad([], 3)", "expect": "[]"}],
             "rule_checks": ["chunk_pad([1, 2, 3, 4, 5], 2)"]},
            {"rung": 2,
             "task": _CHUNK_PAD_TEXT,
             "checks": [
                 {"call": "chunk_pad([1, 2, 3, 4, 5], 3)",
                  "expect": "[[1, 2, 3], [4, 5, None]]"},
                 {"call": "chunk_pad([1, 2], 5)",
                  "expect": "[[1, 2, None, None, None]]"},
                 {"call": "chunk_pad([7, 8], 2)", "expect": "[[7, 8]]"},
                 {"call": "chunk_pad([], 4)", "expect": "[]"}],
             "rule_checks": ["chunk_pad([1, 2, 3, 4, 5], 3)",
                             "chunk_pad([1, 2], 5)"]},
            {"rung": 3,
             "task": _CHUNK_PAD_TEXT,
             "checks": [
                 {"call": "chunk_pad([1, 2, 3, 4, 5], 3)",
                  "expect": "[[1, 2, 3], [4, 5, None]]"},
                 {"call": "chunk_pad([1, 2], 5)",
                  "expect": "[[1, 2, None, None, None]]"},
                 {"call": "chunk_pad([9, 10, 11, 12], 2)",
                  "expect": "[[9, 10], [11, 12]]"},
                 {"call": "chunk_pad([], 2)", "expect": "[]"},
                 {"call": "chunk_pad([5, 6, 7], 1)",
                  "expect": "[[5], [6], [7]]"}],
             "rule_checks": ["chunk_pad([1, 2, 3, 4, 5], 3)",
                             "chunk_pad([1, 2], 5)"]},
        ]},
    "merge_within": {
        "pins": {"rule_class": "boundary", "rule_topic": "degenerate"},
        "relationship": "conflicted",
        "named_shape": "sort-and-sweep",
        "taxonomy": ("sort-and-sweep", "pairwise-other", "unrunnable"),
        "rungs": [
            {"rung": 1,  # control: d=0, pure idiom
             "task": (
                 "Write a Python function merge_within(pairs) taking a "
                 "list of [start, end] inclusive integer ranges, "
                 "possibly unsorted, and returning the merged ranges "
                 "sorted by start, as a list of [start, end] lists. "
                 "Ranges that overlap or share an endpoint merge: "
                 "[1, 4] and [3, 6] become [1, 6], and [1, 3] and "
                 "[3, 5] become [1, 5]. Ranges separated by any gap "
                 "stay separate. An empty list returns []. Note one "
                 "edge case it handles."),
             "checks": [
                 {"call": "merge_within([[1, 3], [3, 6]])",
                  "expect": "[[1, 6]]"},
                 {"call": "merge_within([[1, 4], [2, 5]])",
                  "expect": "[[1, 5]]"},
                 {"call": "merge_within([[5, 7], [1, 2]])",
                  "expect": "[[1, 2], [5, 7]]"},
                 {"call": "merge_within([])", "expect": "[]"}],
             "rule_checks": ["merge_within([[1, 3], [3, 6]])"]},
            {"rung": 2,  # d=1, the P022 touch conflict, one token
             "task": (
                 "Write a Python function merge_within(pairs) taking a "
                 "list of [start, end] inclusive integer ranges, "
                 "possibly unsorted, and returning the merged ranges "
                 "sorted by start, as a list of [start, end] lists. "
                 "Ranges that overlap or sit within distance 1 of each "
                 "other merge: [1, 3] and [4, 6] become [1, 6] because "
                 "the gap between 3 and 4 is 1. Ranges further apart "
                 "stay separate. An empty list returns []. Note one "
                 "edge case it handles."),
             "checks": [
                 {"call": "merge_within([[1, 3], [4, 6]])",
                  "expect": "[[1, 6]]"},
                 {"call": "merge_within([[1, 3], [5, 7]])",
                  "expect": "[[1, 3], [5, 7]]"},
                 {"call": "merge_within([[1, 4], [2, 5]])",
                  "expect": "[[1, 5]]"},
                 {"call": "merge_within([])", "expect": "[]"}],
             "rule_checks": ["merge_within([[1, 3], [4, 6]])",
                             "merge_within([[1, 3], [5, 7]])"]},
            {"rung": 3,  # d a parameter, mixed values across checks
             "task": (
                 "Write a Python function merge_within(pairs, d) "
                 "taking a list of [start, end] inclusive integer "
                 "ranges, possibly unsorted, and a non-negative "
                 "integer distance d, and returning the merged ranges "
                 "sorted by start, as a list of [start, end] lists. "
                 "Ranges that overlap or sit within distance d of "
                 "each other merge, where the distance between [1, 3] "
                 "and [5, 7] is 2, the gap from 3 to 5. With d=2 "
                 "those two become [1, 7]; with d=0 only overlapping "
                 "or endpoint-sharing ranges merge. An empty list "
                 "returns []. Note one edge case it handles."),
             "checks": [
                 {"call": "merge_within([[1, 3], [5, 7]], 2)",
                  "expect": "[[1, 7]]"},
                 {"call": "merge_within([[1, 3], [4, 6]], 0)",
                  "expect": "[[1, 3], [4, 6]]"},
                 {"call": "merge_within([[1, 4], [2, 5]], 0)",
                  "expect": "[[1, 5]]"},
                 {"call": "merge_within([], 3)", "expect": "[]"}],
             "rule_checks": ["merge_within([[1, 3], [5, 7]], 2)",
                             "merge_within([[1, 3], [4, 6]], 0)"]},
        ]},
    "safe_stats": {
        "pins": {"rule_class": "boundary", "rule_topic": "degenerate"},
        "relationship": "separable",
        "named_shape": "sort-slice-average",
        "taxonomy": ("sort-slice-average", "loop-accumulate", "other",
                     "unrunnable"),
        "rungs": [
            {"rung": 1,  # degenerates limited to empty
             "task": (
                 "Write a Python function trimmed_mean(nums) returning "
                 "the mean of the list after dropping exactly one "
                 "occurrence of the minimum and one occurrence of the "
                 "maximum, as a float. An empty list returns None. "
                 "Note one edge case it handles."),
             "checks": [
                 {"call": "trimmed_mean([])", "expect": "None"},
                 {"call": "trimmed_mean([5, 5, 1, 9])", "expect": "5.0"},
                 {"call": "trimmed_mean([3, 1, 2])", "expect": "2.0"}],
             "rule_checks": ["trimmed_mean([])",
                             "trimmed_mean([5, 5, 1, 9])"]},
            {"rung": 2,  # all three degenerate sizes in the check set
             "task": (
                 "Write a Python function trimmed_mean(nums) returning "
                 "the mean of the list after dropping exactly one "
                 "occurrence of the minimum and one occurrence of the "
                 "maximum, as a float. Empty lists, one-element lists, "
                 "and two-element lists return None. Note one edge "
                 "case it handles."),
             "checks": [
                 {"call": "trimmed_mean([])", "expect": "None"},
                 {"call": "trimmed_mean([7])", "expect": "None"},
                 {"call": "trimmed_mean([3, 9])", "expect": "None"},
                 {"call": "trimmed_mean([5, 5, 1, 9])", "expect": "5.0"},
                 {"call": "trimmed_mean([3, 1, 2])", "expect": "2.0"}],
             "rule_checks": ["trimmed_mean([])", "trimmed_mean([7])",
                             "trimmed_mean([3, 9])",
                             "trimmed_mean([5, 5, 1, 9])"]},
            {"rung": 3,  # plus all-equal, resolution stated
             "task": (
                 "Write a Python function trimmed_mean(nums) returning "
                 "the mean of the list after dropping exactly one "
                 "occurrence of the minimum and one occurrence of the "
                 "maximum, as a float. Empty lists, one-element lists, "
                 "and two-element lists return None. When all values "
                 "are equal, one of them still drops as the minimum "
                 "and one as the maximum, and the mean of the rest "
                 "equals that same value. Note one edge case it "
                 "handles."),
             "checks": [
                 {"call": "trimmed_mean([])", "expect": "None"},
                 {"call": "trimmed_mean([7])", "expect": "None"},
                 {"call": "trimmed_mean([3, 9])", "expect": "None"},
                 {"call": "trimmed_mean([5, 5, 1, 9])", "expect": "5.0"},
                 {"call": "trimmed_mean([4, 4, 4, 4])", "expect": "4.0"},
                 {"call": "trimmed_mean([3, 1, 2])", "expect": "2.0"}],
             "rule_checks": ["trimmed_mean([])", "trimmed_mean([7])",
                             "trimmed_mean([3, 9])",
                             "trimmed_mean([5, 5, 1, 9])",
                             "trimmed_mean([4, 4, 4, 4])"]},
        ]},
    "collapse_delims": {
        "pins": {"rule_class": "normalize", "rule_topic": "delimiters"},
        "relationship": "conflicted",
        "named_shape": "single-split",
        "taxonomy": ("single-split", "multi-split-or-regex", "char-walk",
                     "other", "unrunnable"),
        "rungs": [
            {"rung": 1,  # one delimiter type with runs
             "task": (
                 "Write a Python function collapse_delims(s) that "
                 "splits the string on commas, treats any run of "
                 "consecutive commas as one split, drops empty pieces "
                 "at the start and end, and returns the pieces "
                 "rejoined with a single comma between each. Note one "
                 "edge case it handles."),
             "checks": [
                 {"call": "collapse_delims('a,,b,,,c')",
                  "expect": "'a,b,c'"},
                 {"call": "collapse_delims(',a,b,')",
                  "expect": "'a,b'"},
                 {"call": "collapse_delims('a,b')", "expect": "'a,b'"}],
             "rule_checks": ["collapse_delims('a,,b,,,c')",
                             "collapse_delims(',a,b,')"]},
            {"rung": 2,  # two delimiter types mixed
             "task": (
                 "Write a Python function collapse_delims(s) that "
                 "splits the string on commas and semicolons, treats "
                 "any run of consecutive delimiters, mixed or not, as "
                 "one split, drops empty pieces at the start and end, "
                 "and returns the pieces rejoined with a single comma "
                 "between each. Note one edge case it handles."),
             "checks": [
                 {"call": "collapse_delims('a,;b;;c')",
                  "expect": "'a,b,c'"},
                 {"call": "collapse_delims(';a;b,')",
                  "expect": "'a,b'"},
                 {"call": "collapse_delims('a,b,c')",
                  "expect": "'a,b,c'"}],
             "rule_checks": ["collapse_delims('a,;b;;c')",
                             "collapse_delims(';a;b,')"]},
            {"rung": 3,  # three types, edge runs, empty string
             "task": (
                 "Write a Python function collapse_delims(s) that "
                 "splits the string on commas, semicolons, and "
                 "spaces, treats any run of consecutive delimiters, "
                 "mixed or not, as one split, drops empty pieces at "
                 "the start and end, and returns the pieces rejoined "
                 "with a single comma between each. An empty string "
                 "returns ''. Note one edge case it handles."),
             "checks": [
                 {"call": "collapse_delims('a, ;b;; c')",
                  "expect": "'a,b,c'"},
                 {"call": "collapse_delims(',; a;b , ')",
                  "expect": "'a,b'"},
                 {"call": "collapse_delims('')", "expect": "''"},
                 {"call": "collapse_delims('a,b')", "expect": "'a,b'"}],
             "rule_checks": ["collapse_delims('a, ;b;; c')",
                             "collapse_delims(',; a;b , ')",
                             "collapse_delims('')"]},
        ]},
    "token_case": {
        "pins": {"rule_class": "normalize", "rule_topic": "delimiters"},
        "relationship": "separable",
        "named_shape": "split-capitalize-join",
        "taxonomy": ("split-capitalize-join", "regex", "char-walk",
                     "other", "unrunnable"),
        "rungs": [
            {"rung": 1,  # no exceptions in inputs, list merely stated
             "task": _TOKEN_CASE_BASE + " Note one edge case it "
                                        "handles.",
             "checks": [
                 {"call": "token_case('Set_timer_value')",
                  "expect": "'setTimerValue'"},
                 {"call": "token_case('get_value')",
                  "expect": "'getValue'"},
                 {"call": "token_case('count')", "expect": "'count'"}],
             "rule_checks": ["token_case('Set_timer_value')"]},
            {"rung": 2,  # one exception mid-stream
             "task": _TOKEN_CASE_BASE + " Note one edge case it "
                                        "handles.",
             "checks": [
                 {"call": "token_case('get_URL_path')",
                  "expect": "'getURLPath'"},
                 {"call": "token_case('Set_timer_value')",
                  "expect": "'setTimerValue'"},
                 {"call": "token_case('get_value')",
                  "expect": "'getValue'"}],
             "rule_checks": ["token_case('get_URL_path')",
                             "token_case('Set_timer_value')"]},
            {"rung": 3,  # exception at first position, resolution stated
             "task": _TOKEN_CASE_BASE + " An exception token keeps "
                     "its exact form even when it is the first token. "
                     "Note one edge case it handles.",
             "checks": [
                 {"call": "token_case('URL_to_path')",
                  "expect": "'URLToPath'"},
                 {"call": "token_case('get_ID_count')",
                  "expect": "'getIDCount'"},
                 {"call": "token_case('get_value')",
                  "expect": "'getValue'"}],
             "rule_checks": ["token_case('URL_to_path')",
                             "token_case('get_ID_count')"]},
        ]},
    "kth_ordered": {
        "pins": {"rule_class": "tie_break", "rule_topic": "direction",
                 "stated_direction": "reverse_alphabetical"},
        "relationship": "conflicted",
        "named_shape": "single-key-sort",
        "taxonomy": ("single-key-sort", "compound-key-sort",
                     "manual-scan", "other", "unrunnable"),
        "rungs": [
            {"rung": 1,  # control: no ties in inputs
             "task": _KTH_ORDERED_TEXT,
             "checks": [
                 {"call": "kth_ordered(['dd', 'a', 'ccc'], 2)",
                  "expect": "'dd'"},
                 {"call": "kth_ordered(['a', 'bb'], 1)",
                  "expect": "'a'"},
                 {"call": "kth_ordered(['a'], 3)", "expect": "None"}],
             "rule_checks": ["kth_ordered(['dd', 'a', 'ccc'], 2)"]},
            {"rung": 2,  # one tie pair at the k-th position
             "task": _KTH_ORDERED_TEXT,
             "checks": [
                 {"call": "kth_ordered(['bb', 'ab', 'c'], 2)",
                  "expect": "'bb'"},
                 {"call": "kth_ordered(['dd', 'a', 'ccc'], 2)",
                  "expect": "'dd'"},
                 {"call": "kth_ordered(['a', 'bb'], 5)",
                  "expect": "None"}],
             "rule_checks": ["kth_ordered(['bb', 'ab', 'c'], 2)"]},
            {"rung": 3,  # dense ties, k inside the tie run
             "task": _KTH_ORDERED_TEXT,
             "checks": [
                 {"call": "kth_ordered(['ab', 'ba', 'aa', 'c'], 2)",
                  "expect": "'ba'"},
                 {"call": "kth_ordered(['ab', 'ba', 'aa', 'c'], 3)",
                  "expect": "'ab'"},
                 {"call": "kth_ordered(['a', 'bbb'], 1)",
                  "expect": "'a'"},
                 {"call": "kth_ordered([], 1)", "expect": "None"}],
             "rule_checks": ["kth_ordered(['ab', 'ba', 'aa', 'c'], 2)",
                             "kth_ordered(['ab', 'ba', 'aa', 'c'], 3)"]},
        ]},
}

_CLASSIFIERS = {"chunk_pad": _shape_chunk_pad,
                "merge_within": _shape_merge_within,
                "safe_stats": _shape_safe_stats,
                "collapse_delims": _shape_collapse_delims,
                "token_case": _shape_token_case,
                "kth_ordered": _shape_kth_ordered}


def census_shape(family, output_text):
    """Classify one persisted output by the shape it reached for."""
    code = evidence.extract_python(output_text)
    try:
        tree = ast.parse(code)
    except SyntaxError:
        return "unrunnable"
    return _CLASSIFIERS[family](tree)


def get_rung(family, rung):
    for r in FAMILIES[family]["rungs"]:
        if r["rung"] == rung:
            return r
    raise KeyError(f"{family} has no rung {rung}")
