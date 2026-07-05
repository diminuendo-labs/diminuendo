# PACKET-011: The reverse cell (transfer back, amplifier confirmed or not)

Status: DONE
Owner: any Claude Code session. Read /CLAUDE.md first, then this, whole.

## Goal

The single most informative unmeasured cell in the record. PACKET-010 made
it reachable: two llama-origin tie lessons (B/longest_run_char within-task,
B/max_index sibling, both pinned tie_break, direction, last) match
longest_word, a task where qwen has headroom. Measuring it answers two
pre-registered questions at once: does transfer run in the reverse
direction (llama teaching qwen), and does the amplifier seat under matched,
fully pinned tools through the production menu gain without harm, the
doctrine PACKET-009 could not reach.

## The arms

Performer qwen2.5-coder:7b, audience llama3.1:8b, task longest_word only.
Arms none and menu (the two llama-origin lessons from the 081801 B store,
copied packet-local verbatim, delivered through the production menu path,
pins live). R=12 per arm, 24 runs, 48 model calls, detached, checkpointed,
resume-capable. Tools recorded per run and asserted nonzero on every armed
run. Use the confirm/transfer harness pattern as is.

## Report and the pre-registered reading, apply verbatim

Per-check table, rule checks marked, harm column mandatory, prior rates
beside overlapping checks (llama's cells from PACKETS 004 through 009 for
reference, and the demand table's qwen direction evidence, 0.67 at n=3,
which the none arm replaces with a real baseline).
- Reverse transfer: both rule checks move the same direction armed versus
  none AND the pooled rule-check passes differ. Then transfer is
  bidirectional at this scale and the writeup says so at exactly that
  size. Otherwise report the deltas and call it inside noise.
- Amplifier doctrine: the harm column decides. Non-rule checks unharmed
  under matched pinned tools confirms amplifier-plus-tight-pins. Any harm
  signal on the amplifier under MATCHED tools outranks everything else in
  the writeup, say it loudly: it would mean pins bound the wrong hazard
  and the doctrine goes back on the table.
- Both questions read independently. A flat rule-check result with a
  clean harm column is a real and reportable combination.

## Gate

- Both arms at R=12, checkpointed, report persisted, per-check table with
  harm column, tool audit clean from the rows.
- The reading applied verbatim, both questions answered separately.
- Tests green, per-path staging, honest RESULTS and FINDINGS.

## Constraints

- Protected surfaces, tier 2: judge protocol v1, firewall, watch gates,
  lessons.jsonl, watchlist.jsonl, canonical documents, all existing
  stores (packet-local copies only).
- No lesson editing, no generation, no pin changes.
- If wall time forces a cut, cut R evenly across both arms, and say so.

## FINDINGS

Tier 2, flagged and not fixed:

1. Production lessons carry source-task residue, and the residue is
   what the amplifier obeys. The two llama-origin lessons name
   "character runs" and "the last occurrence or longest run", their
   source tasks' nouns, despite the class-level phrasing instruction.
   Delivered onto longest_word, whose stated rule is about the last
   WORD among ties, that residue is adjacent but not identical, and the
   rule checks declined while the boundary checks held. PACKET-007's
   record lift on this same seat came from a hand-authored lesson with
   zero residue ("honor the distinctness the task states"). The
   contrast suggests the hazard the pins bound is topic mismatch, and
   the hazard that remains is content residue inside a matched topic.
   Why the residue survives: the aim screen demands token overlap with
   the failing check, which pulls source-task nouns INTO the rule text,
   while the phrasing instruction pushes them out. The two gates lean
   against each other. What I would do: let the class vocabulary alone
   carry the aim ground for sibling and class-phrased lessons, or add a
   residue screen (source-task function-name tokens banned from lesson
   text). Both are gate changes, a raised hand, and they feed the
   conductor's pre-registered diagnosis split (DECISIONS 2026-07-03,
   the middle-cell ruling): the none arm showed real headroom, so the
   production-store lessons get diagnosed against PACKET-007's
   hand-authored lift, and this is that diagnosis's first exhibit.

## RESULTS

Executed 2026-07-03 by a Claude Code session. Commits: 495b700 (harness
and materials) and the closing commit carrying this section. Run
reverse-20260703-095406 ran detached start to finish, no kill, resume
unused. 132 tests green throughout.

What ran: performer qwen, audience llama, v1 production path, task
longest_word only. Arms none and menu at R=12 each, 24 runs, 48 model
calls, all checkpointed. The two llama-origin tie lessons rode
packet-local and verbatim from the 081801 B store, both through the
full gates at load, both delivered on every armed run (tools=2 on 12 of
12, min 2, audit clean). GATE passed in the run log.

Per-check pass rates (n=12 per arm; prior rates for the same checks
beside, llama's cells for reference, then qwen):

| check | none | menu | priors |
|---|---|---|---|
| 'cat door bird' RULE | 0.67 | 0.42 | llama: P4 0.00 to 0.25, P6 0.08 to 0.50, P9 0.17 to 0.92. qwen unarmed: 0.67 at n=3 (demand table), now 0.67 at n=12 |
| 'a bb cc d' RULE | 0.67 | 0.42 | llama: P4 0.00 to 0.33, P6 0.08 to 0.50, P9 0.17 to 0.92. qwen unarmed: same as above |
| '' (harm column) | 1.00 | 1.00 | |
| 'one' (harm column) | 1.00 | 1.00 | |

Pooled rule checks: none 16/24, menu 10/24.

The pre-registered readings, applied verbatim and independently:
- REVERSE TRANSFER: both rule checks moved the same direction armed
  versus none, and the pooled rule-check passes differ (16/24 against
  10/24). The direction is DOWN, minus 0.25 on each check. The
  criterion is unsigned, exactly as in PACKET-006, so its letter is met
  with a negative sign, and no transfer claim is made: transfer is NOT
  shown to be bidirectional at this scale. The deltas are reported as
  they are. At n=12 a 16-to-10 pooled decline is a lean, not a settled
  effect, and the writeup claims only the lean.
- AMPLIFIER DOCTRINE: the harm column decides, and the harm column is
  clean: both non-rule checks 12 of 12 in both arms. By the verbatim
  criterion, amplifier-plus-tight-pins is CONFIRMED on the harm column.
  AND, said loudly because the packet demands any harm signal on the
  amplifier under matched tools outrank everything: the RULE checks
  declined under matched, fully pinned tools. The decline sits outside
  the pre-registered harm column, which was defined as the non-rule
  checks, but it is a harm-shaped signal on the treatment target
  itself. Both facts stand together: the pins confined the damage to
  nothing outside the rule the lessons address, and the lessons made
  the rule itself worse, not better, on this seat at this n.
- Read against the conductor's pre-registered middle-cell ruling
  (DECISIONS, logged before this run was read): the outcome is neither
  flat-and-clean nor bidirectional-and-clean, so no third-seat
  promotion and no deferral by flatness. The none arm's baseline is
  0.67, real headroom, not ceiling, which selects the ruling's second
  diagnosis branch: production-store lessons against PACKET-007's
  hand-authored lift on the same seat. FINDINGS 1 is that diagnosis's
  first exhibit: source-task residue in the production lessons, absent
  from the hand-authored one that lifted.

Findings, sized to the n:
The most informative cell in the record returned the most informative
kind of answer: a split. The amplifier seat under matched pinned tools
took no collateral damage anywhere the pins were built to protect, and
still lost ground on the very rule the tools address, 0.67 to 0.42 on
both checks at n=12. The demand table's n=3 direction evidence (0.67)
reproduced exactly as the real n=12 baseline, and the four-times
replicated forward direction is untouched by this result. What this
cell adds is a boundary on the transfer claim: qwen-to-llama through
the menu lifts, llama-to-qwen with these two lessons does not, and the
leading suspect is lesson content residue rather than delivery,
because this same seat gained 0.50 to 0.92 in PACKET-007 from a
residue-free hand-authored lesson through the same menu path. One run,
one task, one store: the claim stays that size.

Fixed under tier 1: nothing broke; resume stood ready and unused.

NOT done:
- Nothing cut: both arms at R=12 in full.
- Protected surfaces untouched; no lesson edited, none generated, no
  pin changed.
- Not attempted: the residue diagnosis measurement (hand-authored
  versus production lesson on the same cell), the aim-ground change,
  and any third-seat move (all the conductor's calls, per the
  middle-cell ruling and FINDINGS 1).
