# PACKET-002: Contrastive lessons on class-overlapped pools

Status: DONE (closed by the conductor; see RESULTS)
Owner: any Claude Code session. Read /CLAUDE.md first, then this, whole.

## Goal

Give the transfer probe something that could transfer, then re-run it.
PACKET-001 proved the instrument and returned a null, and the conductor
autopsy (DECISIONS, 2026-07-02) traced the null to two defects, both fixed
here: lessons were distilled from single uncontrasted runs (platitudes and
one-task procedures), and the generation and apply pools shared no rule
classes, so nothing could have carried even from a perfect engine.

## The design being implemented

The concept spec's Section 5 mechanism: the valuable lesson comes from
contrast, the question is what context separates the failure from the times
the same rule worked. A lesson must name the specific stated rule at its
boundary. Rule classes make transfer possible without task overlap: the same
class of trap appears in both pools, in different tasks.

## The work, in order

1. Rule classes. Add a "rule_class" field to every task in probe_tasks.py.
   Use exactly these four classes and no others: tie_break (a stated
   tie-breaking direction), distinctness (distinct-values semantics),
   boundary (empty or degenerate input convention), and normalize (a stated
   normalization step such as case, whitespace, or ordering before compare).
   Classify the existing kept apply tasks; every kept task must carry one.
2. Generation pool v2: 8 new small function tasks, two per rule class, task
   text disjoint from every apply task, checks in the existing format and
   pre-verified against reference solutions exactly as PACKET-001 did (pin
   it in the test). The trap in each generation task must be its rule class.
3. Contrastive generation. New engine path in lesson.py (add, do not replace
   the old one): for one generation task, run the performer R_g=3 times.
   If at least one run fails evidence and at least one passes, distill ONE
   lesson from the contrast: the prompt shows the failing run's failing
   checks and the passing run's output, and requires the lesson to name the
   specific stated rule that separates them. If a task produces no failures
   or no passes in R_g=3, it yields no lesson; lessons come from breaks,
   never from averages. Record per task which case occurred.
4. Content gate, added to lesson.validate, never replacing existing gates:
   the committed lesson carries a "rule" field, non-empty, and the concept
   plus rule text must not be a platitude. Reject any lesson whose combined
   text matches the platitude list: "consider edge cases" and variants
   without a named rule, "built-in methods", "readability", "efficiency",
   "best practice", "clean code". Crude by design, like the metric screen,
   and stated as such in the docstring.
5. The menu matches on rule_class: applies_when gains rule_class, apply
   tasks pass their rule_class in work_features, matching stays otherwise
   unchanged.
6. Re-run the probe at R=3 on the same kept apply pool (now class
   annotated), lessons generated per seat with the contrastive path.
   Same report format, plus a per-rule-class breakdown of ev_mean for the
   lesson columns against the none column.
7. RESULTS appended here: what ran, the matrix, the per-class breakdown,
   how many generation tasks yielded contrast lessons per seat, three to
   six sentences of findings sized to the n, one DECISIONS line.

## Gate

- Every kept apply task and every v2 generation task carries one of the four
  rule classes, pinned by test.
- Every committed lesson names a specific rule (spot-check three in RESULTS,
  quoted).
- Contrast accounting stated: per seat, how many of 8 generation tasks
  yielded a lesson, and why the others did not.
- Six cells at stated R, checkpointed, report persisted, per-class breakdown
  present. Tests green, commits made, RESULTS honest about anything cut.

## Constraints

- The protected surfaces for this packet: the judge protocol (v1), the
  firewall, the existing lesson gates (the content gate adds), lessons.jsonl,
  watchlist.jsonl, and the canonical documents. Tier 2 of CLAUDE.md applies
  to them: flag in FINDINGS, never change. Everything else the packet
  touches or depends on is tier 1 terrain: if it is broken, fix it, test it,
  log it.
- If a generation seat yields fewer than 3 lessons total, run the probe
  anyway and say so; a thin store is a finding, not a failure.
- If wall time forces a cut, cut R on the probe before cutting R_g on
  generation, and say so.

## FINDINGS

(from the executing session's DECISIONS entries and the conductor's review)
- The old uncontrasted generate path's candidates now die at the content
  gate for lack of a rule field, the gate working as ordered.
- The session environment reaps background shells, which killed the probe
  mid-run once and killed the session itself before closure. The tier 1
  resume fix (py probe.py R <run_id>) is what let the run finish detached.
  Long work in Code sessions must launch detached and be read from disk.

## RESULTS

Closed 2026-07-02 by the conductor. The executing session was killed by its
environment after commit fc14724; the detached probe finished on its own,
and every claim below was verified against the run artifacts, not the
session's account.

What ran:
- Rule classes on every task, gen pool v2 (8 tasks, two per class,
  reference-verified, pinned by test), the contrastive lesson path (no
  contrast, no lesson), the content gate (rule field plus platitude screen),
  menu matching on rule_class. 75 tests green at the session's last commit.
- Probe 20260702-051517 at R=3, resumed once after an environment kill:
  48 generation runs (8 tasks x R_G=3 x 2 seats), 144 apply runs, six cells
  at n=24, 192 rows checkpointed, report persisted, harness gate PASSED.

The finding that governs everything else: CONTRAST STARVATION. Within-task
fail-and-pass at R_G=3 occurred on 1 of 16 seat-task combinations. These
models are more deterministic per task than the design assumed. Stores:
A=1 lesson, B=0. Four of six cells therefore ran untreated, and the matrix
is mostly baseline replicas, not treatments.

The one committed lesson is the packet's proof of mechanism, quoted:
"When the largest value appears more than once, return the index of its
last occurrence," rule field naming the stated tie direction, tie_break
class, trail carrying the fail node and the contrast node. The engine
produces a real rule when contrast exists. The platitude era is over.

The one treated comparison, sized honestly: the lesson applied cross-model
moved llama's tie_break evidence 0.58 to 0.92 at n=6. But untreated
replicas size per-class noise up to 0.25 at this n (qwen boundary swung
0.92 to 0.67 between identical conditions), so this is a lead to chase,
not a result to claim. Full matrix and per-class table are in
runs/probe-20260702-051517.report.json and the log.

NOT done: RESULTS and FINDINGS were not appended by the executing session
(it was dead); the conductor closed the packet. Nothing in the packet's
work items was cut. The transfer question remains open, now blocked on
contrast availability, which PACKET-003 addresses.
