# PACKET-022: Arm the floors (first delivery cells, boundary and normalize)

Status: DONE
Owner: any Claude Code session. Read /CLAUDE.md first, then this, whole.

## Goal

The production store holds eleven lessons and eight of them have no
delivery reading anywhere. This packet buys the first delivery evidence
for the two classes that resisted every prior seat: boundary and
normalize. The ground is the deepest unarmed apply floors, qualified
mixed inside the packet per the standing doctrine (DECISIONS
2026-07-03), then armed with single-lesson cells so every reading
attributes to exactly one lesson. The receiving seat is llama3.1:8b,
the measured filter, audience qwen2.5-coder:7b, v1 production path,
detached, checkpointed. The seat neither teaches nor learns: no
distillation, no chair memory, no production store changes,
packet-local byte-copies only.

## The four lessons under test

Byte-copy each from the production store (bench/lessons.jsonl) into a
single-lesson packet-local store per armed cell, and assert each
byte-identical to its production line before any stage B run:

- B1: origin gen_task chunk, pins boundary/degenerate, mistral origin.
- B2: origin gen_task weighted_mean, pins boundary/*, mistral origin.
  The wildcard topic pin. Not delivery-eligible to qwen by standing
  rule; llama is not blocked. This cell is the wildcard's first
  exposure reading and says so in RESULTS.
- N1: origin gen_task split_csvish, pins normalize/delimiters, mistral
  origin.
- N2: origin gen_task depth_max, pins normalize/delimiters, mistral
  origin. Carries the flagged cross-topic residue phrase. Its delivery
  cell is its watch, per the admission record.

## Stage A: ground qualification (gates only, never a treatment baseline)

Candidates in ranked order, two sweeps, each stopping at its first
qualifier:

Boundary sweep: 1. merge_ranges, 2. median, 3. flatten_once.
Normalize sweep: 1. snake_to_camel, 2. balanced.

For each candidate in order: run the none cell at R=12, no tools. Pool
the rule-check readings per the task's standing annotation, printed in
RESULTS before the run. Pooled counts differ by task and the
qualification scales with them, same fraction as PACKET-019:
- One rule check (merge_ranges, flatten_once, snake_to_camel): 12
  pooled readings. QUALIFIES if at least 2 passes AND 2 fails of 12.
- Two rule checks (median, balanced): 24 pooled readings. QUALIFIES if
  at least 4 passes AND 4 fails of 24.

Stop each sweep at its first qualifier and carry that ground to stage
B. If a sweep exhausts its candidates with no qualifier, STOP that
class and close it on the supply answer: the sweep is itself a result,
and the next ground is the conductor's cut. Stage A cells gate. They
are never reused as the treatment baseline.

## Stage B: the delivery readings (fresh cells, interleaved)

One block per qualified class, boundary block first, run to completion
before the normalize block starts.

Boundary block, on the qualified boundary ground: three fresh cells at
R=12 each, interleaved per rep in the fixed order none, armed-B1,
armed-B2, order logged, 36 runs.
Normalize block, on the qualified normalize ground: three fresh cells
at R=12 each, interleaved per rep in the fixed order none, armed-N1,
armed-N2, order logged, 36 runs.

- none: no tools.
- armed: the named lesson only, delivered through the production menu
  path from its single-lesson packet-local store, byte-check asserted
  before any stage B run. Tool audit from the rows: armed tools=1,
  none tools=0, every row.

Drift bar per comparison, scaled as above: 2 of 12 pooled on one-rule
ground, 4 of 24 pooled on two-rule ground.

## The pre-registered readings, signed, exclusive, applied verbatim

Four readings, one per armed cell against its same-block none cell,
each the three-exit form:

- GAIN: armed pooled rule above none pooled by more than the bar. The
  lesson has its first delivery evidence, non-harmful and lifting,
  sized one task, one seat, n=12, direction never a rate.
- HARM: armed pooled rule below none pooled by more than the bar. Said
  loudly. For armed-N2 the writeup names BOTH candidate causes in its
  first sentence: the seat's response and the lesson's cross-topic
  residue, neither chosen at this n. For armed-B2 the writeup names
  BOTH candidate causes in its first sentence: the seat's response and
  the wildcard pin's over-broad ride, neither chosen at this n.
- FLAT: the gap at or under the bar. Inside recorded drift, claims
  nothing, and is still the lesson's first non-harmful delivery
  reading.

Watch columns, pre-registered: every non-rule check in every stage B
cell, any above-bar movement in either direction reported beside the
PACKET-017 floor-cell shape, watch data with NO NAME, grounds no claim.

Harm columns, the standing reconciliation: every decline reported,
above-bar declines said loudly, at-or-under-bar declines inside drift.

Transfer note, pre-registered: every armed cell here is mistral-origin
content received by llama, a new edge in the transfer record. Any GAIN
is spoken as one measurement on that edge, a lean, never a result.

## Gate

- Stage A run in ranked order per sweep with the qualification
  arithmetic printed per candidate, rule-check annotations printed
  before any run.
- Stage B run only on qualified ground, fresh interleaved cells, all
  four byte checks asserted, tool audit clean from the rows, interleave
  verifiable from the row sequence.
- Priors printed beside the table: the seat's stage A counts for the
  ground, and the incumbents' delivery cells for context.
- The four signed readings applied verbatim with their signs and bars;
  the two-cause sentences included verbatim where HARM fires.
- Tests green, per-path staging, honest RESULTS and FINDINGS.

## Constraints

- Protected surfaces, tier 2: judge protocol v1, firewall, watch gates,
  lesson gates, lessons.jsonl, watchlist.jsonl, canonical documents,
  all production stores.
- No distillation, no chair memory, no pin changes, no gate changes.
- Each lesson rides byte-verbatim; any edit voids its cell.
- If wall time forces a cut: complete both stage A sweeps before any
  stage B run, and complete the boundary block whole before the
  normalize block starts. A finished block stands on its own; a
  half-finished block claims nothing. Say what was cut.

## FINDINGS

Tier 2, flagged and not fixed:

1. UNRUNNABLE OUTPUT SPLITS THE POOLED COUNT FROM THE RUNNER'S
   VERDICT. Eight of the boundary block's 36 runs (none 2, armed-B1 2,
   armed-B2 4) returned code that failed to compile: the seat wrote a
   filter-with-else inside a list comprehension in all eight, which
   Python rejects at parse time. The runner scores such a run fail,
   but its per-check readings never exist, so the pooled rule counter
   (the same counter every prior harness used) loses those rows and
   the boundary cells' pooled n landed at 10, 10, and 8 instead of the
   pre-registered 12. Both honest accountings, readings-present and
   unrunnable-as-fail, give identical gaps and the same exit on every
   reading in this packet, and RESULTS reports both. On other ground
   the two views could diverge and split a GAIN from a FLAT, and the
   bars are stated in counts. What I would do: a doctrine line ruling
   which accounting is canonical for pooled rule checks when output
   does not compile. Measurement doctrine, the conductor's call.

## RESULTS

Executed 2026-07-04 by a Claude Code session. Commits: afca50a
(harness, tests, byte-checked materials) and the closing commit
carrying this section. Run armfloors22-20260704-051116 ran detached
start to finish, no kill, resume unused. 200 tests green throughout.
The seat neither taught nor learned: no distillation, no chair memory,
no production store changes, the store verified untouched at eleven
lessons in the closing recount.

What ran: the packet's design whole, 132 runs, every one checkpointed.
Performer llama3.1:8b receiving, audience qwen2.5-coder:7b, v1
production path, pins live. All four packet-local stores byte-checked
against their production lines before any run, asserted by the harness
and re-asserted in the closing verification: armed-B1 (chunk,
boundary/degenerate), armed-B2 (weighted_mean, boundary/*), armed-N1
(split_csvish, normalize/delimiters), armed-N2 (depth_max,
normalize/delimiters), every one mistral-origin. The rule-check
annotations were printed before any run, as the gate requires.

Stage A, gates only, ranked order, the arithmetic printed per
candidate:
- Boundary sweep: merge_ranges 0 passes 12 fails of 12, does not
  qualify, an absolute floor for this seat. median 24 passes 0 fails
  of 24, does not qualify, a ceiling. flatten_once 8 passes 4 fails of
  12, QUALIFIES, and the sweep stopped there.
- Normalize sweep: snake_to_camel 0 passes 12 fails of 12, does not
  qualify, a floor. balanced 19 passes 5 fails of 24, QUALIFIES, and
  the sweep stopped there.

Stage B ran on qualified ground only, fresh interleaved cells in the
fixed order none, armed-1, armed-2 per rep, the boundary block whole
before the normalize block, 72 runs. The interleave was verified exact
from the row sequence in the closing recount, and the tool audit is
clean from the rows: armed tools=1, none tools=0, every row.

The unrunnable-output note, stated before the tables: eight
boundary-block runs (none 2, armed-B1 2, armed-B2 4) returned code
that failed to compile, the same illegal filter-with-else
comprehension shape in all eight, recorded as SyntaxError by the
evidence layer and scored fail by the runner. Their per-check readings
do not exist, so the boundary table shows readings-present counts with
unrunnable-as-fail counts in parentheses. The two accountings give the
same gap and the same exit on every reading below (FINDINGS 1). The
normalize block compiled everywhere, 24 of 24 rule readings per cell.

Boundary block (flatten_once, R=12 per cell, bar 2 of 12 pooled):

| check | none | armed-B1 | armed-B2 |
|---|---|---|---|
| flatten_once([1, [2, [3, 4]]]) RULE | 4/10 (4/12) | 4/10 (4/12) | 2/8 (2/12) |
| flatten_once([[1, 2], [3]]) (watch) | 5/10 (5/12) | 5/10 (5/12) | 2/8 (2/12) |
| flatten_once([]) (watch) | 10/10 (10/12) | 10/10 (10/12) | 8/8 (8/12) |
| unrunnable outputs | 2/12 | 2/12 | 4/12 |

Priors beside the table: the seat's stage A count on this ground, none
8 of 12; calibration n=1 seat B 0.33; the incumbents' delivery cells,
P9 llama receiving (qwen tie lessons, rule checks 0.17 to 0.92, pooled
4/24 to 22/24), P19 mistral receiving (FLAT, armed 13/24 against none
12/24), P15 qwen receiving (none 8/12, rev 12/12, hand 12/12), P21
qwen receiving (none 4/12, rev 11/12, hand 10/12). The stage B none
cell sits at 4 of 12 against stage A's 8 of 12 on the same task,
baseline movement at the size PACKET-021 recorded on range_summary,
absorbed the same way, by same-run interleaving. Stage A gates, never
a baseline.

Normalize block (balanced, R=12 per cell, two rule checks, bar 4 of 24
pooled, all readings present):

| check | none | armed-N1 | armed-N2 |
|---|---|---|---|
| balanced('(a(b)c)') RULE | 12/12 | 12/12 | 12/12 |
| balanced(')(') RULE | 4/12 | 3/12 | 8/12 |
| balanced('') (watch) | 12/12 | 12/12 | 12/12 |
| balanced('((x)') (watch) | 12/12 | 12/12 | 12/12 |

Pooled rule: none 16/24, armed-N1 15/24, armed-N2 20/24. Priors
beside: stage A none 19/24 on this ground, a 3-of-24 move to the fresh
cell, inside the bar; calibration n=1 seat B 0.75; incumbents as
above.

The four pre-registered readings, applied verbatim, each with its
stated sign and bar:

1. armed-B1 against none (chunk lesson on flatten_once, bar 2 of 12):
   FLAT. Pooled rule 4 against 4 readings-present, 4/12 against 4/12
   unrunnable-as-fail, gap 0, at or under the bar. Inside recorded
   drift, claims nothing, and is still the chunk lesson's first
   non-harmful delivery reading.
2. armed-B2 against none (weighted_mean wildcard lesson on
   flatten_once, bar 2 of 12): FLAT. Pooled rule 2 against 4 in both
   accountings, gap 2, at the bar, not more. Not HARM by the reading's
   own definition, so the pre-registered two-cause sentence stays
   uninvoked. This cell is the wildcard pin's first exposure reading,
   said here as the packet requires: the boundary/* pin rode onto
   flatten_once ground, the cell read FLAT with its direction down at
   exactly the bar, and it claims nothing. By the exit's letter this
   is the lesson's first non-harmful delivery reading, with the
   direction and the cell's four unrunnable outputs reported in the
   watch paragraph below.
3. armed-N1 against none (split_csvish lesson on balanced, bar 4 of
   24): FLAT. Pooled rule 15/24 against 16/24, gap 1, inside the bar.
   Claims nothing, and is the split_csvish lesson's first non-harmful
   delivery reading.
4. armed-N2 against none (depth_max residue lesson on balanced, bar 4
   of 24): FLAT. Pooled rule 20/24 against 16/24, gap 4, exactly at
   the bar, not more. Not GAIN by the reading's own definition.
   Direction up, concentrated on the ')(' check, 8/12 against 4/12.
   This cell was the lesson's residue watch per the admission record:
   no harm appeared anywhere in it, the cross-topic residue stayed
   quiet on this ground, and the pre-registered two-cause HARM
   sentence stays uninvoked. First non-harmful delivery reading for
   the lesson.

Watch columns, pre-registered, NO NAME, grounding no claim: one
above-bar movement. The boundary content check flatten_once([[1, 2],
[3]]) declined in the armed-B2 cell, 5 to 2 readings-present, 5/12 to
2/12 unrunnable-as-fail, movement 3 against a 2-of-12 bar. Reported
beside the PACKET-017 floor-cell shape as the packet requires: it does
not match that shape. The PACKET-017 disturbance moved two boundary
checks in opposite directions at once at content floor; here
everything in the cell moved down together, rule check included, and
four of the cell's twelve outputs did not compile, which sits under
both declines. The unrunnable-output counts themselves, 2, 2, and 4
across none, B1, B2, differ by at most 2, at the one-rule bar, inside
drift. Every other watch column is quiet: flatten_once([]) at ceiling
wherever code compiled, and all normalize watch columns at 12/12 in
every cell.

Harm columns, the standing reconciliation, every decline reported:
armed-B2 rule check down 2, at the bar, inside drift, the FLAT of
reading 2. armed-B2 content watch down 3, ABOVE THE BAR, said loudly,
the no-name watch paragraph above. armed-B2 empty-list check down 2
only in the unrunnable-as-fail accounting, at the bar; readings-
present it sat at ceiling on both sides. armed-N1 rule check down 1,
inside drift. No other column declined anywhere.

Transfer note, pre-registered: all four armed cells are mistral-origin
content received by llama, a new edge in the transfer record, now
carrying its first four measurements. No GAIN fired, so nothing on
this edge is spoken as a lean: the edge is measured, not moved, four
FLATs at one task per class, one seat, n=12 per cell, direction never
a rate.

What the readings buy, sized exactly: all four admitted boundary and
normalize lessons now hold their first delivery evidence, all
non-harmful, all FLAT. The two lessons the admission ruling watched
closest both rode without firing HARM: the wildcard's exposure reading
points down at exactly the bar and claims nothing, the residue
lesson's watch cell points up at exactly the bar and claims nothing.
The deepest floors themselves resisted qualification: merge_ranges and
snake_to_camel are absolute floors for this seat at R=12 and median is
a ceiling, so delivery evidence on those grounds, if it is ever
wanted, needs different ground or a different seat, the conductor's
cut.

Fixed under tier 1: nothing broke; resume stood ready and unused.

NOT done:
- Nothing cut: both sweeps whole, both blocks whole at R=12,
  interleaved as specified.
- No distillation, no chair memory, no pin change, no gate change, no
  production store change; all four lessons rode byte-verbatim,
  asserted twice.
- No claim past FLAT anywhere: no GAIN, no HARM, no lean on the new
  transfer edge.
- The accounting doctrine for unrunnable output (FINDINGS 1) and any
  consequence for the ranked board, the conductor's calls.
