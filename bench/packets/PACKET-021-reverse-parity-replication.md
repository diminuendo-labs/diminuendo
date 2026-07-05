# PACKET-021: The reverse and parity replication (PACKET-015 re-run whole)

Status: DONE
Owner: any Claude Code session. Read /CLAUDE.md first, then this, whole.

## Goal

PACKET-015's result is the thesis sentence at n=1: reverse transfer and
origin parity on liftable ground, a lean until it replicates. This
packet is the replication, the same design re-run whole with nothing
varied. If readings 1 and 2 fire again, the leans upgrade to replicated
results, still sized to one task, one seat, two measurements. If either
fails, the PACKET-015 lean is downgraded where it was made, by the
conductor.

## The cells

Performer qwen2.5-coder:7b, audience llama3.1:8b, task range_summary
only, v1 production path, pins live. Three cells at R=12 each, 36 runs,
interleaved per rep in the fixed order none, rev, hand, order logged.
Detached, checkpointed, resume-capable.

- none: no tools.
- rev: the PACKET-014 llama-origin lesson, byte-copied packet-local from
  PACKET-014-lessons.jsonl, byte-check asserted.
- hand: the PACKET-007 concept-shape distinctness lesson, byte-copied
  packet-local from PACKET-013-lesson_hand.jsonl, byte-check asserted.

## The drift bar, stated before the run

2 of 12, the recorded range_summary movement, as in PACKET-015.

## Report and the pre-registered reading, apply verbatim, signs stated

Per-check table, the rule check is range_summary([3, 1, 2, 2]), the
other four checks are the harm columns. Priors printed beside: P15 none
8/12, rev 12/12, hand 12/12; P13 R-none 8/12, R-hand 12/12; P7 none
0.50 at n=24. Tool audit from the rows: rev tools=1, hand tools=1, none
tools=0, every row.

The four readings, independent, each with its sign and the bar,
identical to PACKET-015's:
1. REVERSE TRANSFER: rev rule check ABOVE none by MORE than 2 of 12.
   Fires again and the reverse-transfer lean upgrades to a replicated
   result at two measurements.
2. ORIGIN PARITY: rev and hand within 2 of 12 of EACH OTHER while BOTH
   sit above none by more than 2 of 12. Fires again and the parity
   sentence upgrades to a replicated result at two measurements.
3. HAND LIFT: hand above none by more than 2 of 12, its third
   interleaved measurement.
4. HARM COLUMNS: all four non-rule checks, every cell. Every decline
   reported, above-bar declines said loudly, at-or-under-bar declines
   inside drift.

Any reading that fired in PACKET-015 and fails here is named in RESULTS
as a failed replication, and the downgrade is the conductor's to file.

## Gate

- Three cells at R=12, interleaved as specified, checkpointed, report
  persisted, per-check table with harm columns and priors, tool audit
  clean from the rows, both byte-checks asserted and reported.
- All four readings applied verbatim with their signs and the bar,
  independently.
- Tests green, per-path staging, honest RESULTS and FINDINGS.

## Constraints

- Protected surfaces, tier 2: judge protocol v1, firewall, watch gates,
  lesson gates, lessons.jsonl, watchlist.jsonl, canonical documents, all
  production stores (packet-local copies only).
- No lesson generation, no pin changes, no gate changes.
- Both lessons ride exactly as copied. Any edit voids the arm.
- If wall time forces a cut, cut R evenly across all three cells, and
  say so.

## FINDINGS

(none. The replication asked one question and answered it. The
baseline's movement between runs, 8 of 12 in PACKET-015 to 4 of 12
here, is the recorded drift doing what the doctrine already says it
does, and the same-run design absorbed it: both armed cells cleared
the same-run baseline by margins no drift explains.)

## RESULTS

Executed 2026-07-03 by a Claude Code session. Commits: 32485ae (harness
and byte-checked materials) and the closing commit carrying this
section. Run parity21-20260703-214759 ran detached start to finish, no
kill, resume unused. 189 tests green throughout.

Session-start note, one line as promised: git status flagged
bench/lessons.jsonl modified before any work began; the investigation
found the content byte-identical to HEAD (11 lessons both sides, empty
diff), stat noise only, and the flag cleared itself. No protected
surface was touched by anyone.

What ran: PACKET-015's design whole, nothing varied. Performer qwen,
audience llama, v1 production path, task range_summary. Three cells at
R=12 each, 36 runs, interleaved per rep in the fixed order none, rev,
hand, order logged. Byte checks asserted before any arm ran: the rev
store byte-identical to PACKET-014-lessons.jsonl, the hand store
byte-identical to PACKET-013-lesson_hand.jsonl. Both lessons loaded
through the production path, pins live. Tool audit clean from the rows:
rev tools=1, hand tools=1, none tools=0, every row. GATE passed. The
drift bar, stated before the run: 2 of 12.

Per-check table (n=12 per cell; priors beside):

| check | none | rev | hand | priors |
|---|---|---|---|---|
| [3, 1, 2, 2] RULE | 0.33 (4/12) | 0.92 (11/12) | 0.83 (10/12) | P15: none 8/12, rev 12/12, hand 12/12. P13: 8/12 to 12/12. P7: none 0.50 at n=24 |
| [1, 2, 3, 5] (harm) | 0.67 | 0.67 | 0.67 | |
| [5, 3, 1] (harm) | 0.67 | 0.67 | 0.67 | |
| [] (harm) | 1.00 | 1.00 | 1.00 | |
| [7] (harm) | 1.00 | 1.00 | 1.00 | |

Pooled rule check: none 4/12, rev 11/12, hand 10/12.

The four pre-registered readings, applied verbatim with their signs and
the bar, independently, identical to PACKET-015's. No reading that
fired there fails here: there are NO failed replications to name.
1. REVERSE TRANSFER: FIRES AGAIN. Rev sits above none by 7 of 12,
   more than the bar. The reverse-transfer lean UPGRADES TO A
   REPLICATED RESULT at two measurements: the llama-origin
   machine-born lesson lifted qwen through the production menu twice,
   in two independent runs, against two same-run baselines.
2. ORIGIN PARITY: FIRES AGAIN. Rev and hand sit 1 of 12 apart, within
   the bar of each other, while both clear none by more than the bar
   (7 of 12 and 6 of 12). The parity sentence UPGRADES TO A REPLICATED
   RESULT at two measurements: inherited content performs comparably
   to the seat's best known content on the same ground, twice.
3. HAND LIFT: FIRES, its third interleaved measurement, and the three
   run 8/12 to 12/12, 8/12 to 12/12, 4/12 to 10/12: three same-run
   lifts of 4 to 6 passes each.
4. HARM COLUMNS: CLEAN EVERYWHERE, the sixth consecutive clean harm
   measurement on this seat under matched pinned tools. Every non-rule
   check is identical across all three cells; there is no decline to
   report at any size.

Findings, sized to what two measurements allow:
The thesis sentence replicated. Reverse transfer and origin parity,
each measured twice on the same design with the same byte-identical
materials against fresh same-run baselines, fired both times with
margins past the bar both times. The claim's size grows by exactly one
notch and no more: one task, one seat, one lesson each way, two
measurements, direction never a rate. The none baseline's run-to-run
movement (8 of 12 down to 4 of 12) is the largest drift yet recorded
on this task and both armed cells cleared it from inside the same run,
which is what the interleaved design is for. What the record now
holds: transfer through the production menu measured in both
directions, the reverse direction replicated, parity replicated, and
the machine-born lesson's full no-hands lineage intact from llama's
break to qwen's lift, twice.

Fixed under tier 1: nothing broke; resume stood ready and unused.

NOT done:
- Nothing cut: three cells at R=12 in full, interleaved as specified.
- No lesson generated, no pin changed, no gate changed; both lessons
  rode byte-verbatim, asserted.
- Any upgrade of the claim beyond two measurements, any doctrine
  consequence, and the PACKET-020 admission ruling (all the
  conductor's and Brad's).
