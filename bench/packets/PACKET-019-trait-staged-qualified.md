# PACKET-019: The trait measurement, staged and qualified (mistral)

Status: DONE
Owner: any Claude Code session. Read /CLAUDE.md first, then this, whole.

## Goal

Two trait cells have returned null on ground that lied at R=6. This
packet measures mistral:7b's tool-response trait on ground that must
first prove itself mixed at R=12, per the amended doctrine (DECISIONS
2026-07-03). The instrument is the PACKET-014 llama-origin distinctness
lesson, whose pins (distinctness, values) match both candidate grounds
by their standing annotations, so the cell doubles as that lesson's
third receiving seat. The seat neither teaches nor learns: no
distillation, no chair memory, no production store changes, packet-local
byte-copies only.

## Stage A: ground qualification (gates only, no treatment reading)

Performer mistral:7b, audience llama3.1:8b, v1 production path,
detached, checkpointed. Candidates in ranked order:
1. second_largest (baseline 2/6 task fails)
2. dedupe (baseline 5/6 task fails)

For each candidate in order: run the none cell at R=12, no tools. Pool
the rule-check readings per the pool's standing rule-check annotation,
printed in RESULTS before the run (two rule checks per task, 24 pooled
readings). The ground QUALIFIES if the pooled readings land mixed: at
least 4 passes AND at least 4 fails of 24. Stop at the first qualifier
and proceed to stage B on that ground. If neither candidate qualifies,
STOP and close the packet on that supply answer: the qualification
sweep is itself a result, and the next ground is the conductor's cut.

Stage A cells gate. They are never used as the treatment baseline.

## Stage B: the trait reading (fresh cells, interleaved)

On the qualified ground only. Two fresh cells at R=12 each, interleaved
per rep in the fixed order none then armed, order logged, 24 runs.

- none: no tools.
- armed: the PACKET-014 llama-origin lesson, byte-copied packet-local
  from PACKET-014-lessons.jsonl, byte-check asserted before any stage B
  run. Tool audit from the rows: armed tools=1, none tools=0, every row.

Drift bar: 4 of 24 pooled. The signed three-exit reading, exclusive:
- GAIN: armed pooled rule above none pooled by more than the bar. First
  trait evidence points filter-or-better, and the machine-born lesson
  has its third receiving seat, sized one task, one seat, n=12,
  direction never a rate.
- HARM: armed pooled rule below none pooled by more than the bar. Said
  loudly, and the writeup names BOTH candidate causes in its first
  sentence: the seat's trait, and the instrument's source-task residue
  (the concept text is sum-flavored; PACKET-012 denied residue its
  separation on one cell and did not bury it). Neither cause is chosen
  at this n.
- FLAT: the gap at or under the bar. Inside recorded drift, claims
  nothing.

Boundary-watch, pre-registered, reported as watch data with NO NAME:
every non-rule check in both stage B cells, any above-bar movement in
either direction reported beside the PACKET-017 floor-cell shape. Watch
data grounds no claim.

Harm columns, the standing reconciliation: every decline reported,
above-bar declines said loudly, at-or-under-bar declines inside drift.

## Gate

- Stage A run in ranked order with the qualification arithmetic printed
  per candidate. Stage B run only on qualified ground, fresh interleaved
  cells, byte-check asserted, tool audit clean, priors printed
  (mistral's baseline counts for the ground; the incumbents' trait
  cells for context).
- The three-exit reading applied verbatim with its sign and bar; the
  two-cause sentence included verbatim if HARM fires.
- Tests green, per-path staging, honest RESULTS and FINDINGS.

## Constraints

- Protected surfaces, tier 2: judge protocol v1, firewall, watch gates,
  lesson gates, lessons.jsonl, watchlist.jsonl, canonical documents, all
  production stores.
- No distillation, no chair memory, no pin changes, no gate changes.
- The lesson rides byte-verbatim; any edit voids the cell.
- If wall time forces a cut, complete stage A before any stage B run,
  and cut stage B's R evenly if it must shrink. Say so.

## FINDINGS

(none. The staged doctrine did its job on its first outing: the gate
qualified real mixed ground, the ground reproduced in the fresh cells,
and the reading came back clean. The observations worth carrying are
RESULTS material: a FLAT that finally measures something, and a quiet
boundary-watch for the third cell running.)

## RESULTS

Executed 2026-07-03 by a Claude Code session. Commits: 7e008cc (harness,
the tier 1 annotation fix, byte-checked material) and the closing
commit carrying this section. Run trait19-20260703-201821 ran detached
start to finish, no kill, resume unused. 179 tests green throughout.
The seat neither taught nor learned: no distillation, no chair memory,
no production store changes.

Tier 1, in the packet's terrain, named as required: the stage A
candidates carried no rule_checks annotation (only kept apply tasks got
them in PACKET-005; second_largest and dedupe are dropped candidates).
Annotated from each task's stated rule and pinned by test, printed in
the run log before any run:
- second_largest: second_largest([5, 5, 5]) and
  second_largest([2, 1, 2]), the two distinctness traps.
- dedupe: dedupe([3, 1, 3, 2, 1]) and dedupe(['b', 'a', 'b']), the two
  first-appearance-order traps.

STAGE A, ground qualification in ranked order, gates only:
- second_largest: 13 passes, 11 fails of 24 pooled rule readings.
  QUALIFIES (at least 4 of each). The sweep stops here per the packet;
  dedupe was never run.
Stage A's cell gated and was not reused: stage B ran fresh cells.

STAGE B, the trait reading on second_largest: two fresh cells at R=12
each, 24 runs, interleaved per rep in the fixed order none then armed,
order logged. Byte check asserted before any run: the armed store is
byte-identical to PACKET-014-lessons.jsonl. Tool audit clean from the
rows: armed tools=1, none tools=0, every row. GATE passed.

Per-check table (n=12 per cell; priors beside):

| check | none | armed | priors |
|---|---|---|---|
| [5, 5, 5] RULE | 0.58 (7/12) | 0.58 (7/12) | mistral baseline: task 2/6 fails at R=6 (P17 stage 1) |
| [2, 1, 2] RULE | 0.42 (5/12) | 0.50 (6/12) | same |
| [1, 3, 2] (watch) | 0.83 (10/12) | 1.00 (12/12) | incumbent context: qwen on its trait ground fell 13/24 to 2/24 (P13); llama held flat under mismatched tools (P4, P6) |
| [] (watch) | 1.00 (12/12) | 1.00 (12/12) | P17 floor shape: empty fell 12/12 to 6/12, single rose 2/12 to 6/12 |

Pooled rule checks: none 12/24, armed 13/24.

The signed three-exit reading, applied verbatim with its sign and the
bar: FLAT. The pooled gap is 1 of 24, at or under the 4-of-24 bar,
inside recorded drift, and it claims nothing. Not GAIN, not HARM, so
the two-cause sentence is not invoked. This FLAT differs from the two
before it in the one way that matters: the ground was qualified at
R=12 and reproduced in the fresh cells (none 12/24 mixed), so for the
first time the reading measured the seat rather than the ground. At
this n the seat neither gained from nor was harmed by a matched,
pinned, machine-born lesson on genuinely mixed ground.

Boundary-watch, reported as watch data with no name: the plain
correctness check rose 10 of 12 to 12 of 12, a movement of 2 of 12, at
the per-check bar and not above it; the empty-input check sat 12 of 12
in both cells. Third consecutive quiet watch beside the PACKET-017
floor shape, which remains the only above-bar sighting.

Harm columns, the standing reconciliation: no declines anywhere, in
either watch column or either rule check. Nothing to say loudly.

Findings, sized to the n:
The staged doctrine paid for itself on the first outing: 12 gate runs
bought a ground label that held, and the trait cell finally measured
the seat. What it measured, at one task, one seat, n=12, direction
never a rate: indifference. The third seat holding the machine-born
lesson that lifted qwen to perfect on its matched ground produced one
extra pooled pass and no movement anywhere else. Set beside the
incumbents' cells, the three seats now read as three different tool
responses: qwen amplifies (large gains on matched ground, large harm
under conflict), llama filters (modest gains, ignores what contradicts
it), and mistral's first valid cell sits between, unmoved in either
direction by a tool its ground matched. One cell is a lean, not a
casting entry, and the boundary disturbance from the floor cell still
has no second sighting. The teaching gate's condition
(tool-response-probed) now has its measurement, and what that means
for the gate is the conductor's reading, not this session's.

Fixed under tier 1: the rule_checks annotation, named above.

NOT done:
- dedupe's qualification (the sweep stopped at the first qualifier,
  per the packet).
- Nothing cut: stage A at R=12, stage B both cells at R=12 in full.
- No distillation, no chair memory, no store changes; the lesson rode
  byte-verbatim, asserted.
- Any teaching-gate consequence and any trait naming beyond this one
  cell (the conductor's calls).
