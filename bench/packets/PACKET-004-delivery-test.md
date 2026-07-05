# PACKET-004: The delivery test (friction theater, measured)

Status: DONE
Owner: any Claude Code session. Read /CLAUDE.md first, then this, whole.

## Goal

Answer the concept spec's own open question before any more supply work:
does a lesson delivered as a menu tool change the performer's output, or is
it merely accepted? Three probes have produced no surviving transfer signal,
and every null has been attributed to an instrument cause. This packet tests
the alternative hypothesis directly, with the decision logic pre-registered
below so the result cannot be argued with after the fact.

## Materials, all already on disk

- Lessons: the two correctly aimed tie_break lessons from probe
  20260702-083121 (seat A max_index, seat B max_index). The misaimed lesson
  (seat A shortest_word, rule field carrying the empty-string sentence) is
  EXCLUDED, and RESULTS says so. Copy the two into a packet-local store
  file; do not touch the probe stores or lessons.jsonl.
- Tasks: every apply task in probe_tasks.APPLY_TASKS whose rule_class is
  tie_break, selected by field, not by name.
- Performer: llama3.1:8b only (it has headroom; qwen sits near ceiling on
  this class). Audience: qwen, v1, production path, unchanged.

## The three arms

1. none: the bare performer context, exactly as production.
2. menu: the two lessons delivered as landscape tools through the existing
   menu path, exactly as production. Verify tools reached the prompt.
3. directive: the same two lessons delivered as an explicit instruction
   block in the performer prompt ("APPLY THESE RULES:", then the concept
   and rule text verbatim). Implement as an optional directives parameter
   on the performer prompt in runner.py (terrain, not protected). Directive
   text passes guard_no_metric like everything performer-bound.

Identical tasks, identical criteria, identical audience, only the delivery
varies. R=12 per arm per task. Run detached, read from disk, resume-capable
if the environment kills it.

## Measurement, two levels

- ev_fraction per arm, the coarse level.
- THE SHARP LEVEL: per-check flip rates. For each evidence check on each
  task, the pass rate per arm, reported as a table. The checks that encode
  the tie rule are the treatment target; the packet's question lives there.

## Pre-registered decision logic (apply it verbatim in RESULTS)

- directive is indistinguishable from none on the tie-rule checks:
  capability floor at this model scale. The models cannot use the rule even
  when told directly. Supply work pauses; escalate to the conductor.
- directive beats none, menu does not: friction theater confirmed. The
  delivery is the defect; menu salience and wording become the next packet.
- menu and directive both beat none: the mechanism works. Failure-supply
  calibration (PACKET-003 FINDINGS 3, approved) proceeds with confidence.
- Anything ambiguous: report the table and say ambiguous. Do not force a
  bucket.

## Gate

- Three arms at R=12 per task, every run checkpointed, report persisted
  with the per-check table.
- The misaimed lesson excluded, stated in RESULTS.
- Arm 2 verified to have delivered tools into the prompt (watches_used
  analog: record tools count per run and assert nonzero in arm 2).
- The decision logic applied verbatim. Tests green, commits, honest RESULTS
  and FINDINGS.

## Constraints

- Protected surfaces, tier 2: judge protocol v1, firewall, lesson and watch
  gates, lessons.jsonl, watchlist.jsonl, canonical documents.
- No changes to lesson content. The directive arm delivers the committed
  text verbatim.
- If wall time forces a cut, cut R evenly across arms, never drop an arm.

## FINDINGS

Tier 2, flagged and not fixed. Both findings read the same event, and
both are post-hoc: the pre-registration did not anticipate a lesson
whose rule direction contradicts a task's stated rule.

1. Verbatim rule injection transfers the rule's direction even where it
   is wrong, and the damage spreads. The two lessons say "return the
   last occurrence." On most_common_word, whose stated tie rule is
   alphabetical, the directive arm cratered the tie check (0.33 to
   0.09) and dragged the task's non-tie checks down with it (0.92 to
   0.36, 0.67 to 0.36): the performer contorted whole functions around
   the injected rule. The menu arm, whose framing is "choose what
   fits," lifted the same check (0.33 to 0.75). Delivery that preserves
   the performer's judgment behaved better than delivery that commands,
   on every check measured. Why it matters: the spec's menu design is
   supported against the stronger-delivery alternative, and the risk in
   lesson content is direction-specific wording. What I would do:
   nothing to the menu; fix the wording at the source (finding 2).
2. The lesson wording is task-shaped because within-task contrast made
   it. Both lessons came from max_index, so their text says "index of
   its last occurrence," a task-level rule, not "honor the task's
   stated tie direction," the class-level rule PACKET-003's sibling
   path was designed to elicit. Within-task contrast, the cleaner
   comparison for attribution, produces the narrower wording, and this
   packet shows the narrow wording is what misfires when commanded and
   what a performer must override when it contradicts the task. What I
   would do: when a class-level lesson is wanted, prefer sibling
   phrasing even when within-task contrast exists, or add a distiller
   instruction to state the rule at the class level. Architecture-level
   design either way, the conductor's call.

## RESULTS

Executed 2026-07-02 by a Claude Code session. Commits: 846d89f (harness,
runner directive path, materials, tests) and the closing commit carrying
this section. Run 20260702-171528 ran detached start to finish, no kill;
resume stood ready and unused. 88 tests green.

What ran:
- Materials: the two aimed tie_break lessons from probe 20260702-083121,
  copied by trail-field selection into packets/PACKET-004-lessons.jsonl.
  The misaimed lesson (seat A shortest_word) is EXCLUDED, and the
  harness loader refuses any store containing it, by test.
- runner.run_once gained an optional directives parameter: an APPLY
  THESE RULES block in the performer prompt, performer-bound, passed
  through guard_no_metric. Prompt block pinned by test.
- delivery.py: three arms, identical tasks (the two tie_break apply
  tasks, selected by field), identical criteria, identical qwen v1
  audience, performer llama only. R=12 per arm per task, 72 runs, all
  checkpointed, report persisted with the per-check table. GATE passed.
- Tools verification (gate): the menu arm delivered both lessons on
  every run, min tools 2 of 2. The none and directive arms carried zero
  tools by construction.
- One directive run on most_common_word returned no parseable evidence
  results, so its three check cells are n=11; its coarse ev counted as
  zero. Every other cell is n=12.

Arms, coarse level (ev_mean, n=24 per arm):

| arm | overall | most_common_word | longest_word |
|---|---|---|---|
| none | 0.53 | 0.64 | 0.42 |
| menu | 0.70 | 0.83 | 0.56 |
| directive | 0.40 | 0.25 | 0.54 |

Per-check pass rates, the sharp level (n in parentheses):

| check | tie rule | none | menu | directive |
|---|---|---|---|---|
| most_common_word('b a b a c') | yes | 0.33 (12) | 0.75 (12) | 0.09 (11) |
| most_common_word('z z y') | no | 0.92 (12) | 0.92 (12) | 0.36 (11) |
| most_common_word('') | no | 0.67 (12) | 0.83 (12) | 0.36 (11) |
| longest_word('cat door bird') | yes | 0.00 (12) | 0.25 (12) | 0.42 (12) |
| longest_word('a bb cc d') | yes | 0.00 (12) | 0.33 (12) | 0.42 (12) |
| longest_word('') | no | 0.67 (12) | 0.67 (12) | 0.42 (12) |
| longest_word('one') | no | 1.00 (12) | 1.00 (12) | 0.92 (12) |

The pre-registered decision logic, applied verbatim:
- "directive is indistinguishable from none on the tie-rule checks":
  does not hold. Directive moved both directions, up on the two
  longest_word tie checks (0.00 to 0.42 twice), far down on the
  most_common_word tie check (0.33 to 0.09).
- "directive beats none, menu does not": does not hold. Menu beat none
  on all three tie-rule checks (0.33 to 0.75, 0.00 to 0.25, 0.00 to
  0.33).
- "menu and directive both beat none": does not hold across the
  tie-rule checks as a set. Both beat none on the two longest_word
  checks; on the most_common_word check menu beat none and directive
  fell below it.
- Therefore: AMBIGUOUS. The table is reported and no bucket is forced.

Post-hoc observation, labeled as such and sized to its n: the ambiguity
splits exactly on whether the lesson's rule direction matches the
task's stated rule. Both lessons carry max_index's direction, "the last
occurrence." On longest_word, whose stated tie rule is also "the last,"
both deliveries lifted the tie checks off an absolute floor of 0.00.
On most_common_word, whose stated tie rule is alphabetical, the
directive injected the contradicting direction and collapsed the task,
while the menu still helped. Menu never hurt: on all seven checks the
menu rate is greater than or equal to the none rate. At n=11 to 12 per
cell these are directions, not rates, but the 0.00-floor lifts and the
directive collapse are the largest per-check separations this bench has
produced. The two FINDINGS carry what this implies for lesson wording
and delivery design; the buckets were not built for a wrong-direction
lesson, so the verdict stays ambiguous as pre-registered.

Fixed under tier 1: nothing broke this session. Resume was unused.

NOT done:
- Nothing cut. R=12 ran in full on all three arms, no arm dropped.
- Protected surfaces untouched: judge protocol v1, firewall (the
  directive path calls guard_no_metric, it does not modify it), lesson
  and watch gates, lessons.jsonl, watchlist.jsonl, canonical documents.
- Lesson content unchanged: the directive arm delivered the committed
  text verbatim, which is the point of finding 1.
- No re-run with direction-matched or class-phrased lessons was
  attempted; that is the natural next packet and the conductor's call.
