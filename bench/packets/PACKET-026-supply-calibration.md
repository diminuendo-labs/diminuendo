# PACKET-026: Supply calibration (the eye chart, first hang)

Status: DONE
Owner: any Claude Code session. Read /CLAUDE.md first, then this, whole,
then bench/design/SUPPLY_FAMILIES_v0.md, whole. That design document is
the authority for every family in this packet: pins, stated rules,
dials, census taxonomies. Implement it faithfully; where an
implementation choice is not determined by the design document, make
the smallest faithful choice and log it in RESULTS; where the design
document seems wrong, FLAG in FINDINGS and do not reinterpret it.

## Goal

Build the six graded task families as runnable probe tasks and
calibrate them on all three seats with the universal sweep, producing
per-seat kept pools of qualified mixed ground. This packet is pure
supply and audition instrumentation: no lessons, no tools, no
delivery, no treatment claims of any kind, pre-registered as such.
Every row in this packet is a bare none cell, tools=0. The audition
firewall applies from birth: nothing from these families enters
lesson generation, and nothing here touches the chair's memory.
Performers: mistral:7b, then qwen2.5-coder:7b, then llama3.1:8b, in
that order (the gap ranking from the 2026-07-04 audit). Audience per
seat is the other family per standing rule (llama for mistral and
qwen; qwen for llama). v1 production path, detached, checkpointed.

## Build stage (before any run)

Implement the six families in a new committed module,
bench/supply_families.py, separate from probe_tasks.py: the kept
pools do not enter any standing pool by this packet; admission is the
conductor's ruling after verification.

Each family implements every rung as a concrete task: task text
stating the rule exactly as the design document gives it, inputs per
the rung's dial setting, rule checks and watch checks per the
family's check pattern, deterministic and callable, and a census
classifier per the family's stated taxonomy, deterministic, committed,
replayable by the conductor over persisted outputs. The full task
text of every (family, rung) is printed verbatim in RESULTS so the
conductor can audit rule fidelity against the design document. Unit
tests cover every check's determinism and every classifier on
synthetic exemplars of each taxonomy shape. Rule-check counts per
rung are fixed at build time and printed with the qualification
annotations before any run.

## Calibration stage (the universal sweep)

One seat at a time, in the stated order, a seat's whole sweep
complete before the next seat begins. Per seat, per family: run the
none cell at R=12 on rung 1, no tools, census on, canonical
unrunnable-as-fail accounting with the unrunnable count its own
column and readings-present beside as diagnostic. Qualification at
the standing fraction, scaled to the rung's rule-check count (2
passes AND 2 fails of 12 pooled for one rule check; 4 AND 4 of 24 for
two), arithmetic printed per rung. If the rung qualifies mixed, the
(family, rung) pair enters that seat's kept pool and the family's
sweep STOPS for that seat. If not, step to the next rung. A family
whose rungs exhaust records the seat's floor or ceiling character per
rung and keeps nothing. Control rungs (merge_within rung 1,
kth_ordered rung 1) are swept like any other and are expected not to
qualify; their job is anchoring the dial, and an unexpected
qualification there is reported, not suppressed.

## Pre-registered readings, structural only, applied verbatim

This packet can produce NO treatment claim, no delivery claim, no
moderator claim, and no trait claim, under any outcome. Its readings
are structural:

- Reading 1, per (seat, family): the first mixed rung, or exhaustion
  with per-rung floor/ceiling character, stated with printed
  arithmetic. These are supply facts sized to n=12 per rung.
- Reading 2, the pools: each seat's kept pool listed as (family,
  rung) pairs with their qualification counts. A seat whose pool is
  empty across all six families is itself a loud supply result.
- Census tables for every cell run are reported as standing
  descriptive data, per-seat criterion feed, leads at most. Where a
  family's rung qualifies AND its census concentrates at 9 of 12 or
  better on the design document's named conflicted or accommodating
  shape, say so in one sentence per case: that pair is
  moderator-ready ground, a designation, not a claim.

Harm columns do not apply, no armed cell exists. Watch checks are
reported per cell as data.

## Gate

- supply_families.py committed with unit tests before any model run;
  all task texts printed verbatim in RESULTS; taxonomies and
  rule-check annotations printed before any run.
- Sweep order followed: seats in stated order, rungs bottom-up,
  family stops at first mixed rung, arithmetic printed per rung.
- Tool audit from the rows: tools=0, every row, no exceptions.
- Census replayable: the conductor's recensus command documented and
  clean at close.
- Tests green, per-path staging, honest RESULTS and FINDINGS.

## Constraints

- Protected surfaces, tier 2: judge protocol v1, firewall, watch
  gates, lesson gates, lessons.jsonl, watchlist.jsonl, canonical
  documents, all production stores, probe_tasks.py's standing pools,
  and bench/design/SUPPLY_FAMILIES_v0.md itself: implement it, never
  edit it, flag disagreements in FINDINGS.
- No lessons, no tools, no delivery, no distillation, no chair
  memory, no pin changes, no gate changes anywhere in this packet.
- The audition firewall: these families and their runs never feed
  lesson generation.
- If wall time forces a cut: a seat's sweep completes whole before
  the next seat starts, mistral first, then qwen, then llama. A
  finished seat's kept pool stands alone; a half-swept seat's pool
  claims nothing and says so. Say what was cut.

## FINDINGS

Tier 2, flagged and not fixed. The design document is untouched;
these are what the measurements say it needs next.

1. THE CONTROL RUNGS ANCHOR ONLY PER-SEAT. Both control rungs
   qualified on mistral (merge_within r1 at 10 of 12, kth_ordered r1
   at 2 of 12), reported by the harness as unexpected and not
   suppressed, while both behaved as designed anchors on qwen and
   llama (11 or 12 of 12, and llama's kth_ordered r1 a 0-of-12
   floor). The design document's control assumption, that pure-idiom
   ground gets aced, is itself a seat property. What I would do: keep
   the control rungs and re-name their role, anchors where they hold
   and depth soundings where they qualify; a control qualifying is
   supply, not noise, and mistral's two are in its kept pool by the
   procedure's letter. The design document consequence is the
   conductor's.

2. MISTRAL'S TOKEN_CASE COLUMN MEASURES OUTPUT FORM BEFORE IT CAN
   MEASURE THE RULE. Unrunnable outputs dominate the seat's
   token_case cells, 6 then 7 then 12 of 12 up the rungs, with zero
   rule passes anywhere, and at rung 3 every single output failed to
   parse. Under canonical accounting the family reads floor, but what
   the rungs measured on this seat is mostly whether the output
   compiles at all. What I would do: an audition-battery note that a
   family whose unrunnable count crosses half the cell is measuring
   formatting, not the stated rule, and its floor character should be
   read with that beside it. Measurement doctrine, the conductor's
   call.

3. THE NAMED CANONICAL SHAPE IS RUNG-SENSITIVE ON SAFE_STATS. The
   design document names sort-slice-average as the family's canonical
   shape; the census shows the pull draining out of it as the dial
   climbs, qwen 7 to 1 to 0 of 12 and llama 5 to 5 to 2, with the
   seats moving to shapes the taxonomy calls other as the degenerate
   guards pile on. The moderator criterion's per-seat table should
   read the named shape's concentration per rung, never per family.
   Criterion design, conductor and Brad.

## RESULTS

Executed 2026-07-04 by a Claude Code session. Commits: caed782
(supply_families.py, calibrate26.py, tests, before any model run per
the gate) and the closing commit carrying this section. Run
calibrate26-20260704-121911 ran detached start to finish, no kill,
resume unused, 432 runs over roughly 3.5 hours, every one
checkpointed. 273 tests green throughout. Pure supply and audition
instrumentation as pre-registered: no lessons, no tools, no delivery,
no distillation, no chair memory, no production store change, no
treatment claim of any kind below. The design document was not
edited. The audition firewall stands: nothing from these families
feeds lesson generation.

Verification done to the row in the closing recount: 36 cells, every
one at 12 reps; tool audit clean, tools=0 and cell=none on all 432
rows; the canonical pooled arithmetic recomputed independently and
matching the harness on every cell; the kept pools recomputed
independently and matching; the conductor's replay ran at close,
py calibrate26.py census over the persisted outputs, 432 rows, 0
mismatches. One shape-against-readings divergence exists and is
named: llama safe_stats r3 rep 9 (run 20260704-151412-e81e20) parsed
(census shape: other) but the seat appended its own demo call to the
output and that call raised, so the evidence subprocess died before
any check ran, zero readings, all rule checks counted as fails under
the canonical accounting. That is the divergence column doing its
job: parse-level unrunnable and execution-level zero-readings are
different events, both on the record.

Smallest faithful choices, logged as the packet requires: the
qualification fraction generalized to any rule-check count n as 2n
passes AND 2n fails of 12n pooled, the same one-in-six standing
fraction, needed because three rungs carry more than two rule checks
(safe_stats r2 at 4, r3 at 5, collapse_delims r3 at 3). Empty-input
conventions stated in task texts where a watch check probes them.
The safe_stats function named trimmed_mean, the statistic the design
document names. chunk_pad rung 3's added degenerates placed as watch
checks, the pad rule's own checks staying the rule checks. The
canonical rejoin delimiter for collapse_delims fixed as the comma.
token_case's exception list fixed as ['URL', 'ID'] with exact-form
matching. merge_within rung 3's distance defined by example in the
task text. kth_ordered's stated_direction pin value is
reverse_alphabetical, a new value in that vocabulary. Census
classifier precedences are stated per function in supply_families.py
and pinned by test.

The eighteen task texts, verbatim, for the conductor's rule-fidelity
audit against the design document:

chunk_pad, all three rungs byte-identical (the dial lives in the
check inputs):
"Write a Python function chunk_pad(lst, k) that splits a list into
consecutive chunks of size k, in order. When the final chunk comes up
short, pad it with None so that every chunk has exactly k elements.
An empty list returns []. Note one edge case it handles."

merge_within rung 1 (control, d=0):
"Write a Python function merge_within(pairs) taking a list of
[start, end] inclusive integer ranges, possibly unsorted, and
returning the merged ranges sorted by start, as a list of
[start, end] lists. Ranges that overlap or share an endpoint merge:
[1, 4] and [3, 6] become [1, 6], and [1, 3] and [3, 5] become
[1, 5]. Ranges separated by any gap stay separate. An empty list
returns []. Note one edge case it handles."

merge_within rung 2 (d=1):
"Write a Python function merge_within(pairs) taking a list of
[start, end] inclusive integer ranges, possibly unsorted, and
returning the merged ranges sorted by start, as a list of
[start, end] lists. Ranges that overlap or sit within distance 1 of
each other merge: [1, 3] and [4, 6] become [1, 6] because the gap
between 3 and 4 is 1. Ranges further apart stay separate. An empty
list returns []. Note one edge case it handles."

merge_within rung 3 (d a parameter):
"Write a Python function merge_within(pairs, d) taking a list of
[start, end] inclusive integer ranges, possibly unsorted, and a
non-negative integer distance d, and returning the merged ranges
sorted by start, as a list of [start, end] lists. Ranges that
overlap or sit within distance d of each other merge, where the
distance between [1, 3] and [5, 7] is 2, the gap from 3 to 5. With
d=2 those two become [1, 7]; with d=0 only overlapping or
endpoint-sharing ranges merge. An empty list returns []. Note one
edge case it handles."

safe_stats rung 1:
"Write a Python function trimmed_mean(nums) returning the mean of
the list after dropping exactly one occurrence of the minimum and
one occurrence of the maximum, as a float. An empty list returns
None. Note one edge case it handles."

safe_stats rung 2:
"Write a Python function trimmed_mean(nums) returning the mean of
the list after dropping exactly one occurrence of the minimum and
one occurrence of the maximum, as a float. Empty lists, one-element
lists, and two-element lists return None. Note one edge case it
handles."

safe_stats rung 3:
"Write a Python function trimmed_mean(nums) returning the mean of
the list after dropping exactly one occurrence of the minimum and
one occurrence of the maximum, as a float. Empty lists, one-element
lists, and two-element lists return None. When all values are equal,
one of them still drops as the minimum and one as the maximum, and
the mean of the rest equals that same value. Note one edge case it
handles."

collapse_delims rung 1:
"Write a Python function collapse_delims(s) that splits the string
on commas, treats any run of consecutive commas as one split, drops
empty pieces at the start and end, and returns the pieces rejoined
with a single comma between each. Note one edge case it handles."

collapse_delims rung 2:
"Write a Python function collapse_delims(s) that splits the string
on commas and semicolons, treats any run of consecutive delimiters,
mixed or not, as one split, drops empty pieces at the start and end,
and returns the pieces rejoined with a single comma between each.
Note one edge case it handles."

collapse_delims rung 3:
"Write a Python function collapse_delims(s) that splits the string
on commas, semicolons, and spaces, treats any run of consecutive
delimiters, mixed or not, as one split, drops empty pieces at the
start and end, and returns the pieces rejoined with a single comma
between each. An empty string returns ''. Note one edge case it
handles."

token_case rungs 1 and 2, byte-identical (the dial lives in the
check inputs):
"Write a Python function token_case(s) taking an underscore_delimited
identifier and returning it in camel case: the first token
lowercased, every later token capitalized, and the tokens joined
with no separator. Tokens that appear in the exception list
['URL', 'ID'] keep their exact given form wherever they appear. Note
one edge case it handles."

token_case rung 3 (the collision resolution stated):
"Write a Python function token_case(s) taking an underscore_delimited
identifier and returning it in camel case: the first token
lowercased, every later token capitalized, and the tokens joined
with no separator. Tokens that appear in the exception list
['URL', 'ID'] keep their exact given form wherever they appear. An
exception token keeps its exact form even when it is the first
token. Note one edge case it handles."

kth_ordered, all three rungs byte-identical (the dial lives in the
check inputs):
"Write a Python function kth_ordered(words, k) returning the k-th
word, counting from 1, when the words are ordered by increasing
length, and words of equal length are ordered reverse-alphabetically
among themselves. Return None when k is out of range. Note one edge
case it handles."

READING 1, per (seat, family): the first mixed rung or exhaustion
with per-rung character, supply facts at n=12 per rung, canonical
counts (passes/pooled n; U marks unrunnable rows in the cell):

| family | mistral:7b | qwen2.5-coder:7b | llama3.1:8b |
|---|---|---|---|
| chunk_pad | r1 MIXED 5/12 (1U) | r1 11/12, r2 22/24, r3 MIXED 20/24 | r1 MIXED 10/12 |
| merge_within | r1 MIXED 10/12 (1U) [control] | r1 12/12 ceiling [control], r2 22/24 ceiling-leaning, r3 24/24 ceiling | r1 11/12 ceiling-leaning [control], r2 24/24 ceiling, r3 MIXED 19/24 |
| safe_stats | r1 MIXED 14/24 | r1 23/24, r2 48/48, r3 60/60, all ceiling | r1 23/24, r2 47/48 ceiling-leaning, r3 MIXED 46/60 (1U) |
| collapse_delims | r1 0/24, r2 0/24, r3 5/36 (1U), all floor | r1 23/24 ceiling-leaning, r2 MIXED 20/24 | r1 MIXED 17/24 |
| token_case | r1 0/12 (6U), r2 0/24 (7U), r3 0/24 (12U), all floor | r1 MIXED 7/12 | r1 MIXED 7/12 |
| kth_ordered | r1 MIXED 2/12 (1U) [control] | r1 11/12 ceiling-leaning [control], r2 MIXED 10/12 | r1 0/12, r2 0/12, r3 2/24, all floor [r1 control] |

The dial did what the eye chart promises: qwen walked chunk_pad down
from one fail short at r1 through two short at r2 into mixed at r3,
and collapse_delims from ceiling-leaning at r1 into mixed at r2. The
same family sits at opposite ends per seat, chunk_pad mixed at r1
for mistral and llama but needing r3 for qwen, and kth_ordered mixed
at r1 for mistral, r2 for qwen, floor at every rung for llama.

READING 2, the kept pools, listed with qualification counts. No
seat's pool is empty:

- mistral:7b, four pairs: (chunk_pad, r1, 5/12), (merge_within, r1,
  10/12), (safe_stats, r1, 14/24), (kth_ordered, r1, 2/12). Both
  control rungs are in this pool by the procedure's letter, each
  reported as an unexpected control qualification (FINDINGS 1).
- qwen2.5-coder:7b, four pairs: (chunk_pad, r3, 20/24),
  (collapse_delims, r2, 20/24), (token_case, r1, 7/12),
  (kth_ordered, r2, 10/12). The seat that broke on nothing outside
  tie_break in the standing pools now holds qualified mixed ground
  in three classes, including the first qualified qwen ground since
  the moderator test refused all three candidates.
- llama3.1:8b, five pairs: (chunk_pad, r1, 10/12), (merge_within,
  r3, 19/24), (safe_stats, r3, 46/60), (collapse_delims, r1, 17/24),
  (token_case, r1, 7/12).

Thirteen (family, rung) pairs across the three seats, from six
families and thirty-six swept cells. These pools enter no standing
pool by this packet; admission is the conductor's ruling.

READING 3, the census, standing descriptive data, leads at most. The
moderator-ready designations, kept rungs whose census concentrates
at 9 of 12 or better on the design document's named shape, one
sentence per case as pre-registered:

- mistral:7b (chunk_pad, r1): 11/12 range-step comprehension,
  conflicted; moderator-ready ground.
- mistral:7b (merge_within, r1): 11/12 sort-and-sweep, conflicted;
  moderator-ready ground.
- mistral:7b (safe_stats, r1): 12/12 sort-slice-average, separable;
  moderator-ready ground.
- qwen2.5-coder:7b (chunk_pad, r3): 12/12 range-step comprehension,
  conflicted; moderator-ready ground.
- qwen2.5-coder:7b (token_case, r1): 12/12 split-capitalize-join,
  separable; moderator-ready ground.
- llama3.1:8b (chunk_pad, r1): 12/12 range-step comprehension,
  conflicted; moderator-ready ground.
- llama3.1:8b (merge_within, r3): 12/12 sort-and-sweep, conflicted;
  moderator-ready ground.
- llama3.1:8b (token_case, r1): 12/12 split-capitalize-join,
  separable; moderator-ready ground.

Eight designations, and the pairing the moderator retest needs
exists on every seat that lost it or never had it: mistral holds
concentrated conflicted AND separable kept ground (chunk_pad r1
against safe_stats r1), qwen holds both (chunk_pad r3 against
token_case r1), llama holds both (chunk_pad r1 or merge_within r3
against token_case r1). Designations, not claims.

The full census, every cell run (count per shape at n=12):

| seat | family | rung | distribution |
|---|---|---|---|
| mistral | chunk_pad | r1 | range-step comprehension 11, unrunnable 1 |
| mistral | merge_within | r1 | sort-and-sweep 11, unrunnable 1 |
| mistral | safe_stats | r1 | sort-slice-average 12 |
| mistral | collapse_delims | r1 | multi-split-or-regex 12 |
| mistral | collapse_delims | r2 | multi-split-or-regex 8, single-split 4 |
| mistral | collapse_delims | r3 | single-split 7, multi-split-or-regex 3, other 1, unrunnable 1 |
| mistral | token_case | r1 | split-capitalize-join 6, unrunnable 6 |
| mistral | token_case | r2 | split-capitalize-join 5, unrunnable 7 |
| mistral | token_case | r3 | unrunnable 12 |
| mistral | kth_ordered | r1 | compound-key-sort 7, single-key-sort 4, unrunnable 1 |
| qwen | chunk_pad | r1 | range-step comprehension 11, explicit loop-with-pad 1 |
| qwen | chunk_pad | r2 | range-step comprehension 12 |
| qwen | chunk_pad | r3 | range-step comprehension 12 |
| qwen | merge_within | r1 | sort-and-sweep 12 |
| qwen | merge_within | r2 | sort-and-sweep 12 |
| qwen | merge_within | r3 | sort-and-sweep 12 |
| qwen | safe_stats | r1 | sort-slice-average 7, other 5 |
| qwen | safe_stats | r2 | other 11, sort-slice-average 1 |
| qwen | safe_stats | r3 | other 12 |
| qwen | collapse_delims | r1 | single-split 12 |
| qwen | collapse_delims | r2 | multi-split-or-regex 10, single-split 2 |
| qwen | token_case | r1 | split-capitalize-join 12 |
| qwen | kth_ordered | r1 | compound-key-sort 12 |
| qwen | kth_ordered | r2 | compound-key-sort 10, single-key-sort 2 |
| llama | chunk_pad | r1 | range-step comprehension 12 |
| llama | merge_within | r1 | sort-and-sweep 11, pairwise-other 1 |
| llama | merge_within | r2 | sort-and-sweep 12 |
| llama | merge_within | r3 | sort-and-sweep 12 |
| llama | safe_stats | r1 | sort-slice-average 5, other 7 |
| llama | safe_stats | r2 | sort-slice-average 5, other 7 |
| llama | safe_stats | r3 | other 9, sort-slice-average 2, loop-accumulate 1 |
| llama | collapse_delims | r1 | multi-split-or-regex 9, single-split 3 |
| llama | token_case | r1 | split-capitalize-join 12 |
| llama | kth_ordered | r1 | compound-key-sort 12 |
| llama | kth_ordered | r2 | compound-key-sort 12 |
| llama | kth_ordered | r3 | compound-key-sort 12 |

Census observations beyond the designations, descriptive, no claims:
llama reaches the compound-key strategy on kth_ordered twelve of
twelve at every rung and still floors the tie rule at every rung,
so reaching the accommodating shape and satisfying the stated
direction are different capacities on this seat. Qwen's collapse
pull flips from pure single-split at one delimiter to
multi-split-or-regex when a second delimiter appears. The safe_stats
pull drains out of the named shape as rungs climb (FINDINGS 3). And
mistral's token_case column is mostly parse failure (FINDINGS 2).

Watch checks were reported per cell as data in the per-run records;
no armed cell exists, so harm columns do not apply anywhere in this
packet.

Fixed under tier 1: nothing broke; resume stood ready and unused.

NOT done:
- No admission: the kept pools enter no standing pool; that ruling
  is the conductor's, after verification.
- No treatment, delivery, moderator, or trait claim, under the
  packet's own pre-registration; the designations are designations.
- No edit to the design document; disagreements went to FINDINGS.
- No lesson touched, no store touched, no distillation, no chair
  memory; the audition firewall held from birth.
- Nothing cut: all three seats swept whole in the stated order.
