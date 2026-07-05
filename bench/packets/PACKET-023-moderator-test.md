# PACKET-023: The moderator test (idiom conflict, classified then measured)

Status: DONE
Owner: any Claude Code session. Read /CLAUDE.md first, then this, whole.

## Goal

The idiom-conflict moderator is the record's leading untested
hypothesis (adopted design-level, DECISIONS 2026-07-03; spec v0.7
Section 12): tools nudge the amplifier toward the canonical solution
shape, and tasks split on whether the stated rule fights that shape or
extends it. This packet tests it directly with the sharpest available
design: one lesson, one seat, two grounds classified in opposite
directions before the run. Everything is held fixed except the
classification, so the readings land on the moderator and nothing else.
Performer qwen2.5-coder:7b (the amplifier, where the moderator was
observed), audience llama3.1:8b, v1 production path, detached,
checkpointed. The seat neither teaches nor learns: no distillation, no
chair memory, no production store changes, packet-local byte-copy only.

## The classification, pre-registered before any run

The criterion: name the canonical solution shape the task statement
pulls a code model toward, then locate the stated rule. FIGHTS when
satisfying the rule requires changing code inside the idiom's core.
EXTENDS when the rule is a separable step around the intact idiom.

All eight apply tasks, classified by the criterion. The two measured
anchors are marked; they calibrated the criterion and cannot confirm it.

- longest_word: FIGHTS (anchor, measured harm three times). Idiom
  max(words, key=len) returns the first tie; the rule says last,
  replacing the selection inside the idiom.
- range_summary: EXTENDS (anchor, measured lift, replicated). The
  distinctness rule is sorted(set(nums)) prepended; the run-collapse
  idiom runs intact.
- most_common_word: FIGHTS. Counter.most_common and max-by-count both
  hard-code first-encountered on ties; alphabetical tie-break replaces
  the selection key inside the idiom.
- merge_ranges: FIGHTS, the mildest call. The sweep idiom merges on
  start <= current_end; the touch rule changes that comparison to
  start <= current_end + 1, one token, but inside the core.
- flatten_once: FIGHTS. The one-level comprehension assumes every
  element iterable; keeping non-list elements as is requires a type
  branch the flat comprehension cannot express. Supporting observation,
  not evidence: llama forced the rule into the idiom eight times in
  PACKET-022 and produced the same illegal filter-with-else shape each
  time.
- median: EXTENDS. The empty-list None is a prepended guard; the
  even-length float average falls out of true division. The sort-and-
  index idiom runs untouched.
- snake_to_camel: EXTENDS. Dropping empty parts is a separable filter
  on the split list before the intact capitalize-join idiom. Noted
  wrinkle: the filter interacts with which part is first.
- balanced: AMBIGUOUS, excluded from the confirmatory test, and now
  measured as such. Two candidate shapes with opposite classifications:
  the counter sweep, which the stated rule restates (extends), and the
  count-equality shortcut, which the rule fights. The conductor's
  census of the PACKET-022 artifacts shows llama sampling BOTH inside
  one cell, 8 shortcut and 4 sweep at n=12, so the reached-for shape is
  a distribution per seat and task, not a value. A task whose
  distribution splits classifies nothing.

The census consequence, stated for the whole table: the criterion
presumes each task's canonical pull is concentrated on one shape. That
concentration is measurable per seat and this packet measures it for
qwen (the census instrument below) instead of assuming it.

## The instrument

One lesson, byte-copied from the production store (bench/lessons.jsonl)
into a single-lesson packet-local store, byte-check asserted before any
stage B run:

- B1: origin gen_task chunk, pins boundary/degenerate, mistral origin,
  production line 8. Its pins match both test grounds, which is the
  whole design: the same lesson rides a FIGHTS ground and an EXTENDS
  ground.

The weighted_mean wildcard lesson is blocked to qwen by standing rule
and never enters this packet. Single-lesson stores make the block
structural.

## Stage A: ground qualification (gates only, never a treatment baseline)

Performer qwen2.5-coder:7b. Candidates in ranked order, two sweeps,
each stopping at its first qualifier:

FIGHTS sweep: 1. flatten_once, 2. merge_ranges. The strongest conflict
leads, by design: the sweep stops at its first qualifier, and a FLAT on
the mildest conflict would be ambiguous between moderator-false and
conflict-too-small. Leading with the hard conflict makes a FLAT read
against the moderator, not against the instrument.
EXTENDS sweep: 1. median (the only boundary-pinned EXTENDS task; no
fallback exists that keeps the one-lesson design pure).

For each candidate in order: run the none cell at R=12, no tools, the
rule-check annotations printed before any run. Qualification at the
standing fraction: one-rule ground (merge_ranges, flatten_once), at
least 2 passes AND 2 fails of 12 pooled; two-rule ground (median), at
least 4 passes AND 4 fails of 24 pooled. A sweep that exhausts its
candidates closes that side on the supply answer: qwen's floors and
ceilings on this ground are themselves results, and the moderator
stays untested on that side, said plainly.

## Stage B: the moderator cells (fresh, interleaved)

One block per qualified side, FIGHTS block first, run whole before the
EXTENDS block starts. Per block: two fresh cells at R=12 each,
interleaved per rep in the fixed order none then armed, order logged,
24 runs. none: no tools. armed: B1 through the production menu path
from its single-lesson store. Tool audit from the rows: armed tools=1,
none tools=0, every row. Unrunnable outputs counted as fails in every
pooled rule count per the standing doctrine (DECISIONS 2026-07-04),
with the per-cell unrunnable count reported as its own column and
readings-present shown beside as the diagnostic.

Drift bars, scaled as standing: 2 of 12 pooled on one-rule ground,
4 of 24 pooled on two-rule ground.

## The pre-registered readings, signed, exclusive, applied verbatim

Reading 1, the FIGHTS cell (armed against none on the qualified FIGHTS
ground): the classification predicts DOWN.
- Armed below none by more than the bar: the prediction lands, spoken
  as one supporting measurement, a lean, never a rate.
- Armed above none by more than the bar: the classification is WRONG on
  this task, said loudly in the first sentence, and the moderator is
  downgraded where it was adopted, by the conductor.
- Gap at or under the bar: FLAT, claims nothing, supports nothing.

Reading 2, the EXTENDS cell (armed against none on median): the
classification predicts UP.
- Armed above none by more than the bar: the prediction lands, one
  supporting measurement, a lean.
- Armed below none by more than the bar: the classification is WRONG on
  this task, said loudly, the moderator downgraded where adopted.
- Gap at or under the bar: FLAT, claims nothing, supports nothing.

Reading 3, the joint statement, pre-registered: the moderator gains
support only if BOTH cells land their predicted sign. One landed and
one FLAT is partial direction, named as such, no upgrade. Either cell
landing opposite its sign downgrades the moderator in spec v0.7
Section 12 and in DECISIONS where it was adopted, conductor's work.

The census instrument, pre-registered as descriptive: every output in
every cell, stage A included, is classified by the solution shape it
reached for, the shape taxonomy stated per task in the run log before
any run (for flatten_once: comprehension, loop-with-branch, other,
unrunnable; for merge_ranges: sweep, other, unrunnable; for median:
sort-and-index, other, unrunnable). The per-cell shape distribution is
reported as its own table. Its pre-registered role, exact: census data
interprets a FLAT (a none cell whose census shows the seat rarely
reaching the conflicted idiom explains a FLAT as pull-too-weak) and
contextualizes a landed sign, and it NEVER flips a signed exit in
either direction. Census claims are descriptive at their n, filed as
leads at most.

Watch columns, pre-registered: every non-rule check in every stage B
cell, any above-bar movement in either direction reported as watch
data with NO NAME, grounding no claim. The amplifier's
collateral-safety property has held four consecutive measurements;
these cells extend that series or break it, and a break is said loudly.

Harm columns, the standing reconciliation: every decline reported,
above-bar declines said loudly, at-or-under-bar declines inside drift.

## Gate

- Stage A run in ranked order per sweep, qualification arithmetic
  printed per candidate, annotations printed before any run.
- Stage B only on qualified ground, fresh interleaved cells, byte check
  asserted, tool audit clean from the rows, interleave verifiable from
  the row sequence, unrunnable counts reported per cell.
- The census table reported for every cell run, stage A included, with
  the shape taxonomy printed before any run and the classifier logic
  committed with the harness so the conductor can re-run it on the
  persisted outputs.
- Priors printed beside the tables: qwen's prior cells on this lesson
  class and the two anchor measurements the classification was
  calibrated on.
- The three readings applied verbatim with their signs and bars.
- Tests green, per-path staging, honest RESULTS and FINDINGS.

## Constraints

- Protected surfaces, tier 2: judge protocol v1, firewall, watch gates,
  lesson gates, lessons.jsonl, watchlist.jsonl, canonical documents,
  all production stores, and the classification table above, which is
  pre-registration and must not be edited after the first run.
- No distillation, no chair memory, no pin changes, no gate changes.
- The lesson rides byte-verbatim; any edit voids the cell.
- If wall time forces a cut: complete both sweeps before any stage B
  run, and complete the FIGHTS block whole before the EXTENDS block. A
  finished block stands alone; a half block claims nothing. Say what
  was cut.

## FINDINGS

Tier 2, flagged and not fixed. The classification table above is
untouched, per the constraint; both findings are about what the
measured census says the table's criterion needs next.

1. THE CONCENTRATION PRESUMPTION FAILS PER-SEAT ON FLATTEN_ONCE. The
   table classifies flatten_once FIGHTS by naming the flat
   comprehension as the canonical pull. Qwen's measured pull sits on
   loop-with-branch, 10 of 12, with the rule passing 11 of 12: the
   seat mostly reaches the shape that accommodates the rule, so there
   is no conflict to moderate on this task for this seat. Llama's
   PACKET-022 record shows the opposite pull on the same task, the
   comprehension forced into illegality eight times. The
   FIGHTS/EXTENDS classification is seat-dependent exactly where this
   packet's census consequence said it could be, and now with
   measurements on both sides. What I would do: fold a per-seat
   concentration condition into the criterion before the next
   moderator cut, a task classifies FIGHTS for a seat only when that
   seat's none-cell census concentrates on the conflicted shape, and
   derive sweep candidates per seat from census data instead of from
   the table's seat-free reading. Criterion design, conductor and
   Brad.

2. GROUND SUPPLY FOR THE MODERATOR TEST ON QWEN IS EMPTY AT THIS
   DESIGN. The one-lesson boundary/degenerate design admits exactly
   three candidate grounds and all three missed the standing bar, two
   by exactly one reading: flatten_once one fail short of mixed,
   merge_ranges one pass short. The bar held and should hold; the
   supply is the verdict. What I would do: the next moderator cut
   derives its FIGHTS candidate from census-concentrated ground
   (merge_ranges is fully concentrated here but near-floor), which
   likely means new boundary/degenerate probe tasks of intermediate
   difficulty for this seat, calibrated before the packet is cut. The
   conductor's cut.

## RESULTS

Executed 2026-07-04 by a Claude Code session. Commits: 8ad2b70
(harness, tests, byte-checked material) and the closing commit
carrying this section. Run moderator23-20260704-071554 ran detached
start to finish, no kill, resume unused. 217 tests green throughout.
The seat neither taught nor learned: no distillation, no chair memory,
no production store changes, the store verified untouched at eleven
lessons in the closing recount.

What ran: 36 runs, all stage A, every one checkpointed. Performer
qwen2.5-coder:7b, audience llama3.1:8b, v1 production path. The byte
check on the packet-local B1 store was asserted before any run and
re-asserted at close by the committed check. The census taxonomy was
printed per task in the run log before any run, the rule-check
annotations likewise, and the classifier logic is committed with the
harness. The conductor's replay ran at close: py moderator23.py census
over the persisted outputs, 36 rows, 0 mismatches, and the
shape-unrunnable against zero-readings divergence is 0 rows.

Stage A, gates only, ranked order, canonical accounting
(unrunnable-as-fail, DECISIONS 2026-07-04), the arithmetic printed per
candidate. No unrunnable output appeared anywhere, so the canonical
and readings-present accountings are identical on every count:

- FIGHTS sweep: flatten_once 11 passes, 1 fail of 12, one fail short
  of mixed, does not qualify, a near-ceiling. merge_ranges 1 pass, 11
  fails of 12, one pass short of mixed, does not qualify, a
  near-floor. The sweep exhausted.
- EXTENDS sweep: median 24 passes, 0 fails of 24, a ceiling, does not
  qualify. The sweep exhausted.

STAGE B DID NOT RUN. Both sides closed on the supply answer the packet
pre-registered as itself a result: qwen's floors and ceilings on this
ground are the finding, and the moderator stays untested on both
sides, said plainly. No armed cell exists anywhere in this packet. The
tool audit from the rows: every row tools=0, none cells only. The
interleave requirement is vacuous with no stage B rows.

The three pre-registered readings, applied verbatim: their ground
never qualified, so none of the three fired. Reading 1 unmeasured,
reading 2 unmeasured, reading 3 the joint statement: no support and no
downgrade. The moderator stands exactly where it stood, adopted
design-level and untested, and nothing in this packet moves spec v0.7
Section 12 in either direction.

The census, reported for every cell run, descriptive at n=12, leads at
most, and it is the packet's yield:

| cell (all stage A, none) | shape distribution | rule check |
|---|---|---|
| flatten_once | loop-with-branch 10, comprehension 2, other 0, unrunnable 0 | 11/12 |
| merge_ranges | sweep 12, other 0, unrunnable 0 | 1/12 |
| median | sort-and-index 12, other 0, unrunnable 0 | 24/24 |

Census observations, no claims grounded:
- flatten_once: the seat's pull does not concentrate on the conflicted
  comprehension; it concentrates on the branching loop that
  accommodates the rule, and the rule passes with it. Beside the
  PACKET-022 record, where llama forced the comprehension into the
  same illegal shape eight times on this task, the canonical pull is
  measured seat-dependent (FINDINGS 1).
- merge_ranges: the pull is total, sweep 12 of 12, and the stated rule
  loses inside the intact idiom 11 of 12. The idiom-pull precondition
  the moderator presumes is measured present on this FIGHTS-classified
  task, in a none cell, with no tool anywhere near it. Descriptive.
- median: concentrated pull, rule satisfied everywhere, no headroom.

Priors, printed beside the tables as the gate requires: the two
anchors the classification was calibrated on, longest_word FIGHTS
(three same-direction declines on this seat, gaps 6/24, 4/24, 11/24)
and range_summary EXTENDS (replicated lifts on this seat, none 8/12 to
rev 12/12 and hand 12/12 in P15, none 4/12 to rev 11/12 and hand 10/12
in P21); no prior boundary-class delivery cell to this seat exists,
and after this packet that is still true. Calibration n=1 priors for
the grounds: flatten_once 0.33, merge_ranges 0.75, median 1.00. The
stage A cells supersede them: calibration was one run of the whole
check set, and flatten_once inverted from 0.33 to a near-ceiling
11/12 on its rule check at n=12.

Watch columns: no stage B cell ran, so no watch data exists. The
amplifier's collateral-safety series stands at four consecutive
measurements, neither extended nor broken by this packet.

Harm columns: no armed cell ran; there is no decline to reconcile.

Fixed under tier 1: nothing broke; resume stood ready and unused.

NOT done:
- Stage B, by the packet's own gate: no ground qualified.
- The three readings: unfired, their ground never existed.
- Any moderator claim in either direction, any change to spec v0.7
  Section 12 or the DECISIONS adoption (the conductor's).
- Any edit to the classification table: protected, untouched.
- No distillation, no chair memory, no pin change, no gate change; the
  lesson rode nowhere because no armed cell ran, and its store stayed
  byte-identical to production line 8, asserted twice.
- The per-seat criterion condition and the next ground supply
  (FINDINGS 1 and 2), the conductor's calls.
