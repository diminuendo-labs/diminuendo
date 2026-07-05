# PACKET-031: Mistral self-delivery on registry ground (G2 re-scoped)

Status: DONE
Owner: any Claude Code session. Read /CLAUDE.md first, then this, whole.

## Goal

One cell, two questions, both pre-registered. First: the seat's
response to its own lesson, the self-delivery measurement PACKET-024
designed and its qualification gate refused, now on ground the eye
chart qualified. Second: mistral's second trait-series cell, extending
PACKET-019's FLAT lean, with the attribution caveat below carried on
every exit. Performer mistral:7b, audience llama3.1:8b, v1 production
path, detached, checkpointed. The seat neither teaches nor learns: no
distillation, no chair memory, no production store changes,
packet-local byte-copies only.

## The two-cause caveat, pre-registered on every non-FLAT exit

The instrument is mistral-origin delivered to mistral. Any non-FLAT
exit names BOTH candidate causes in its first sentence: the seat's
tool-response trait, and self-origin effects (the seat receiving its
own distilled lesson). Neither cause is chosen at this n. A FLAT
carries the caveat as context only. This is the price of the one
packet answering two questions, paid knowingly on Brad's Go.

## Ground and instrument

Ground: safe_stats rung 1, mistral's strongest registry candidacy
(14 of 24 in P026, census 12 of 12 sort-slice-average, separable).
Candidacy is not qualification: stage A qualifies fresh.
Rule checks, the standing annotation: trimmed_mean([]) and
trimmed_mean([5, 5, 1, 9]).

Instrument: production lesson line 8, origin_seat mistral:7b,
boundary class, degenerate topic, concept "Handle empty and None
inputs by returning an empty list." Its pins match the family's own
(rule_class boundary, rule_topic degenerate), a genuine pin match,
not wildcard absence, and its concept addresses the empty-input trap
in the ground's first rule check directly. The armed store is a
fresh raw byte copy of production line 8, cut by this packet:
PACKET-024's four stores verified JSON-equal to production but not
byte-identical (serialization only), so they are noted and not
reused. Byte check asserted with line position before any stage B
run.

## Build gates, deterministic, before any model run

The conductor ran each at cut time per the desk-check rule (DESK
CHECK section below, verbatim). The session re-runs them as
committed, tested code. Any failure stops the packet uncut.

1. The byte check: the packet-local store byte-identical to
   production line 8, position asserted.
2. The delivery-path check: menu.query on the single-lesson store
   with the ground's features serves exactly one tool, equal to the
   lesson's concept plus applies_when. This is the production
   serving path, not injection: the pins match, so the firewall has
   nothing to refuse.
3. The rule-checks annotation present for safe_stats rung 1, printed
   in the log before any run.
4. Audit wiring: armed rows assert tools=1 directives=0, none rows
   tools=0 directives=0, from the rows.

## Stage A: fresh qualification (gates only, never a baseline)

12 bare runs on safe_stats rung 1, tools=0. Pool the two rule checks:
24 readings, unrunnable-as-fail standing, unrunnable count a standing
column. QUALIFIES if mixed at the generalized fraction: at least 4
passes AND at least 4 fails of 24. If the gate fails, STOP and close
the packet on the supply answer: registry candidacy moved under fresh
measurement, the precedent stands, and the next ground is the
conductor's with Brad. Stage A rows are gate-only.

## Stage B: the reading (fresh cells, interleaved)

On qualified ground only. Two fresh cells at R=12, interleaved per
rep in the fixed order none then armed, order logged, 24 runs.
Census on, the standing instrument, same-run discipline.

- none: no tools.
- armed: the byte-checked line 8 store served through menu.query
  with the ground's features, tools=1 every armed row.

## Readings, pre-registered, applied verbatim in RESULTS

Drift bar: 4 of 24 pooled, armed against the stage B none cell only.
The three-exit reading, exclusive, with the two-cause caveat wired
per its section:

- GAIN: armed pooled rule above none by more than the bar. First
  self-delivery evidence points receptive, both causes named, sized
  one task, one seat, n=12, direction never a rate.
- HARM: armed pooled rule below none by more than the bar. Said
  loudly, both causes named in the first sentence, and the
  collateral-safety series is checked for its first break.
- FLAT: the gap at or under the bar. Inside recorded drift. Beside
  P019's FLAT it extends the indifference lean to two cells, one
  cross-origin and one self-origin, each sized to its own n and the
  self cell carrying its caveat.

Observability per standing doctrine: RESULTS names which exits
remained observable against the fresh stage B none cell. A none cell
at ceiling leaves GAIN unobservable and that direction claims
NOTHING; at floor, the same for HARM.

Effective-n sizing per the standing addendum: RESULTS reports the
within-row correlation of the two rule checks; if they never
disagree inside a row, the independent unit is the run and the
claim sizes to n=12.

Boundary-watch, pre-registered, reported as watch data with NO NAME:
every non-rule check in both stage B cells, any above-bar movement
in either direction reported. Watch data grounds no claim. Harm
columns per the standing reconciliation: every decline reported,
above-bar declines said loudly.

Priors, printed before the run: P019's trait cell FLAT (none 12/24,
armed 13/24, cross-origin instrument); this ground's candidacy 14 of
24 (P026); P024 refused by qualification, zero self-delivery
measurements exist.

## Constraints

Protected surfaces, tier 2: judge protocol v1, the firewall, watch
gates, lesson gates, lessons.jsonl, watchlist.jsonl, menu.py,
runner.py, the pins, the canonical documents, all production stores.
No distillation, no chair memory, no pin changes, no gate changes.
The lesson rides byte-verbatim; any edit voids the cell. Tier rules
per CLAUDE.md. Per-path git staging only. On any wakeup, read git
log and this packet before writing anything. If wall time forces a
cut, complete stage A before any stage B run, and cut stage B's R
evenly if it must shrink; say so.

## Deliverables

Tests green, one commit staged per path, RESULTS appended to this
file: what ran, the gate arithmetic, the three-exit reading verbatim
with its caveat, observability named, effective-n reported, watch
data, what was fixed under tier 1, what was NOT done. FINDINGS its
own section when tier 2 items exist. Never claim beyond what ran.

## DESK CHECK (conductor, at cut time, verbatim output)

rule_checks: ['trimmed_mean([])', 'trimmed_mean([5, 5, 1, 9])']
delivery-path: menu serves line 8 single-store: 1 tool(s)
tool equals lesson concept+applies_when: True
line 8 md5: 588e6eaf31f77559556d15b2d44e040f
line 8 origin_seat: mistral:7b
line 8 concept: Handle empty and None inputs by returning an empty
list.
P024 stores B1, B2, N1, N2 against production: JSON-equal,
byte-different, serialization only; noted, not reused.

## RESULTS

Executed 2026-07-04 by a Claude Code session. Commits: 8bbb80d (the
harness, tests, and the fresh raw byte copy of production line 8,
before any model run) and the closing commit carrying this section.
Run selfdel31-20260704-204738 ran detached start to finish, no kill,
resume unused, 36 runs, every one checkpointed and persisted to
bench/runs. 326 tests green throughout. The seat neither taught nor
learned: no distillation, no chair memory, no production store
changes, every protected surface untouched. No tier 2 discoveries
were made, so this packet carries no FINDINGS section.

What ran, in the packet's order. All build gates re-ran as
committed, tested code before any model run and matched the desk
check: the byte check TRUE against production line 8 with position
asserted and md5 588e6eaf31f77559556d15b2d44e040f, identical to the
desk check value and pinned by test; the delivery-path check serving
exactly one tool through menu.query on the ground's own features,
equal to the lesson's concept plus applies_when, the production
serving path with a genuine pin match, nothing injected; the
rule-check annotation printed before any run. Audits recounted clean
from all 36 rows at close: armed tools=1 directives=0, none tools=0
directives=0, every row, and the interleave verified exact.

Stage A, fresh qualification: 19 passes, 5 fails of 24 canonical, 0
unrunnable, QUALIFIES at the standing mixed fraction. The candidacy
number moved again under fresh measurement (14 of 24 in P026, 19 of
24 here), the P027 precedent holding in the direction that opens
packets this time.

Stage B, the reading cells: none 15 of 24 canonical (1 unrunnable
row), armed 20 of 24 (0 unrunnable). The stage B none cell sits 4
under stage A's gate cell, movement at the bar's own size, absorbed
by the same-run interleaved design; stage A gates and is never the
baseline.

THE READING, the three-exit form applied verbatim at the 4-of-24
bar, armed against the stage B none cell only:

GAIN, and its first sentence carries both pre-registered candidate
causes: the movement has two live explanations, the seat's
tool-response trait and self-origin effects, the seat receiving its
own distilled lesson, and neither cause is chosen at this n. Armed
20 of 24 sits above none 15 of 24 by 5, more than the bar. The first
self-delivery evidence on the record points receptive, sized one
task, one seat, n=12 per cell, direction never a rate.

Observability, named per the standing doctrine: the fresh stage B
none cell sat at 15 of 24, neither ceiling nor floor, so BOTH exits
were observable, 9 readings of headroom upward and 15 downward. The
GAIN is read against a baseline that could have shown either sign.

Effective-n, per the standing addendum: the two rule checks disagree
inside rows, 7 of 12 none rows and 4 of 12 armed rows, so the
readings are not run-locked and the pooled 24-reading accounting
stands as the sizing, with the within-row correlation reported here
rather than assumed away. The claim does not collapse to n=12 runs;
it is one cell either way.

What this does to the trait series, said carefully: PACKET-019's
FLAT (none 12/24, armed 13/24, cross-origin instrument) stands at
its own n. This cell is the series' second measurement and its first
non-FLAT, on a self-origin instrument, and the two-cause caveat is
exactly why the two cells do not merge into one story: the seat may
be more receptive than the indifference lean suggested, or the seat
may respond to its own distilled content specifically. Neither is
chosen. The lean is not extended and not overturned; it now has a
countervailing measurement whose attribution is deliberately open.

Per-check canonical (none / armed): rule trimmed_mean([]) 11/12 to
12/12; rule trimmed_mean([5, 5, 1, 9]) 4/12 to 8/12; watch
trimmed_mean([3, 1, 2]) 4/12 to 7/12. The lesson's concept addresses
the empty-input trap and the empty-input check was already near
ceiling; the movement concentrated on the trim check, which the
concept does not address directly. Descriptive, beside the reading.

Boundary-watch, NO NAME, grounding no claim: the single watch column
moved up 3 of 12 in the armed cell, above the 2-of-12 per-check
size. Reported and left nameless.

Harm columns, the standing reconciliation: no column declined in the
armed cell at any size. There is no harm to reconcile.

Census, the standing instrument, descriptive: stage A none 12 of 12
sort-slice-average; stage B none 11 of 12 with 1 unrunnable; armed
10 of 12 with 2 other. Concentration held broadly through delivery;
the armed cell's 2-row drift to other shapes is inside recorded
census movement and claims nothing.

The one no-readings row, named: stage B none rep 3 failed to parse
(census unrunnable, ev 0.0), all rule checks counted as fails under
canon; shape-against-readings divergence 0 rows. The conductor's
replay ran at close: py selfdel31.py census, 36 rows, 0 mismatches.

Priors, named for what they are: P019's trait cell FLAT at its own
counter; this ground's candidacy 14 of 24 in P026, moved to 19 of 24
fresh; zero self-delivery measurements existed before this cell, and
P024's designed measurement was refused by qualification, so this is
the first.

Fixed under tier 1: nothing broke; resume stood ready and unused.

NOT done:
- No cause chosen between trait and self-origin: the caveat is the
  claim's shape, by pre-registration, and separating the two needs a
  cross-origin cell on this seat and ground, the conductor's cut.
- No trait-series upgrade, no casting entry, no registry annotation:
  the conductor's.
- No pin change, no gate change, no store touched; the lesson rode
  byte-verbatim through the production path, asserted twice.
- Nothing cut: stage A whole, stage B whole at R=12.

## CONDUCTOR DOWNGRADE, appended at the P032 close (2026-07-04)

The GAIN above is downgraded to an unreplicated single-cell
direction, per PACKET-032's pre-registered exit: the replication on
fresh cells read armed 16 of 24 against none 19 of 24, FAILS TO
REPLICATE, FLAT. The side-by-side, never pooled: gap 5 up here, gap
3 down there, identical bytes through the identical instrument, the
baseline itself moving 4 between packets. The two-cause caveat is
moot at this n: there is no replicated signal to attribute. The
per-check texture noted above did not recur. This section is the
filing the standing discipline requires, in the place the claim was
made; the cells above stay exactly as measured.
