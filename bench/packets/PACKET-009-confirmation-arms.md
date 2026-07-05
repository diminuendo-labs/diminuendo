# PACKET-009: The confirmation arms (clean stores, pins live)

Status: DONE (closed by the conductor; see RESULTS)
Owner: any Claude Code session. Read /CLAUDE.md first, then this, whole.

## Goal

Measure the hardened stack end to end. Every prior treatment measurement
used stores that predate some part of the machinery (unpinned copies,
hand-authored variants, pre-screen lessons). The genpass 20260703-053623
store is the first fully production-grade supply: conditional, declarative,
topic-pinned, direction-pinned. This packet measures it through the
production menu with every pin live, in both teaching directions.

## Work item 1: within-task phrasing alignment (conductor-approved)

The within-task distiller prompt aligns to the sibling prompt's class-level
phrasing requirement: the lesson names the class's stated rule,
conditionally, never the one task's instance of it. Pinned by the
prompt-capture test. No regeneration in this packet; the change serves
future passes.

## Work item 2: enumerate the matched pairings

Programmatically, from the pins: for every lesson in the 053623 stores and
every apply task in probe_tasks, a pairing is matched when rule_class
matches, rule_topic matches or the lesson is wildcard, and stated_direction
matches or is unpinned. Copy the stores packet-local, verbatim. Report the
full pairing table, including the structurally empty cells: a lesson whose
pins match no apply task is a supply finding, name it. Expected pairings at
minimum: qwen tie lessons to llama on longest_word (the fourth measurement
of that comparison, now at production posture), and the B distinctness
lesson to qwen on range_summary (the PACKET-007 record lift, retested
through the real menu instead of hand-authored variants).

## Work item 3: the arms

For every matched pairing where the performer is the other seat from the
lesson's origin: arms none and menu, R=12 per arm per task, production
menu path, pins live, tools recorded per run and asserted nonzero on
matched armed runs. Add one deliberate topic-mismatch cell as the pin
regression: assert tools=0 on every such armed run, cheap, no extra model
cost beyond its none arm if reused.

## Report and the pre-registered reading

Per-check tables per pairing, harm columns always, prior rates from
PACKETS 004 through 007 beside any overlapping check.
- The tie pairing is read as replication four: consistent direction
  sustains the transfer evidence, a flat result gets said plainly and
  weighed against three priors, not spun.
- The distinctness pairing is read against PACKET-007's lift: if the
  production menu with pins reproduces the direction, the amplifier-plus-
  tight-pins doctrine has its confirmation; if it does not, say so and the
  doctrine goes back on the table.
- Structural empties and any harm signal outrank everything else in the
  writeup.

## Gate

- Phrasing alignment pinned by test. Pairing table complete with empties
  named. All matched cross-seat pairings at R=12 per arm, checkpointed,
  report persisted, tool audit clean, pin regression asserted.
- The reading applied verbatim. Tests green, per-path staging only,
  commits, honest RESULTS and FINDINGS.

## Constraints

- Protected surfaces, tier 2: judge protocol v1, firewall, watch gates,
  lessons.jsonl, watchlist.jsonl, canonical documents. The phrasing
  alignment in work item 1 is conductor-approved and in scope.
- No lesson editing, no new generation. The 053623 stores ride verbatim.
- If wall time forces a cut, cut R evenly within a pairing, never drop a
  pairing, and say so.

## FINDINGS

(none raised by the session; it was environment-killed after its build
commit. The conductor's own reading of the enumeration is in RESULTS.)

## RESULTS

Closed 2026-07-03 by the conductor. The session died after commit 54abfff;
the detached run finished alone (confirm-20260703-064149, gate PASSED in
its log); every claim below verified against the report and rows, not any
account.

What ran: work item 1 shipped and pinned (within-task prompt aligned to
class-level phrasing, prompt-capture test). Pairing enumeration from pins,
the pin regression (4 of 4 mismatch cells, tools=0 asserted from rows),
and the one matched cross-seat cell at R=12 per arm, 48 runs, all
checkpointed. 128 tests green at the session's last commit.

The enumeration is the packet's first result: three of five lessons are
STRUCTURALLY EMPTY, their pins match no apply task. Both punctuation-
pinned normalize lessons and the pairs-pinned distinctness lesson have no
in-pool target. Consequence one: the distinctness retest of PACKET-007's
record lift was UNREACHABLE, because the real lesson pins to pairs and
range_summary's stated rule is values. The pin is correct, the PACKET-007
lift used a hand-authored values-matched variant, so the doctrine
(amplifier plus tight pins) remains doctrine, not confirmed, exactly as
the pre-registered reading requires. Consequence two, the supply
directive: correct narrowing has a coverage cost, and supply topics and
apply topics must overlap or the store is a shelf of tools with no
matching job. Three of five is the current overlap failure rate.

The one matched cell is REPLICATION FOUR, and it is the strongest and
cleanest measurement this project has produced: qwen's tie lessons through
the production menu, pins live, moved llama's rule checks 0.17 to 0.92
each (pooled 4 of 24 to 22 of 24) at n=12 per arm, with the non-rule
checks unharmed (0.92 to 1.00 and 1.00 to 1.00). Four measurements, four
configurations, one direction, consistent, and largest under the fully
hardened stack. The pre-registered reading: the transfer evidence is
sustained and strengthened. Still one direction, still one rule class,
still small models, and the claim stays exactly that size.

NOT done: the distinctness pairing (structurally unreachable, above), any
reverse-direction cell (no llama-origin lesson matches a qwen-headroom
task in this pool), RESULTS by the executing session (dead). Nothing in
scope was cut.

Correction, appended 2026-07-03 after the session's chat-only report: the
"48 runs" line above conflates counts. The cell is 24 runs (12 per arm),
each run making two model calls, 48 calls total. Every n and every rate
stands unchanged. The conflation was the conductor's.
