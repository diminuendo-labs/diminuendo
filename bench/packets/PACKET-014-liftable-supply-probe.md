# PACKET-014: Supply probe on the liftable ground (llama, distinctness)

Status: DONE
Owner: any Claude Code session. Read /CLAUDE.md first, then this, whole.

## Goal

The clean reverse-transfer test does not exist yet because its material
does not exist. PACKET-013 established the liftable ground: qwen gains
on range_summary through the production menu (8/12 to 12/12). The
reverse test the thesis needs is a llama-origin lesson delivered to qwen
on that ground, and llama's measured breaks so far are tie-class only.
This probe measures whether llama supplies breaks and contrast pairs in
the distinctness class. A probe measures supply and structure. It makes
no treatment claims and carries no signed treatment readings.

## The probe

Performer llama3.1:8b, evidence execution as the label, v1 production
path, R=6 per task, detached, checkpointed, resume-capable.

Tasks: every distinctness-class task in the v1 pool and every same-class
sibling of range_summary, enumerated from the pool by rule_class, the
enumeration printed in RESULTS before any run. If the pool holds fewer
than two tasks in the class, say so and stop: that is a supply answer,
not a failure.

## Report, pre-registered structure

- Per task: pass/fail at R=6 from evidence, per-check readout persisted.
- Contrast enumeration under the standing engine rules: within-task
  pairs first, sibling pairs second, conjunction filter applied (the
  candidate breaks for the seat AND carries an in-pool topic). Every
  eligible pair listed.
- If at least one eligible pair exists: run genpass at full gates into a
  packet-local store only (PACKET-014-lessons.jsonl), PACKET-010
  precedent, and report every gate outcome, accepts and rejects both.
  Production stores untouched.
- The closing line states plainly whether the reverse-on-liftable-ground
  cell is now reachable: a gated llama-origin distinctness lesson exists
  or does not. Counts only, no treatment claims, no rates.

## Gate

- Full enumeration printed, R=6 per task complete or the shortfall
  stated, checkpointed, report persisted, per-check readouts on disk.
- Genpass outcomes reported if attempted, packet-local store only.
- Tests green, per-path staging, honest RESULTS and FINDINGS.

## Constraints

- Protected surfaces, tier 2: judge protocol v1, firewall, watch gates,
  lesson gates, lessons.jsonl, watchlist.jsonl, canonical documents, all
  production stores.
- No pin changes, no gate changes, no delivery arms, no qwen runs.
- If wall time forces a cut, cut R evenly across tasks, and say so.

## FINDINGS

(none this packet. The one observation worth a line stays tier 3: break
supply in this class is thin for llama, one generation-eligible break in
42 generation-pool runs, and the same task had passed every run of two
earlier R_G=3 passes, so R=6 bought the break that R_G=3 missed twice.
A count, recorded in RESULTS where it belongs.)

## RESULTS

Executed 2026-07-03 by a Claude Code session. Commits: 52abeb2 (harness
and tests) and the closing commit carrying this section and the
packet-local store. Run probe14-20260703-142225 ran detached start to
finish, no kill, resume unused. 154 tests green throughout. A probe:
counts only, no treatment claims, no rates.

The enumeration, printed in the run log before any run, 12 tasks:

| task | pool | topic | gen eligible | topic in apply pool |
|---|---|---|---|---|
| count_unique | generation | values | yes | yes |
| sum_distinct | generation | values | yes | yes |
| count_distinct_pairs | generation | pairs | yes | no |
| sum_of_modes | generation | values | yes | yes |
| count_distinct_over | generation | values | yes | yes |
| third_largest_distinct | generation | values | yes | yes |
| mode_count | generation | values | yes | yes |
| second_largest | apply | values | no | yes |
| dedupe | apply | values | no | yes |
| range_summary | apply | values | no | yes |
| nth_smallest | apply | values | no | yes |
| count_pairs | apply | pairs | no | no |

Apply-pool tasks were probed for supply knowledge and excluded from
generation material by the standing disjointness rule; range_summary is
the apply target itself.

The supply table, R=6 per task, evidence as the label, 72 runs all
checkpointed with per-check readouts on disk:

| task | case | fails/runs | conjunction |
|---|---|---|---|
| count_unique | all_pass | 0/6 | no (no break) |
| sum_distinct | MIXED | 1/6 | YES |
| count_distinct_pairs | mixed | 1/6 | no (orphan topic pairs) |
| sum_of_modes | all_pass | 0/6 | no (no break) |
| count_distinct_over | all_pass | 0/6 | no (no break) |
| third_largest_distinct | all_pass | 0/6 | no (no break) |
| mode_count | all_pass | 0/6 | no (no break) |
| second_largest | all_pass | 0/6 | apply pool, excluded |
| dedupe | all_pass | 0/6 | apply pool, excluded |
| range_summary | mixed | 2/6 | apply pool, excluded |
| nth_smallest | all_pass | 0/6 | apply pool, excluded |
| count_pairs | mixed | 1/6 | apply pool, excluded |

Eligible contrast pairs under the standing engine rules (within-task
first, sibling second, conjunction filter applied, per-class cap two):
exactly one. Within-task on sum_distinct (fail and pass inside its own
six runs, topic values, in the apply pool via range_summary).
count_distinct_pairs broke again and stays filtered on the orphan-topic
half of the conjunction, as designed.

Distillation, full gates, packet-local store only
(PACKET-014-lessons.jsonl, production stores untouched): one attempt,
one commit, zero rejects. Every gate outcome reported: accepts 1,
rejects 0.

The committed lesson, quoted with its pins:
- llama-origin, sum_distinct, within-task. Concept: "When writing a
  function to sum distinct values, ensure that each value is counted
  only once regardless of how many times it repeats in the input
  list." Rule: "When the task states 'distinct values,' ignore
  repetitions and include each value only once in the calculation."
  Pins: rule_class=distinctness, rule_topic=values. Conditional,
  declarative, topic-pinned, and by the pins it matches range_summary,
  the liftable ground, and no other kept apply task.

Supply counts worth carrying: one generation-eligible break in 42
generation-pool runs, all of it on sum_distinct, which had passed every
run of two earlier R_G=3 passes; llama also broke on range_summary
itself (2 of 6, apply target, recorded not mined) and on
count_distinct_pairs (orphan topic, filtered).

THE CLOSING SENTENCE, as the packet requires: a gated llama-origin
distinctness lesson with an in-pool topic now exists, so the reverse
cell on liftable ground IS REACHABLE.

Fixed under tier 1: nothing broke; resume stood ready and unused.

NOT done:
- No treatment arms, no qwen runs, no signed readings, per the packet.
- No pin, gate, or production-store change; the new lesson lives in the
  packet-local store only.
- The reverse-on-liftable-ground measurement itself: the next packet's,
  now unblocked.
