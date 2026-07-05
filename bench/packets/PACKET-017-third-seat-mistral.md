# PACKET-017: Third-seat onboarding, executed (mistral:7b)

Status: DONE
Owner: any Claude Code session. Read /CLAUDE.md first, then this, whole.

## Goal

PACKET-016 promoted the third seat and closed at stage 0 on supply. Brad
pulled the seat on the conductor's recommendation: mistral:7b, a
different family from both existing seats, in the ruled 7 to 9B class,
instruct-capable. This packet executes PACKET-016's stages 1 and 2
verbatim against that named seat. The seat neither teaches nor learns
anywhere in this packet: no production store changes, no chair memory,
all delivered lessons are packet-local byte-copies.

## Stage 0, reduced to a presence check

Run `ollama list` and assert mistral:7b is installed. Print the
confirmation in RESULTS before any run. If it is absent, STOP and report:
the pull is Brad's surface, not a session's.

## Stage 1: baseline probe (counts only)

mistral:7b performs every task in both v1 pools at R=6, evidence
execution as the label, detached, checkpointed, per-check readouts
persisted. A probe: counts, no treatment claims, no rates.

Report: the full pass/fail table by task, the headroom map (every task
with at least one fail), and the break-supply view (generation-pool
fails carrying an in-pool topic, eligible contrast pairs enumerated
under the standing conjunction filter). No distillation in this packet.

## Stage 2: first tool-response reading (conditional, signed)

Run stage 2 only if stage 1 shows headroom on range_summary (at least
one fail in its six baseline runs). If it shows none, say so, skip stage
2, and close: the trait probe needs different ground and that is the
conductor's next cut.

Two cells, interleaved per rep, R=12 each, task range_summary, audience
llama3.1:8b (mistral is neither existing family, stated for the record):
- none: no tools.
- armed: the PACKET-014 llama-origin lesson, byte-copied packet-local
  from PACKET-014-lessons.jsonl, byte-check asserted.

Drift bar: 2 of 12, the recorded range_summary movement. One signed
reading, three exits, exclusive:
- GAIN: armed rule check above none by more than the bar. The seat's
  first trait evidence points filter-or-better, and the reverse lesson
  has its second receiving seat.
- HARM: armed rule check below none by more than the bar. Said loudly,
  it outranks everything else in the writeup: a matched pinned tool
  harmed a new seat, amplifier-doctrine evidence on a second seat.
- FLAT: the gap sits at or under the bar. Inside recorded drift, claims
  nothing, the trait stays unmeasured.
Harm columns: all four non-rule checks both cells, every decline
reported, above-bar declines said loudly, at-or-under-bar declines
inside drift.

## Gate

- Stage 0 confirmation printed before any run. Stage 1 complete at R=6
  across both pools or the shortfall stated. Stage 2 run or its skip
  justified from stage 1 counts. Checkpointed, reports persisted, tool
  audit from rows where armed cells exist, byte-check asserted.
- The signed reading applied verbatim with its sign and the bar.
- Tests green, per-path staging, honest RESULTS and FINDINGS.

## Constraints

- Protected surfaces, tier 2: judge protocol v1, firewall, watch gates,
  lesson gates, lessons.jsonl, watchlist.jsonl, canonical documents, all
  production stores.
- No distillation, no chair memory, no pin changes, no gate changes.
- The delivered lesson rides byte-verbatim; any edit voids the cell.
- If wall time forces a cut, finish stage 1 before starting stage 2, and
  cut stage 2's R evenly if it is the stage that must shrink. Say so.

## FINDINGS

Tier 2, flagged and not fixed:

1. THE RESISTANT PAIRS ARE MINABLE THROUGH THE THIRD SEAT. Mistral
   breaks with a passing partner in boundary/degenerate (chunk 1/6,
   weighted_mean 1/6, both mixed) and normalize/delimiters
   (split_csvish 2/6 mixed, depth_max 6/6 all_fail beside passing
   class siblings), the two pairs that resisted every candidate wave
   on both existing seats and that sit over the apply pool's deepest
   unarmed floors. The seat did not teach in this packet, per the
   ruling; whether and when it may teach is the conductor's call, and
   the supply is now on the record waiting for it.
2. The stage 2 headroom condition admitted the wrong kind of ground.
   The condition was at least one fail in six, and range_summary gave
   six of six: an absolute floor, so the armed cell had nothing to
   move and the rule check read 0 of 12 against 0 of 12. A trait probe
   on a new seat wants partial competence, mixed ground, not mere
   failure. Stage 1's mixed tasks are the shopping list (median 1/6,
   nth_smallest 1/6, second_largest 2/6 among the kept-pool-adjacent
   candidates). What I would do: the next trait cut conditions on
   mixed, not on any-fail. Condition design, the conductor's call.
3. The harm-column disturbance at floor is trait-adjacent evidence
   worth a designed measurement: under a matched pinned tool the new
   seat's boundary behavior moved in both directions at once (the
   empty-input check fell 12/12 to 6/12, the single-number check rose
   2/12 to 6/12) while every content check sat at 0. A tool it could
   not use still changed what it did. That is neither the filter nor
   the amplifier signature as recorded; it is a third shape, measured
   once, at floor, and it should be measured on mixed ground before
   anyone names it.

## RESULTS

Executed 2026-07-03 by a Claude Code session. Commits: bd33d55 (harness,
byte-checked material, Brad's pull log committed as a run record) and
the closing commit carrying this section. Run onboard17-20260703-161320
ran detached start to finish, no kill, resume unused. 166 tests green
throughout. The seat neither taught nor learned: no distillation, no
chair memory, no production store changes.

STAGE 0, printed before any run: mistral:7b installed (4.4 GB, pulled
by Brad), confirmed from ollama list. Audience llama3.1:8b, stated for
the record: mistral is neither existing family. Armed-lesson byte check
asserted: the packet-local copy is byte-identical to
PACKET-014-lessons.jsonl.

STAGE 1, the baseline probe: 40 tasks, both v1 candidate pools, R=6,
240 runs, evidence as the label, all checkpointed with per-check
readouts. Counts only. The full table:

Generation pool: max_index all_fail 6/6; shortest_word mixed 4/6;
count_unique all_pass; sum_distinct all_pass; average mixed 1/6; chunk
mixed 1/6; count_word all_pass; equal_ignoring_spaces mixed 2/6;
count_distinct_pairs mixed 4/6; sum_of_modes mixed 5/6; weighted_mean
mixed 1/6; range_step mixed 1/6; title_words mixed 1/6; count_token
all_fail 6/6; longest_run_char mixed 5/6; least_frequent_word mixed
5/6; count_distinct_over all_pass; third_largest_distinct mixed 2/6;
mode_count mixed 1/6; clamp all_pass; nth_page mixed 5/6; split_csvish
mixed 2/6; depth_max all_fail 6/6.

Apply pool: second_largest mixed 2/6; most_common_word all_fail 6/6;
top_k all_fail 6/6; dedupe mixed 5/6; mode mixed 5/6; merge_ranges
all_fail 6/6; longest_word mixed 5/6; median mixed 1/6; range_summary
all_fail 6/6; flatten_once all_fail 6/6; snake_to_camel all_fail 6/6;
nth_smallest mixed 1/6; is_rotation all_fail 6/6; truncate_words
all_pass; balanced all_pass; interleave all_fail 6/6; count_pairs
mixed 3/6.

Headroom map: 33 of 40 tasks carry at least one fail [corrected at
conductor review: the session wrote 30, its own verified table counts
33, seven all_pass tasks], the broadest
headroom of any seat on the record. Break-supply view: 12
generation-pool tasks are conjunction-eligible (break for the seat AND
carry an in-pool topic), and the standing engine rules enumerate EIGHT
eligible contrast pairs spanning ALL FOUR classes, two per class at
the cap: tie_break within-task on shortest_word and longest_run_char;
distinctness within-task on sum_of_modes and third_largest_distinct;
boundary within-task on chunk and weighted_mean; normalize within-task
on split_csvish and sibling on depth_max paired with count_word. The
boundary and normalize pairs are the record's two resistant pairs,
broken for the first time by any seat (FINDINGS 1). No distillation
ran: enumeration only, per the packet.

STAGE 2, run because stage 1 showed range_summary headroom (6 of 6
fails satisfies the packet's at-least-one condition; FINDINGS 2 names
what that admitted). Two cells interleaved per rep, none then armed,
R=12 each, 24 runs, tool audit clean from the rows (armed tools=1,
none tools=0, every row). Drift bar 2 of 12 as stated.

| check | none | armed |
|---|---|---|
| [3, 1, 2, 2] RULE | 0.00 (0/12) | 0.00 (0/12) |
| [1, 2, 3, 5] (harm) | 0.00 | 0.00 |
| [5, 3, 1] (harm) | 0.00 | 0.00 |
| [] (harm) | 1.00 (12/12) | 0.50 (6/12) |
| [7] (harm) | 0.17 (2/12) | 0.50 (6/12) |

The signed three-exit reading, applied verbatim: FLAT. The rule-check
gap is zero, at or under the bar, inside recorded drift, claims
nothing, and the casting trait stays unmeasured. Not GAIN, not HARM by
the reading's own definition, which lives on the rule check.

Harm columns, every decline reported: the empty-input check DECLINED
ABOVE THE BAR under the matched pinned tool, 12 of 12 to 6 of 12, said
loudly as the packet demands. The single-number check rose above the
bar in the same cell, 2 of 12 to 6 of 12. The two content-adjacent
checks sat at zero in both cells. A tool the seat could not use on
this ground still moved its boundary behavior in both directions
(FINDINGS 3). One task, one seat, n=12, direction never a rate.

Findings, sized to what an onboarding can claim:
The third seat is onboarded to the letter of the ruling: baselined
across both pools and tool-response-probed, teaching and learning
nothing. What the baseline shows is a seat unlike either incumbent:
broad headroom including tasks both existing seats ace, break supply
in all four classes including the two the record calls resistant, and
a first tool response that is neither the filter's indifference nor
the amplifier's obedience but a boundary-behavior disturbance at
content floor. The trait needs its measurement on mixed ground before
it gets a name, and the resistant-pair supply waits on a teaching
ruling. Counts and one flat signed reading: that is the whole claim.

Fixed under tier 1: nothing broke; resume stood ready and unused.

NOT done:
- No distillation, no chair memory, no store changes: the seat neither
  taught nor learned, per the packet and the ruling.
- The trait measurement on mixed ground and any teaching decision
  (FINDINGS 2 and 1, the conductor's calls).
