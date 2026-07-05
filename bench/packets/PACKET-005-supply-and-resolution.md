# PACKET-005: Supply, phrasing, and resolution

Status: DONE
Owner: any Claude Code session. Read /CLAUDE.md first, then this, whole.

## Goal

PACKET-004 proved the delivery mechanism works, is check-local, and is safe
only in menu form. This packet fixes the three things standing between that
result and a probe that can measure transfer: failure supply (three classes
produce no lessons), lesson phrasing (direction-specific wording is a
measured hazard), and report resolution (task-mean aggregation diluted a
real check-local signal into noise three probes running).

## The work, in order

1. The two approved gate changes (DECISIONS 2026-07-02, conductor rulings):
   a. Aim screen: a committed lesson's rule text must share ground with the
      failing check that produced it, a token-overlap screen after
      stopword removal, crude and documented like the other screens. Applies
      to both contrast paths.
   b. Precedence: the per-class cap (two lessons per class per seat)
      replaces the has-a-lesson trigger, so an all-fail sibling with a
      passing partner gets mined when the cap has room.
2. Direction-safe phrasing, PACKET-004's cure. Both contrast prompts must
   require the lesson to be conditional on the task's stated rule, never
   absolutized from one task: the shape is "follow the tie direction the
   task states" or "when the task states X, do X", not "always return the
   last occurrence". Additionally: tasks whose rule class is tie_break gain
   a stated_direction field in probe_tasks.py (last, alphabetical, first),
   exposed in work_features. A lesson that is direction-specific anyway
   must carry that direction in applies_when so the menu never surfaces it
   against a contradicting task. Pin with tests: a direction-mismatched
   lesson does not surface.
3. Generation-pool headroom, per class per seat (PACKET-003 FINDINGS 3,
   approved). Calibrate exactly as PACKET-001 calibrated the apply pool:
   run candidates at R_G=3 per seat, swap in harder siblings until every
   class has at least one failing seat-task, record the calibration table
   in the module docstring. Reference-verify every new check, pinned by
   test, as always.
4. Re-run the probe at R=3. The report gains the check-level treatment
   readout: for every apply-task check, pass rate per cell, with the
   checks that encode each task's stated rule marked, the same sharp level
   PACKET-004 used. Keep everything else in the report as is.
5. RESULTS here: contrast accounting, at least four committed lessons
   quoted spanning at least three rule classes (if supply still falls
   short after calibration, that is a finding, quote what exists and say
   so), the matrix, the per-class table, and the check-level table for the
   treated classes. Findings sized to the n. One DECISIONS line.

## Gate

- Both gate changes tested: the aim screen rejects a mismatched rule (use
  PACKET-003's misaimed lesson as the fixture), the cap-based precedence
  mines the PACKET-003 shortest_word shape (stub-tested).
- Direction pinning tested: a direction-specific lesson never surfaces on
  a contradicting task.
- Calibration table present, every class breaks somewhere for at least one
  seat, or RESULTS states which class resisted and what was tried.
- Probe ran six cells at stated R with the check-level readout persisted.
- Tests green, commits, honest RESULTS and FINDINGS, detached runs read
  from disk.

## Constraints

- Protected surfaces, tier 2: judge protocol v1, firewall, lessons.jsonl,
  watchlist.jsonl, canonical documents. The lesson gates: the two approved
  changes above are in scope by conductor ruling; anything further is a
  raised hand.
- Do not weaken any screen to raise the lesson count.
- If wall time forces a cut, cut probe R before generation work, and say
  so.

## FINDINGS

Tier 2, flagged and not fixed:

1. The code seat has almost no headroom on this generation pool. qwen
   produced failures only on max_index and count_token, both by sampling
   luck, and passed every run of the six harder candidates in gencal.
   Its store can carry lessons from at most two classes at this pool
   difficulty. Why it matters: the A-lessons columns of the matrix
   measure a mostly empty treatment. What I would do: author a harder
   candidate generation per class specifically against the code seat,
   or accept that transfer measurement at this model scale runs mainly
   through the llama seat. Instrument design, the conductor's call.
2. Class-level matching has a content gap inside the class. The
   normalize lessons are about punctuation stripping and uppercase
   words, and the menu correctly serves them to snake_to_camel and
   balanced, whose normalize rules are about underscores and
   parentheses. The rule_class key narrowed delivery and the
   stated_direction key narrowed it again for ties, but two lessons of
   the same class can still talk past each other's content. What I
   would do: a finer applicability key naming the normalized thing
   (case, whitespace, punctuation, delimiters), the same narrowing
   move as stated_direction. Spec-level applicability design, a raised
   hand.
3. The probe format cannot carry check-level claims at R=3. Each
   rule-check cell lands n=3, and unarmed baselines swung 0.00 to 1.00
   between runs at that n (most_common_word's tie check read 0.33 at
   n=12 in PACKET-004 and 1.00 at n=3 here, same arm). The check-level
   readout now exists in the report and it works, but the six-cell
   format spreads runs thin. What I would do: for treatment questions,
   PACKET-004's focused-arm format at R=12 on the treated tasks; keep
   the probe for supply accounting and coarse structure. Measurement
   design, the conductor's call.

## RESULTS

Executed 2026-07-02 into 2026-07-03 by a Claude Code session. Commits:
944a8c1 (gate changes, phrasing, readout, tests), f901e06 (gen pool
calibration and selection), and the closing commit carrying this
section. Probe 20260702-215407 ran detached start to finish, no kill.
98 tests green throughout.

What ran, in packet order:
- Aim screen, both contrast generators: rule text must share tokens
  with a ground of the failing checks plus the rule-class vocabulary.
  The ground includes class vocabulary because the packet's own
  conditional phrasing names the class, not the function; the
  reconciliation is recorded in DECISIONS. PACKET-003's misaimed
  lesson is the rejection fixture, pinned by test.
- Cap precedence: sibling mining now runs for any unmined fail-task
  with a passing partner while the class cap has room. The PACKET-003
  shortest_word shape is stub-tested and mines both lessons.
- Direction safety: tie_break tasks carry stated_direction (last,
  alphabetical, smallest) into work_features; both prompts demand
  conditional phrasing and direction pinning; a direction-mismatched
  lesson never surfaces, pinned by test AND verified live: the tie
  lesson pinned to "last" rode into every longest_word armed run and
  into zero most_common_word runs across all armed cells.
- Gen pool calibration (gencal 20260702-211540): the six harder
  candidates measured at R_G=3 per seat; table in the probe_tasks.py
  docstring; every class now breaks for at least one seat (tie_break
  both seats on record, the other three via llama). Selection: the
  tie_break incumbents plus all six new candidates.
- Probe 20260702-215407 at R=3: 48 gen runs, 144 apply runs, six cells
  at n=24, 192 rows checkpointed, report persisted with the per-class
  breakdown, per-seat per-class contrast accounting, and the
  check-level table with rule checks marked. Harness GATE passed.

Contrast accounting (per seat per class):
- A tie_break: max_index mixed (1 within-task lesson), shortest_word
  all_pass. A normalize: count_token mixed (1 within-task lesson),
  title_words all_pass. A distinctness and boundary: both siblings
  all_pass, nothing broke.
- B tie_break: BOTH siblings all_fail, no passing partner, no lesson,
  the all-fail case as designed. B distinctness: count_distinct_pairs
  mixed (1 lesson), sum_of_modes all_pass. B normalize: title_words
  mixed and count_token mixed (2 lessons). B boundary: both all_pass.
- Sibling lessons: zero. The cap-mining shape (unmined fail-task plus
  passing partner in class) did not occur this run: every class either
  had within-task contrast or had nothing usable. The mechanism
  remains stub-proven, live-unexercised.
- Totals: A=2, B=3, five lessons spanning three classes (tie_break,
  distinctness, normalize). Boundary stayed dry this run: gencal broke
  it via range_step for llama, this probe's R_G=3 sample did not.

The five committed lessons, quoted (concept, then rule):
1. A, max_index, tie_break: "When the task states that if the largest
   value appears more than once, return the index of its last
   occurrence, ensure your code follows this directive." Rule: "follow
   the direction the task states." applies_when pins
   stated_direction=last. Conditional and pinned, the PACKET-004 cure
   in effect.
2. A, count_token, normalize: "When the task states 'strip leading and
   trailing punctuation from each word', follow this direction." Rule:
   "Apply stripping of leading and trailing punctuation to each word
   before comparison."
3. B, count_distinct_pairs, distinctness: "When the task states that
   each distinct pair should be counted once no matter how many times
   its values repeat, ensure that pairs are stored in a way that
   disregards order." Rule: "Convert potential pairs to tuples and sort
   them before adding to a set to maintain uniqueness regardless of
   order." Conditional concept; the rule drifts toward a recipe, noted.
4. B, title_words, normalize: "When the task states that words already
   entirely uppercase stay exactly as they are, respect that rule by
   not applying title casing to those words." Rule: "Follow the
   direction the task states, specifically ensuring words already in
   all uppercase remain unchanged."
5. B, count_token, normalize: "When the task states that substrings
   inside longer words never count, ensure that only complete,
   whitespace-separated words are considered during the comparison."
   Rule: "Follow the direction to strip leading and trailing
   punctuation from each word before comparing case-insensitively."

The matrix (ev_mean / pass_rate, n=24 per cell):

| performer | none | A lessons | B lessons |
|---|---|---|---|
| A (qwen) | 0.83 / 0.63 | 0.82 / 0.58 | 0.78 / 0.50 |
| B (llama) | 0.63 / 0.13 | 0.69 / 0.17 | 0.61 / 0.21 |

Per-class ev_mean (n per cell in parentheses):

| class | A\|none | A\|A | A\|B | B\|none | B\|A | B\|B |
|---|---|---|---|---|---|---|
| tie_break (6) | 0.92 | 0.92 | 0.83 | 0.71 | 0.72 | 0.49 |
| distinctness (3) | 0.87 | 0.53 | 0.73 | 0.73 | 0.87 | 0.47 |
| boundary (9) | 0.89 | 0.89 | 0.86 | 0.63 | 0.74 | 0.73 |
| normalize (6) | 0.62 | 0.75 | 0.62 | 0.50 | 0.50 | 0.62 |

Check-level table for the treated classes (pass rate, n=3 per cell;
rule checks only):

| rule check | A\|none | A\|A | A\|B | B\|none | B\|A | B\|B |
|---|---|---|---|---|---|---|
| most_common_word('b a b a c') | 1.00 | 1.00 | 1.00 | 1.00 | 0.33 | 0.33 |
| longest_word('cat door bird') | 0.67 | 0.67 | 0.33 | 0.00 | 0.33 | 0.00 |
| longest_word('a bb cc d') | 0.67 | 0.67 | 0.33 | 0.00 | 0.33 | 0.00 |
| range_summary([3, 1, 2, 2]) | 1.00 | 0.00 | 1.00 | 0.67 | 0.67 | 0.33 |
| snake_to_camel('__a__b_') | 0.00 | 0.33 | 0.00 | 0.00 | 0.00 | 0.00 |
| balanced('(a(b)c)') | 1.00 | 1.00 | 1.00 | 1.00 | 0.67 | 1.00 |
| balanced(')(') | 1.00 | 1.00 | 1.00 | 0.00 | 0.67 | 0.33 |

Tool delivery, verified from the rows: the tie lesson rode only on
longest_word (never most_common_word, the direction pin working), the
normalize lessons rode on snake_to_camel and balanced, the distinctness
lesson rode on range_summary. most_common_word ran unarmed in every
cell, so its armed-column swing (1.00 to 0.33) is baseline noise at
n=3, and the same check read 0.33 unarmed at n=12 in PACKET-004.

Findings, sized to the n:
Supply is fixed in direction: five lessons across three classes,
against three then one then three in the prior probes, and every
lesson is conditionally phrased with the one direction-specific lesson
correctly pinned. The one class-and-direction-matched cross-model
treatment, llama's longest_word armed with qwen's tie lesson, lifted
both tie checks 0.00 to 0.33 at n=3, the same direction PACKET-004
measured at n=12; nothing else in the check table clears the noise
that unarmed cells demonstrate at this n (a baseline swung 0.00 to
1.00 between runs). B tie_break went all_fail on both siblings, so the
cap-mining fix stayed unexercised live and llama got no tie lesson,
which also removed this run's chance to replicate PACKET-004 within
the probe. The check-level readout works and is in the report; what it
mostly shows is that R=3 cannot fund check-level claims (FINDINGS 3).
No transfer claim is made in either direction at this n.

Fixed under tier 1: nothing broke; resume stood ready and unused.

NOT done:
- Nothing cut: R=3 and R_G=3 ran in full, six cells, all mechanisms.
- Protected surfaces beyond the two approved gate changes: untouched.
  The aim-screen ground design (class vocabulary added to the failing
  check) is documented in DECISIONS and flagged here for the
  conductor's read.
- Not attempted: harder code-seat generation tasks, a within-class
  content key, or a focused-arm re-measurement (FINDINGS 1 to 3, all
  the conductor's calls).
