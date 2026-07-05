# PACKET-007: Lesson shape and the obedient seat

Status: DONE
Owner: any Claude Code session. Read /CLAUDE.md first, then this, whole.

## Goal

PACKET-006 measured the first menu harm, on qwen, carried by the one lesson
whose rule field drifted into a procedure. Two approved changes and one
decomposition in a single packet: enforce the spec's own definition (a
lesson is a concept plus conditions, never a procedure) as a gate, and
measure whether qwen's harm is about lesson shape or seat obedience.

## Work item 1: the declarative-shape screen

Add to lesson.validate, never replacing existing gates: the rule field must
be declarative about what the task states, never imperative about what code
to write. Screen: reject rule text containing implementation-imperative
patterns (convert, use a, store in, sort them, add to a, loop, iterate,
call, append to, create a, initialize), crude and documented like the other
screens. The PACKET-006 harm lesson (B, count_distinct_pairs, "convert
potential pairs to tuples and sort them before adding to a set") is the
rejection fixture, pinned by test. The two PACKET-005 tie and title_words
lessons are the pass fixtures. Both distiller prompts gain the matching
instruction: the rule states what the task requires, never how to code it.

## Work item 2: the qwen delivery decomposition (PACKET-004 format)

Performer qwen, audience llama, R=12 per arm per task, detached.

Materials: two hand-authored lesson variants carrying the SAME rule content
in two shapes, provenance "hand", committed to a packet-local store only:
- concept shape: "When the task states each distinct pair counts once
  regardless of repeats, honor the distinctness the task states."
- recipe shape: the PACKET-006 harm lesson's text verbatim.
Plus the same two shapes for a tie rule (concept: PACKET-005 lesson 1
verbatim; recipe: "Use max() with a reversed index scan to return the last
occurrence").

Tasks: range_summary (matched class for the distinctness pair, qwen has
headroom) and most_common_word (its alphabetical tie CONTRADICTS the tie
lessons' last direction; deliver the tie lessons here with the direction
pin stripped in the packet-local copies, labeled as deliberately
mismatched, to measure obedience under contradiction).

Arms per task: none / menu-concept / menu-recipe. Six cells at R=12 plus
the two none baselines: 96 runs.

## Pre-registered reading, apply verbatim

- Recipe harms where concept does not, on either task: the shape is the
  hazard, the screen in work item 1 is the cure, menu safety holds for
  concept-shaped lessons on qwen until contradicted.
- Both shapes harm on the contradicting task: qwen obeys tools regardless
  of shape, per-seat delivery policy becomes a conductor decision
  (candidates: no cross-model lessons for obedient seats, or
  directive-style filtering upstream).
- Neither harms anywhere: PACKET-006's harm does not replicate, say so
  plainly and downgrade it the way PACKET-002's lead was downgraded.
- Mixed or partial: report the table, name it ambiguous, force nothing.

## Gate

- Shape screen rejects the fixture, passes the two pass-fixtures, both
  distiller prompts updated, pinned by tests.
- All arms at R=12, checkpointed, report persisted with per-check tables
  and harm columns, tool delivery audited from rows.
- The reading applied verbatim. Tests green, commits, honest RESULTS and
  FINDINGS.

## Constraints

- Protected surfaces, tier 2: judge protocol v1, firewall, watch gates,
  lessons.jsonl, watchlist.jsonl, canonical documents. The lesson-gate
  change in work item 1 is conductor-approved and in scope.
- The hand-authored variants live only in the packet-local store, provenance
  "hand", and never enter any probe store.
- If wall time forces a cut, cut R evenly, never drop an arm, and say so.

## FINDINGS

Tier 2, flagged and not fixed:

1. THE MENU DELIVERS CONCEPTS ONLY, AND THE SHAPE SCREEN GUARDS A FIELD
   THAT NEVER RIDES. Found while building work item 2, load-bearing for
   reading every delivery result in the record: menu.query returns
   concept plus applies_when, nothing else. The rule field, where work
   item 1's screen now enforces declarative shape, never reaches a
   performer. PACKET-006's harm rode in the recipe lesson's concept
   text, which is itself procedure-tinged ("ensure that pairs are
   stored in a way that disregards order"). Why it matters: the new
   screen improves distillation quality and protects nothing at the
   delivery surface. What I would do: extend the imperative screen to
   the concept field (a further lesson-gate change), or change what the
   menu carries (a spec-level delivery surface change). Either is a
   conductor call; this packet's decomposition worked around it by
   carrying its two shapes in the concept fields, stated in the store's
   own trail notes.
2. Obedience cuts both ways, and policy should weigh the benefit side.
   The same seat that harmed under a contradicting tool posted the
   largest armed lift the bench has measured when the tool was right
   (rule check 0.50 to 0.92, content checks up about 0.45, matched
   concept-shaped lesson). Withholding delivery from obedient seats
   would forfeit that. The production direction pin already prevents
   the exact contradiction measured here (these tie variants rode only
   because the packet stripped their pins to force the contradiction).
   The exposure that remains is contradictions not expressible as
   applicability pins. What I would do: prefer widening applicability
   pinning (the stated_direction move, generalized, the same family as
   the deferred rule_topic key) over per-seat delivery bans. The
   conductor's decision either way, per the pre-registered reading.

## RESULTS

Executed 2026-07-03 by a Claude Code session. Commits: 53578ef (work
item 1), ebe73da (work item 2 build), and the closing commit carrying
this section. Run 20260703-043045 ran detached start to finish, no
kill, resume unused. 116 tests green throughout.

Work item 1, delivered:
- The declarative-shape screen is in lesson.validate: the listed
  implementation imperatives are rejected in the rule field. The
  PACKET-006 harm lesson is the rejection fixture and the PACKET-005
  tie and title_words lessons are the pass fixtures, all pinned by
  test. Both distiller prompts carry the matching instruction ("the
  rule states what the task requires, never how to code it"), pinned
  by a prompt-capture test.
- Honest fallout, logged in DECISIONS: transfer.py's store B now dies
  at the gates because it carries the recipe lesson. The PACKET-006
  record stands; the instrument is superseded, pinned by test.

Work item 2, what ran:
- Four hand-authored variants, provenance hand, packet-local store
  only, structure-checked by the loader, which deliberately does NOT
  run lesson.validate: the recipe variants are gate-violating
  instruments and a test pins that the production gates refuse them.
- The tie variants carry stated_direction "*" (pin stripped) and a
  deliberately_mismatched label, per the packet, so the menu serves
  them against most_common_word's alphabetical rule.
- The shapes ride in the CONCEPT fields because the menu delivers
  concepts (FINDINGS 1); the rule fields carry the same shapes for
  store faithfulness.
- obedience.py: qwen performer, llama audience, v1 production path.
  Three arms per task, none at n=24 and each menu arm at n=12, per the
  packet's 96-run total. 96 of 96 runs, checkpointed, every armed run
  carried exactly one tool, report persisted, harness GATE passed.

Per-check pass rates (none / menu_concept / menu_recipe; none n=24,
menu arms n=12; rule checks marked; PACKET-006 P2 rates beside
range_summary for the replication read):

most_common_word, the contradicting task (tie variants, pins stripped):
| check | none | concept | recipe |
|---|---|---|---|
| 'b a b a c' RULE | 1.00 (24/24) | 0.67 (8/12) | 0.75 (9/12) |
| 'z z y' | 1.00 | 1.00 | 0.75 |
| '' | 1.00 | 1.00 | 0.92 |
Pooled rule checks: none 24/24, concept 8/12, recipe 9/12.

range_summary, the matched task (distinctness variants):
| check | none | concept | recipe | P6 P2 (none / menu-recipe) |
|---|---|---|---|---|
| [3, 1, 2, 2] RULE | 0.50 (12/24) | 0.92 (11/12) | 0.58 (7/12) | 0.75 / 0.25 |
| [1, 2, 3, 5] | 0.38 | 0.83 | 0.50 | 0.58 / 0.33 |
| [5, 3, 1] | 0.42 | 0.83 | 0.50 | 0.58 / 0.42 |
| [] | 1.00 | 1.00 | 1.00 | 1.00 / 1.00 |
| [7] | 1.00 | 1.00 | 1.00 | 1.00 / 1.00 |
Pooled rule checks: none 12/24, concept 11/12, recipe 7/12.

The pre-registered reading, applied verbatim:
- "Recipe harms where concept does not, on either task": does not hold.
  On the contradicting task both shapes harmed. On the matched task the
  recipe did not harm (0.58 armed against 0.50 unarmed).
- "Both shapes harm on the contradicting task": HOLDS. Against a
  perfect 24/24 baseline, the concept shape dropped the rule check to
  8/12 and the recipe to 9/12. Per the pre-registration: qwen obeys
  tools regardless of shape, and per-seat delivery policy becomes a
  conductor decision. FINDINGS 2 carries the evidence that the policy
  should weigh both directions of obedience, and the note that the
  production direction pin already blocks this exact serving: the
  contradiction only reached qwen because the packet stripped the pins.
- "Neither harms anywhere": does not hold (the contradicting task
  harmed). But its downgrade clause applies to the specific PACKET-006
  claim: the P2 harm DID NOT REPLICATE. The same recipe lesson on the
  same task read 0.75 to 0.25 in PACKET-006 and reads 0.50 to 0.58
  here, with the unarmed baseline itself moving 0.75 to 0.50 between
  runs. The PACKET-006 harm is downgraded the way PACKET-002's lead
  was downgraded: a single-run signal that replication dissolved.
- Mixed or partial: the matched task adds structure the branches did
  not pre-register, reported without forcing: the concept-shaped
  matched lesson produced the largest armed lift yet measured
  (rule check 0.50 to 0.92, both content checks up about 0.45, the
  boundary checks untouched), while the recipe shape produced roughly
  nothing. Shape mattered exactly where the tool was right.

Findings, sized to the n:
The obedient-seat story is now coherent across every cell measured:
qwen does what the tool says. Given a right, declaratively phrased
tool it posts the biggest lift the bench has seen (11/12 against
12/24). Given the same content as a recipe it gains little (7/12).
Given a contradicting tool it harms in either shape (8/12 and 9/12
against 24/24). PACKET-006's specific harm reading did not survive
replication, and what replaced it is sharper: the hazard is
contradiction plus obedience, not recipe shape alone, and the benefit
is correctness plus obedience. llama ignores its tools' errors and
gains modestly from their truths; qwen amplifies both. The n=12 to 24
cells here are the bench's strongest instrument to date, and the
harm-and-lift pattern above is consistent within this run across all
eight content checks.

Fixed under tier 1: nothing broke; resume stood ready and unused.

NOT done:
- Nothing cut: all arms at stated R, 96 of 96 runs.
- Protected surfaces beyond the approved gate change: untouched. The
  hand variants never enter any probe store, pinned by the loader and
  by test.
- Not attempted: the concept-field shape screen, the menu delivery
  surface change, and any per-seat delivery policy (FINDINGS 1 and 2,
  the conductor's calls).
