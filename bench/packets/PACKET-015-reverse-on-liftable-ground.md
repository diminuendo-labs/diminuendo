# PACKET-015: The clean reverse test (origin parity on liftable ground)

Status: DONE
Owner: any Claude Code session. Read /CLAUDE.md first, then this, whole.

## Goal

This is the measurement the transfer bet has been waiting for. The
record holds four consistent forward measurements (qwen-origin lessons
lifting llama) and zero clean reverse ones: every reverse attempt ran on
ground where nothing helps the receiving seat. PACKET-013 established
the liftable ground (qwen gains on range_summary through the menu, 8/12
to 12/12) and PACKET-014 supplied the material (a gated llama-origin
distinctness lesson whose pins match that ground). This packet delivers
the inherited lesson and the seat's best known content on the same
ground, same run, and reads them against each other. The parity reading
is the thesis sentence: inherited lessons perform comparably to the
seat's own best, or they do not.

## The cells

Performer qwen2.5-coder:7b, audience llama3.1:8b, task range_summary
only, v1 production path, pins live. Three cells at R=12 each, 36 runs,
72 model calls, detached, checkpointed, resume-capable.

- none: no tools.
- rev: the PACKET-014 llama-origin lesson, copied packet-local
  byte-verbatim from PACKET-014-lessons.jsonl, byte-check asserted.
- hand: the PACKET-007 concept-shape distinctness lesson, copied
  packet-local byte-verbatim from PACKET-013-lesson_hand.jsonl,
  byte-check asserted.

Interleaving: for each rep index 0 through 11, run all three cells in
the fixed order none, rev, hand before the next rep, order logged.
Prompts identical across cells.

## The drift bar for this task, stated before the run

Recorded baseline movement on range_summary: 0.50 (PACKET-007, n=24) to
0.67 (PACKET-013, n=12), a movement of 2 of 12. The bar is 2 of 12. A
gap at or under the bar is inside recorded drift and claims nothing.

## Report and the pre-registered reading, apply verbatim, signs stated

Per-check table, the rule check is range_summary([3, 1, 2, 2]), the
other four checks are the harm columns. Priors printed beside: P13
R-none 8/12 and R-hand 12/12, P7 none 0.50 and concept arm 0.92. Tool
audit from the rows: rev tools=1, hand tools=1, none tools=0, every row.

Four readings, independent, each with its sign and the bar:

1. REVERSE TRANSFER ON LIFTABLE GROUND, the headline: rev rule check
   ABOVE none by MORE than 2 of 12. Fires and it is the first measured
   cross-family transfer in the reverse direction, sized exactly: one
   task, one seat, one lesson, n=12, direction never a rate.
2. ORIGIN PARITY, the thesis sentence: rev and hand within 2 of 12 of
   EACH OTHER while BOTH sit above none by more than 2 of 12. Fires and
   inherited content performed comparably to the seat's best known
   content on the same ground, which is the load-bearing bet of the
   chair-holds-memory thesis, measured at this size for the first time.
3. HAND LIFT, SECOND REPLICATION: hand rule check above none by more
   than 2 of 12, under the interleaved design for the second time.
4. HARM COLUMNS, doctrine reconciliation pre-registered: all four
   non-rule checks, every cell. Every decline is reported. A decline
   above the bar under a matched tool outranks everything else in the
   writeup, say it loudly. A decline at or under the bar is reported as
   inside recorded drift and claims nothing.

## Gate

- Three cells at R=12, interleaved as specified, checkpointed, report
  persisted, per-check table with harm columns, priors beside, tool
  audit clean from the rows, both byte-checks asserted and reported.
- All four readings applied verbatim with their signs and the bar,
  independently.
- Tests green, per-path staging, honest RESULTS and FINDINGS.

## Constraints

- Protected surfaces, tier 2: judge protocol v1, firewall, watch gates,
  lesson gates, lessons.jsonl, watchlist.jsonl, canonical documents, all
  production stores (packet-local copies only).
- No lesson generation, no pin changes, no gate changes.
- Both lessons are used exactly as copied. Any edit voids the arm.
- If wall time forces a cut, cut R evenly across all three cells, and
  say so.

## FINDINGS

(none. Nothing touched a protected surface and nothing needs a ruling:
the run answered the questions it was built to ask. The one observation
worth carrying lives in RESULTS where it belongs: the rev lesson is the
production pipeline end to end, a llama break distilled at full gates,
pinned, menu-delivered, and it lifted the other seat.)

## RESULTS

Executed 2026-07-03 by a Claude Code session. Commits: bf4587d (harness
and byte-checked materials) and the closing commit carrying this
section. Run parity15-20260703-151821 ran detached start to finish, no
kill, resume unused. 159 tests green throughout.

What ran: performer qwen, audience llama, v1 production path, task
range_summary only. Three cells at R=12 each, 36 runs, 72 model calls,
interleaved per rep in the fixed order none, rev, hand, the order
logged per rep in the run log. Byte checks asserted before any arm ran:
the rev store is byte-identical to PACKET-014-lessons.jsonl and the
hand store is byte-identical to PACKET-013-lesson_hand.jsonl. Both
lessons loaded through the production path with pins live, no injection
surface needed. Tool audit clean from the rows: rev tools=1, hand
tools=1, none tools=0, on every row. GATE passed. The drift bar, stated
in the packet before the run: 2 of 12.

Per-check table (n=12 per cell; priors beside):

| check | none | rev | hand | priors |
|---|---|---|---|---|
| [3, 1, 2, 2] RULE | 0.67 (8/12) | 1.00 (12/12) | 1.00 (12/12) | P13: R-none 8/12, R-hand 12/12. P7: none 0.50 (n=24), concept 0.92 (n=12) |
| [1, 2, 3, 5] (harm) | 0.67 | 0.75 | 0.75 | |
| [5, 3, 1] (harm) | 0.67 | 0.75 | 0.75 | |
| [] (harm) | 1.00 | 1.00 | 1.00 | |
| [7] (harm) | 1.00 | 1.00 | 1.00 | |

Pooled rule check: none 8/12, rev 12/12, hand 12/12. The same-run none
baseline reproduced PACKET-013's same-run baseline exactly, 8 of 12
both times.

The four pre-registered readings, applied verbatim with their signs and
the bar, independently:
1. REVERSE TRANSFER ON LIFTABLE GROUND, the headline: FIRES. The rev
   rule check sits above none by 4 of 12, more than the bar. This is
   the first measured cross-family transfer in the reverse direction,
   sized exactly as the packet demands: one task, one seat, one lesson,
   n=12, direction never a rate.
2. ORIGIN PARITY, the thesis sentence: FIRES. Rev and hand sit within
   the bar of each other, at zero apart, 12 of 12 both, while both sit
   above none by 4 of 12, more than the bar. Inherited content
   performed comparably to the seat's best known content on the same
   ground: the load-bearing bet of the chair-holds-memory thesis,
   measured at this size for the first time, and at this n the
   inherited lesson and the hand-authored one are indistinguishable.
3. HAND LIFT, SECOND REPLICATION: FIRES. Hand sits above none by 4 of
   12, more than the bar, under the interleaved design for the second
   time, with the same cell values as PACKET-013 (8/12 to 12/12).
4. HARM COLUMNS, all four non-rule checks, every cell: NO DECLINES
   ANYWHERE. The two content-adjacent checks moved up 1 of 12 in both
   armed cells, at or under the bar, inside recorded drift, claiming
   nothing. The two boundary checks are 12 of 12 in every cell. Fifth
   consecutive measurement with the amplifier's harm column clean
   under matched pinned tools.

Findings, sized to the n:
The measurement the transfer bet was waiting for came back affirmative
on every pre-registered reading. The rev lesson is the production
pipeline end to end with zero hand intervention anywhere in its
lineage: llama failed sum_distinct in a supply probe, the engine
distilled the failure against its own passing run at full gates, the
pins routed the lesson to the one apply task its topic matches, the
menu delivered it, and the other seat went from 8 of 12 to 12 of 12
holding it, exactly matching what the conductor's hand-authored best
achieved beside it in the same interleaved run. Transfer now runs in
both directions on the record: four replicated forward measurements
and one clean reverse measurement on ground chosen by the idiom
doctrine's prediction. Every claim here is one task, one seat, one
lesson, n=12: direction, never a rate, and the parity sentence is
exactly that size too.

Fixed under tier 1: nothing broke; resume stood ready and unused.

NOT done:
- Nothing cut: three cells at R=12 in full, interleaved as specified.
- No lesson generated, no pin changed, no gate changed; both lessons
  rode byte-verbatim, asserted.
- Not attempted: replication of the reverse cell, wider-ground parity,
  or any third-seat move (the standing rulings hold; what this result
  means for them is the conductor's reading, not this session's).
