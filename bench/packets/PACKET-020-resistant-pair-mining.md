# PACKET-020: Mining the resistant pairs (mistral teaches)

Status: DONE
Owner: any Claude Code session. Read /CLAUDE.md first, then this, whole.

## Goal

The teaching gate is open for mistral:7b (DECISIONS 2026-07-03:
baselined, tool-response-probed with a valid qualified cell, ruling
filed). This packet is the seat's first teaching work: distillation from
the PACKET-017 baseline record, where the seat broke with passing
partners on all four classes, including boundary/degenerate and
normalize/delimiters, the two pairs no other seat has ever supplied. The
prize is the record's first gated lessons in those two classes. No new
model runs are required for supply: the breaks, passes, per-check
readouts, and traces live in the PACKET-017 run record on disk.

## The work

Input: the eight eligible contrast pairs enumerated in PACKET-017
RESULTS, verbatim, two per class at the cap:
- tie_break within-task: shortest_word, longest_run_char
- distinctness within-task: sum_of_modes, third_largest_distinct
- boundary within-task: chunk, weighted_mean
- normalize within-task: split_csvish; sibling: depth_max with
  count_word

Run genpass at FULL gates over all eight, in class order as listed,
from the PACKET-017 run artifacts (runs/onboard17-20260703-161320.*).
Output to a packet-local store only: PACKET-020-lessons.jsonl.
Production stores untouched; admission is a separate conductor-and-Brad
ruling, not this packet's.

Report every gate outcome, accepts and rejects both, per pair, with the
failing screen named on every reject. A reject is a result, not a
failure of the packet.

## Report, pre-registered structure (a supply packet: counts, no
treatment claims)

- Per pair: attempted, gate outcome, and for accepts the lesson quoted
  in full with its pins.
- The closing counts: attempts, accepts, rejects by screen, and the
  class coverage of the resulting store (which of the four classes now
  hold at least one gated mistral-origin lesson).
- The closing sentence states plainly whether the record now holds its
  first gated boundary-class and normalize-class lessons.

## Gate

- All eight pairs attempted in order, every outcome reported, the store
  persisted packet-local, no production store touched.
- Tests green, per-path staging, honest RESULTS and FINDINGS.

## Constraints

- Protected surfaces, tier 2: judge protocol v1, firewall, watch gates,
  lesson gates, lessons.jsonl, watchlist.jsonl, canonical documents, all
  production stores.
- No gate changes, no pin changes, no delivery arms, no new model runs
  for supply (distillation calls themselves are permitted as the engine
  makes them).
- If a pair's artifacts prove insufficient for distillation, report it
  as such per pair and continue; do not re-run the seat to manufacture
  supply.

## FINDINGS

Two quality observations for the admission ruling, flagged and not
acted on, because admission is not this packet's:
1. The weighted_mean lesson wildcarded its topic (applies_when
   rule_topic "*", the generator's right under the prompt rules for
   genuinely general content), so by its pins it rides every boundary
   task, empty and degenerate alike. Whether a wildcard from a
   single-task contrast deserves that reach is an admission question.
2. The depth_max sibling lesson carries a trace of its pass-partner's
   topic: its rule says "e.g., case normalization", count_word's
   subject, on a delimiters-pinned lesson. It cleared every screen
   (the aim ground shares the class vocabulary by design). The
   PACKET-011 residue mechanism, cross-topic this time, mild, one
   lesson of eight, recorded for the admission read.

## RESULTS

Executed 2026-07-03 by a Claude Code session. Commits: b67a0a5 (harness
and tests) and the closing commit carrying this section and the
packet-local store. Run mine20-20260703-211439 ran detached start to
finish, no kill, resume unused. 184 tests green throughout. A supply
packet: counts, no treatment claims, no delivery arms, and no new model
runs for supply: every failing and passing run came from the
onboard17-20260703-161320 stage 1 artifacts on disk (240 rows), with
only the engine's own distillation calls made.

Per pair, in class order, every gate outcome (rejects would name their
screen; there were none):

| pair | type | outcome |
|---|---|---|
| tie_break shortest_word | within-task | COMMITTED, first attempt |
| tie_break longest_run_char | within-task | COMMITTED, first attempt |
| distinctness sum_of_modes | within-task | COMMITTED, first attempt |
| distinctness third_largest_distinct | within-task | COMMITTED, first attempt |
| boundary chunk | within-task | COMMITTED, first attempt |
| boundary weighted_mean | within-task | COMMITTED, first attempt |
| normalize split_csvish | within-task | COMMITTED, first attempt |
| normalize depth_max + count_word | sibling | COMMITTED, first attempt |

The eight committed lessons, quoted in full, all provenance engine,
all origin_seat mistral:7b in the trail:
1. shortest_word (tie_break, direction, last). Concept: "When handling
   ties in the task, always return the last word with the shortest
   length." Rule: "If multiple words have the same shortest length,
   the function should return the last such word encountered."
2. longest_run_char (tie_break, direction, last). Concept: "When
   multiple runs have the same length, choose the character of the
   last such run." Rule: "When several consecutive runs of a single
   character tie for longest, return the character that appears in
   the string last."
3. sum_of_modes (distinctness, values). Concept: "When calculating the
   sum of modes, only distinct values should be considered, each
   counted once." Rule: "When the task states that the function should
   return the sum of the distinct most frequent values in the list,
   ensure that each mode is counted only once regardless of its
   frequency."
4. third_largest_distinct (distinctness, values). Concept: "When the
   task states to find a distinct value, consider each unique element
   separately without repetition." Rule: "when the task specifies
   'distinct' values, ensure that all returned elements are unique and
   not repeated in the output."
5. chunk (boundary, degenerate). Concept: "Handle empty and None
   inputs by returning an empty list." Rule: "When the input list is
   empty or None, return an empty list instead of attempting to
   process it."
6. weighted_mean (boundary, rule_topic wildcarded to "*", FINDINGS 1).
   Concept: "Handle cases where the input lists are empty or the total
   weight is zero by returning None." Rule: "When the task states that
   the function should return None for empty lists or a zero total
   weight, follow this direction."
7. split_csvish (normalize, delimiters). Concept: "When writing a
   function to split and normalize a string, ensure that leading and
   trailing whitespace is removed from each field and empty fields are
   discarded." Rule: "Follow the direction the task states by trimming
   whitespace around each field and dropping fields that are empty
   after trimming."
8. depth_max, sibling with count_word (normalize, delimiters,
   FINDINGS 2). Concept: "Normalize delimiters before processing."
   Rule: "When the task states to normalize delimiters, ensure all
   relevant characters are standardized according to the specified
   rules (e.g., case normalization) before proceeding with the
   comparison or counting operation."

Closing counts: 8 attempts, 8 accepts, 0 rejects (no screen fired).
Store class coverage: boundary, distinctness, normalize, tie_break,
all four. The store is packet-local (PACKET-020-lessons.jsonl);
production stores untouched; admission is the separate ruling.

THE CLOSING SENTENCE: the record now holds its first gated
boundary-class lesson and its first gated normalize-class lesson, YES
on both.

Fixed under tier 1: nothing broke; resume stood ready and unused.

NOT done:
- No delivery arms, no treatment claims, no new supply runs, per the
  packet.
- No production-store admission (the separate conductor-and-Brad
  ruling), and the two FINDINGS observations feed that read.
- The reverse replication stays queued where the record put it.
