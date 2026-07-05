# PACKET-013: The task-and-topic contrast (one seat, two tasks, one run)

Status: DONE
Owner: any Claude Code session. Read /CLAUDE.md first, then this, whole.

## Goal

PACKET-012 left the open contrast task-and-topic shaped: tie lessons of
any authorship measured so far do not help qwen on longest_word through
the menu, while the same seat took the record lift from matched content
on range_summary in PACKET-007. This packet puts both tasks inside one
interleaved run on the same seat, which reads the contrast directly and
executes the drift doctrine (DECISIONS 2026-07-03) at the same time:
same-run baselines, interleaved arms, no cross-run comparison.

## The cells

Performer qwen2.5-coder:7b, audience llama3.1:8b, v1 production path.
Four cells at R=12 each, 48 runs, 96 model calls, detached, checkpointed,
resume-capable, confirm/transfer harness pattern.

- L-none: longest_word, no tools.
- L-prod: longest_word, the two llama-origin tie lessons, copied
  packet-local byte-verbatim from PACKET-012-lessons_prod.jsonl,
  byte-check asserted. The replicated decline's third measurement.
- R-none: range_summary, no tools.
- R-hand: range_summary, the PACKET-007 concept-shape distinctness
  lesson, copied byte-verbatim from PACKET-007-lessons.jsonl (the line
  with shape "concept" and topic "distinctness"), byte-check asserted.
  It carries confidence and provenance, so it loads through the
  production path from a packet-local store. If any gate rejects it
  anyway, use the PACKET-012 injection surface, pinned by test, and say
  so in FINDINGS.

Interleaving: for each rep index 0 through 11, run all four cells in the
fixed order L-none, L-prod, R-none, R-hand before the next rep. The
order is logged. Prompts are identical within a task across its two
cells.

## Report and the pre-registered reading, apply verbatim, signs stated

Per-check table per task, rule checks marked, harm columns mandatory,
each task read ONLY against its own same-run none cell. PACKET-011 and
PACKET-012 cells printed beside as priors for longest_word, PACKET-007
cells as priors for range_summary. Tool audit from the rows: L-prod
tools=2, R-hand tools=1, none cells tools=0, every row.

Four readings, independent, each with its sign:

1. TASK MODERATION, the headline: R-hand pooled rule checks ABOVE R-none
   AND L-prod pooled rule checks BELOW L-none, both inside this one run.
   Then the same seat through the same menu on the same day gains on one
   task and loses on the other, the moderator is task-and-topic, and the
   next design targets what separates the tasks, not who authored the
   lesson.
2. RANGE LIFT REPLICATION: R-hand ABOVE R-none, both rule checks up,
   pooled differing. Replicates PACKET-007's lift under the drift
   doctrine. If this does not fire, the PACKET-007 record-lift claim is
   downgraded by the conductor where it was made, in DECISIONS and in
   the PACKET-007 record.
3. LONGEST DECLINE, THIRD MEASUREMENT: L-prod pooled BELOW L-none. Third
   same-direction measurement of the decline. It stays a lean and the
   writeup says direction, never a rate.
4. HARM COLUMNS: every non-rule check in every cell. Any decline under
   matched tools outranks everything else in the writeup, say it loudly.

A gap smaller than 4 of 24 on any comparison is reported as inside the
recorded drift and claims nothing, per the doctrine.

## Gate

- Four cells at R=12, interleaved as specified, checkpointed, report
  persisted, per-check tables with harm columns and same-run baselines,
  priors printed beside, tool audit clean from the rows, byte-checks on
  both lesson stores asserted and reported.
- All four readings applied verbatim with their signs, independently.
- Tests green, per-path staging, honest RESULTS and FINDINGS.

## Tier 1 authorization, ruled in DECISIONS 2026-07-03

menu.query currently raises KeyError on a lesson missing required
fields. Fix it in this packet's terrain: decline the lesson instead of
raising, add the test, one DECISIONS line, name it in RESULTS. No other
menu behavior changes.

## Constraints

- Protected surfaces, tier 2: judge protocol v1, firewall, watch gates,
  lesson gates, lessons.jsonl, watchlist.jsonl, canonical documents, all
  existing stores (packet-local copies only).
- No lesson generation, no pin changes, no gate changes.
- Both lesson stores are used exactly as copied. Any edit voids the arm.
- If wall time forces a cut, cut R evenly across all four cells, and say
  so.

## FINDINGS

Tier 2, flagged and not fixed:

1. A grounded hypothesis for what separates the tasks, from the run's
   own outputs: tools nudge the amplifier toward the canonical idiom,
   and the tasks split on whether the canonical idiom honors the rule.
   Two sampled failing L-prod outputs (runs 20260703-120034-f589c7 and
   20260703-120205-7f70af, both ev 0.50) are the textbook one-liner,
   max(words, key=len), which returns the FIRST longest word and
   breaks the stated last-tie rule by construction, while the lessons
   riding those runs say to follow the stated direction. Honoring
   longest_word's rule requires REPLACING the idiomatic core with a
   manual pass; honoring range_summary's rule requires ADDING a step
   (distinct before sort) that leaves the idiom intact, and that task
   lifted to 12 of 12 armed. If this holds, the delivery moderator is
   whether the stated rule fights the canonical solution shape, which
   is a property of the task, measurable in advance, and a casting
   input the spec's forecaster family could consume. What I would do:
   classify apply tasks by idiom-conflict and test the moderator
   directly. Design-level, the conductor's call.

## RESULTS

Executed 2026-07-03 by a Claude Code session. Commits: 6f10d4e (tier 1
menu fix, harness, byte-checked materials) and the closing commit
carrying this section. Run contrast13-20260703-120009 ran detached
start to finish, no kill, resume unused. 146 tests green throughout.

Tier 1, as authorized in the packet: menu.query now declines a lesson
missing the fields the menu consumes instead of raising KeyError, no
other menu behavior changed, pinned by test; the PACKET-012 gate-check
test was updated to pin the new behavior with the history noted in its
docstring. Named here as required.

What ran: performer qwen, audience llama, v1 production path. Four
cells at R=12 each, 48 runs, 96 model calls, interleaved by rep in the
fixed order L-none, L-prod, R-none, R-hand, the order logged per rep in
the run log. Byte checks asserted before any arm ran and again at
resume-load: the prod store is byte-identical to
PACKET-012-lessons_prod.jsonl, and the hand store's single line is
byte-identical to its source line in PACKET-007-lessons.jsonl (selected
by shape concept, topic distinctness). The hand lesson carries
confidence and provenance and loaded through the production path, no
injection surface needed. Tool audit clean from the rows: L-prod
tools=2, R-hand tools=1, none cells tools=0, on every row. GATE passed.

Per-check tables, each task against its own same-run none cell only,
priors beside:

longest_word (L-none / L-prod; priors P11 none 0.67 menu 0.42, P12
none 0.50 prod 0.33 hand 0.42):
| check | L-none | L-prod |
|---|---|---|
| 'cat door bird' RULE | 0.58 | 0.08 |
| 'a bb cc d' RULE | 0.50 | 0.08 |
| '' (harm) | 1.00 | 1.00 |
| 'one' (harm) | 1.00 | 1.00 |
Pooled rule checks: L-none 13/24, L-prod 2/24.

range_summary (R-none / R-hand; priors P7 none 0.50 at n=24,
concept arm 0.92 at n=12):
| check | R-none | R-hand |
|---|---|---|
| [3, 1, 2, 2] RULE | 0.67 | 1.00 |
| [1, 2, 3, 5] (harm) | 0.33 | 0.42 |
| [5, 3, 1] (harm) | 0.33 | 0.42 |
| [] (harm) | 1.00 | 1.00 |
| [7] (harm) | 1.00 | 1.00 |
Pooled rule checks: R-none 8/12, R-hand 12/12.

The four pre-registered readings, applied verbatim with their signs,
independently, each task read only against its own same-run none cell:
1. TASK MODERATION, the headline: FIRES. R-hand pooled (12/12) sits
   above R-none (8/12) AND L-prod pooled (2/24) sits below L-none
   (13/24), both inside this one interleaved run. The same seat through
   the same menu on the same day gained on one task and lost on the
   other. The moderator is task-and-topic, and the next design targets
   what separates the tasks, not who authored the lesson (FINDINGS 1
   offers the grounded candidate).
2. RANGE LIFT REPLICATION: FIRES. The task's one rule check moved up
   (0.67 to 1.00) and the pooled passes differ (8/12 against 12/12).
   The gap arithmetic against the drift bar, stated: the gap is 4 of
   12, one third, and the drift bar is 4 of 24, one sixth, so the gap
   clears the bar as a proportion and equals it as a raw count on half
   the trials. PACKET-007's lift replicates under the drift doctrine.
   No downgrade goes to the conductor.
3. LONGEST DECLINE, THIRD MEASUREMENT: FIRES. L-prod (2/24) sits below
   L-none (13/24), a gap of 11 of 24, the largest of the three
   same-direction measurements (6/24, then 4/24, now 11/24). Per the
   packet it stays a lean and this writeup says direction, never a
   rate.
4. HARM COLUMNS: CLEAN EVERYWHERE. Both longest_word boundary checks
   1.00 in both cells; both range_summary boundary checks 1.00 in both
   cells; the two range_summary content checks moved up under tools
   (0.33 to 0.42 each), not down. Nothing declined, nothing to say
   loudly, and the amplifier's collateral-safety property under pinned
   tools holds for the fourth measurement running.

Findings, sized to the n:
The contrast the record has been circling since PACKET-011 is now
measured inside one run, and it is real at this size: the same seat,
same menu, same hour, lifted a distinctness task to perfect while
collapsing a tie task to near zero, with every boundary check in every
cell untouched. Both same-run gaps clear the drift bar; the sub-bar
gaps (the range content checks, up 1 of 12 each) claim nothing. The
task, not the author, moderates delivery on this seat: PACKET-012
showed hand-authored and production tie lessons landing within 2 of 24
of each other, and this run shows the identical production pair
swinging from harmless to harmful as the task changes. The sampled
armed failures give the mechanism a face: qwen answered the tie task
with the canonical first-tie idiom while holding tools that state the
last-tie rule. Everything here is one seat, two tasks, n=12 per cell,
and the writeup claims direction at that size, never rates.

Fixed under tier 1: the authorized menu fix, named above.

NOT done:
- Nothing cut: four cells at R=12 in full, interleaved as specified.
- No lesson generated, no pin changed, no gate changed; both stores
  byte-verbatim, asserted.
- Not attempted: the idiom-conflict classification and its direct test
  (FINDINGS 1), and any third-seat work (stays deferred under the
  standing rulings; nothing here promotes it).
