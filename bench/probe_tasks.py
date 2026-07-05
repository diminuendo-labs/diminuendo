"""Task pools for the transfer probe. Constants only, no config framework.

Built for PACKET-001, extended for PACKET-002. The first probe's apply
tasks gave qwen no headroom (1.00 in every cell, zero signal), so this
module separates the candidate pool from the kept pool. calibrate.py runs
every candidate once per seat with no lessons and records the evidence
fraction. A task is kept only if at least one seat scored below 1.0 on
it, and the kept pool must leave each seat's baseline mean evidence
fraction between 0.3 and 0.9.

Every apply candidate states a subtle rule that plausible solutions
ignore. PACKET-002 names the classes: every task carries a rule_class,
one of exactly four. tie_break is a stated tie-breaking direction.
distinctness is distinct-values semantics. boundary is an empty or
degenerate input convention. normalize is a stated normalization step
such as case, whitespace, or ordering before compare. The class is the
trap. Rule classes are what make transfer measurable without task
overlap: the same class of trap appears in the generation pool and the
apply pool, in different tasks.

The generation pool is v2 (PACKET-002): eight new tasks, two per rule
class, text disjoint from every apply task. The v1 generation pool was
replaced here and lives in git history. Generation and application
pools are disjoint, checked by test.

CALIBRATION RECORD (calibrate run 20260702-011304, one run per task per
seat, so each cell is n=1, direction only; A=qwen2.5-coder:7b,
B=llama3.1:8b, no lessons, cross-family audience):

  kept task           A     B
  most_common_word    1.00  0.67
  merge_ranges        0.75  0.75
  longest_word        0.50  0.50
  median              1.00  0.75
  range_summary       0.40  0.60
  flatten_once        0.33  0.33
  snake_to_camel      0.25  0.25
  balanced            1.00  0.75

  kept-pool baseline mean: A=0.65, B=0.58. Both inside the 0.3 to 0.9
  band the packet demands.

  dropped, both seats 1.00 (no headroom for either seat): second_largest,
  top_k, dedupe, mode, nth_smallest, is_rotation, truncate_words,
  interleave, count_pairs. They stay in the candidate pool for future
  swaps and re-calibration.

PACKET-005 additions: tie_break tasks carry stated_direction (last,
alphabetical, smallest), exposed in work_features so direction-specific
lessons pin it in applies_when. Kept apply tasks carry rule_checks, the
check calls that encode the task's stated rule, the report's sharp
level. The generation pool gains harder candidate siblings for the three
classes that never broke (both probes, both seats, all_pass at R_G=3).

GEN POOL CALIBRATION RECORD (gencal run 20260702-211540, R_G=3 per task
per seat, case per seat; A=qwen2.5-coder:7b, B=llama3.1:8b, no lessons,
cross-family audience. Incumbents cite the R_G=3 gen_accounting already
on record in the probe 20260702-051517 and 20260702-083121 reports
instead of being re-bought):

  new candidate         class         A         B
  count_distinct_pairs  distinctness  all_pass  mixed
  sum_of_modes          distinctness  all_pass  all_pass
  weighted_mean         boundary      all_pass  all_pass
  range_step            boundary      all_pass  mixed
  title_words           normalize     all_pass  all_pass
  count_token           normalize     all_pass  mixed

  incumbents on record: max_index and shortest_word break (mixed or
  all_fail) for one or both seats in both probes. count_unique,
  sum_distinct, average, chunk, count_word, equal_ignoring_spaces are
  all_pass for both seats in both probes, no headroom.

  kept: the tie_break incumbents plus the six new candidates. Every
  class has at least one failing seat-task: tie_break for both seats,
  distinctness, boundary, and normalize for seat B. Seat A (qwen)
  breaks nowhere outside tie_break even on the harder candidates, so
  its store can only carry tie_break lessons at this pool difficulty.
  Stated in the PACKET-005 RESULTS.

PACKET-008 addition: every task carries a rule_topic naming the thing
its stated rule governs, one word from the fixed per-class vocabulary
in RULE_TOPICS, exposed in work_features. The stated_direction move,
generalized: topic-specific lessons pin rule_topic in applies_when and
the menu's contradiction logic keeps them off mismatched tasks, while
genuinely general lessons wildcard it and ride the whole class.

PACKET-010: the conjunction filter. A generation task earns a slot only
if it breaks for at least one seat AND its (rule_class, rule_topic)
pair exists in the apply pool, because PACKET-009 measured the cost of
either half alone: three of five production lessons pinned to orphan
topics, and the in-pool-topic incumbents never broke.

CONJUNCTION CALIBRATION RECORD (demand demand-20260703-071812, gencal
gencal-20260703-072720, R_G=3 per seat; A=qwen2.5-coder:7b,
B=llama3.1:8b):

  candidate               pair                       A         B
  longest_run_char        tie_break/direction        all_pass  mixed
  least_frequent_word     tie_break/direction        all_pass  mixed
  count_distinct_over     distinctness/values        all_pass  all_pass
  third_largest_distinct  distinctness/values        all_pass  all_pass
  mode_count              distinctness/values        all_pass  mixed
  clamp                   boundary/degenerate        all_pass  all_pass
  nth_page                boundary/degenerate        all_pass  all_pass
  split_csvish            normalize/delimiters       all_pass  all_pass
  depth_max               normalize/delimiters       all_pass  all_pass

  kept: the tie incumbents max_index and shortest_word (in-pool topic,
  breakage on record in three probes) plus longest_run_char,
  least_frequent_word, and mode_count. RESISTANT pairs, two candidates
  tried and nothing broke, named not forced: boundary/degenerate and
  normalize/delimiters. Dropped incumbents, each failing one half of
  the conjunction: count_token and title_words (orphan topics
  punctuation and case), count_distinct_pairs (orphan topic pairs),
  sum_of_modes, weighted_mean, range_step (no breakage on record).
  Seat A (qwen) broke on none of the nine candidates, consistent with
  its whole record outside tie_break, so new supply is llama-origin,
  which is the reverse-direction hunt by construction.
"""

RULE_CLASSES = ("tie_break", "distinctness", "boundary", "normalize")

RULE_TOPICS = {"tie_break": ("direction",),
               "distinctness": ("pairs", "values"),
               "boundary": ("empty", "degenerate"),
               "normalize": ("case", "whitespace", "punctuation",
                             "delimiters")}

FEATURES = {"operation": "write_code", "target": "function",
            "language": "python", "size": "small"}

CRITERIA = ["the function is correct",
            "the code is concise and readable",
            "at least one edge case is named"]

# ---------------------------------------------------------------------------
# Generation pool candidates (PACKET-005): the v2 incumbents plus harder
# siblings for the classes that never broke. gencal.py measures headroom
# per class per seat at R_G=3, GEN_KEPT below names the pool. These seed
# lessons through the contrast paths, they are never applied. The trap in
# each task is its rule class, stated in the task text. tie_break tasks
# carry stated_direction, exposed in work_features, so lessons can pin a
# direction in applies_when and the menu never surfaces a direction-
# specific lesson against a contradicting task.
# ---------------------------------------------------------------------------

CANDIDATE_GEN_TASKS = [
    {"name": "max_index", "rule_class": "tie_break",
     "rule_topic": "direction",
     "stated_direction": "last",
     "task": ("Write a Python function max_index(nums) returning the index "
              "of the largest value in the list. When the largest value "
              "appears more than once, return the index of its last "
              "occurrence, not the first. Note one edge case it handles."),
     "checks": [{"call": "max_index([1, 3, 3])", "expect": "2"},
                {"call": "max_index([5])", "expect": "0"},
                {"call": "max_index([2, 1, 2])", "expect": "2"},
                {"call": "max_index([4, 1])", "expect": "0"}]},
    {"name": "shortest_word", "rule_class": "tie_break",
     "rule_topic": "direction",
     "stated_direction": "last",
     "task": ("Write a Python function shortest_word(s) returning the "
              "shortest whitespace-separated word in the string. On ties "
              "return the last such word, not the first. An empty string "
              "returns ''. Note one edge case it handles."),
     "checks": [{"call": "shortest_word('bb a cc d')", "expect": "'d'"},
                {"call": "shortest_word('aa bb')", "expect": "'bb'"},
                {"call": "shortest_word('one')", "expect": "'one'"},
                {"call": "shortest_word('')", "expect": "''"}]},
    {"name": "count_unique", "rule_class": "distinctness",
     "rule_topic": "values",
     "task": ("Write a Python function count_unique(nums) returning how "
              "many values appear exactly once in the list. Values that "
              "repeat do not count at all: [1, 2, 2, 3] has two such "
              "values, 1 and 3. An empty list returns 0. Note one edge "
              "case it handles."),
     "checks": [{"call": "count_unique([1, 2, 2, 3])", "expect": "2"},
                {"call": "count_unique([5, 5])", "expect": "0"},
                {"call": "count_unique([])", "expect": "0"},
                {"call": "count_unique([7])", "expect": "1"}]},
    {"name": "sum_distinct", "rule_class": "distinctness",
     "rule_topic": "values",
     "task": ("Write a Python function sum_distinct(nums) returning the "
              "sum of the distinct values in the list, each value counted "
              "once no matter how many times it repeats. An empty list "
              "returns 0. Note one edge case it handles."),
     "checks": [{"call": "sum_distinct([1, 2, 2])", "expect": "3"},
                {"call": "sum_distinct([3, 3, 3])", "expect": "3"},
                {"call": "sum_distinct([])", "expect": "0"},
                {"call": "sum_distinct([-1, -1, 2])", "expect": "1"}]},
    {"name": "average", "rule_class": "boundary",
     "rule_topic": "empty",
     "task": ("Write a Python function average(nums) returning the "
              "arithmetic mean of the list as a float, even when the mean "
              "is a whole number. An empty list returns None, never zero. "
              "Note one edge case it handles."),
     "checks": [{"call": "average([1, 2])", "expect": "1.5"},
                {"call": "average([2, 2])", "expect": "2.0"},
                {"call": "average([])", "expect": "None"},
                {"call": "average([3])", "expect": "3.0"}]},
    {"name": "chunk", "rule_class": "boundary",
     "rule_topic": "degenerate",
     "task": ("Write a Python function chunk(lst, size) splitting the list "
              "into consecutive chunks of the given size, as a list of "
              "lists, with the last chunk shorter when the list does not "
              "divide evenly. When size is zero or negative return []. "
              "Note one edge case it handles."),
     "checks": [{"call": "chunk([1, 2, 3, 4, 5], 2)",
                 "expect": "[[1, 2], [3, 4], [5]]"},
                {"call": "chunk([], 2)", "expect": "[]"},
                {"call": "chunk([1, 2], 0)", "expect": "[]"},
                {"call": "chunk([1, 2], 5)", "expect": "[[1, 2]]"}]},
    {"name": "count_word", "rule_class": "normalize",
     "rule_topic": "case",
     "task": ("Write a Python function count_word(s, w) returning how many "
              "of the whitespace-separated words in s equal the word w, "
              "comparing case-insensitively. Substrings inside longer "
              "words never count. An empty string returns 0. Note one "
              "edge case it handles."),
     "checks": [{"call": "count_word('The the THE', 'the')", "expect": "3"},
                {"call": "count_word('theater the', 'the')", "expect": "1"},
                {"call": "count_word('', 'a')", "expect": "0"},
                {"call": "count_word('Dog dog DOG cat', 'DOG')",
                 "expect": "3"}]},
    {"name": "equal_ignoring_spaces", "rule_class": "normalize",
     "rule_topic": "whitespace",
     "task": ("Write a Python function equal_ignoring_spaces(a, b) "
              "returning True when the two strings are equal after "
              "removing every whitespace character and lowercasing both. "
              "Note one edge case it handles."),
     "checks": [{"call": "equal_ignoring_spaces('a b', 'AB')",
                 "expect": "True"},
                {"call": "equal_ignoring_spaces('a', 'b')",
                 "expect": "False"},
                {"call": "equal_ignoring_spaces('x  y z', 'xYZ')",
                 "expect": "True"},
                {"call": "equal_ignoring_spaces('', ' ')",
                 "expect": "True"}]},
    # ---- harder siblings, PACKET-005, for the classes that never broke ----
    {"name": "count_distinct_pairs", "rule_class": "distinctness",
     "rule_topic": "pairs",
     "task": ("Write a Python function count_distinct_pairs(nums, target) "
              "returning how many distinct unordered value pairs in the "
              "list sum to target, each distinct pair counted once no "
              "matter how many times its values repeat: [1, 3, 1, 3] with "
              "target 4 has exactly one such pair. An empty list returns "
              "0. Note one edge case it handles."),
     "checks": [{"call": "count_distinct_pairs([1, 3, 1, 3], 4)",
                 "expect": "1"},
                {"call": "count_distinct_pairs([2, 2, 2], 4)",
                 "expect": "1"},
                {"call": "count_distinct_pairs([0, 5, 2, 3, 5, 0], 5)",
                 "expect": "2"},
                {"call": "count_distinct_pairs([], 1)", "expect": "0"}]},
    {"name": "sum_of_modes", "rule_class": "distinctness",
     "rule_topic": "values",
     "task": ("Write a Python function sum_of_modes(nums) returning the "
              "sum of the distinct most frequent values in the list, each "
              "counted once no matter how often it appears: [1, 1, 2, 2, 3] "
              "returns 3. An empty list returns 0. Note one edge case it "
              "handles."),
     "checks": [{"call": "sum_of_modes([1, 1, 2, 2, 3])", "expect": "3"},
                {"call": "sum_of_modes([5])", "expect": "5"},
                {"call": "sum_of_modes([])", "expect": "0"},
                {"call": "sum_of_modes([2, 2, 2, 1])", "expect": "2"}]},
    {"name": "weighted_mean", "rule_class": "boundary",
     "rule_topic": "degenerate",
     "task": ("Write a Python function weighted_mean(values, weights) "
              "returning the weighted arithmetic mean as a float. Empty "
              "lists return None, and a zero total weight also returns "
              "None, never a crash. Note one edge case it handles."),
     "checks": [{"call": "weighted_mean([1, 3], [1, 1])", "expect": "2.0"},
                {"call": "weighted_mean([2], [0])", "expect": "None"},
                {"call": "weighted_mean([], [])", "expect": "None"},
                {"call": "weighted_mean([1, 2], [0, 2])",
                 "expect": "2.0"}]},
    {"name": "range_step", "rule_class": "boundary",
     "rule_topic": "degenerate",
     "task": ("Write a Python function range_step(start, stop, step) "
              "returning the list of integers from start up to but not "
              "including stop, advancing by step. When step is zero or "
              "negative return [], never loop or crash. When start is at "
              "or past stop return []. Note one edge case it handles."),
     "checks": [{"call": "range_step(1, 6, 2)", "expect": "[1, 3, 5]"},
                {"call": "range_step(3, 3, 1)", "expect": "[]"},
                {"call": "range_step(1, 4, 0)", "expect": "[]"},
                {"call": "range_step(5, 1, 1)", "expect": "[]"}]},
    {"name": "title_words", "rule_class": "normalize",
     "rule_topic": "case",
     "task": ("Write a Python function title_words(s) returning the "
              "string with every whitespace-separated word title-cased "
              "(first letter upper, the rest lower) and runs of whitespace "
              "collapsed to single spaces, except that words already "
              "entirely uppercase stay exactly as they are. An empty "
              "string returns ''. Note one edge case it handles."),
     "checks": [{"call": "title_words('hello  world')",
                 "expect": "'Hello World'"},
                {"call": "title_words('NASA rocks')",
                 "expect": "'NASA Rocks'"},
                {"call": "title_words('mIxEd')", "expect": "'Mixed'"},
                {"call": "title_words('')", "expect": "''"}]},
    {"name": "count_token", "rule_class": "normalize",
     "rule_topic": "punctuation",
     "task": ("Write a Python function count_token(s, w) returning how "
              "many whitespace-separated words in s equal w after "
              "stripping leading and trailing punctuation from each word "
              "and comparing case-insensitively. Substrings inside longer "
              "words never count. An empty string returns 0. Note one "
              "edge case it handles."),
     "checks": [{"call": "count_token('The cat, the CAT.', 'cat')",
                 "expect": "2"},
                {"call": "count_token('cathedral cat', 'cat')",
                 "expect": "1"},
                {"call": "count_token('\"dog!\"', 'DOG')", "expect": "1"},
                {"call": "count_token('', 'x')", "expect": "0"}]},
    # ---- PACKET-010: topic-covering candidates, every rule_topic on the
    # ---- demand table (demand-20260703-071812), traps aimed at the pair
    {"name": "longest_run_char", "rule_class": "tie_break",
     "rule_topic": "direction", "stated_direction": "last",
     "task": ("Write a Python function longest_run_char(s) returning the "
              "character of the longest consecutive run of one character. "
              "When several runs tie for longest, return the character of "
              "the last such run, not the first. An empty string returns "
              "''. Note one edge case it handles."),
     "checks": [{"call": "longest_run_char('aabbb')", "expect": "'b'"},
                {"call": "longest_run_char('aabb')", "expect": "'b'"},
                {"call": "longest_run_char('x')", "expect": "'x'"},
                {"call": "longest_run_char('')", "expect": "''"}]},
    {"name": "least_frequent_word", "rule_class": "tie_break",
     "rule_topic": "direction", "stated_direction": "alphabetical",
     "task": ("Write a Python function least_frequent_word(s) returning "
              "the lowercase whitespace-separated word with the lowest "
              "count, breaking ties alphabetically. An empty string "
              "returns ''. Note one edge case it handles."),
     "checks": [{"call": "least_frequent_word('b a b')", "expect": "'a'"},
                {"call": "least_frequent_word('c a c a b b')",
                 "expect": "'a'"},
                {"call": "least_frequent_word('z y')", "expect": "'y'"},
                {"call": "least_frequent_word('')", "expect": "''"}]},
    {"name": "count_distinct_over", "rule_class": "distinctness",
     "rule_topic": "values",
     "task": ("Write a Python function count_distinct_over(nums, k) "
              "returning how many distinct values in the list are "
              "strictly greater than k, each value counted once no matter "
              "how many times it repeats. An empty list returns 0. Note "
              "one edge case it handles."),
     "checks": [{"call": "count_distinct_over([3, 3, 5], 2)",
                 "expect": "2"},
                {"call": "count_distinct_over([1, 1], 5)", "expect": "0"},
                {"call": "count_distinct_over([4, 4, 4], 3)",
                 "expect": "1"},
                {"call": "count_distinct_over([], 0)", "expect": "0"}]},
    {"name": "third_largest_distinct", "rule_class": "distinctness",
     "rule_topic": "values",
     "task": ("Write a Python function third_largest_distinct(nums) "
              "returning the third largest distinct value in the list, or "
              "None when there are fewer than three distinct values. Note "
              "one edge case it handles."),
     "checks": [{"call": "third_largest_distinct([5, 5, 4, 3])",
                 "expect": "3"},
                {"call": "third_largest_distinct([2, 2, 1, 1])",
                 "expect": "None"},
                {"call": "third_largest_distinct([9, 8, 7, 6])",
                 "expect": "7"},
                {"call": "third_largest_distinct([])", "expect": "None"}]},
    {"name": "mode_count", "rule_class": "distinctness",
     "rule_topic": "values",
     "task": ("Write a Python function mode_count(nums) returning how "
              "many distinct values tie for the highest frequency in the "
              "list, each counted once. An empty list returns 0. Note one "
              "edge case it handles."),
     "checks": [{"call": "mode_count([1, 1, 2, 2, 3])", "expect": "2"},
                {"call": "mode_count([4])", "expect": "1"},
                {"call": "mode_count([])", "expect": "0"},
                {"call": "mode_count([1, 2, 3])", "expect": "3"}]},
    {"name": "clamp", "rule_class": "boundary",
     "rule_topic": "degenerate",
     "task": ("Write a Python function clamp(value, lo, hi) returning "
              "value clamped into the inclusive range lo to hi. When lo "
              "is greater than hi the range is degenerate: return None, "
              "never swap the bounds. Note one edge case it handles."),
     "checks": [{"call": "clamp(5, 1, 3)", "expect": "3"},
                {"call": "clamp(2, 3, 1)", "expect": "None"},
                {"call": "clamp(0, -1, 1)", "expect": "0"},
                {"call": "clamp(1, 1, 1)", "expect": "1"}]},
    {"name": "nth_page", "rule_class": "boundary",
     "rule_topic": "degenerate",
     "task": ("Write a Python function nth_page(items, size, n) returning "
              "page n of the list split into consecutive pages of the "
              "given size, counting pages from 1. When size is zero or "
              "negative, or n is less than 1, or the page is past the "
              "end, return []. Note one edge case it handles."),
     "checks": [{"call": "nth_page([1, 2, 3, 4], 2, 2)",
                 "expect": "[3, 4]"},
                {"call": "nth_page([1], 2, 2)", "expect": "[]"},
                {"call": "nth_page([1, 2], 0, 1)", "expect": "[]"},
                {"call": "nth_page([1, 2, 3], 2, 1)",
                 "expect": "[1, 2]"}]},
    {"name": "split_csvish", "rule_class": "normalize",
     "rule_topic": "delimiters",
     "task": ("Write a Python function split_csvish(s) splitting the "
              "string on commas into a list of fields, trimming "
              "whitespace around each field and dropping fields that are "
              "empty after trimming. An empty string returns []. Note one "
              "edge case it handles."),
     "checks": [{"call": "split_csvish('a, b,c')",
                 "expect": "['a', 'b', 'c']"},
                {"call": "split_csvish('a, ,b')", "expect": "['a', 'b']"},
                {"call": "split_csvish('')", "expect": "[]"},
                {"call": "split_csvish(' x ')", "expect": "['x']"}]},
    {"name": "depth_max", "rule_class": "normalize",
     "rule_topic": "delimiters",
     "task": ("Write a Python function depth_max(s) returning the "
              "maximum nesting depth of square brackets in the string, "
              "counting only the characters [ and ] and ignoring "
              "everything else. When a closing bracket appears before its "
              "opener, or any opener is never closed, return -1. An empty "
              "string returns 0. Note one edge case it handles."),
     "checks": [{"call": "depth_max('[a[b]]')", "expect": "2"},
                {"call": "depth_max(']fine[')", "expect": "-1"},
                {"call": "depth_max('[[')", "expect": "-1"},
                {"call": "depth_max('')", "expect": "0"}]},
]

# Kept generation pool under the PACKET-010 conjunction: breaks for at
# least one seat AND carries an apply-pool (rule_class, rule_topic) pair.
# Selection recorded in the module docstring. The two-per-class law is
# retired; topic coverage with breakage is the pool law now.
GEN_KEPT = ("max_index", "shortest_word", "longest_run_char",
            "least_frequent_word", "mode_count")

GEN_TASKS = [t for t in CANDIDATE_GEN_TASKS if t["name"] in GEN_KEPT]

# ---------------------------------------------------------------------------
# Candidate application pool: 17 tasks. calibrate.py measures these,
# KEPT below names the survivors. rule_class names each task's trap.
# ---------------------------------------------------------------------------

CANDIDATE_APPLY_TASKS = [
    {"name": "second_largest", "rule_class": "distinctness",
     "rule_topic": "values",
     "task": ("Write a Python function second_largest(nums) returning the "
              "second largest distinct value in the list, or None when there "
              "are fewer than two distinct values. Note one edge case it "
              "handles."),
     "checks": [{"call": "second_largest([1, 3, 2])", "expect": "2"},
                {"call": "second_largest([5, 5, 5])", "expect": "None"},
                {"call": "second_largest([])", "expect": "None"},
                {"call": "second_largest([2, 1, 2])", "expect": "1"}],
     "rule_checks": ["second_largest([5, 5, 5])",
                     "second_largest([2, 1, 2])"]},
    {"name": "most_common_word", "rule_class": "tie_break",
     "rule_topic": "direction",
     "stated_direction": "alphabetical",
     "task": ("Write a Python function most_common_word(s) returning the "
              "lowercase whitespace-separated word with the highest count, "
              "breaking ties alphabetically. An empty string returns ''. "
              "Note one edge case it handles."),
     "checks": [{"call": "most_common_word('b a b a c')", "expect": "'a'"},
                {"call": "most_common_word('z z y')", "expect": "'z'"},
                {"call": "most_common_word('')", "expect": "''"}],
     "rule_checks": ["most_common_word('b a b a c')"]},
    {"name": "top_k", "rule_class": "boundary",
     "rule_topic": "degenerate",
     "task": ("Write a Python function top_k(nums, k) returning a list of "
              "the k largest values in descending order, keeping duplicates. "
              "If k is zero or negative return []. If k exceeds the list "
              "length return all values sorted descending. Note one edge "
              "case it handles."),
     "checks": [{"call": "top_k([4, 1, 4, 2], 2)", "expect": "[4, 4]"},
                {"call": "top_k([3, 1, 2], 0)", "expect": "[]"},
                {"call": "top_k([1, 2], 5)", "expect": "[2, 1]"},
                {"call": "top_k([], 3)", "expect": "[]"}]},
    {"name": "dedupe", "rule_class": "distinctness",
     "rule_topic": "values",
     "task": ("Write a Python function dedupe(items) returning the list "
              "with duplicates removed, preserving the order of first "
              "appearance. Note one edge case it handles."),
     "checks": [{"call": "dedupe([3, 1, 3, 2, 1])", "expect": "[3, 1, 2]"},
                {"call": "dedupe([])", "expect": "[]"},
                {"call": "dedupe(['b', 'a', 'b'])", "expect": "['b', 'a']"},
                {"call": "dedupe([7, 7, 7])", "expect": "[7]"}],
     "rule_checks": ["dedupe([3, 1, 3, 2, 1])",
                     "dedupe(['b', 'a', 'b'])"]},
    {"name": "mode", "rule_class": "tie_break",
     "rule_topic": "direction",
     "stated_direction": "smallest",
     "task": ("Write a Python function mode(nums) returning the most "
              "frequent value in the list, breaking ties by returning the "
              "smallest such value. An empty list returns None. Note one "
              "edge case it handles."),
     "checks": [{"call": "mode([1, 2, 2, 3])", "expect": "2"},
                {"call": "mode([4, 4, 1, 1])", "expect": "1"},
                {"call": "mode([])", "expect": "None"},
                {"call": "mode([7])", "expect": "7"}]},
    {"name": "merge_ranges", "rule_class": "boundary",
     "rule_topic": "degenerate",
     "task": ("Write a Python function merge_ranges(pairs) taking a list of "
              "[start, end] inclusive integer ranges, possibly unsorted, and "
              "returning the merged ranges sorted by start, as a list of "
              "[start, end] lists. Ranges that overlap or touch merge: "
              "[1, 3] and [4, 6] become [1, 6]. Note one edge case it "
              "handles."),
     "checks": [{"call": "merge_ranges([[1, 3], [4, 6]])",
                 "expect": "[[1, 6]]"},
                {"call": "merge_ranges([[5, 7], [1, 2]])",
                 "expect": "[[1, 2], [5, 7]]"},
                {"call": "merge_ranges([[1, 4], [2, 3]])",
                 "expect": "[[1, 4]]"},
                {"call": "merge_ranges([])", "expect": "[]"}],
     "rule_checks": ["merge_ranges([[1, 3], [4, 6]])"]},
    {"name": "longest_word", "rule_class": "tie_break",
     "rule_topic": "direction",
     "stated_direction": "last",
     "task": ("Write a Python function longest_word(s) returning the "
              "longest whitespace-separated word in the string. On ties "
              "return the last such word, not the first. An empty string "
              "returns ''. Note one edge case it handles."),
     "checks": [{"call": "longest_word('cat door bird')", "expect": "'bird'"},
                {"call": "longest_word('a bb cc d')", "expect": "'cc'"},
                {"call": "longest_word('')", "expect": "''"},
                {"call": "longest_word('one')", "expect": "'one'"}],
     "rule_checks": ["longest_word('cat door bird')",
                     "longest_word('a bb cc d')"]},
    {"name": "median", "rule_class": "boundary",
     "rule_topic": "degenerate",
     "task": ("Write a Python function median(nums) returning the middle "
              "value of the sorted list when the length is odd, or the "
              "average of the two middle values as a float when the length "
              "is even. An empty list returns None. Note one edge case it "
              "handles."),
     "checks": [{"call": "median([3, 1, 2])", "expect": "2"},
                {"call": "median([1, 2, 3, 4])", "expect": "2.5"},
                {"call": "median([5, 5])", "expect": "5.0"},
                {"call": "median([])", "expect": "None"}],
     "rule_checks": ["median([5, 5])", "median([])"]},
    {"name": "range_summary", "rule_class": "distinctness",
     "rule_topic": "values",
     "task": ("Write a Python function range_summary(nums) taking a list of "
              "integers, possibly unsorted with duplicates, and returning a "
              "string of the distinct values in ascending order, collapsing "
              "consecutive runs into 'start-end' and joining pieces with "
              "commas, so [1, 2, 3, 5] becomes '1-3,5'. A single number "
              "stays a single number, never a range. An empty list returns "
              "''. Note one edge case it handles."),
     "checks": [{"call": "range_summary([1, 2, 3, 5])", "expect": "'1-3,5'"},
                {"call": "range_summary([3, 1, 2, 2])", "expect": "'1-3'"},
                {"call": "range_summary([5, 3, 1])", "expect": "'1,3,5'"},
                {"call": "range_summary([])", "expect": "''"},
                {"call": "range_summary([7])", "expect": "'7'"}],
     "rule_checks": ["range_summary([3, 1, 2, 2])"]},
    {"name": "flatten_once", "rule_class": "boundary",
     "rule_topic": "degenerate",
     "task": ("Write a Python function flatten_once(lst) that flattens "
              "exactly one level of nesting: elements that are lists "
              "contribute their items in order, and every other element is "
              "kept as is. Deeper nesting stays nested. Note one edge case "
              "it handles."),
     "checks": [{"call": "flatten_once([[1, 2], [3]])", "expect": "[1, 2, 3]"},
                {"call": "flatten_once([1, [2, [3, 4]]])",
                 "expect": "[1, 2, [3, 4]]"},
                {"call": "flatten_once([])", "expect": "[]"}],
     "rule_checks": ["flatten_once([1, [2, [3, 4]]])"]},
    {"name": "snake_to_camel", "rule_class": "normalize",
     "rule_topic": "delimiters",
     "task": ("Write a Python function snake_to_camel(s) converting a "
              "snake_case identifier to camelCase, so 'foo_bar_baz' becomes "
              "'fooBarBaz'. Leading, trailing, and repeated underscores are "
              "dropped: '__a__b_' becomes 'aB'. An empty string returns ''. "
              "Note one edge case it handles."),
     "checks": [{"call": "snake_to_camel('foo_bar_baz')",
                 "expect": "'fooBarBaz'"},
                {"call": "snake_to_camel('__a__b_')", "expect": "'aB'"},
                {"call": "snake_to_camel('word')", "expect": "'word'"},
                {"call": "snake_to_camel('')", "expect": "''"}],
     "rule_checks": ["snake_to_camel('__a__b_')"]},
    {"name": "nth_smallest", "rule_class": "distinctness",
     "rule_topic": "values",
     "task": ("Write a Python function nth_smallest(nums, n) returning the "
              "nth smallest distinct value in the list, counting from 1. "
              "Return None when n is less than 1 or exceeds the number of "
              "distinct values. Note one edge case it handles."),
     "checks": [{"call": "nth_smallest([5, 1, 3], 2)", "expect": "3"},
                {"call": "nth_smallest([2, 2, 1], 2)", "expect": "2"},
                {"call": "nth_smallest([1, 2], 3)", "expect": "None"},
                {"call": "nth_smallest([1], 0)", "expect": "None"}]},
    {"name": "is_rotation", "rule_class": "boundary",
     "rule_topic": "empty",
     "task": ("Write a Python function is_rotation(a, b) returning True "
              "when string b is a rotation of string a, such as 'cdeab' of "
              "'abcde'. Strings of different lengths are never rotations, a "
              "string counts as a rotation of itself, and two empty strings "
              "count as rotations. Note one edge case it handles."),
     "checks": [{"call": "is_rotation('abcde', 'cdeab')", "expect": "True"},
                {"call": "is_rotation('abc', 'acb')", "expect": "False"},
                {"call": "is_rotation('', '')", "expect": "True"},
                {"call": "is_rotation('aa', 'a')", "expect": "False"}]},
    {"name": "truncate_words", "rule_class": "normalize",
     "rule_topic": "whitespace",
     "task": ("Write a Python function truncate_words(s, n) returning the "
              "first n whitespace-separated words of the string joined by "
              "single spaces, so runs of whitespace collapse. When n is "
              "zero or negative return ''. When the string has fewer than "
              "n words return them all. Note one edge case it handles."),
     "checks": [{"call": "truncate_words('the  quick  brown fox', 2)",
                 "expect": "'the quick'"},
                {"call": "truncate_words('a b', 5)", "expect": "'a b'"},
                {"call": "truncate_words('a b c', 0)", "expect": "''"},
                {"call": "truncate_words('', 3)", "expect": "''"}]},
    {"name": "balanced", "rule_class": "normalize",
     "rule_topic": "delimiters",
     "task": ("Write a Python function balanced(s) returning True when the "
              "parentheses in the string are balanced, considering only the "
              "characters '(' and ')' and ignoring everything else. A "
              "closing parenthesis must never appear before its opening "
              "partner: ')(' is not balanced. An empty string is balanced. "
              "Note one edge case it handles."),
     "checks": [{"call": "balanced('(a(b)c)')", "expect": "True"},
                {"call": "balanced(')(')", "expect": "False"},
                {"call": "balanced('')", "expect": "True"},
                {"call": "balanced('((x)')", "expect": "False"}],
     "rule_checks": ["balanced('(a(b)c)')", "balanced(')(')"]},
    {"name": "interleave", "rule_class": "boundary",
     "rule_topic": "degenerate",
     "task": ("Write a Python function interleave(a, b) returning a single "
              "list alternating elements from the two lists, starting with "
              "a. When one list is longer, its remaining elements are "
              "appended at the end. Note one edge case it handles."),
     "checks": [{"call": "interleave([1, 2], ['a', 'b'])",
                 "expect": "[1, 'a', 2, 'b']"},
                {"call": "interleave([1, 2, 3], ['x'])",
                 "expect": "[1, 'x', 2, 3]"},
                {"call": "interleave([], [1, 2])", "expect": "[1, 2]"}]},
    {"name": "count_pairs", "rule_class": "distinctness",
     "rule_topic": "pairs",
     "task": ("Write a Python function count_pairs(nums, target) returning "
              "the number of index pairs i < j where nums[i] + nums[j] "
              "equals target. Equal values at different indices count as "
              "distinct pairs: [2, 2, 2] with target 4 has three pairs. "
              "Note one edge case it handles."),
     "checks": [{"call": "count_pairs([1, 2, 3], 4)", "expect": "1"},
                {"call": "count_pairs([2, 2, 2], 4)", "expect": "3"},
                {"call": "count_pairs([], 5)", "expect": "0"},
                {"call": "count_pairs([5], 5)", "expect": "0"}]},
]

# ---------------------------------------------------------------------------
# Kept pool. Every task where at least one seat scored below 1.0 in the
# calibration run recorded in the module docstring. Exactly the eligible
# eight, and both seat baselines sit inside the band, so no swaps.
# Kept-pool rule classes: tie_break 2, distinctness 1, boundary 3,
# normalize 2. Distinctness is thin here and the report's per-class
# breakdown must state its n.
# ---------------------------------------------------------------------------

KEPT = ("most_common_word", "merge_ranges", "longest_word", "median",
        "range_summary", "flatten_once", "snake_to_camel", "balanced")

APPLY_TASKS = [t for t in CANDIDATE_APPLY_TASKS if t["name"] in KEPT]
