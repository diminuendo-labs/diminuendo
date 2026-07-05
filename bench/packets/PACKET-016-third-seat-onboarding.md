# PACKET-016: Third-seat onboarding (staged, per the standing ruling)

Status: DONE (closed at stage 0 on the packet's own supply rule)
Owner: any Claude Code session. Read /CLAUDE.md first, then this, whole.

## Goal

The third seat is promoted per the standing ruling (DECISIONS
2026-07-03): the bidirectional-and-clean condition is met on the record.
The onboarding requirements apply verbatim: a different family in the
same size class, baselined and tool-response-probed before it teaches or
learns. This packet is that onboarding, staged, and the seat neither
teaches nor learns anywhere in it. No production store changes, no chair
memory created, all delivered lessons are packet-local byte-copies.

## Stage 0: seat selection

Run `ollama list`. Select the first installed model satisfying all
three: a different family from qwen2.5-coder:7b and llama3.1:8b (not a
qwen, not a llama), instruct-capable, in the 7 to 9B size class. Print
the full model list, the selection, and the reason in RESULTS before any
run. If no installed model qualifies, STOP: report the list and close
the packet on that supply answer. Pulling a model is Brad's call, not a
session's.

## Stage 1: baseline probe (counts only)

The selected seat performs every task in both v1 pools at R=6, evidence
execution as the label, detached, checkpointed, per-check readouts
persisted. A probe: counts, no treatment claims, no rates.

Report: the full pass/fail table by task, the headroom map (every task
with at least one fail), and the break-supply view (generation-pool
fails carrying an in-pool topic, eligible contrast pairs enumerated
under the standing conjunction filter). No distillation in this packet:
the seat does not teach.

## Stage 2: first tool-response reading (conditional, signed)

Run stage 2 only if stage 1 shows headroom on range_summary (at least
one fail in its six baseline runs). If it shows none, say so, skip stage
2, and close: the trait probe needs different ground and that is the
conductor's next cut.

Two cells, interleaved per rep, R=12 each, task range_summary, audience
llama3.1:8b unless the selected seat is closer to llama in family, in
which case audience qwen2.5-coder:7b, stated in RESULTS:
- none: no tools.
- armed: the PACKET-014 llama-origin lesson, byte-copied packet-local
  from PACKET-014-lessons.jsonl, byte-check asserted.

Drift bar: 2 of 12, the recorded range_summary movement. One signed
reading, three exits, exclusive:
- GAIN: armed rule check above none by more than the bar. The seat's
  first trait evidence points filter-or-better, and the reverse lesson
  has its second receiving seat.
- HARM: armed rule check below none by more than the bar. Said loudly,
  it outranks everything else in the writeup: a matched pinned tool
  harmed a new seat, which is amplifier-doctrine evidence on a second
  seat.
- FLAT: the gap sits at or under the bar. Inside recorded drift, claims
  nothing, the trait stays unmeasured.
Harm columns: all four non-rule checks both cells, every decline
reported, above-bar declines said loudly, at-or-under-bar declines
inside drift.

## Gate

- Stage 0 printed before any run. Stage 1 complete at R=6 across both
  pools or the shortfall stated. Stage 2 run or its skip justified from
  stage 1 counts. Checkpointed, reports persisted, tool audit from rows
  where armed cells exist.
- Tests green, per-path staging, honest RESULTS and FINDINGS.

## Constraints

- Protected surfaces, tier 2: judge protocol v1, firewall, watch gates,
  lesson gates, lessons.jsonl, watchlist.jsonl, canonical documents, all
  production stores.
- No distillation, no chair memory, no pin changes, no gate changes.
- The delivered lesson rides byte-verbatim; any edit voids the cell.
- If wall time forces a cut, finish stage 1 before starting stage 2, and
  cut stage 2's R evenly if it is the stage that must shrink. Say so.

## FINDINGS

(none. Stage 0 is a selection procedure and it selected nothing; the
supply answer is RESULTS material, not a raised hand. The one pointer
worth restating is already in the record: the 2026-07-01 DECISIONS
entry names the candidate families for a third seat, gemma3 or
mistral, several GB, waiting on Brad's go.)

## RESULTS

Executed 2026-07-03 by a Claude Code session. One commit, this one: the
packet closed at stage 0 before any model run, so there are no run
records, no stage 1 counts, and no stage 2 reading. 159 tests green,
suite unchanged.

Stage 0, the seat selection, printed here before any run as the packet
requires. The full installed list from ollama list, verbatim:

| model | size | qualifies | why not |
|---|---|---|---|
| llama3.1:8b | 4.9 GB | no | an existing seat, llama family |
| qwen2.5-coder:7b | 4.7 GB | no | an existing seat, qwen family |
| glm-ocr-optimized:latest | 2.2 GB | no | different family, but OCR-specialized, not instruct-capable for reasoning, and under the 7 to 9B class |
| glm-ocr:latest | 2.2 GB | no | same as above |
| qwen3-vl:4b-instruct | 3.3 GB | no | qwen family, and 4B, out of class |
| qwen3-vl:4b | 3.3 GB | no | qwen family, 4B, and not instruct-tuned |
| qwen2.5vl:7b | 6.0 GB | no | qwen family |

Selection: NONE. No installed model satisfies all three conditions (a
family other than qwen and llama, instruct-capable, 7 to 9B class). The
non-qwen non-llama models on disk are the two glm-ocr variants, which
the record ruled out for reasoning work on 2026-07-01 and which fail
the size class besides. Per the packet's own rule the session STOPS
here and closes on the supply answer: pulling a model is Brad's call,
not a session's.

Stage 1: not run, stage 0 selected no seat. Stage 2: not run, stage 1
did not exist. The conditional structure of the packet executed exactly
as written, and the shortest honest answer is the whole answer: the
third seat is promoted by ruling and blocked on model supply. The
candidate families named in the record on day one, gemma3 and mistral
in the 7 to 9B class, remain the shopping list, several GB each,
waiting on Brad's go.

Fixed under tier 1: nothing; no code was needed and none was written.

NOT done:
- Stage 1 and stage 2, by the packet's own stop rule.
- No model pulled, no run records created, no stores touched, no chair
  memory, no distillation: the seat that does not exist neither taught
  nor learned.
