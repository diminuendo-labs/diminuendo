# PACKET-001: Probe volume

Status: DONE
Owner: any Claude Code session. Read /CLAUDE.md first, then this, whole.

## Goal

Make the transfer probe matrix mean something. The first probe (see
runs/probe-20260701-200427.report.json and DECISIONS) had two flaws: the
apply tasks gave qwen no headroom (its rows read 1.00 everywhere, zero
signal), and two tasks per cell is noise. Fix the instrument, then run it at
volume.

## The work, in order

1. Build a candidate apply-task pool of 14 to 18 small Python function tasks,
   each with 3 to 5 evidence checks in the existing format
   ({"call": ..., "expect": "<repr>"}). Favor tasks with a subtle stated
   rule that plausible solutions ignore (tie-breaking, distinctness,
   ordering, empty-input conventions). Same FEATURES dict as probe.py uses.
2. Calibrate for headroom. Run every candidate once per performer (qwen and
   llama), no lessons, cross-family audience, and record the evidence
   fraction per seat. Keep a task only if at least one seat scores below 1.0
   on it. The kept pool must leave EACH seat with a baseline mean evidence
   fraction between 0.3 and 0.9. If a seat sits outside that band, swap
   tasks until it does not. Target kept pool: 8 to 12 apply tasks.
3. Grow the generation pool to 6 tasks, same format, disjoint from the apply
   pool. Generation and application tasks must never overlap.
4. Parameterize probe.py: task pools importable from a bench/probe_tasks.py
   module (constants, no config framework), and a repeats parameter so each
   cell runs every apply task R times. Keep the checkpointing exactly as is.
5. Run the full six cells with the calibrated pools at R=2 minimum (R=3 if
   wall time allows). State the resulting per-cell n in the report.
6. Report: the matrix (ev_mean and pass_rate per cell, with n), the baseline
   row per seat from step 2, and three to six sentences of findings sized to
   the n. One line in DECISIONS.md. RESULTS section appended to this file.

## Gate

- The kept apply pool is committed in bench/probe_tasks.py with each task's
  per-seat baseline recorded in a comment or docstring.
- Both seats' baselines sit inside the 0.3 to 0.9 band, stated in RESULTS.
- All six cells ran at the stated R, every run checkpointed, report
  persisted in runs/.
- Tests green, one commit minimum, RESULTS honest about anything cut.

## Constraints

- Do not modify the judge protocol (v1 stays), the firewall, the lesson
  gates, or any canonical document.
- Do not touch lessons.jsonl or watchlist.jsonl. The probe uses its own
  per-run stores, keep that.
- Wall time will be long (roughly 100 to 200 local model calls). That is
  expected. If it must be cut, cut R before cutting pool size, and say so.

## RESULTS

Executed 2026-07-02 by a Claude Code session. Two commits: 4d643be (the
instrument and the calibration record) and the closing commit carrying
this section and the probe run.

What ran:
- Candidate pool built in bench/probe_tasks.py: 17 apply candidates and 6
  generation tasks, disjoint, each apply candidate stating a subtle rule
  (tie-break direction, distinctness, adjacency merging, float convention,
  empty-input convention). Every check was verified satisfiable against a
  reference solution through the real evidence harness before any model
  saw it, 23 of 23 clean, and that verification is pinned as a unit test.
- Calibration (calibrate.py, run 20260702-011304): all 17 candidates, one
  run per performer seat, no lessons, cross-family audience. 34 runs, each
  checkpointed to runs/, report persisted.
- Selection: exactly 8 of 17 candidates had headroom (at least one seat
  below 1.0), the packet's keep rule, landing inside the 8 to 12 target.
  Kept: most_common_word, merge_ranges, longest_word, median,
  range_summary, flatten_once, snake_to_camel, balanced. Per-task per-seat
  baselines are recorded in the probe_tasks.py docstring.
- probe.py parameterized: pools import from probe_tasks.py, a repeats
  parameter, per-cell n stated in the report. Checkpointing unchanged.
- Full probe (run 20260702-012616) at R=3: 12 generation runs, 6 lessons
  committed per store, 144 apply runs, six cells at n=24 each, 156 rows
  checkpointed, report persisted, the harness gate line PASSED.

Gate, item by item:
- Kept pool committed in probe_tasks.py with per-seat baselines in the
  docstring: done.
- Both seats' baselines inside the band: A=0.65, B=0.58, band 0.3 to 0.9,
  holds.
- All six cells ran at the stated R (R=3), every run checkpointed
  (probe-20260702-012616.rows.jsonl), report persisted in runs/: done.
- Tests green: 60. Commits: two, stated above.

Baseline row per seat (step 2, kept pool, one run per task per seat):
- A (qwen2.5-coder:7b): 0.65
- B (llama3.1:8b): 0.58

The matrix (ev_mean / pass_rate, n=24 per cell, rows=performer,
cols=lesson source):

| performer | none | A lessons | B lessons |
|---|---|---|---|
| A (qwen) | 0.80 / 0.54 | 0.80 / 0.50 | 0.80 / 0.54 |
| B (llama) | 0.62 / 0.17 | 0.64 / 0.25 | 0.59 / 0.17 |

Findings, sized to the n:
The instrument is fixed. qwen's rows sat at 1.00 everywhere in the first
probe and now read 0.80, so both rows carry signal. At n=24 per cell the
lesson columns move nothing that clears noise: qwen is flat at 0.80
across none, A, and B, and llama's spread (0.62, 0.64, 0.59) is smaller
than the run-to-run scatter at this n. The gradient the first probe
showed for llama (0.50 to 0.83 to 1.00 at two easy tasks per cell) does
not reappear on the calibrated pool, which is what volume is for. The
gap that does show is between performers, not between lesson columns.
Separately, pass rates sit far below evidence in every llama cell (0.17
to 0.25 against ev 0.59 to 0.64): the qwen judge fails outputs that
execution partially clears, consistent with the judgecal read that
neither local judge is a reliable criteria detector on its own. The
honest claim at this n: no measurable transfer effect on evidence
fraction, in either direction.

NOT done:
- Nothing in the packet was cut. R=3 ran, the higher stated option.
- Out of scope by the packet's own constraints and untouched: the judge
  protocol (v1 stayed), the firewall, the lesson gates, lessons.jsonl,
  watchlist.jsonl, canonical documents.
- The 9 no-headroom candidates were dropped, not rewritten. They stay in
  the candidate pool for future swaps and re-calibration.
- Not attempted: per-task effect breakdowns beyond the persisted rows,
  production-temperature judging, any interpretation of pass_rate as a
  transfer measure (the audience is a detector, not the ruler).
