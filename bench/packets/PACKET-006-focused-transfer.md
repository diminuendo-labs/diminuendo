# PACKET-006: Focused transfer arms

Status: DONE
Owner: any Claude Code session. Read /CLAUDE.md first, then this, whole.

## Goal

The first treatment measurement at an n that can carry a claim. PACKET-005
produced five conditionally phrased lessons across three classes and proved
the probe format cannot fund check-level claims at R=3 (FINDINGS 3, adopted
as doctrine). This packet measures those lessons in the PACKET-004
focused-arm format, R=12, on class-matched apply tasks where the performer
has measured rule-check headroom. Two pre-registered questions in one run:
do topic-matched lessons transfer across seats, and do topic-mismatched
lessons of the same class do anything (prediction: no effect, no harm, the
menu safety property).

## Materials, all on disk

The five committed lessons from probe 20260702-215407, copied into a
packet-local store exactly as PACKET-004 did. No new lesson generation in
this packet. Apply tasks and their rule checks from probe_tasks.py as is.

## The pairings (performer, apply tasks, lesson store)

Label each pairing topic_matched true or false in the harness and report.

1. llama, longest_word, store A (tie_break lesson, stated_direction=last).
   topic_matched=true. This is PACKET-004's comparison in the same format,
   the replication.
2. qwen, range_summary, store B (distinctness lesson). topic_matched=true.
   Cross-model in the direction never yet treated: llama teaching qwen,
   on a task where qwen's baseline has headroom.
3. qwen, snake_to_camel, store B (normalize lessons: punctuation,
   uppercase). topic_matched=false: the class matches, the normalized
   thing does not (underscores and casing versus punctuation stripping).
   FINDINGS 2's evidence cell.
4. llama, snake_to_camel and balanced, store A (normalize lesson:
   punctuation stripping). topic_matched=false for both tasks.

## Arms and size

Two arms per pairing: none (bare production context) and menu (the store's
lessons through the production menu path, tools count recorded and
asserted nonzero on every armed run of a class-matched task). R=12 per arm
per task. 120 runs total. Detached, checkpointed, resume-capable.

## Report and the pre-registered reading

Per-check pass rates per arm per pairing, rule checks marked, n stated.
Also the harm column: non-rule checks, armed versus none, per pairing.
Reading rules, apply verbatim in RESULTS:
- A topic-matched pairing shows transfer only if every rule check in the
  pairing moves the same direction armed versus none AND the pooled
  rule-check passes differ. Otherwise report the deltas and call it inside
  noise.
- Topic-mismatched pairings are read against the prediction: no effect on
  rule checks, no harm on any check. A harm signal here outranks
  everything else in importance, say so loudly if it appears.
- Cross-run reference: where a check overlaps PACKET-004 or PACKET-005,
  put the prior rates beside the new ones.

## Gate

- All four pairings at R=12 per arm, every run checkpointed, report
  persisted with per-check tables and the harm column.
- Tool delivery asserted from the rows (armed runs of matched-class tasks
  carry nonzero tools; the tie lesson never rides a direction-mismatched
  task).
- The reading rules applied verbatim. Tests green, commits, honest RESULTS
  and FINDINGS.

## Constraints

- Protected surfaces, tier 2: judge protocol v1, firewall, lesson and
  watch gates, lessons.jsonl, watchlist.jsonl, canonical documents.
- No lesson generation, no lesson editing. The stores ride verbatim.
- If wall time forces a cut, cut R evenly across arms within a pairing,
  never drop a pairing, and say so.

## FINDINGS

Tier 2, flagged and not fixed:

1. THE MENU SAFETY PROPERTY IS PER-PERFORMER, NOT GLOBAL. Said loudly
   because the packet says harm outranks everything: pairing 2, the
   topic-matched llama-teaches-qwen cell, declined under menu delivery
   across the task's whole content side (rule check 9/12 to 3/12,
   neighbors 7/12 to 4/12 and 7/12 to 5/12, boundary checks untouched,
   n=12 per cell). PACKET-004 measured "menu never hurt" on llama only,
   and PACKET-006 reconfirms it on llama (pairing 4 flat), but qwen
   treats a menu tool with more obedience than judgment on this
   evidence. Why it matters: the spec's shape-the-landscape principle
   was verified on one seat and assumed for the other. What I would do:
   a PACKET-004-format delivery test on qwen with matched and
   contradicting lessons before any reliance on menu safety for the
   code seat.
2. The recipe-shaped rule is the proximate suspect in that harm. The
   lesson that rode pairing 2 is the one whose rule field drifted into
   implementation advice ("convert potential pairs to tuples and sort
   them before adding to a set"), written against count_distinct_pairs
   and surfaced onto range_summary, where sets and pair-tuples are the
   wrong shapes. The gates screen for topic overlap, platitudes, and
   metric terms; nothing screens for imperative recipe shape, and
   PACKET-005's RESULTS noted the drift without a mechanism to stop
   it. What I would do: a shape screen or a distiller instruction
   keeping the rule field declarative (what the task states, never
   what code to write). A lesson-gate change, a raised hand.

## RESULTS

Executed 2026-07-03 by a Claude Code session. Commits: 7d6d856 (harness
and tests) and the closing commit carrying this section. Run
20260703-014859 ran detached start to finish, no kill, resume unused.
105 tests green throughout.

What ran:
- The five PACKET-005 lessons copied verbatim into packet-local stores
  (A=2, B=3, byte-identical to the probe stores), size-checked and
  gate-checked by the harness loader. No lesson generation, no editing.
- transfer.py: four pairings as specified, two arms each, R=12 per arm
  per task, 120 runs, all checkpointed, report persisted with per-check
  tables, pooled rule-check counts, and the tool audit.
- Tool delivery, verified from the rows (gate): every armed run carried
  tools (min 1). The audit shows the tie lesson rode only longest_word,
  the distinctness lesson only range_summary, the normalize lessons
  only snake_to_camel and balanced. No lesson rode outside its class,
  and the direction-pinned lesson never met a contradicting task.

Per-check pass rates (none / menu, n=12 per cell unless shown; rule
checks marked; prior rates for overlapping checks in brackets):

Pairing 1, llama + longest_word + store A tie lesson, topic_matched
true. THE REPLICATION.
| check | none | menu | prior |
|---|---|---|---|
| 'cat door bird' RULE | 0.08 | 0.50 | [P4: 0.00 to 0.25 at n=12; P5 probe: 0.00 to 0.33 at n=3] |
| 'a bb cc d' RULE | 0.08 | 0.50 | [P4: 0.00 to 0.33 at n=12; P5 probe: 0.00 to 0.33 at n=3] |
| '' | 1.00 | 0.92 | |
| 'one' | 1.00 | 1.00 | |
Pooled rule checks: none 2/24, menu 12/24.

Pairing 2, qwen + range_summary + store B distinctness lesson,
topic_matched true. Llama teaching qwen, first treated measurement.
| check | none | menu | prior |
|---|---|---|---|
| [3, 1, 2, 2] RULE | 0.75 | 0.25 | [P5 probe: A|none 1.00, A|B armed 1.00, both n=3] |
| [1, 2, 3, 5] | 0.58 | 0.33 | |
| [5, 3, 1] | 0.58 | 0.42 | |
| [] | 1.00 | 1.00 | |
| [7] | 1.00 | 1.00 | |
Pooled rule checks: none 9/12, menu 3/12.

Pairing 3, qwen + snake_to_camel + store B normalize lessons,
topic_matched false. One armed run returned no parseable evidence, so
its cells are n=11.
| check | none | menu | prior |
|---|---|---|---|
| '__a__b_' RULE | 0.00 | 0.18 (2/11) | [P5 probe: A|none 0.00, A|B armed 0.00, n=3] |
| 'foo_bar_baz' | 0.00 | 0.18 (2/11) | |
| 'word' | 0.00 | 0.18 (2/11) | |
| '' | 1.00 | 0.91 (10/11) | |

Pairing 4, llama + snake_to_camel and balanced + store A normalize
lesson, topic_matched false.
| check | none | menu |
|---|---|---|
| snake '__a__b_' RULE | 0.00 | 0.00 |
| snake 'foo_bar_baz' | 0.00 | 0.00 |
| snake 'word' | 0.00 | 0.00 |
| snake '' | 1.00 | 1.00 |
| balanced '(a(b)c)' RULE | 1.00 | 1.00 |
| balanced ')(' RULE | 0.50 | 0.42 |
| balanced '' | 1.00 | 1.00 |
| balanced '((x)' | 1.00 | 0.92 |
Pooled rule checks: none 18/36, menu 17/36.

The reading rules, applied verbatim:
- Pairing 1 (matched): every rule check moved the same direction armed
  versus none (both up, +0.42 each), and the pooled rule-check passes
  differ (2/24 against 12/24). By the pre-registered criterion this
  pairing SHOWS TRANSFER. It is the third measurement of this
  comparison and the third in the same direction (0.25/0.33 at n=12,
  0.33 at n=3, now 0.50/0.50 at n=12). The harm column is clean (one
  boundary run of twelve dipped). A qwen-taught, conditionally phrased,
  direction-pinned lesson moved llama's rule-check performance through
  the production menu path.
- Pairing 2 (matched): the criterion's letter is also met: the single
  rule check moved in one direction and the pooled passes differ (9/12
  against 3/12). The direction is DOWN. The pre-registration did not
  sign the criterion, so no transfer is claimed; what the numbers show
  is an armed decline across the task's content checks on a matched
  pairing, and the honest name for that is harm. Flagged loudly in
  FINDINGS 1, with FINDINGS 2 naming the recipe-shaped rule as the
  proximate suspect.
- Pairing 3 (mismatched, prediction no effect and no harm): the
  prediction does not cleanly hold. All three content checks moved 0/12
  to 2/11 armed, a small effect in the helpful direction where none was
  predicted; no harm signal (the one dip is a single unparseable-output
  run). At 2 of 11 this is direction, not a rate.
- Pairing 4 (mismatched, prediction no effect and no harm): the
  prediction holds. Every delta is at most one run of twelve, pooled
  18/36 against 17/36. Menu safety on llama, reconfirmed.

Findings, sized to the n:
The bench has its first pre-registered transfer PASS, and its first
menu-harm measurement, in the same run, split by performer. The
matched lesson helped the seat that judges its tools (llama, pairing 1)
and hurt the seat that appears to obey them (qwen, pairing 2), while
the mismatched pairings stayed near-flat both ways. The one lesson
whose rule field drifted into a recipe is exactly the one that hurt,
carried onto a task whose right implementation shares nothing with the
recipe. At n=12 per cell these are the strongest and most repeatable
separations the bench has produced: the pairing 1 effect has now
survived three independent measurements, and the pairing 2 harm is a
six-of-twelve to three-of-twelve reversal of a strong baseline. Both
questions the packet pre-registered are answered: topic-matched
lessons transfer across seats in at least one direction, and the menu
safety property is a per-performer fact, not a system property.

Fixed under tier 1: nothing broke; resume stood ready and unused.

NOT done:
- Nothing cut: all four pairings at R=12, both arms, 120 of 120 runs.
- Protected surfaces untouched. No lesson generated or edited.
- Not attempted: the qwen delivery test and the rule shape screen
  (FINDINGS 1 and 2, the conductor's calls).
