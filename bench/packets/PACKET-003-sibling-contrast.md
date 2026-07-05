# PACKET-003: Cross-task contrast within rule classes

Status: DONE
Owner: any Claude Code session. Read /CLAUDE.md first, then this, whole.

## Goal

Fix contrast starvation and re-run the probe with populated stores.
PACKET-002 proved the contrastive engine produces a real rule when contrast
exists, and proved contrast almost never exists within a single task:
fail-and-pass at R_G=3 occurred on 1 of 16 seat-task combinations, leaving
stores at A=1 and B=0 and the matrix mostly untreated.

## The design

Widen the contrast source from within-task to within-class. Each rule class
has two generation tasks (the siblings). A seat that fails one sibling and
passes the other has a contrast: same seat, same stated rule class,
different task. The lesson question is unchanged and gets sharper: what
does the stated rule require that the failing attempt ignored, given the
same class of rule was honored in the sibling? Seat origin is preserved,
both sides of every contrast come from the same seat's own runs.

Precedence when both exist: within-task contrast first (the cleaner
comparison, only sampling varied), sibling contrast as the fallback.

## The work, in order

1. Extend the contrastive path in lesson.py (add, never replace): a
   sibling-contrast function taking the failing run's summary and failing
   checks from task X, and a passing run's summary from sibling task Y of
   the same rule class. The prompt shows both and requires the lesson to
   name the specific stated rule of the CLASS, not the task. Same content
   gate, same rule field requirement.
2. Update the probe's generation phase: after R_G=3 runs per generation
   task per seat, build contrasts per seat per class: within-task pairs
   first, then sibling pairs for classes still without a lesson. At most
   two lessons per class per seat. Record the accounting: per seat per
   class, which contrast type fired or why none did (all-pass, all-fail
   with no passing sibling, and so on).
3. The all-fail class is a real case: if a seat fails every run of both
   siblings in a class, no lesson for that class from that seat, and the
   accounting says so. Lessons come from contrast, never from averages.
4. Re-run the probe at R=3 on the kept apply pool. Same report format,
   per-class breakdown, plus the contrast accounting in the report.
5. RESULTS here: matrix, per-class table, contrast accounting, three
   committed lessons quoted, findings sized to the n, one DECISIONS line.
   Launch the probe detached and read it from disk, per PACKET-002's
   FINDINGS: the environment reaps shells.

## Gate

- Sibling-contrast path tested with stubs (no model calls in tests),
  including precedence (within-task beats sibling) and the all-fail case.
- Contrast accounting present in the report, per seat per class.
- Every committed lesson names a specific rule; three quoted in RESULTS.
- Six cells at stated R, checkpointed, report persisted. Tests green,
  commits made, RESULTS and FINDINGS honest.

## Constraints

- Protected surfaces, tier 2 of CLAUDE.md: judge protocol (v1), firewall,
  existing lesson gates (additions only), lessons.jsonl, watchlist.jsonl,
  canonical documents.
- Do not lower the content gate to raise the lesson count. A thin store
  after a widened source is a finding about these models, not a gate
  problem.
- If wall time forces a cut, cut R on the probe before R_G, and say so.

## FINDINGS

Tier 2, flagged and not fixed:

1. The content gate passes a misaimed rule. Lesson 2 below (seat A,
   shortest_word) filled its rule field with a stated rule from the task,
   but the wrong one: the empty-string boundary sentence, with the task's
   trailing "Note one edge case it handles" instruction copied in, instead
   of the tie direction the failing check actually broke on. The gate
   checks presence and platitudes, not aim, so it committed. Why it
   matters: a lesson can carry a true rule that teaches nothing about the
   break that produced it, and at menu time it still surfaces as if it
   did. What I would do: have the distiller receive and echo the failing
   check, and validate that the rule text and the failing check share
   ground, either by a second-model read or a token-overlap screen. Both
   change the lesson gates, a protected surface, so this is a raised hand.
2. The precedence rule leaves break material unmined. B's shortest_word
   was all_fail with a passing sibling available, but the class already
   had its within-task lesson from max_index, so the fallback never
   looked at it. Three verified failures went untaught. What I would do:
   allow the sibling pair to fill the second slot of the per-class cap
   when within-task produced only one lesson. That is a change to the
   packet's stated design, so flagged, not made.
3. The generation pool starves the mechanism upstream of the fix this
   packet built. Six of eight class-seat combinations produced zero
   failures at R_G=3 (both siblings all_pass), so no contrast of any
   kind was possible outside tie_break. The sibling machinery is built,
   tested, and live, and it never fired because the pool gives these
   models no headroom in three of four classes. What I would do:
   calibrate the generation pool for per-class per-seat headroom exactly
   as PACKET-001 calibrated the apply pool, swapping in harder siblings
   until every class breaks somewhere. That is the experiment's design,
   the conductor's call.

## RESULTS

Executed 2026-07-02 by a Claude Code session. Commits: 44d91a3 (the
mechanism and its tests) and the closing commit carrying this section.
Probe 20260702-083121 ran detached start to finish, no kill, no resume
needed; the resume path from PACKET-002 stood ready and unused.

What ran:
- lesson.generate_sibling_contrast added (old paths untouched): fail on
  one sibling, pass on the other, same seat, same rule class, and the
  lesson must name the stated rule of the class. Same content gate.
- Probe generation phase rebuilt: contrasts per seat per class,
  within-task pairs first, sibling as fallback for classes still without
  a lesson, at most two lessons per class per seat, all-fail recorded
  with its reason. Stub-tested: precedence, sibling firing, the all-fail
  case, the cap, resume. 78 tests green.
- Probe 20260702-083121 at R=3: 48 generation runs, 144 apply runs, six
  cells at n=24, 192 rows checkpointed, report persisted with per-class
  breakdown and contrast accounting, harness GATE passed.

Contrast accounting (per seat per class, R_G=3):
- A tie_break: both siblings mixed, 2 within-task lessons committed.
- A distinctness, boundary, normalize: both siblings all_pass, nothing
  broke, no lesson possible.
- B tie_break: max_index mixed, 1 within-task lesson committed;
  shortest_word all_fail, unmined because the class already had its
  lesson (see FINDINGS 2).
- B distinctness, boundary, normalize: both siblings all_pass.
- Sibling lessons: zero. The fallback's trigger, a class with no lesson
  and at least one fail plus one pass across siblings, never occurred.
  The starvation moved upstream: it is no longer pairing, it is the
  absence of failures outside tie_break (see FINDINGS 3).

The three committed lessons, all tie_break, all within-task, quoted:
1. Seat A, max_index. Rule: "When the largest value in the list appears
   more than once, return the index of its last occurrence, not the
   first." Aimed at the exact stated rule the failing run broke.
2. Seat A, shortest_word. Concept: "When there is a tie for the shortest
   word, return the last such word." Rule field misaimed: "An empty
   string returns ''. Note one edge case it handles." A stated rule, the
   wrong one, and the gate passed it (FINDINGS 1).
3. Seat B, max_index. Rule: "If the largest value is found at multiple
   positions, return the index of the last occurrence instead of the
   first." Aimed correctly.

The matrix (ev_mean / pass_rate, n=24 per cell):

| performer | none | A lessons | B lessons |
|---|---|---|---|
| A (qwen) | 0.84 / 0.58 | 0.82 / 0.62 | 0.77 / 0.54 |
| B (llama) | 0.61 / 0.21 | 0.63 / 0.21 | 0.65 / 0.29 |

Per-class ev_mean (n per cell in parentheses):

| class | A\|none | A\|A | A\|B | B\|none | B\|A | B\|B |
|---|---|---|---|---|---|---|
| tie_break (6) | 0.83 | 0.78 | 1.00 | 0.72 | 0.69 | 0.81 |
| distinctness (3) | 0.93 | 1.00 | 0.80 | 0.20 | 0.33 | 0.27 |
| boundary (9) | 0.89 | 0.92 | 0.71 | 0.69 | 0.75 | 0.72 |
| normalize (6) | 0.71 | 0.62 | 0.62 | 0.58 | 0.54 | 0.58 |

Treated cells consumed the stores as designed: A|A and B|A each saw both
of A's lessons, A|B and B|B saw B's one, and the lessons surfaced only
on tie_break tasks, per the rule_class pin.

Findings, sized to the n:
The sibling mechanism is built and tested, and this run gave it nothing
to do: the classes that needed it produced no failures at all. Three
lessons committed, all tie_break, and the tie_break treated deltas at
n=6 (A|A -0.05, A|B +0.17, B|A -0.03, B|B +0.09) all sit inside the
untreated noise band, which spans up to 0.21 on classes where no lesson
exists anywhere (A boundary 0.71 to 0.92 across three unarmed
conditions). The sharpest fact is cross-probe: PACKET-002's lead, llama
tie_break 0.58 to 0.92 armed with qwen's lesson, read 0.72 to 0.69 on
the same comparison this run. A +0.34 delta became -0.03 under
replication, which is what noise does and what single-probe leads at
n=6 are worth. Baselines themselves moved between probes (B|none
distinctness 0.40 then 0.20), so per-class cells at n=3 to 9 cannot
carry a transfer claim in either direction. The transfer question
stays open, now blocked on failure supply in three of four classes,
which is an instrument problem with a known fix (FINDINGS 3).

Fixed under tier 1: nothing needed fixing this session; the PACKET-002
resume fix was in place and unused.

NOT done:
- Nothing in the packet was cut. R=3 ran, R_G=3 ran, all six cells.
- Protected surfaces untouched: judge protocol v1, firewall, existing
  lesson gates (the sibling path adds a generator, not a gate change),
  lessons.jsonl, watchlist.jsonl, canonical documents.
- Not attempted: any change to the content gate, the precedence rule,
  or the generation pool (all flagged in FINDINGS instead).
