# PACKET-012: The residue diagnosis (what harmed the amplifier)

Status: DONE
Owner: any Claude Code session. Read /CLAUDE.md first, then this, whole.

## Goal

PACKET-011 measured the reverse cell and got a split: harm column clean,
rule checks down 0.67 to 0.42 under matched, fully pinned tools. FINDINGS
1 names the leading hypothesis: the production lessons carry source-task
residue ("character runs", "occurrence"), and the amplifier seat obeys
the residue, while PACKET-007's residue-free hand-authored lesson lifted
this same seat 0.50 to 0.92 through the same menu path. This packet
measures that hypothesis directly. It also decides, per the conductor's
standing rulings, what the delivery diagnosis says before any third-seat
work, and what gate change, if any, gets designed after.

## The arms

Performer qwen2.5-coder:7b, audience llama3.1:8b, task longest_word only,
v1 production path, pins live. Three arms at R=12 each, 36 runs, 72 model
calls, detached, checkpointed, resume-capable, confirm/transfer harness
pattern as is.

- none: no tools. Replicates PACKET-011's baseline (0.67).
- prod: the same two llama-origin tie lessons from the 081801 B store,
  copied packet-local verbatim, identical to PACKET-011's menu arm.
  Replicates the decline or fails to.
- hand: exactly one conductor-authored residue-free lesson, printed below,
  used verbatim, packet-local, provenance marked hand_authored. It never
  enters any production store.

The hand lesson, verbatim:

```json
{
  "concept": "When several candidates tie on the stated measure, the task's stated tie direction picks the winner.",
  "rule": "When candidates tie, return the one the task's stated tie direction selects.",
  "applies_when": {
    "operation": "write_code",
    "target": "function",
    "language": "python",
    "size": "small",
    "rule_class": "tie_break",
    "rule_topic": "direction",
    "stated_direction": "last"
  },
  "trail": {
    "gen_task": "hand_authored",
    "contrast_type": "hand_authored"
  }
}
```

Pins are identical to the production pair so menu matching is identical.
The lesson text carries no source-task noun: no run, no character, no
occurrence, no word. If the harness's load gates reject the hand lesson,
that is a tier 2 FINDINGS item, not a gate change: report it and run the
arm with the lesson injected by the same mechanism PACKET-007 used.

## Report and the pre-registered reading, apply verbatim, signs stated

Per-check table, rule checks marked, harm column mandatory, PACKET-011's
cells printed beside as priors. Tool audit from the rows: prod arm
tools=2 on every armed run, hand arm tools=1 on every armed run.

Four questions, read independently, each with its sign:

1. REPLICATION: prod pooled rule checks BELOW none pooled rule checks.
   Replicates the PACKET-011 decline and the decline stands as a lean at
   combined n. If prod is at or above none, the PACKET-011 decline is
   downgraded to noise by the conductor, in DECISIONS and in PACKET-011
   RESULTS, where the claim was made.
2. RESIDUE SEPARATION: hand pooled rule checks AT OR ABOVE none, while
   prod sits below none. Then residue is the separator, the FINDINGS 1
   hypothesis gains its first direct evidence, and the gate change gets
   designed from this table.
3. DELIVERY HAZARD: hand pooled rule checks BELOW none. Then the hazard
   is delivery to this seat, not residue, the amplifier doctrine question
   deepens, and the third seat stays deferred with the diagnosis still
   open.
4. LIFT: both rule checks UP under hand versus none AND pooled passes
   differ. Then residue-free content lifts this seat through the
   production menu, reverse transfer re-opens as content-limited, and
   the claim is sized to one task, one seat, n=12.

Harm column in every arm: both non-rule checks. Any decline there under
matched tools outranks everything else in the writeup, say it loudly.

All directional results at n=12 per arm are leans, never rates, and the
writeup says so.

## Gate

- Three arms at R=12, checkpointed, report persisted, per-check table
  with harm column and PACKET-011 priors, tool audit clean from the rows.
- All four readings applied verbatim with their signs, independently.
- Tests green, per-path staging, honest RESULTS and FINDINGS.

## Constraints

- Protected surfaces, tier 2: judge protocol v1, firewall, watch gates,
  lesson gates, lessons.jsonl, watchlist.jsonl, canonical documents, all
  existing stores (packet-local copies only).
- No lesson generation, no pin changes, no gate changes. The gate change
  is this packet's possible consequence, ruled by the conductor after,
  never its work.
- The hand lesson is used exactly as printed. Any edit to it voids the
  arm.
- If wall time forces a cut, cut R evenly across all three arms, and say
  so.

## FINDINGS

Tier 2, flagged and not fixed:

1. The hand lesson dies at the production gates, as the packet
   anticipated: lesson.validate rejects it for missing confidence and
   provenance fields, and menu.query raises KeyError on the missing
   confidence rather than declining it. Per the packet's own
   contingency the arm ran with the lesson injected by the PACKET-007
   mechanism: the delivery surface received exactly what the menu
   emits for a matched lesson, concept plus applies_when, after the
   public matcher confirmed the match at the same score the production
   pair matched at. The lesson text was never touched, pinned by test.
   Incidental instrument observation, one line: the menu crashes on a
   confidence-less lesson instead of rejecting it, a sharp edge for
   any future hand-authored material.
2. The none baseline moved 0.67 to 0.50 between PACKET-011 and this
   run, the identical cell at n=12 twice, and that drift is the
   yardstick every within-run gap here must be read against. The
   hand-to-none gap (2 of 24) is smaller than the baseline's own
   run-to-run movement (4 of 24); the prod-to-none gap (4 of 24, same
   direction twice, 10 of 48 combined) is the only separation in this
   diagnosis that survives the yardstick as a lean. What I would do:
   any future single-cell claim at n=12 should carry a same-run
   baseline, never a prior run's, which this packet's design already
   did, and the conductor may want a paired-run design (same prompts,
   interleaved arms) before trusting sub-0.10 gaps at this n at all.

## RESULTS

Executed 2026-07-03 by a Claude Code session. Commits: a56b12d (harness
and materials) and the closing commit carrying this section. Run
diagnose-20260703-102824 ran detached start to finish, no kill, resume
unused. 138 tests green throughout.

What ran: performer qwen, audience llama, v1 production path, task
longest_word, three arms at R=12 each, 36 runs, 72 model calls, all
checkpointed, GATE passed. The prod arm rode the two llama-origin
lessons packet-local and verbatim (byte-identical to PACKET-011's menu
arm store). The hand arm rode the conductor's lesson exactly as
printed; its gate rejection and the injection path are FINDINGS 1. Tool
audit clean from the rows: prod tools=2 on 12 of 12 armed runs, hand
tools=1 on 12 of 12.

Per-check pass rates (n=12 per arm; PACKET-011's cells beside as
priors):

| check | none | prod | hand | P11 priors (none / menu) |
|---|---|---|---|---|
| 'cat door bird' RULE | 0.50 | 0.33 | 0.42 | 0.67 / 0.42 |
| 'a bb cc d' RULE | 0.50 | 0.33 | 0.42 | 0.67 / 0.42 |
| '' (harm column) | 1.00 | 1.00 | 1.00 | 1.00 / 1.00 |
| 'one' (harm column) | 1.00 | 1.00 | 1.00 | 1.00 / 1.00 |

Pooled rule checks: none 12/24, prod 8/24, hand 10/24. PACKET-011:
none 16/24, menu 10/24.

The four pre-registered readings, applied verbatim with their signs,
independently:
1. REPLICATION: FIRES. Prod pooled (8/24) sits below none pooled
   (12/24), the same direction as PACKET-011 (10/24 below 16/24). The
   decline stands as a lean at combined n: prod-armed 18/48 against
   unarmed 28/48 across the two runs. No downgrade goes to the
   conductor.
2. RESIDUE SEPARATION: DOES NOT FIRE. The sign requires hand at or
   above none while prod sits below; hand (10/24) is below none
   (12/24). Residue is not shown to be the separator, and per the
   packet the gate change is NOT designed from this table.
3. DELIVERY HAZARD: FIRES BY SIGN, and the size is stated with it.
   Hand pooled (10/24) is below none (12/24), so the letter of the
   reading holds: the hazard reads as delivery to this seat rather
   than residue, the amplifier doctrine question deepens, and the
   third seat stays deferred with the diagnosis open. The size: the
   hand-to-none gap is 2 of 24, smaller than the none baseline's own
   movement between adjacent runs of this identical cell (FINDINGS 2),
   so this reading fires at the weakest lean the record has reported.
4. LIFT: DOES NOT FIRE. Both rule checks moved down under hand versus
   none, not up. Residue-free content did not lift this seat on this
   task, against the same content's structure lifting it on
   range_summary in PACKET-007.

Harm column, mandatory, all arms: clean. Both non-rule checks 12 of 12
in every arm. Nothing declined there, so nothing outranks the readings
above; the amplifier's collateral-safety property under pinned tools
holds for the third measurement running.

Findings, sized to the n:
The diagnosis returns an ordering, not a verdict: none 12, hand 10,
prod 8, of 24, with clean harm everywhere. The prod decline is the
only within-run separation that survives the baseline-drift yardstick,
and it now stands twice in the same direction. The residue hypothesis
is neither confirmed (reading 2 failed) nor buried: hand beat prod by
2 of 24 while still trailing none, which is what one would see if
residue contributes part of the drag and delivery-to-this-seat the
rest, and equally what one would see from noise at this n. What the
run establishes at its stated size: tie lessons of any authorship so
far measured do not help qwen on longest_word through the menu, while
the same seat took a large lift from matched content on a different
task and topic in PACKET-007. The open contrast is now task-and-topic
shaped, not authorship shaped. All directional statements here are
leans at n=12 per arm, never rates.

Fixed under tier 1: nothing broke; resume stood ready and unused.

NOT done:
- Nothing cut: three arms at R=12 in full.
- No gate change designed (reading 2 did not fire); no lesson
  generated, no pin changed, the hand lesson untouched as printed.
- Not attempted: the paired-run baseline design (FINDINGS 2), the menu
  sharp-edge fix (FINDINGS 1), and any third-seat work (deferred by
  the standing rulings, and this diagnosis leaves it deferred).
