# PACKET-010: Topic-covering supply (the conjunction filter)

Status: DONE
Owner: any Claude Code session. Read /CLAUDE.md first, then this, whole.

## Goal

Cure the structural-empty rate at its cause. PACKET-009 found three of
five lessons pinned to topics no apply task carries, and the standing-down
session's flag sharpened the diagnosis: the generation tasks that break
carry orphan topics, and the tasks with in-pool topics never break. So the
filter is a conjunction, applied before calibration: a candidate earns a
slot only if it plausibly breaks for at least one seat AND carries a
rule_topic that exists in the apply pool. One aim inside that: the
reverse-direction hunt, llama-origin lessons that match qwen-headroom
apply tasks, the transfer cell no measurement has reached.

## The work, in order

1. Enumerate the demand side programmatically: every (rule_class,
   rule_topic) pair present in the apply pool, and per pair, which seats
   have rule-check headroom there (from the PACKET-001 calibration and
   later run records). Report this table first; it is the shopping list.
2. Author 2 to 3 candidates per demanded pair, task text disjoint from
   every apply task, checks reference-verified and pinned by test, traps
   aimed at the pair's stated rule. Candidates whose topic is not on the
   shopping list are not written, whatever else recommends them.
3. Calibrate (gencal pattern, R_G=3 per seat) and keep only candidates
   that broke for at least one seat. Report the kept table per pair per
   seat. A demanded pair where nothing breaks after two candidate swaps
   is reported as resistant, not forced.
4. Generation pass at full gates (genpass pattern, both contrast paths,
   class-level phrasing). Quote every committed lesson with its pins.
5. Re-run the pairing enumeration from PACKET-009's confirm harness
   against the new stores plus the 053623 stores. Report: matched
   cross-seat pairings, structural-empty rate before and after, and
   whether a reverse-direction cell (llama-origin lesson, qwen-headroom
   task) now exists. No arms in this packet: supply only, the measurement
   is the next packet's.

## Gate

- The demand table, the kept-candidate table, and the enumeration
  before-and-after are all in RESULTS with numbers.
- Every committed lesson conditional, declarative, topic-pinned, quoted.
- No screen, pin, or gate loosened to raise any count. Resistant pairs
  named, not forced.
- Tests green, per-path staging, detached runs read from disk, honest
  RESULTS and FINDINGS.

## Constraints

- Protected surfaces, tier 2: judge protocol v1, firewall, watch gates,
  lessons.jsonl, watchlist.jsonl, canonical documents, and the existing
  probe stores (append new stores, never touch old ones).
- If wall time forces a cut, cut candidate count per pair before cutting
  R_G, and say so.

## FINDINGS

Tier 2, flagged and not fixed:

1. The code seat breaks on nothing new, nine candidates deep. qwen
   passed every run of every new candidate at R_G=3 (27 runs), as it
   has passed everything outside tie_break since PACKET-002. Its supply
   remains tie-only, so every future cross-seat cell teaching llama
   will be a tie cell until harder qwen-breaking tasks exist. What I
   would do: candidates authored specifically against the code seat
   (multi-constraint tasks, or tasks at a size above "small"), which is
   an instrument-design decision with spec implications for the task
   vocabulary, the conductor's call.
2. Two demanded pairs are RESISTANT: boundary/degenerate and
   normalize/delimiters. Two candidates each, both seats, all_pass at
   R_G=3, reported per the packet's own rule, not forced. The apply
   tasks in those pairs hold the record's deepest unarmed floors
   (merge_ranges 0.00 everywhere, snake_to_camel 0.00 nearly
   everywhere), so the tasks where lessons are most needed are exactly
   the pairs where no generation task breaks yet. What I would do:
   author a second wave aimed lower (harder degenerate and delimiter
   traps), or accept the floors as unteachable at this model scale
   until the pool grows.
3. One-line screen gap, tier 3 by size: the shape screen's "use a"
   pattern misses "use an", and one committed rule leans procedural
   through that gap ("use an operation that processes items in reverse
   order"). Named in RESULTS beside the quote; extending the pattern
   is a gate change, so it waits for a ruling.

## RESULTS

Executed 2026-07-03 by a Claude Code session. Commits: a6baf67 (demand
table and candidates), 62de1ea (conjunction calibration and pool law),
and the closing commit carrying this section, the genpass gate fix, and
the enumeration. Runs: demand-20260703-071812 (no model calls), gencal
20260703-072720 (54 runs), genpass 20260703-081801 (30 runs plus
distillations), coverage-20260703-084650 (no model calls). All detached
model runs finished without kills; resume stood ready and unused. 128
tests green throughout. Supply only: no arms ran, per the packet.

Work item 1, the demand table (demand-20260703-071812, headroom read
programmatically from unarmed rule-check records in three committed
reports):

| pair | apply tasks | qwen | llama |
|---|---|---|---|
| boundary/degenerate | merge_ranges, median, flatten_once | HEADROOM (0.00) | HEADROOM (0.00) |
| distinctness/values | range_summary | HEADROOM (0.50, n=24) | HEADROOM (0.67) |
| normalize/delimiters | snake_to_camel, balanced | HEADROOM (0.00) | HEADROOM (0.00) |
| tie_break/direction | most_common_word, longest_word | HEADROOM (0.67) | HEADROOM (0.00) |

All four pairs demanded, both seats. The shopping list was the whole
store.

Work item 2: nine candidates authored, two to three per demanded pair,
every rule_topic on the shopping list by construction, texts disjoint,
all checks reference-verified through the one-blob evidence test.

Work item 3, calibration (gencal 20260703-072720, R_G=3 per seat):

| candidate | pair | qwen | llama |
|---|---|---|---|
| longest_run_char | tie_break/direction | all_pass | mixed KEPT |
| least_frequent_word | tie_break/direction | all_pass | mixed KEPT |
| count_distinct_over | distinctness/values | all_pass | all_pass |
| third_largest_distinct | distinctness/values | all_pass | all_pass |
| mode_count | distinctness/values | all_pass | mixed KEPT |
| clamp | boundary/degenerate | all_pass | all_pass |
| nth_page | boundary/degenerate | all_pass | all_pass |
| split_csvish | normalize/delimiters | all_pass | all_pass |
| depth_max | normalize/delimiters | all_pass | all_pass |

RESISTANT pairs, named not forced: boundary/degenerate and
normalize/delimiters (two candidates each, nothing broke). The kept
pool under the conjunction: max_index, shortest_word (incumbents,
in-pool topic, breakage in three probes), longest_run_char,
least_frequent_word, mode_count. Dropped incumbents, each failing one
half of the conjunction: count_token, title_words,
count_distinct_pairs (orphan topics), sum_of_modes, weighted_mean,
range_step (no breakage). The two-per-class pool law is retired for
topic-coverage-with-breakage, pinned by test.

Work item 4, generation at full gates (genpass 20260703-081801): four
lessons, ZERO screen rejections, every lesson conditional, declarative,
and fully pinned. mode_count went all_pass this pass (mixed in gencal,
sampling), so no values lesson landed. Seat B produced tie lessons for
the first time in the record: the enlarged tie class gave llama a
passing sibling, and both paths fired. Quoted:
1. A, max_index, within-task. Concept: "When the task states to return
   the index of the last occurrence of the maximum value, follow that
   direction." Rule: "If multiple occurrences of the maximum value
   exist, locate the last one and provide its index rather than the
   first." Pins: tie_break, direction, last.
2. A, shortest_word, within-task. Concept: "When the task requires
   handling ties by returning the last occurrence, prioritize ordering
   or iteration that naturally favors the latter." Rule: "If the task
   specifies to return the last word in case of a tie when sorting or
   selecting items, use an operation that processes items in reverse
   order." Pins: tie_break, direction, last. The rule leans procedural
   through the "use an" screen gap, FINDINGS 3.
3. B, longest_run_char, within-task, THE FIRST LLAMA-ORIGIN TIE
   LESSON. Concept: "When multiple consecutive character runs have the
   same length, return the last such run's character." Rule: "When
   several runs tie for longest, follow the direction to return the
   character of the last such run." Pins: tie_break, direction, last.
4. B, max_index, sibling (paired with longest_run_char's pass).
   Concept: "When the task states to return the last occurrence or
   longest run, follow that direction." Rule: "Follow the stated
   direction of returning the last occurrence or longest run when
   applicable." Pins: tie_break, direction, last.
Fixed under tier 1: the genpass gate line hardcoded four classes from
the PACKET-008 pool and printed FAILED against the two-class pool; the
criterion is now computed from the pool, and the run itself is complete
by its artifacts (30 of 30 runs checkpointed, report persisted, both
seats' accounting covering both classes).

Work item 5, the enumeration before and after
(coverage-20260703-084650, confirm.matched, pins alone):
- BEFORE (053623 stores): 5 lessons, 3 of 5 structurally empty, one
  cross-seat cell (llama on longest_word), no reverse-direction cell.
- AFTER (053623 plus 081801): 9 lessons, 3 of 9 empty, and every empty
  is a pre-conjunction lesson: the conjunction-era store is 0 of 4
  empty. Cross-seat cells: llama on longest_word (now four qwen-origin
  tie lessons) and, NEW, qwen on longest_word armed with llama-origin
  lessons. THE REVERSE-DIRECTION CELL EXISTS, twice over
  (B/longest_run_char within-task and B/max_index sibling), on a task
  where the demand table shows qwen headroom (0.67 at n=3, direction
  evidence only).

Findings, sized to a supply pass:
The conjunction filter did what it was built to do: zero orphan
lessons from the new pool against three of five before, and the
reverse-direction cell that no measurement has reached now exists by
construction. It arrived through tie_break rather than the expected
distinctness route, because mode_count declined to break at generation
time after breaking in calibration, which is R_G=3 sampling doing what
small samples do. Supply remains narrow: all four new lessons are
tie/direction/last, qwen breaks on nothing new (FINDINGS 1), and the
two resistant pairs sit exactly over the record's deepest floors
(FINDINGS 2). No treatment claim is made; the reverse-direction
measurement is the next packet's.

NOT done:
- No arms, per the packet. The reverse cell is enumerated, not
  measured.
- Resistant pairs not forced; no third candidate wave authored.
- No screen, pin, or gate loosened anywhere; the one gate change is
  the tier-1 genpass gate-line fix, logged.
