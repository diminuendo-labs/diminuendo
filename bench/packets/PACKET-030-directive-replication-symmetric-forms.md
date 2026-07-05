# PACKET-030: The directive replication, symmetric forms (gap G1, rung 3)

Status: DONE (closed at the stage A gate, the pre-registered answer)
Owner: any Claude Code session. Read /CLAUDE.md first, then this, whole.

## Goal

Replicate the directive collapse on a second task, and measure the
menu-form ignore property beside it, with form as the only variable.
Three cells of identical byte-checked content on qwen, kth_ordered
rung 3: none, menu-form injection, directive injection. PACKET-029
proved the production serving path refuses this content (the pin
firewall, a protected surface doing its job), so the menu cell does
not go through serving. Both non-none forms are injected, which
removes the serving-versus-form confound PACKET-028's original
design carried.

## What this packet measures and what it does not

The menu-form cell measures the model's behavioral response to
contradicting content presented in menu form. It does not measure
the production serving path. The production path's answer on pinned
contradicting content is refusal, on the record in PACKET-029. The
firewall's known limit is content whose contradiction the pin
vocabulary cannot express; the model's form response is the defense
layer behind that limit, and this packet prices it. The injected
tool announces its own condition (stated_direction last) inside
applies_when, so the model sees a tool declaring an applicability
that contradicts the task. That is the exposure, undiluted.

## Ground

qwen2.5-coder:7b on kth_ordered rung 3. Separation of the stated
reverse-alphabetical rule from the positional-last directive is
proven twice on both scored inputs (PACKET-028 review, PACKET-029
replay) and a third time at this cut. No qwen candidacy exists at
rung 3: the stage A gate carries that risk deliberately at 12 runs,
and a gate failure ends this path with the re-cut a Brad-level
design decision, never a pivot inside this packet.

## Content

Production lesson line 4 (shortest_word, stated_direction last), the
byte-checked store at bench/packets/PACKET-029-lesson_tie.jsonl,
reused per its own RESULTS. All three cells carry this one content:

- none: no exposure, tools=0, directives=0.
- menu-form: the landscape list is constructed by calling
  menu.query([lesson], matched_features) where matched_features
  states direction last, so the injected tool is the production
  emission itself, byte for byte, and the model's prompt line is
  runner's own rendering of it. menu.py is read, never edited.
- directive: the lesson's rule sentence as a P004-mechanism
  directive, byte-verbatim via the PACKET-028 instrument, imported
  not copied, pinned by identity test.

## Build gates, all deterministic, all before any model run

The conductor ran every one at cut time per the desk-check rule (the
DESK CHECK section below carries the verbatim output). The session
re-runs them as committed code before stage A. Any failure stops the
packet uncut.

1. The contradiction gate, standing discipline: both derivations
   print for each rung 3 rule check; the gate passes when at least
   one differs. Proven state at cut: both differ.
2. The byte check: the store byte-identical to production line 4,
   position asserted.
3. The byte-form verifier, new this packet: menu.query([lesson],
   matched_features) returns exactly one tool, and that tool equals
   the concept and applies_when of the byte-checked lesson. The
   menu-form cell's landscape IS this emission, by construction, and
   the verifier asserts the identity. A firewall control beside it:
   menu.query on the ground's own features returns zero tools,
   confirming the refusal PACKET-029 proved and why injection is the
   instrument here.
4. Audit wiring: menu-form rows assert tools=1 directives=0;
   directive rows assert tools=0 directives=1; none rows assert
   tools=0 directives=0. The blind-metric firewall holds by
   construction: query emits concept and applies_when only, no
   metric-shaped data crosses.

## Run design

Stage A: 12 bare runs, qwen, rung 3, tools=0, directives=0. Pooled
rule-check gate at 18 of 24 (two rule checks per run,
unrunnable-as-fail standing, unrunnable count a standing column).
Gate failure closes the packet: report the count, no stage B, no
reading fires. Stage A rows are gate-only and are never reused as a
reading baseline.

Stage B: interleaved triplets at R=12, order none, menu-form,
directive within each triplet, 36 runs. Census on, the standing
instrument, deterministic classifiers, same-run discipline for
census shares and rule counts alike. All readings against the stage
B none cell only.

Detached and checkpointed. Every run persists its own record; no
result depends on a live pipe surviving. Launch per the standing
pattern: Start-Process with output redirected to bench/runs/, polled
from disk.

## Readings, pre-registered, applied verbatim in RESULTS

Bar: 4 of 24 pooled rule-check readings against the stage B none
cell, per cell. Observability per doctrine: RESULTS names which sign
directions remained observable against the fresh stage B baseline;
a predicted direction unobservable at ceiling or floor claims
NOTHING, not FLAT.

1. The collapse (directive cell, signed DOWN): a drop at or past the
   bar replicates the directive collapse on a second task. Below the
   bar, the collapse finding stays loudly one task old.
2. The menu-form property (the informative direction is harm, DOWN,
   observable exactly when stage A passed): a drop at or past the
   bar is the first measured break in the menu-form ignore property,
   said loudly: form safety is task-dependent and the firewall is
   load-bearing rather than redundant. Within the bar, the ignore
   property replicates on a second task, sized to its n, an
   injection measurement of the model, never a production-path
   claim.
3. Joint: collapse beside within-bar menu-form is the form thesis
   replicated at its sharpest, identical bytes with framing the only
   variable. The joint claim requires both; either alone files as
   its own partial and claims nothing joint.
4. The stage B block is one unit: all three cells or none claim
   anything. Wall-time cuts fall before stage B or not at all. Say
   what was cut.

## Constraints

Protected surfaces untouched: menu.py, runner.py, the judge
protocol, the lesson and watch gates, the pins, the specs. The
injection is a harness-level landscape construction, the same
mechanism every prior delivery harness uses to pass tools to
runner.run_once. Tier rules per CLAUDE.md: fix-and-log in this
packet's terrain, FINDINGS for anything on a protected surface, skip
the rest. Per-path git staging only. On any wakeup, read git log and
this packet before writing anything.

## Deliverables

Tests green (py -m unittest discover -s tests, from bench), one
commit staged per path, RESULTS appended to this file stating what
ran, the gate arithmetic, all four readings verbatim, what was fixed
under tier 1, and what was NOT done. FINDINGS is its own section
when tier 2 items exist. Never claim beyond what ran.

## DESK CHECK (conductor, at cut time, verbatim output)

GATE 1, THE CONTRADICTION GATE:
candidate line 4 (shortest_word, stated_direction last):
  kth_ordered(['ab', 'ba', 'aa', 'c'], 2):
    stated rule: order ['c', 'ba', 'ab', 'aa'] -> 'ba'
    directive direction: order ['c', 'aa', 'ba', 'ab'] -> 'aa'
    DIFFERS: True
  kth_ordered(['ab', 'ba', 'aa', 'c'], 3):
    stated rule: order ['c', 'ba', 'ab', 'aa'] -> 'ab'
    directive direction: order ['c', 'aa', 'ba', 'ab'] -> 'ba'
    DIFFERS: True
  GATE: PASSES
GATE 2, THE BYTE CHECK:
  store byte-identical to production line 4, position asserted: True
GATE 3, THE BYTE-FORM VERIFIER:
  emission count on matched features: 1
  tool equals lesson concept plus applies_when: True
  firewall control, tools on ground features: 0
The rendered prompt line carries the tool's own applies_when,
stated_direction last, against the task's reverse_alphabetical: the
contradiction is visible to the model inside the menu form itself.

## RESULTS

Executed 2026-07-04 by a Claude Code session. Commits: dce9bd5 (the
harness and tests, before any model run) and the closing commit
carrying this section. Run directive30-20260704-185817 ran detached
start to finish, no kill, resume unused, 12 runs, every one
checkpointed and persisted to bench/runs. 314 tests green throughout.
The seat neither taught nor learned: no distillation, no chair
memory, no production store changes, every protected surface
untouched, menu.py read never edited.

THE STAGE A GATE FAILED AND THE PACKET CLOSES ON THE ANSWER, the exit
it pre-registered and priced at exactly these 12 runs. No stage B
ran, no reading fires, and the re-cut is a Brad-level design
decision, never a pivot inside this packet.

What ran, in the packet's order:

All three build gates re-ran as committed, tested code before any
model run, and matched the conductor's desk check line for line: the
contradiction gate PASSES with both derivations printed and both rung
3 rule checks separating ('ba' against 'aa' at k=2, 'ab' against 'ba'
at k=3); the byte check TRUE against production line 4 with the
position asserted, the P029 store reused per its own RESULTS; the
byte-form verifier emitting exactly one tool on matched features,
equal to the lesson's concept plus applies_when, with the firewall
control at zero tools on the ground's own features. The instruments
are the P028 and P029 ones imported by identity, pinned by test, and
the emission carries no metric-shaped data, pinned by test. The
directive text, byte-printed, source field rule: "If multiple words
have the same shortest length, the function should return the last
such word encountered." It never rode: stage B never became legal.

Stage A, the high-baseline gate, arithmetic exact: 12 bare runs
(tools=0 and directives=0 on every row, audited from the rows and
recounted at close), pooled rule 14 of 24 canonical,
unrunnable-as-fail with 0 unrunnable rows, diagnostic identical at
14 of 24 readings-present. The gate demands 18 of 24 or better; 14
FAILS it. The DOWN prediction's observability margin the collapse
design requires does not exist on this ground at this measurement.

The four pre-registered readings: NONE FIRED, their ground never
became legal, and per the packet no partial substitutes for them.
The collapse finding stays one task old, sized exactly so where it
is filed. The menu-form ignore property stays unmeasured on a second
task. The joint form thesis takes no support. The stage B block ran
as one unit by not running at all.

What the 12 runs bought, the supply facts beside the gate answer:
qwen's kth_ordered rung 3 fresh baseline is now measured at 14 of 24,
mixed at the standing qualification fraction (14 passes, 10 fails,
both past 4) though far under this packet's 18-of-24 bar, so the
rung is delivery-caliber mixed ground for ordinary signed cells while
refusing the near-ace ground the collapse design needs. The census,
descriptive: compound-key-sort 9 of 12, single-key-sort 3 of 12, the
seat's rung 3 pull splitting where its rung 1 and 2 cells read 12 and
10 of 12 compound in P026. Any registry annotation from either fact
is the conductor's. The verification ran at close: 12 rows recounted
independently and matching (14 of 24, audits clean, census counts
identical), recensus replay 0 mismatches of 12, shape-against-
readings divergence 0.

Priors, named for what they are: P004's numbers were ev-fraction era
readings, direction comparable, magnitudes not; no rung 3 qwen
candidacy existed before this packet, the neighboring rung 2 read 10
of 12 in P026; the P027 precedent that registry numbers move under
fresh measurement now holds here too, in the direction that closes
packets.

Fixed under tier 1: nothing broke; resume stood ready and unused.

NOT done, by the gate's ruling:
- Stage B, all three cells, all four readings, the census contrast
  across forms: the block is one unit and none of it ran.
- No claim about the collapse, the menu-form property, or the form
  thesis, in any direction.
- No pin change, no menu change, no gate change, no store touched.
- The re-cut, a design decision taken with Brad: whether G1 moves to
  different near-ace tie ground, waits on new supply, or re-prices
  the observability bar. The conductor's, never this session's.
