# Diminuendo bench decisions log (public, redacted)

This is a curated copy of the project decisions log. Non-research
entries are removed for public release: the production ground plan
and its trigger, the corporate and open-source-terms logistics, and
release sequencing tied to those. What remains is the research
record: the packet rulings, the measurement discipline, the
findings, and the corrections. The research rulings and corrections
in this log are complete as of this release. Nothing research
bearing was removed. A few entries are kept with a single off-topic
sentence scrubbed; those are noted in the release manifest.

# Bench decisions log

One line per architecture call, one reason. Newest at the bottom.
- 2026-07-01 | Plan created as BENCH_BUILD_PLAN.md, authored this session from Tech
  Spec Section 11 plus the transfer probe. No prior plan existed.
- 2026-07-01 | Model access confirmed: Ollama locals only, no API keys. CLI auth has
  worked before for the wider stack and stays available as a later third seat.
- 2026-07-01 | First tasks are synthetic. Real tasks replace them once the spine holds.
- 2026-07-01 | Standalone bench with an adapter boundary, confirmed by Brad. Stack
  integration comes after the spine, not before.
- 2026-07-01 | Python 3.14 via the py launcher. The python alias is not on PATH.
- 2026-07-01 | Repo-local git identity set with a placeholder email. Brad replaces it
  with his real email before any remote push.
- 2026-07-01 | OPEN, needs Brad: the probe needs a second model family. qwen2.5-coder:7b
  is the code seat. The glm models on disk are OCR-specialized and wrong for reasoning
  tasks, and qwen3-vl is the same family as the code seat, which defeats the
  decorrelation the probe measures. Candidate fix: pull one general model from a
  different family (llama3.1:8b, gemma3, or mistral). A download of several GB, so it
  waits for Brad's go.
- 2026-07-01 | score.py is in-memory with a plain-data snapshot (to_dict), no database.
  Simple first, persistence added when the runner needs it. Edge sources (structural,
  semantic, missing) recorded per edge because the three carry different trust.
- 2026-07-01 | Second probe seat chosen: llama3.1:8b. Different family, same
  capability class as qwen2.5-coder:7b. Also becomes the audience over qwen
  performances, ending same-model self-scoring. Pull on Brad's go.
- 2026-07-01 | Executable evidence runs generated code in a subprocess with a
  timeout. Contains hangs and crashes, is not a sandbox. Revisit before any
  untrusted task enters the loop.
- 2026-07-01 | Evidence outranks the audience only toward fail on the checks it
  covers. An audience fail is never overridden by an evidence pass: evidence
  covers correctness checks, not every criterion, and silence is not safety.
- 2026-07-01 | First live audience false flag, run 20260701-183102-1a5e87. The
  audience failed the work claiming an edge case was unhandled, and evidence had
  proven that exact case passing. Recorded as the first real credibility input
  the flag tally will consume. Same-model audience made this more likely.
- 2026-07-01 | Generator applies_when values constrained to the exact feature
  value or "*". The first unconstrained attempt wrote a free description, which
  contradicted the features and emptied the menu: Gate 2 failed once, honestly,
  before it passed.
- 2026-07-01 | Known issue: the audience renames criteria into its own JSON keys.
  Harmless now, matters when catch-better teaches criteria back to it.
- 2026-07-01 | lessons.jsonl is append-only. The malformed first lesson stays as
  history and stays dormant by contradiction, nothing is deleted.
- 2026-07-01 | llama3.1:8b pulled and live. First cross-family cycle ran clean:
  qwen performs, llama judges, Gate 2 passed with two lessons on the menu. The
  audience_model rides in each run's summary.json.
- 2026-07-01 | Long model runs never stream through the tool pipe. The loop logs
  to runs/loop-*.log, run_once persists runs/*.summary.json, launches use a short
  tool timeout and the files get polled. Learned when a transport timeout killed
  a run and left nothing.
- 2026-07-01 | Process lesson, mine: a blind regex edit rewrote the print inside
  the logger itself and made it recursive. Syntax check passed, runtime crashed.
  Mechanical edits to code get re-read function by function before running.
- 2026-07-01 | Phase 3 built and Gate 3 passed live. The loop rule is structural:
  musicians are pure calls made by the principal's scheduler, no code path exists
  to push upward. The flag tally is its own module and file, weight blast times
  credibility times surprise, floored above zero. The principal's review is
  read-only and verifies each claim against the node's own record.
- 2026-07-01 | Seeded faults are first-class (mutate_code hook in run_once),
  labeled in the summary, never hidden. They are the spec's own Seam 3 signal
  for testing detectors.
- 2026-07-01 | The seeded run demonstrated the floor thesis across families: the
  llama audience passed sabotaged code that reads clean, execution caught it.
  Kinds of checker decorrelate, model diversity alone does not.
- 2026-07-01 | Cascade tests redirect runner.RUNS to a temp dir. The real runs/
  directory holds run records only, never test artifacts.
- 2026-07-01 | Gate 4 passed: the transfer probe ran all six cells, 16 runs
  checkpointed, report persisted. Matrix (ev_mean): qwen 1.00 everywhere, a
  ceiling effect, the apply tasks gave it no headroom, so its rows carry zero
  signal. llama: none 0.50, qwen-lessons 0.83, own-lessons 1.00. Direction is
  not against the transfer bet, and at two tasks per cell it proves nothing.
  Volume decides, and the harness is now the thing that can produce it.
- 2026-07-01 | Probe metric call: evidence fraction over verdicts. Pass rates
  are polluted by audience criteria judgments (one cell posted 0.00 pass rate
  over 0.83 evidence). The audience is a detector, not the probe's ruler.
- 2026-07-01 | Next probe iteration needs apply tasks calibrated so BOTH seats
  have headroom, and more of them. A task set one model aces is a broken
  instrument for that model's rows.
- 2026-07-01 | Catch-better built: watchlist.py (audience criteria store, same
  gates as lessons), hindsight.py (natural-miss sweep + latency_mix), watch
  items injected into the audience prompt. Seeded runs never teach: the fault
  was invisible in the audience's input, so a watch item from it cannot work.
- 2026-07-01 | The loop closed live, lineage on disk: a probe-era break the
  audience passed and evidence caught became a watch item ("ties broken
  lexicographically"), and the next same-class break was caught live by the
  armed audience citing that watch as its reason, with evidence confirming the
  break was real. The latency mix shifted one unit earlier (3 to 4 caught
  live). n=1, and the causal claim is strong but not proven: no unarmed
  control ran on the same output. The mechanism gate passed regardless.
- 2026-07-01 | The discovery-latency mix (hindsight.latency_mix) is now
  computed from the run record. It is the slope's measurable signature from
  the spec, in code, one data point old.
- 2026-07-01 | Unarmed control built (control.py): same output, same judge,
  temperature 0, fixed seed, only the watchlist varies. Judging refactored to
  one shared path (runner.judge_output) so the instrument and the live loop
  cannot drift. Both columns always reported: converted misses and induced
  false alarms.
- 2026-07-01 | The control downgraded my own result. Retro-control on the
  live catch: the deterministic judge catches that break unarmed, so the
  watch was not necessary and the anecdote is not supported. Qualifier: the
  control speaks for a temp-0 judge, production judges at sampling
  temperature, where the original misses really happened. Necessity is
  refuted, production effect is unmeasured.
- 2026-07-01 | Batch control, n=5: win column empty (0 conversions), cost
  column nonzero (1 induced false alarm), 1 break missed even armed, and 2
  clean outputs failed unarmed. The binding problem exposed is the judge's
  own baseline noise, not the watchlist. The spec's warning holds: the
  ingredients are backed, the magnitudes disappoint. Not a rate at this n,
  but the honest direction.
- 2026-07-01 | The control is the day's best result even though it tore one
  down: the system caught its own flattering claim before it hardened into a
  belief. Extract, do not apologize.
- 2026-07-02 | Judge calibration built (judgecal.py): the run record is a
  labeled corpus, re-judged under protocol v1/v2 by judge qwen/llama,
  deterministic, false-alarm and miss rates by class. Field-contract lesson
  paid: the corpus filter must require every field the harness consumes, and
  records predating a field are excluded, never guessed.
- 2026-07-02 | Calibration table, n=7 (2 broken, directional only): v1 qwen
  FA 0.40 miss 0.50. llama as judge is a rubber stamp, FA 0.00 by failing
  nothing, miss 1.00. v2 halved qwen's false alarms to 0.20 and suppressed
  its only true catch, miss 1.00. No condition is good. Production stays v1.
- 2026-07-02 | The v2 design error, mine: it optimized for low false alarms
  in an architecture where audience fails are verified claims and misses fall
  to slower detectors. False alarms are absorbed, misses are expensive.
  Converting uncertainty into pass is silence-is-not-safety violated in
  prompt form. v3 direction, designed not built: a three-way verdict, pass,
  fail with cited evidence, or uncertain-escalate, with uncertainty entering
  the flag tally as a low-weight raised hand instead of a forced binary.
- 2026-07-02 | Standing read at this model scale: neither local judge is a
  reliable criteria detector on its own, and execution carries the catching
  load. Consistent with the whole week: decorrelation by kinds of checker.
- 2026-07-02 | Conducting model adopted for the build itself: design,
  teardown, and review stay in the strong-model thread; grinding fans out to
  Claude Code sessions as work packets in bench/packets/, each carrying task,
  criteria, and gate, results appended to the packet. CLAUDE.md at the repo
  root is the baton every session reads first. The repo is the memory, not
  any session's context, which is the project's own thesis applied to its
  own construction.
- 2026-07-02 | PACKET-001: probe task pools moved to probe_tasks.py and the
  apply pool calibrated for headroom (calibrate.py, run 20260702-011304).
  Rule as packeted: keep only tasks where some seat scores below 1.0, pool
  mean per seat inside 0.3 to 0.9. Exactly 8 of 17 candidates qualified,
  baselines A=0.65, B=0.58. Every check pre-verified against a reference
  solution through the real evidence harness, because a check no correct
  solution passes is a broken instrument. Checks pinned by test.
- 2026-07-02 | PACKET-001 probe volume ran (probe 20260702-012616): six cells
  at R=3, n=24 per cell, on the calibrated 8-task pool. Matrix ev_mean is
  flat across lesson columns: qwen 0.80/0.80/0.80, llama 0.62/0.64/0.59,
  spread inside run-to-run noise at this n. The first probe's transfer
  gradient does not reappear on a calibrated instrument. What survives is
  the performer gap (qwen 0.80 over llama about 0.62) and the judge gap
  (llama pass rates 0.17 to 0.25 under qwen judging against ev near 0.62),
  the same judge-noise read judgecal gave. No transfer effect measurable
  at this n, direction included.
- 2026-07-02 | Conductor autopsy of the null: the twelve probe lessons are
  generation-task procedures and content-free platitudes, none touching the
  apply pool's rule classes. Two defects. The engine distills from single
  uncontrasted runs, skipping the spec's own core mechanism (Section 5, the
  contrast question), so form gates pass and information is absent. And
  PACKET-001's pools were disjoint at the rule-class level, not just the task
  level, my authoring miss, so even a perfect lesson could not have carried.
  The transfer bet is untested, not refuted. PACKET-002 fixes both, then
  re-runs the probe.
- 2026-07-02 | PACKET-002 mechanism built: rule_class on every task (four
  classes exactly, pinned by test), generation pool v2 (8 tasks, two per
  class, reference-verified like PACKET-001), contrastive engine path
  lesson.generate_contrastive (a failing and a passing attempt at the same
  task, R_G=3, no contrast means no lesson), content gate added to
  lesson.validate (non-empty rule field naming the stated rule, platitude
  screen, crude by design like the metric screen), and the menu matches
  rule_class through work_features with the matcher unchanged. The old
  uncontrasted generate path stays in code per packet, and its candidates
  now die at the content gate for lack of a rule field, which is the gate
  working as ordered. Noted in the packet FINDINGS.
- 2026-07-02 | Tier 1 fix, paid for twice: the session environment reaps
  background shells, and it stopped probe 20260702-051517 mid-run at 108 of
  192 rows (PACKET-001's probe got the same kill at its natural end, masked).
  The probe now resumes from its own record: py probe.py R <run_id> reuses
  the run id, reloads checkpointed runs from their summaries, skips
  completed work, and never distills the same contrast twice. Tested with
  stubs. Relaunches run detached from the tool's process tree and get
  polled by file, which was already the written rule for pipes and now
  covers process trees too.
- 2026-07-02 | PACKET-002 closed by the conductor: the executing session was
  environment-killed after its last commit, the detached probe finished
  alone, artifacts verified from disk. Proof of mechanism landed: the first
  real rule-lesson ("return the index of the last occurrence" at the stated
  tie), platitudes dead at the content gate. The governing finding is
  contrast starvation, within-task fail-and-pass on 1 of 16 seat-tasks, so
  stores were A=1 B=0 and the matrix is mostly baseline replicas. The one
  treated cell (llama tie_break 0.58 to 0.92 at n=6 on qwen's lesson) is a
  lead, not a result: untreated replicas show per-class noise up to 0.25.
- 2026-07-02 | PACKET-003 cut: sibling contrast within rule classes. A fail
  on one sibling plus a pass on the other, same seat, is a contrast, with
  within-task pairs taking precedence. Seat origin preserved. The content
  gate is not lowered to raise the count.
- 2026-07-02 | PACKET-003 mechanism built: lesson.generate_sibling_contrast
  distills from a fail on one sibling and a pass on the other, same seat,
  and must name the stated rule of the class, not the task. The probe's
  generation phase now builds contrasts per seat per class: within-task
  first, sibling as fallback for classes still without a lesson, at most
  two lessons per class per seat, and an all-fail class yields nothing
  with the reason recorded. Stub-tested: precedence, sibling firing, the
  all-fail case, the cap, and resume.
- 2026-07-02 | PACKET-003 probe ran (20260702-083121, R=3, n=24 per cell,
  GATE passed, detached, no kill): three lessons, all tie_break, all
  within-task. The sibling fallback never fired because six of eight
  class-seat cells produced zero failures, both siblings all_pass. The
  starvation moved upstream from pairing to failure supply. PACKET-002's
  transfer lead did not replicate: llama tie_break armed with qwen's
  lesson read 0.72 to 0.69 against last probe's 0.58 to 0.92, a +0.34
  delta becoming -0.03 under replication, and every treated per-class
  delta sits inside the untreated noise band at n=6. One committed lesson
  misaimed its rule field at the wrong stated rule and passed the content
  gate, flagged tier 2 in the packet with two more design findings. Next
  instrument fix, conductor's call: per-class per-seat headroom
  calibration of the generation pool, so every class breaks somewhere.
- 2026-07-02 | Conductor review of PACKET-003: accepted, all claims verified
  against the report (gen_accounting confirmed, matrix confirmed, misaimed
  rule read verbatim). Rulings on the three raised hands: FINDINGS 1
  approved as a crude aim screen (token overlap between rule text and the
  failing check, gate addition, built later). FINDINGS 2 approved, per-class
  cap replaces the has-a-lesson trigger. FINDINGS 3 approved in principle
  and deferred behind PACKET-004.
- 2026-07-02 | The deferral's reason, stated so the trap stays visible:
  three probes, zero surviving transfer signal, every null attributed to an
  instrument cause, each attribution evidenced. A chain of instrument
  excuses is also what protecting a bet looks like from the inside. So the
  alternative hypothesis gets tested directly before more supply work:
  PACKET-004 runs the spec's friction-theater test, three delivery arms
  (none, menu, explicit directive) on the existing aimed lessons, decision
  logic pre-registered in the packet.
- 2026-07-02 | PACKET-004 harness built (delivery.py): three delivery arms
  on identical tasks, criteria, and audience, only delivery varies. The
  runner gains an optional directives parameter, performer-bound and passed
  through guard_no_metric. Materials ride in a packet-local store
  (packets/PACKET-004-lessons.jsonl), the two aimed lessons selected by
  trail field, the misaimed one excluded with the loader enforcing it.
  Per-check pass rates are the report's sharp level, the three tie-rule
  checks marked as the treatment target. Resume-capable like the probe.
  The pre-registered decision logic stays in the packet and is applied in
  RESULTS by the reader, never computed by the harness.
- 2026-07-02 | PACKET-004 ran (delivery 20260702-171528, R=12 per arm per
  task, 72 runs, GATE passed, detached, no kill). Verbatim decision:
  AMBIGUOUS, no bucket forced. The structure behind the ambiguity,
  post-hoc: the buckets assumed the lesson helps or does nothing, and the
  lesson carries a direction. Where its "last occurrence" direction
  matches the task's stated tie rule, menu and directive both lift the
  tie checks off a 0.00 floor (to 0.25 to 0.42 at n=12). Where it
  contradicts the task (alphabetical ties), the directive injects the
  wrong direction and collapses the whole task (tie check 0.33 to 0.09,
  clean checks 0.92 to 0.36) while the menu still lifts (0.33 to 0.75).
  Menu never hurt on any of seven checks. Delivery that preserves
  performer judgment beat delivery that commands. Two tier 2 FINDINGS in
  the packet: direction-specific lesson wording is the hazard, and
  within-task contrast is what produces task-shaped wording, the
  class-level phrasing being exactly what the sibling path was built to
  elicit.
- 2026-07-02 | Conductor review of PACKET-004: accepted, every number
  verified against the report including the strongest claim, menu never
  hurt on any of seven checks while the directive collapsed a task the
  model otherwise aced. Rulings: friction theater refuted, the menu
  delivery changes output (three tie checks lifted, two off a 0.00 floor);
  the capability-floor hypothesis dies with it. The spec's shape-the-
  landscape principle survived a stress test against the command
  alternative with a measured safety property: tools that contradict the
  task get ignored, commands get obeyed into collapse. The flat probe
  matrices are explained: the effect is check-local and task-mean
  aggregation diluted it, three probes running.
- 2026-07-02 | PACKET-005 cut: the two approved gate changes (aim screen,
  cap precedence), direction-safe lesson phrasing with stated_direction in
  applicability (the spec's narrowing curing PACKET-004's hazard),
  generation-pool headroom calibration per class per seat, and the probe
  re-run with the check-level readout as the report's sharp level.
- 2026-07-02 | PACKET-005 built. Aim screen: token overlap between rule
  text and a ground of the failing checks plus the rule-class vocabulary,
  in both contrast generators, the only place the failing check is in
  hand. The class vocabulary is in the ground because the approved
  conditional phrasing names the class, not the function under test; a
  pure check-token ground would reject the phrasing the same packet
  mandates. Cap precedence: sibling mining runs for any unmined fail-task
  with a passing partner while the class cap (two) has room. Direction
  safety: tie_break tasks carry stated_direction into work_features, both
  prompts demand conditional phrasing and direction pinning, the menu
  refuses mismatches by existing contradiction logic, pinned by test.
  Gen pool: six harder candidates for the three all-pass classes,
  reference-verified; gencal.py measures them at R_G=3 per seat. Probe:
  rows carry per-check results, report carries the check-level table with
  rule checks marked. 98 tests green.
- 2026-07-03 | PACKET-005 probe ran (20260702-215407, R=3, n=24 per cell,
  GATE passed, detached, no kill). Supply moved: five lessons across
  three classes (tie_break, distinctness, normalize), all conditionally
  phrased, the one direction-specific lesson pinned to its direction and
  the pin verified live (rode every longest_word armed run, zero
  most_common_word runs). B tie_break went all_fail on both siblings, no
  passing partner, so cap mining stayed unexercised live and boundary
  stayed dry by sampling. The class-and-direction-matched treatment,
  llama longest_word on qwen's tie lesson, lifted both tie checks 0.00
  to 0.33 at n=3, PACKET-004's direction again; everything else sits
  inside noise that unarmed n=3 cells demonstrate by swinging 0.00 to
  1.00 between runs. Standing read: the probe measures supply and
  structure, the focused-arm format measures treatment. Three FINDINGS
  raised: code-seat headroom, the within-class content gap, and R=3
  check-level resolution.
- 2026-07-03 | Conductor review of PACKET-005: accepted, verified to the
  row level. The direction pin held live (all twelve armed
  most_common_word runs carried zero tools), the matched treatment is in
  the record (both longest_word rule checks 0 of 3 unarmed, 1 of 3 armed),
  stores and pins as claimed. Rulings: FINDINGS 3 adopted as standing
  doctrine, the probe measures supply and structure, the focused-arm
  format measures treatment. FINDINGS 1 (qwen-targeted generation) and
  FINDINGS 2 (a rule_topic applicability key) approved and deferred behind
  one focused measurement of the five existing lessons.
- 2026-07-03 | PACKET-006 cut: focused transfer arms, R=12, four pairings
  labeled topic_matched true or false. The matched pairings are the
  transfer test (including llama teaching qwen for the first time), the
  mismatched pairings are FINDINGS 2's evidence and a menu-safety check,
  prediction pre-registered as no effect, no harm. Reading rules verbatim
  in the packet.
- 2026-07-03 | PACKET-006 harness built (transfer.py): the five
  PACKET-005 lessons ride verbatim from packet-local store copies, four
  pairings, two arms, resume-capable, rows carry per-check results and
  the tool concepts that rode each run, report carries per-check tables,
  pooled rule-check counts (the packet's transfer criterion input), and
  the tool audit. Reading rules stay in the packet, applied in RESULTS by
  the reader, never computed by the harness. 105 tests green.
- 2026-07-03 | PACKET-006 ran (transfer 20260703-014859, 120 runs, GATE
  passed, detached, no kill). The first pre-registered transfer PASS:
  llama on longest_word armed with qwen's direction-pinned tie lesson,
  both rule checks 0.08 to 0.50 at n=12, pooled 2/24 to 12/24, third
  consistent measurement of this comparison. And the first menu-harm
  measurement: qwen on range_summary armed with llama's matched
  distinctness lesson declined 9/12 to 3/12 on the rule check and across
  the content checks, meeting the criterion's unsigned letter with a
  negative sign. The menu safety property is per-performer: llama judges
  its tools (mismatched pairing flat, safety reconfirmed), qwen obeys
  them, and the one recipe-shaped rule is the proximate suspect. Two
  FINDINGS raised: per-seat delivery safety measurement, and a
  declarative-shape screen for the rule field. Mismatched-pairing
  prediction held on llama, wobbled helpfully at 2/11 on qwen.
- 2026-07-03 | Conductor review of PACKET-006: accepted, verified to the
  digit (pooled 2/24 to 12/24 on P1, 9/12 to 3/12 on P2's rule check with
  boundary checks untouched, the content-side fingerprint of a misapplied
  recipe). The first pre-registered transfer PASS stands: chair memory
  carried value across model families through the production menu, third
  consistent measurement. The harm finding stands with it: the one lesson
  violating the spec's own definition (a lesson is not a procedure) is the
  one that harmed, on the seat that obeys tools. The definition is a
  measured safety requirement now, not prose.
- 2026-07-03 | Rulings: both PACKET-006 hands approved and combined.
  PACKET-007 cut: the declarative-shape screen on the rule field (fixture:
  the recipe lesson) plus the qwen delivery decomposition, same rule
  content in concept and recipe shape on matched and contradicting tasks,
  reading pre-registered including the branch that downgrades the harm if
  it fails to replicate. Spec v0.6 candidates grew: the transfer evidence
  statement, per-performer menu safety, and lesson-shape enforcement.
- 2026-07-03 | PACKET-007 built. Shape screen in lesson.validate: the
  listed implementation imperatives rejected in the rule field, the
  PACKET-006 harm lesson as the fixture, both distiller prompts carry the
  instruction. Fallout pinned honestly: transfer.py's store B now dies at
  the gates, the record stands and the instrument is superseded. Found
  while building work item 2 and load-bearing for reading every delivery
  result: the menu serves concept plus applies_when ONLY, the rule field
  never reaches a performer. PACKET-006's harm rode in the recipe
  lesson's concept text. The decomposition therefore carries its two
  shapes in the concept fields, and the discovery is flagged tier 2 in
  the packet. Obedience harness (obedience.py): qwen, two tasks, three
  arms, none at R=24 and menu arms at R=12 per the packet's 96-run total,
  hand variants packet-local with tie pins stripped and labeled. 116
  tests green.
- 2026-07-03 | PACKET-007 ran (obedience 20260703-043045, 96 runs, GATE
  passed, detached, no kill). The pre-registered contradiction branch
  fired: both shapes harm qwen on the contradicting task (rule check
  24/24 unarmed to 8/12 concept and 9/12 recipe), so qwen obeys tools
  regardless of shape and per-seat delivery policy goes to the
  conductor. The PACKET-006 harm did not replicate and is downgraded
  like PACKET-002's lead: same recipe lesson, same task, 0.75 to 0.25
  then, 0.50 to 0.58 now. Unregistered structure reported without
  forcing: the matched concept-shaped lesson posted the largest armed
  lift yet measured (0.50 to 0.92 rule check), recipe shape roughly
  nothing. The coherent read: qwen amplifies its tools in both
  directions, llama filters them. Two FINDINGS: the menu delivers
  concepts only so the shape screen guards a field that never rides,
  and obedience policy should weigh benefit, favoring wider
  applicability pinning over delivery bans. The direction pin already
  blocks this packet's exact contradiction; it only reached qwen
  because the pins were stripped by design.
- 2026-07-03 | Conductor review of PACKET-007: accepted, verified to the
  cell. The contradiction branch stands (24/24 unarmed to 8/12 and 9/12
  under contradicting tools of either shape), the PACKET-006 harm is
  downgraded per its own pre-registration, and the conductor's recipe-
  fingerprint reading of that harm dies with it, the fourth premature
  signal this bench has executed, two of them the conductor's. The
  standing model across three delivery packets: llama filters its tools,
  qwen amplifies them in both directions. Tool-response style is a casting
  dimension. The production direction pin already blocks the measured
  contradiction; it fired only because the packet stripped pins by design.
- 2026-07-03 | Rulings: both PACKET-007 hands approved into PACKET-008.
  The imperative screen extends to the concept field, the field that
  rides. No per-seat delivery bans: widen pinning instead, the deferred
  rule_topic key comes live. Fewer, cleaner, tighter-pinned lessons is the
  stated direction. Spec v0.6 candidates grew again: amplifier and filter
  seats, the delivery-surface fact, the shape screens, and the downgrade
  discipline itself.
- 2026-07-03 | PACKET-008 executed. Work item 1: the imperative screen
  covers the concept field, one inflection added ("stored in") because
  the packet's own fixture demanded it. Work item 2: rule_topic on all 31
  tasks from the fixed per-class vocabulary, exposed in work_features,
  pinned prompts and menu behavior; the PACKET-006 punctuation-on-
  delimiters mismatch is unservable by construction now. Work item 3:
  genpass 20260703-053623 at full gates, five lessons committed, all
  conditional, declarative, and topic-pinned. All five rejections were
  aim-screen kills of count_token within-task phrasing, and the sibling
  path delivered its first live commits in both seats as the rescue,
  evidence filed for the deferred class-level phrasing ruling. Zero
  imperative and zero platitude rejections at one pass: the prompts
  teach shape upstream. llama tie_break all_fail is three runs
  consistent. Process note: a git add -A swept the conductor's untracked
  v0.6 draft into a commit, caught and soft-reset immediately, explicit
  per-path staging since.
- 2026-07-03 | Conductor review of PACKET-008: accepted against the record
  (the results paste arrived empty, which changed nothing, the artifacts
  are the account). Five production-grade lessons, zero screen rejections
  at generation, the aim screen concentrated on within-task phrasing, and
  the sibling machinery's first live commits in both seats, two packets
  after it was built. The git add -A incident is Section 10's broadcast-
  from-source ambiguity observed in the meta-build, self-caught; per-path
  staging is now in the baton.
- 2026-07-03 | Ruling: the deferred within-task phrasing question closes
  on PACKET-008's data. The within-task distiller prompt aligns to
  class-level conditional phrasing, in PACKET-009 work item 1.
- 2026-07-03 | PACKET-009 cut: the confirmation arms. The 053623 stores
  measured through the production menu with every pin live, both teaching
  directions, pairings enumerated from the pins with structural empties
  named as supply findings, the tie comparison as replication four, and
  PACKET-007's record lift retested through the real path. Readings
  pre-registered including the branches that hurt.
- 2026-07-03 | PACKET-009 built. Within-task distiller prompt aligned to
  class-level conditional phrasing per the ruling, pinned by the capture
  test. confirm.py enumerates pairings from the pins, and the enumeration
  itself is the first result: of five production-grade lessons, three are
  structurally empty (both count_token punctuation lessons match no
  delimiters apply task, the count_distinct_pairs lesson matches no
  values apply task), and the packet's expected distinctness retest is
  unreachable through the production menu, the pins that cured harm cut
  supply. One cross-seat cell survives: llama on longest_word armed with
  both qwen tie lessons, replication four. Pin regression asserted clean
  on four deliberate mismatch cells at zero model cost. 128 tests green.
- 2026-07-03 | PACKET-009 closed by the conductor (session died after its
  build commit, the detached run finished alone, artifacts verified from
  the report and rows). Replication four is the project's strongest and
  cleanest result: qwen's tie lessons through the production menu, pins
  live, moved llama's rule checks 0.17 to 0.92 each, pooled 4/24 to 22/24
  at n=12 per arm, non-rule checks unharmed. Four consistent measurements
  in four configurations, one direction, one class, small models, and the
  claim stays that size.
- 2026-07-03 | The enumeration finding governs the next supply move:
  correct narrowing has a coverage cost. Three of five lessons are
  structurally empty, pins matching no apply task, which also made the
  PACKET-007 distinctness confirmation unreachable, so amplifier-plus-
  tight-pins remains doctrine, unconfirmed, per its own pre-registration.
  Supply topics and apply topics must overlap by construction: the next
  pass aims generation at in-pool topics or adds apply tasks per topic,
  never loosens a pin to force a match.
- 2026-07-03 | The stand-down session's three chat-only flags carried into
  the record by the conductor: the 24-runs-48-calls correction appended to
  PACKET-009 RESULTS (the conflation was the conductor's), the harm-column
  row-level support absorbed, and the supply diagnosis adopted as
  PACKET-010's spine: the filter is a conjunction, breaks for a seat AND
  carries an in-pool topic, applied before calibration. The raised-hand
  channel working from a session that was already standing down.
- 2026-07-03 | The wrap: CONTINUATION rewritten to the July 3 state,
  PACKET-010 cut (topic-covering supply, the reverse-direction hunt,
  supply only, measurement next). The strong-model window closes with the
  operating system tier-agnostic: packets, gates, verification discipline,
  and the record are the memory. Nine packets closed, 128 tests, one
  four-times-replicated result, and every dead signal buried where it was
  born.
- 2026-07-03 | PACKET-010 executed. The demand table said all four pairs,
  both seats. Nine conjunction-compliant candidates calibrated: llama
  broke on three (both new tie tasks and mode_count), qwen on zero, and
  two pairs are resistant (boundary/degenerate, normalize/delimiters,
  two candidates each, nothing broke), named not forced. Pool law
  changed: two-per-class retired for topic-coverage-with-breakage,
  pinned by test. Genpass at full gates: four lessons, zero rejections,
  including the first llama-origin tie lessons in the record (the
  enlarged tie class finally gave llama a passing sibling). Enumeration
  before and after: empty rate 3/5 to 3/9 with every remaining empty
  pre-conjunction (new store 0/4), and the reverse-direction cell EXISTS,
  qwen on longest_word under two llama-origin lessons, enumerated not
  measured. Tier 1 fix: the genpass gate line computed against a
  hardcoded four classes, now against the pool. Supply stays narrow:
  everything new is tie/direction/last, and the resistant pairs sit over
  the record's deepest unarmed floors.
- 2026-07-03 | Conductor review of PACKET-010: accepted against the record
  (tests green, coverage report verified, the session closed itself
  properly with a tier-1 gate-line fix done right). The conjunction filter
  validated by its own numbers, zero orphan lessons in the new store, the
  first llama-origin lessons exist, and the reverse-direction cell is
  reachable. Resistant pairs (boundary/degenerate, normalize/delimiters)
  sit over the record's deepest floors and stay named, not forced.
- 2026-07-03 | PACKET-011 cut, the window's last packet from this
  conductor: the reverse cell, one task, two arms, two pre-registered
  questions in one measurement, bidirectional transfer and the amplifier
  doctrine, read independently, harm column deciding the second. The
  conductor chair transfers with the record: whoever reviews PACKET-011
  verifies against artifacts, never accounts, and closes from the record
  if the session dies. Everything needed is in CONTINUATION.md, CLAUDE.md,
  and this file's tail.

- 2026-07-03 | Third-seat onboarding approved in principle, Brad's ruling
  delivered in chat and logged by the conductor. Trigger is PACKET-011's
  close: bidirectional-and-clean promotes onboarding to the next packet,
  flat-or-harmful defers it behind delivery diagnosis. Onboarding
  requirements per the record: a different family in the same size class,
  baselined and tool-response-probed before it teaches or learns.
  Unassigned branch, flagged at logging: reverse flat with the harm
  column clean, the combination the packet pre-registers as real and
  reportable, falls under neither trigger and takes Brad's call at close.

- 2026-07-03 | Brad's ruling on the flagged middle cell, logged beside the
  original: flat-and-clean DEFERS the third seat, promotion requires
  bidirectional-and-clean only, no branch of flat-and-clean promotes. The
  deferred diagnosis splits on the none arm's baseline. At or near
  ceiling: the cell was uninformative, select a different qwen-headroom
  pairing and re-measure before any third-seat work. Real headroom:
  diagnose the difference between the production-store lessons and
  PACKET-007's hand-authored matched content, which lifted the same seat
  (verified against the packet record: range_summary, rule check 0.50 to
  0.92, the largest armed lift measured), before any third-seat work.
- 2026-07-03 | PACKET-011 executed (reverse 20260703-095406, 24 runs, GATE
  passed, detached, no kill). The split answer: the harm column is clean,
  both non-rule checks 12/12 in both arms, so amplifier-plus-tight-pins
  is confirmed on its own criterion, AND the rule checks declined under
  matched pinned tools, 0.67 to 0.42 each, pooled 16/24 to 10/24 at n=12,
  said loudly per the packet. Reverse transfer is NOT shown: the unsigned
  criterion fires with a negative sign, as in PACKET-006, and no claim is
  made. The forward result stands untouched. Outcome is neither
  flat-and-clean nor bidirectional-and-clean: third seat stays deferred,
  and the none baseline (0.67, real headroom, the n=3 demand evidence
  reproduced exactly at n=12) selects the diagnosis branch. First exhibit
  filed in FINDINGS: source-task residue in both production lessons
  ("character runs", "longest run") against the residue-free
  hand-authored lesson that lifted this same seat, with the mechanism
  named: the aim screen pulls source nouns in while the phrasing
  instruction pushes them out, two gates leaning against each other.

- 2026-07-03 | Conductor review of PACKET-011: accepted against the record.
  Independent recount from the rows, done before reading the session's
  RESULTS, matched every report cell: pooled rule 16/24 none against
  10/24 menu, non-rule 48/48 across both arms, tools=2 on all twelve
  armed rows. The session applied the readings honestly, refusing the
  unsigned transfer criterion's letter (met with a negative sign, no
  transfer claimed), and said the rule-check decline loudly per the
  outranking clause. One inspected failing armed run adds a mechanism
  exhibit: qwen wrote reversed iteration with >=, inverting the tie
  direction the lessons teach, over-construction of behavior the unarmed
  seat already had. On that run the audience passed and evidence failed,
  the catching load sitting where the record says it lives.
- 2026-07-03 | Ruling on PACKET-011 FINDINGS 1: raised hand accepted, no
  gate change now. Source-task residue is the leading hypothesis, not a
  finding, and the aim-screen-against-phrasing tension it names is real
  and stays open until measured. Per Brad's middle-cell ruling the
  baseline showed real headroom (0.67), which selects the diagnosis
  branch: production-store lessons against hand-authored residue-free
  content on the same seat. PACKET-012 is that measurement. The gate
  change, residue screen or aim-ground change, gets designed from what
  it shows, never before.
- 2026-07-03 | Third-seat trigger applied per the standing rulings: the
  outcome is harmful on the taught checks, so the third seat is DEFERRED
  behind the delivery diagnosis. No branch promotes here.
- 2026-07-03 | Doctrine, paid for twice (PACKET-006, PACKET-011): a
  pre-registered directional reading states its sign. Same-direction-and-
  pooled-differ without a sign was satisfied downward twice. PACKET-012's
  readings comply.
- 2026-07-03 | PACKET-012 executed (diagnose 20260703-102824, 36 runs,
  GATE passed, detached, no kill). The ordering, clean harm everywhere:
  none 12/24, hand 10/24, prod 8/24 on pooled rule checks. Reading 1
  fires: the prod decline replicates, twice in the same direction,
  18/48 armed against 28/48 unarmed combined, and stands as a lean.
  Reading 2 does not fire: hand sits below none, residue is not shown
  to be the separator, no gate change gets designed. Reading 3 fires by
  sign at the weakest lean on record: hand trails none by 2/24 while
  the none baseline itself moved 4/24 between adjacent runs of this
  identical cell, the drift named as the yardstick. Reading 4 does not
  fire. Standing state: tie lessons of any authorship measured so far
  do not help qwen on longest_word through the menu, the same seat took
  the record lift from matched content on range_summary in PACKET-007,
  so the open contrast is task-and-topic shaped, not authorship shaped.
  Third seat stays deferred, diagnosis open. The hand lesson died at
  the gates as the packet anticipated (missing confidence and
  provenance, menu KeyError) and rode the PACKET-007 injection surface
  untouched, pinned by test; the menu's crash on confidence-less
  lessons is filed as a sharp edge.

- 2026-07-03 | Conductor review of PACKET-012: accepted against the record.
  Independent recount from the diagnose rows matched every cell: none
  12/24, prod 8/24, hand 10/24 pooled rule, harm 24/24 in every arm,
  tools 0/2/1 on every row. The hand lesson on disk matches the packet
  print byte-for-byte with no extra fields, and the prod store is
  byte-identical to the PACKET-011 arm store. The four signed readings
  were applied exactly as pre-registered, and reading 3's fire is
  recorded as uninformative under the drift yardstick the session itself
  named.
- 2026-07-03 | Ruling on PACKET-012 FINDINGS 1: the menu's KeyError on a
  confidence-less lesson is an instrument defect, not a gate question.
  Fix authorized: menu.query declines a lesson missing required fields
  instead of raising, with a test, carried as tier 1 terrain by
  PACKET-013. The gates themselves behaved correctly and stay untouched.
- 2026-07-03 | Ruling on PACKET-012 FINDINGS 2, adopted as measurement
  doctrine: a single-cell claim reads only against a same-run baseline,
  never a prior run's. A gap smaller than the observed run-to-run drift
  of the same cell is not a claim at any size. Sub-0.10 gaps at n=12
  require an interleaved design before they are trusted. The none
  baseline's 0.67 to 0.50 movement on the identical cell is the recorded
  exhibit.
- 2026-07-03 | PACKET-013 cut from what the data says: the open contrast
  is task-and-topic shaped, so the packet puts both tasks in one
  interleaved run on the same seat. longest_word none against the
  replicated-decline prod pair (third measurement), range_summary none
  against the PACKET-007 concept-shape distinctness lesson (the record
  lift, now tested under the drift doctrine). Four cells, R=12,
  interleaved by rep, signed readings, same-run baselines only. If the
  range lift fails to replicate, the PACKET-007 claim gets downgraded
  where it was made, by the conductor.
- 2026-07-03 | PACKET-013 tier 1, as authorized: menu.query declines a
  lesson missing the fields the menu consumes (concept, applies_when,
  confidence) instead of raising KeyError, no other menu behavior
  changed, pinned by test. The PACKET-012 gate-check test updated to pin
  the new behavior with the history noted in its docstring: validate
  still refuses the field-less lesson, the menu now shelves it silently.
- 2026-07-03 | PACKET-013 executed (contrast13 20260703-120009, 48 runs
  interleaved, GATE passed, detached, no kill, byte checks asserted).
  All four signed readings fired: task moderation inside one run (R-hand
  12/12 above R-none 8/12 while L-prod 2/24 sat below L-none 13/24),
  the PACKET-007 range lift replicated under the drift doctrine (no
  downgrade), the longest_word decline measured a third time at its
  largest (11/24 gap, three same-direction measurements, still spoken
  as direction), and harm columns clean everywhere for the fourth
  measurement running. The task moderates delivery on the amplifier
  seat, not the lesson's author. Grounded mechanism candidate filed in
  FINDINGS from sampled armed failures: qwen answers the tie task with
  the canonical first-tie idiom, max(words, key=len), while holding
  tools that state the last-tie rule, so the moderator candidate is
  whether the stated rule fights the canonical solution shape,
  classifiable in advance, a casting input. Next design targets the
  task separator.

- 2026-07-03 | Conductor review of PACKET-013: accepted against the record.
  Independent recount matched every cell: L-none 13/24 and L-prod 2/24 on
  pooled rule, R-none 8/12 and R-hand 12/12, boundary harm columns 12/12
  in every cell, range content checks up 4/12 to 5/12 under tools, tools
  0/2/0/1 on every row. Interleaving verified from the row sequence
  itself. Both byte checks re-verified independently. The mechanism
  exhibit spot-checked: the cited armed failure contains the canonical
  first-tie one-liner, byte-true. One correction filed against the
  conductor's own PACKET-011 exhibit: the over-construction read
  (reversed plus >=) was one sample of a broader pattern, under tools
  the seat regresses toward the canonical shape, sometimes decorated,
  sometimes bare, and the session's idiom-pull hypothesis covers both.
- 2026-07-03 | Ruling on PACKET-013 FINDINGS 1: the idiom-conflict
  moderator is adopted as the leading hypothesis, design-level, untested.
  It now shapes both live threads. It predicts where a fair reverse
  transfer test lives, on ground where the stated rule extends the
  canonical idiom instead of fighting it, which PACKET-013 measured
  range_summary to be. And it is a candidate forward-classifiable
  casting input for the forecaster family; no spec change until the
  moderator is tested directly, per the load-bearing rule.
- 2026-07-03 | PACKET-014 cut: the supply probe for the clean reverse
  test. PACKET-013 established the liftable ground (qwen gains on
  range_summary through the menu). The reverse question Brad named as
  thesis-level needs a llama-origin lesson on that ground, and llama's
  measured breaks so far are tie-class only. The probe measures whether
  llama supplies breaks and contrast pairs in the distinctness class,
  and if eligible pairs exist, runs genpass at full gates into a
  packet-local store, PACKET-010 precedent. Probes measure supply and
  structure, no treatment claims. CONTINUATION.md is three packets
  stale and gets refreshed after the direction call this fork lands.
- 2026-07-03 | PACKET-014 executed (probe14 20260703-142225, 72 runs,
  GATE passed, detached, no kill). Counts: twelve distinctness tasks
  enumerated before any run, seven generation-eligible; llama broke on
  one generation-eligible values task (sum_distinct, 1 of 6, after two
  all-pass R_G=3 passes, so R=6 bought the break R_G=3 missed twice),
  on the orphan-topic count_distinct_pairs (filtered by the
  conjunction, as designed), and on range_summary itself (2 of 6, the
  apply target, recorded not mined, disjointness held). One eligible
  pair, one distillation attempt, one commit, zero rejects, into the
  packet-local store only: a conditional, declarative, values-pinned
  llama-origin distinctness lesson that matches range_summary by its
  pins. The closing sentence: the reverse cell on liftable ground IS
  REACHABLE. The measurement is the next packet's.

- 2026-07-03 | Conductor review of PACKET-014: accepted against the record.
  Independent recount matched every count: 72 rows, twelve tasks at n=6,
  the fail column identical cell for cell (sum_distinct 1/6,
  count_distinct_pairs 1/6, range_summary 2/6, count_pairs 1/6, the rest
  0/6). The packet-local store holds exactly one lesson, distinctness and
  values pins, engine provenance, confidence present, trail to
  sum_distinct, concept text as quoted. The R=6 note stands as recorded:
  the probe bought the break two R_G=3 passes missed.
- 2026-07-03 | PACKET-015 cut: the clean reverse test, origin parity on
  liftable ground. Three interleaved arms on range_summary, qwen
  performing: none, rev (the PACKET-014 llama-origin lesson), hand (the
  PACKET-007 lesson that lifted this seat twice). Signed readings with
  the drift bar stated per task (recorded range_summary baseline
  movement is 2 of 12, the bar). The parity reading is the thesis
  sentence pre-registered: inherited content performing comparably to
  the seat's best known content on the same ground. The harm doctrine
  and the drift doctrine are reconciled in the packet before the run:
  every decline is reported, a decline above the bar outranks everything,
  a decline at or under the bar is inside recorded drift and claims
  nothing. CONTINUATION.md refreshed to the current state in the same
  commit, as promised in this file on the PACKET-014 cut.
- 2026-07-03 | PACKET-015 executed (parity15 20260703-151821, 36 runs,
  GATE passed, detached, no kill, byte checks asserted, tool audit
  clean). ALL FOUR SIGNED READINGS FIRE. The rule check: none 8/12, rev
  12/12, hand 12/12, the same-run none baseline reproducing PACKET-013's
  exactly. Reading 1: the first measured cross-family reverse transfer,
  rev above none by 4/12 against a 2/12 bar. Reading 2, the thesis
  sentence: origin parity holds at zero distance, the inherited lesson
  and the seat's best hand-authored content indistinguishable at n=12,
  both above baseline past the bar. Reading 3: the hand lift's second
  interleaved replication at identical cell values. Reading 4: harm
  columns clean everywhere, fifth consecutive clean measurement, the two
  content-adjacent checks up 1/12 each, inside drift, claiming nothing.
  The rev lesson's lineage is the production pipeline end to end with no
  hand anywhere in it: llama's sum_distinct break, full-gate
  distillation, topic pins, menu delivery, the other seat lifted.
  Transfer now runs in both directions on the record. Every claim one
  task, one seat, one lesson, n=12, direction never a rate. What this
  means for the standing rulings is the conductor's reading.

- 2026-07-03 | Conductor review of PACKET-015: accepted against the record.
  Independent recount matched every cell: rule check none 8/12, rev
  12/12, hand 12/12; content checks 8/12 to 9/12 in both armed cells,
  inside the bar; boundaries 12/12 everywhere; tools 0/1/1 on every row;
  interleave verified from the row sequence; both stores byte-identical
  to their sources. All four signed readings fired as applied. The
  reverse-transfer and parity results stand at their stated size, one
  task, one seat, one lesson, n=12, direction never a rate, and per the
  replication doctrine they are leans until the cell replicates. The
  reverse replication is queued behind third-seat onboarding.
- 2026-07-03 | Ruling, executing the standing third-seat tree: PROMOTED.
  Brad's pre-registered condition was bidirectional-and-clean. PACKET-011
  fired the harmful branch and deferred behind the delivery diagnosis;
  that diagnosis is now complete (task moderation measured, the idiom
  hypothesis adopted, the confound removed) and the condition is met on
  unconfounded ground: transfer measured in both directions with harm
  columns clean in five consecutive measurements. The onboarding
  requirements apply verbatim as Brad ruled them: a different family in
  the same size class, baselined and tool-response-probed before it
  teaches or learns. PACKET-016 carries the onboarding. Brad can
  override this reading; the record says the condition is met.
- 2026-07-03 | PACKET-016 cut: third-seat onboarding, staged. Stage 0
  selects the seat from the installed models by the ruled requirements,
  or stops with a supply answer if none qualifies. Stage 1 baselines the
  seat across both pools, counts only. Stage 2, only if stage 1 shows
  headroom on the liftable ground, runs the seat's first tool-response
  reading, armed with the PACKET-014 lesson against none, signed, which
  measures the casting trait and gives the reverse lesson its second
  receiving seat in one cell. The seat neither teaches nor learns in
  this packet. CONTINUATION.md updated in the same commit where the
  promotion made it stale.
- 2026-07-03 | PACKET-016 executed and closed at stage 0 on the packet's
  own supply rule, no model runs. The installed list holds no qualifying
  seat: every candidate is an existing seat's family (llama3.1:8b,
  qwen2.5-coder:7b, three qwen vision variants) or a glm-ocr model,
  which the record ruled out for reasoning on day one and which sits
  under the size class besides. The third seat is promoted by ruling
  and blocked on model supply. The shopping list is unchanged from the
  2026-07-01 entry: gemma3 or mistral in the 7 to 9B class, several GB,
  Brad's go required. Stage 1 and stage 2 did not run; the seat that
  does not exist neither taught nor learned.

- 2026-07-03 | Third seat named: mistral:7b, pulled by Brad on the
  conductor's recommendation. The teardown behind the pick, in the record
  so nobody relitigates it: mistral is a genuinely separate lineage in
  the ruled class; gemma3's installed sizes (4B, 12B) straddle the class
  so the qualifying gemma is gemma2:9b; and deepseek-r1:7b and :8b are
  disqualified despite the name, they are distills on qwen and llama
  bases, a family violation in substance. PACKET-017 cut: PACKET-016's
  stages 1 and 2 executed verbatim against the named seat, stage 0
  reduced to a presence check. The closed packet stays closed; the new
  one inherits its spec.
- 2026-07-03 | PACKET-017 executed (onboard17 20260703-161320, 264 runs,
  GATE passed, detached, no kill). Mistral:7b is onboarded to the
  letter: baselined across both pools at R=6, tool-response-probed,
  taught nothing, learned nothing. Stage 1 counts: headroom on 30 of 40
  tasks, the broadest on record, and eight eligible contrast pairs
  spanning all four classes at the cap, including the two resistant
  pairs (boundary/degenerate, normalize/delimiters) broken for the
  first time by any seat. Stage 2 on range_summary read FLAT: the rule
  check sat 0/12 in both cells because the packet's any-fail condition
  admitted floor ground, not mixed ground, so the trait stays
  unmeasured. Said loudly per the packet: the empty-input harm column
  declined above the bar under the matched tool (12/12 to 6/12) while
  the single-number check rose above it (2/12 to 6/12), a
  boundary-behavior disturbance at content floor that matches neither
  recorded trait signature. Three hands raised: the resistant-pair
  supply waits on a teaching ruling, the next trait cut should
  condition on mixed ground, and the disturbance deserves a designed
  measurement before it gets a name.

- 2026-07-03 | Conductor review of PACKET-017: accepted with one
  correction. Independent recount matched the stage 1 table cell for
  cell across all 40 tasks and the stage 2 table exactly (rule 0/12 both
  cells, empty-input 12/12 to 6/12, single-number 2/12 to 6/12, tools
  0/1 on every row). The one error: the session's headroom summary wrote
  30 of 40 while its own verified table counts 33, corrected in place in
  the packet RESULTS at review. The eight-pair enumeration is consistent
  with the verified counts. The flat reading and the loudly-said
  boundary decline stand as written.
- 2026-07-03 | Rulings on PACKET-017's three raised hands. FINDINGS 2,
  adopted as doctrine: a trait cut conditions on MIXED ground at the
  rule-check level (partial competence, not floor, not ceiling), never
  on any-fail; the floor cell that taught this is the exhibit. FINDINGS
  3: the boundary-behavior disturbance is real data measured once at
  floor and gets NO NAME until its designed measurement on mixed ground;
  the trait packet carries pre-registered boundary-watch columns for it.
  FINDINGS 1, the teaching ruling: the seat's teaching gate STAYS CLOSED
  until the trait is measured. Brad's onboarding requirement is
  tool-response-probed before it teaches or learns, and the probe came
  back trait-unmeasured on floor ground; the letter ran, the spirit did
  not, and the spirit holds. The resistant-pair mining is queued
  immediately behind the trait reading.
- 2026-07-03 | PACKET-018 cut: the mistral trait measurement on mixed
  ground. longest_word qualifies at the check level (rule checks 1/6
  each at baseline, verified from the stage 1 readouts before the cut),
  and the production tie pair matches it by pins. The pre-registration
  carries an honest ambiguity, stated with the sign: GAIN on this ground
  is strong filter-or-better evidence, gaining where the amplifier seat
  lost; HARM is ambiguous between the amplifier trait and the
  idiom-conflict ground and the writeup must say so; FLAT claims
  nothing. Boundary-watch columns pre-registered for the FINDINGS 3
  shape, reported as watch data, unnamed.
- 2026-07-03 | PACKET-018 executed (trait18 20260703-184848, 24 runs,
  GATE passed, detached, no kill, byte check and tool audit clean). The
  reading: FLAT, pooled rule checks none 0/24 against armed 1/24, a gap
  of 1 inside the 4-of-24 bar, claiming nothing, and the ambiguity
  sentence stays uninvoked. The run's real contribution is the premise
  failing under measurement: the mixed label from stage 1's R=6 (rule
  checks 1/6 each) did not reproduce, the none cell sat at floor, and
  the trait is now unmeasured twice at 48 runs of cost with the ground
  at fault both times. FINDINGS 1 raises the qualification fix: trait
  ground must reproduce as mixed at the rule-check level, two or more
  passes in six or n of 12 or more, before the next cut. Boundary-watch
  came back quiet: the empty-input check moved 2/12 down, at the bar,
  one-directional, unlike the above-bar two-directional floor-cell
  disturbance, recorded as unnamed watch data beside it. The seat
  neither taught nor learned; the teaching gate stays closed with the
  trait still unmeasured.

- 2026-07-03 | Conductor review of PACKET-018: accepted against the record.
  Independent recount matched every cell (rule checks 0/12 and 0/12 none
  against 0/12 and 1/12 armed; watch checks 3/12 to 1/12 and 12/12 flat;
  tools 0 and 2 on every row; interleave verified from the row sequence;
  store byte-identical to PACKET-012's). The FLAT reading and the quiet
  boundary-watch stand as written. Conductor's ownership, filed where the
  claim was made: the cut conditioned on an R=6 label under the
  conductor's own day-old doctrine, one rule-check pass in six read as
  verified mixed. The doctrine was insufficient as written and the
  24-run cost lands on the cut, not the session.
- 2026-07-03 | Doctrine amended on PACKET-018 FINDINGS 1, superseding the
  qualification method in the 2026-07-03 mixed-ground entry (the mixed
  requirement itself stands): trait-ground qualification is staged
  inside the packet. The same-run none cell runs first at R=12 and gates
  the armed cell, which launches only if the pooled rule readings land
  mixed, at least 4 passes and at least 4 fails of 24. A wrong ground
  label now costs 12 runs, not 24, and the qualification IS the
  treatment baseline, so no run is spent twice. R=6 labels are casting
  hints, never ground qualification.
- 2026-07-03 | The open fork, logged and awaiting Brad's ruling because it
  amends his own: the third seat's trait is currently unmeasurable with
  existing material. longest_word is disqualified by failed
  reproduction, range_summary sits at rule-check floor for this seat,
  and no other gated lesson matches any mistral ground by pins. The
  teaching gate as ruled (tool-response-probed before it teaches or
  learns) therefore deadlocks the seat entirely, including the
  resistant-pair supply that only this seat has ever provided. The
  proposed split: the gate's rationale, tool response sets how tightly a
  seat's menu gets pinned, governs delivery TO a seat, not generation
  FROM its breaks, and the receiving seats' traits are measured. Opening
  generation-from while keeping delivery-to gated would unblock the
  resistant-pair mining without touching what the gate protects. Brad's
  call, no packet cut until he rules.

- 2026-07-03 | DOWNGRADE, the conductor's own, filed where the claim was
  made: the 2026-07-03 open-fork entry claimed the third seat's trait is
  unmeasurable with existing material and proposed splitting the
  teaching gate. Brad's forcing question (is this the floor or a lesson
  not yet learned) found the flaw, and the claim was wrong twice. First,
  hand-authored instruments are standing practice for trait measurement
  (PACKET-007 characterized qwen's trait with them) and origin was
  measured not to moderate delivery, so "no gated engine lesson" never
  implied "unmeasurable." Second, the no-match check was run against the
  kept pool only; the candidate pool holds second_largest and dedupe,
  both annotated distinctness/values, both mixed for mistral at
  baseline, and both matched by the PACKET-014 llama-origin lesson's
  pins. The split proposal is WITHDRAWN as premature. The teaching gate
  stands exactly as Brad ruled it and opens by its own wording when the
  trait measures.
- 2026-07-03 | Doctrine refined: the staged-qualification amendment said
  the qualification is the treatment baseline. Corrected: qualification
  GATES only. The treatment reading takes fresh interleaved none and
  armed cells on the qualified ground, per the drift doctrine, at 12
  extra runs of cost. A gate read and a baseline read are different
  jobs and stop sharing a sample.
- 2026-07-03 | PACKET-019 cut: the trait measurement done right. Stage A
  qualifies ground in ranked order (second_largest, then dedupe), none
  cell at R=12, mixed means at least 4 passes and 4 fails of the 24
  pooled rule readings, stop on the first qualifier or close with a
  supply answer if neither holds. Stage B on the qualified ground:
  fresh interleaved none and armed at R=12 each, armed is the
  PACKET-014 llama-origin lesson byte-copied, three-exit signed reading
  at the 4-of-24 bar, boundary-watch columns unnamed, and if HARM fires
  the writeup names both candidate causes (seat trait, and the
  instrument's source-task residue, which PACKET-012 denied separation
  but did not bury). The cell doubles as the llama-origin lesson's
  third receiving seat, claim sized to one task, one seat, n=12 if it
  lands. The seat neither teaches nor learns.
- 2026-07-03 | PACKET-019 tier 1, in the packet's own terrain: the stage
  A candidates carried no rule_checks annotation (only kept apply tasks
  got them in PACKET-005, and second_largest and dedupe are dropped
  candidates). Annotated from each task's stated rule: second_largest
  pins its two distinctness traps ([5,5,5] and [2,1,2]), dedupe pins its
  two first-appearance-order traps ([3,1,3,2,1] and ['b','a','b']),
  boundary checks stay unannotated. Pinned by test, printed in RESULTS
  before the run per the packet.
- 2026-07-03 | PACKET-019 executed (trait19 20260703-201821, 36 runs,
  GATE passed, detached, no kill, byte check and tool audit clean). The
  staged doctrine worked first time: second_largest qualified at stage A
  (13 passes, 11 fails of 24, the sweep stopped there, dedupe unrun) and
  the ground REPRODUCED in stage B's fresh cells (none 12/24 mixed), so
  the trait cell measured the seat, not the ground, for the first time.
  The reading: FLAT, armed 13/24 against none 12/24, gap 1 inside the
  4-of-24 bar, claiming nothing, the two-cause sentence uninvoked. The
  machine-born lesson's third receiving seat neither gained nor lost
  from it on matched mixed ground. Boundary-watch quiet for the third
  cell running, the floor-cell disturbance still without a second
  sighting. Three seats now read as three tool responses at their
  stated sizes: qwen amplifies, llama filters, mistral's one valid cell
  sits unmoved between them, a lean not a casting entry. The seat
  neither taught nor learned; the teaching gate's condition now has its
  measurement and the gate consequence is the conductor's reading.

- 2026-07-03 | Conductor review of PACKET-019: accepted against the record.
  Independent recount matched every cell: stage A 13 passes 11 fails of
  24 exactly; stage B rule checks 7/12 and 5/12 none against 7/12 and
  6/12 armed (12/24 and 13/24 pooled); watch columns as written; stage B
  interleave verified true across all twelve reps; the armed store
  byte-identical to PACKET-014's; tools 0 and 1 on every row. The FLAT
  stands, and for the first time it is a measurement of the seat: the
  ground qualified at R=12 and reproduced in the fresh cells. The tier 1
  annotation of the two candidate grounds is accepted as in-terrain,
  pinned, and printed before the run as required.
- 2026-07-03 | Ruling, the teaching gate: OPEN for mistral:7b. Brad's
  condition was baselined and tool-response-probed before it teaches or
  learns. The baseline is PACKET-017's, and the probe now has a valid
  measurement: one qualified, reproduced cell reading indifferent, armed
  13/24 against none 12/24 under a matched machine-born lesson. The
  letter and the spirit are both met. Sizing filed with the ruling: the
  trait entry is a LEAN, one cell, not a casting profile, and it gets
  replicated opportunistically in future delivery cells rather than by
  a dedicated packet. Brad can override; the condition as he worded it
  is satisfied on the record.
- 2026-07-03 | PACKET-020 cut, executing the standing queue (the
  resistant-pair mining was queued immediately behind the trait
  reading): distillation from the PACKET-017 record. The eight
  enumerated eligible pairs, genpass at full gates, packet-local store
  only, every gate outcome reported, accepts and rejects both. The
  prize is the record's first lessons in the boundary and normalize
  classes, the two that resisted every prior seat, from the seat that
  plays worst and breaks widest. Production-store admission is NOT this
  packet's and stays a separate conductor-and-Brad ruling. The reverse
  replication remains queued directly behind.
- 2026-07-03 | PACKET-020 executed (mine20 20260703-211439, GATE passed,
  detached, no kill, no new supply runs, distillation from the
  PACKET-017 artifacts only). A clean sweep: 8 attempts, 8 accepts, 0
  rejects, every screen silent, all four classes covered in the
  packet-local store, every lesson origin-stamped mistral:7b. The
  closing sentence: the record now holds its first gated boundary-class
  and normalize-class lessons, YES on both, from the seat that plays
  worst and breaks widest. Two quality observations filed for the
  admission ruling: the weighted_mean lesson wildcarded its topic and
  by pins rides every boundary task, and the depth_max sibling lesson
  carries a mild cross-topic trace of its pass-partner ("case
  normalization" on a delimiters pin), the PACKET-011 residue mechanism
  at its faintest. Admission stays the separate ruling; the reverse
  replication stays queued.

- 2026-07-03 | Conductor review of PACKET-020: accepted against the record.
  Independent verification: eight lessons in the packet-local store with
  the claimed classes, pins, engine provenance, and mistral origin
  stamps; the weighted_mean topic pin is the literal wildcard; the
  depth_max lesson carries the cross-topic phrase as flagged; production
  lessons.jsonl untouched; the close commit touched only packet and run
  files; no new model-run artifacts exist, distillation only. First
  gated boundary and normalize lessons on record, from the third seat's
  first teaching work.
- 2026-07-03 | The conductor's admission recommendation, filed for Brad's
  ruling (admission is conductor-and-Brad by the standing rule): admit
  NONE of the eight yet. The bar proposed: a lesson enters the
  production store on its first non-harmful delivery reading, which
  matches the discipline everywhere else in this record, no signal
  believed before it shows up in a measurement. All eight stay
  packet-local and delivery-eligible. The two flagged lessons carry
  extra conditions: weighted_mean's wildcard topic pin rides every
  boundary task by pins, which is the measured amplifier exposure class,
  so it is not delivery-eligible to qwen until regenerated or narrowed;
  and the wildcard passing the gates is a gate gap, logged as a LEAD for
  a future screen, not changed now, gate changes are paid for by
  measured failures. depth_max's faint residue needs no special
  handling beyond its delivery cell being its watch.
- 2026-07-03 | PACKET-021 cut, executing the standing queue: the reverse
  and parity replication. PACKET-015's design re-run whole: three
  interleaved cells on range_summary, qwen performing, none, rev, hand,
  R=12 each, byte-copies, the 2-of-12 bar, the same four signed
  readings. Framing pre-registered: readings 1 and 2 firing again
  upgrade the reverse-transfer and parity leans to replicated results,
  still sized to one task, one seat, two measurements. Either failing
  downgrades the PACKET-015 lean where it was made, by the conductor.

- 2026-07-03 | ADMISSION RULED BY BRAD: admit. The Patron overrode the
  conductor's hold recommendation, and the ruling is executed as
  conductor work on the protected surface: all eight PACKET-020 lessons
  appended to the production store byte-verbatim from the packet-local
  store, verified (store 3 to 11 lessons, appended tail byte-identical,
  tests green after the append). The production store now spans all
  four rule classes and two origin seats plus the pre-pin era three.
  Standing conditions that survive admission because they are delivery
  rules, not admission bars: weighted_mean's wildcard-topic lesson is
  not delivery-eligible to qwen until regenerated or narrowed (the
  measured amplifier exposure), and the wildcard-past-the-gates lead
  stands for a future screen. First production admission on the record,
  and the precedent it sets is Brad's bar, not the conductor's.
- 2026-07-04 | PACKET-021 executed (parity21 20260703-214759, 36 runs,
  GATE passed, detached, no kill, byte checks and tool audit clean,
  interleave logged). THE THESIS REPLICATED, no failed replications to
  name. Rule check none 4/12, rev 11/12, hand 10/12. Reading 1 fires
  again, rev above none by 7/12: reverse transfer UPGRADES to a
  replicated result at two measurements. Reading 2 fires again, rev and
  hand 1/12 apart with both clearing none past the bar: origin parity
  UPGRADES to a replicated result at two measurements. Reading 3, the
  hand lift, fires a third time (8 to 12, 8 to 12, 4 to 10). Reading 4:
  harm columns identical across all three cells, the sixth consecutive
  clean harm measurement. The none baseline moved 8/12 to 4/12 between
  runs, the largest recorded drift on this task, and the same-run
  interleaved design absorbed it whole. Claims stay sized: one task,
  one seat, one lesson each way, two measurements, direction never a
  rate. Session start note: a transient modified flag on lessons.jsonl
  was investigated before any work and proved byte-identical to HEAD,
  stat noise, no surface touched.

- 2026-07-04 | Conductor review of PACKET-021: accepted against the record.
  Independent recount matched every cell, the interleave verified true
  across all twelve reps, both stores byte-identical to their sources,
  tools 0/1/1 on every row, production store untouched at eleven. The
  upgrades stand as pre-registered: reverse transfer and origin parity
  are REPLICATED RESULTS at two measurements, the hand lift stands at
  three, harm columns clean six consecutive. Claims stay sized: one
  task, one seat, one lesson each way, two measurements, direction never
  a rate. The stat-noise note is accepted as investigated and clean.
  Conductor's flag for Brad, spec consequence: v0.6 Section 1 reads
  "first evidence in one direction at small n, the reverse direction is
  unmeasured," which is now stale against the record. A v0.7 pass is
  proposed as the next conductor-and-Brad canonical task, on Brad's go,
  never a packet's.

- 2026-07-04 | SPEC VERSIONED on Brad's go: DIMINUENDO_TECHNICAL_SPEC_v0.7
  created from v0.6 with the second window's grades. The load-bearing
  edits, each traceable to the packet record: Section 1 chair-holds-
  memory now carries bidirectional replicated transfer with origin
  parity; Section 5 tool response now reads three seats three responses,
  corrects the pins claim (harm occurred under fully pinned matched
  tools on idiom-conflict ground, superseding "only with pins
  stripped"), and carries the task-moderates-delivery finding plus the
  trait-ground doctrine; Section 5 transfer break updated to replicated
  bidirectional with the supply constraint moved to delivery evidence;
  Section 6 casting profile adds the indifferent trait value and the
  mixed-ground read condition; Section 12 adds the delivery moderator as
  the new open center with its three named remainders. v0.6 archived,
  read never edited. Pointer documents reconciled: 00_START_HERE,
  01_PROJECT_INSTRUCTIONS, CLAUDE.md all reference v0.7. Voice scan
  clean.
- 2026-07-04 | HANDOVER.md created at the repo root: the chair-transfer
  document carrying the next conductor's kickoff prompt, the
  packet-kickoff pattern, the verification ritual as practiced and
  proven this window, the window's established results at their sizes,
  the standing conditions that survive the transfer, and the ranked
  board pointer. CONTINUATION.md was refreshed at the PACKET-021 close
  and stands current. The chair transfers with the record: this window
  closes at PACKET-021 with the queue empty, the tree clean, and every
  claim in the record traced to artifacts.

- 2026-07-04 | PACKET-022 cut by the new conductor, executing the top of
  the ranked board from the handover: first delivery cells for the
  admitted boundary and normalize lessons at the deepest unarmed apply
  floors. Design: llama3.1:8b receives (the measured filter, lowest
  harm risk for a first delivery reading, and every cell a new
  mistral-to-llama transfer edge; qwen is blocked for the wildcard
  lesson by standing rule and carries the untested idiom-conflict harm
  risk, which deserves its own designed cell, not a first-arming
  ride-along). Two ranked qualification sweeps per the staged doctrine,
  stop at first qualifier per class, then single-lesson armed cells so
  every reading attributes to one lesson: none, armed-A, armed-B
  interleaved at R=12 per qualified ground. Bars scale with the
  ground's rule-check count (2 of 12 pooled one-rule, 4 of 24 pooled
  two-rule), qualification at the PACKET-019 fraction. The depth_max
  cell is the residue watch the admission ruling named; the
  weighted_mean cell is the wildcard's first exposure reading. Seat
  choice is flagged for Brad's override before kickoff.

- 2026-07-04 | Brad ruled on the PACKET-022 seat flag: go as cut, llama
  receives. The safe-and-methodical path is chosen deliberately, one
  packet per seat, cut from the last reading, no pre-queued repeats.
  The qwen version waits on the idiom-conflict moderator classification
  either way.

- 2026-07-04 | PACKET-022 executed (armfloors22 20260704-051116, 132
  runs, GATE passed, detached, no kill, all four byte checks asserted
  twice, tool audit and interleave verified from the rows). Stage A:
  merge_ranges 0/12 and snake_to_camel 0/12 are absolute floors for
  llama and median 24/24 a ceiling; flatten_once qualified 8 passes 4
  fails of 12, balanced qualified 19 passes 5 fails of 24, both sweeps
  stopped at their first qualifier. Stage B: all four pre-registered
  readings FLAT at their scaled bars. chunk 4 against 4 on flatten_once;
  the weighted_mean wildcard 2 against 4, down at exactly the bar, its
  first exposure reading on over-broad ground; split_csvish 15/24
  against 16/24; the depth_max residue lesson 20/24 against 16/24, up
  at exactly the bar, its watch cell quiet of harm. All four admitted
  floor lessons now hold first non-harmful delivery evidence, and the
  mistral-to-llama edge has its first four measurements, no lean. One
  above-bar watch decline in the armed-B2 cell reported no-name beside
  the PACKET-017 shape and not matching it, with eight unrunnable
  boundary outputs (the same SyntaxError comprehension shape in all
  eight) under it. Tier 2 flag filed: the pooled-count accounting for
  unrunnable output needs a doctrine ruling, both accountings agreeing
  on every exit here. 200 tests green.

- 2026-07-04 | Conductor review of PACKET-022: accepted against the
  record. Independent recount matched every cell in both accountings,
  stage A arithmetic confirmed (merge_ranges 0/12 floor, median 24/24
  ceiling, flatten_once 8p/4f qualified, snake_to_camel 0/12 floor,
  balanced 19p/5f qualified), interleave verified exact from the row
  sequence in both blocks, tool audit clean on all 72 stage B rows, all
  four packet-local stores byte-identical to their production lines by
  the conductor's own hashes, production store untouched at eleven, 200
  tests green rerun by the conductor. The four readings re-applied
  verbatim from the packet against the recount: FLAT, FLAT, FLAT, FLAT,
  the same exits. All four admitted boundary and normalize lessons hold
  their first non-harmful delivery evidence. The commit swept nothing
  foreign: every run record in 8bac3d0 sits inside the run's own window.
- 2026-07-04 | DOCTRINE RULED on PACKET-022 FINDINGS 1, the unrunnable
  accounting: unrunnable-as-fail is canonical for pooled rule checks.
  The bars are stated in counts at fixed R, and readings-present shrinks
  the denominator, so cells would silently compare different n's. A run
  whose output does not compile followed no rule, and the canonical
  accounting keeps the pooled counter consistent with the runner's own
  verdict. Readings-present stays as a reported diagnostic beside it,
  and the per-cell unrunnable count is a standing reported column from
  here on. The cost, named: unrunnable-as-fail cannot separate a lesson
  that degrades rule-following from one that degrades compilation. When
  that distinction matters it gets its own designed measurement, not a
  quiet accounting flip.

- 2026-07-04 | THE MODERATOR CLASSIFICATION FILED, board item 2, design
  work, conductor authored for Brad's teardown before any run. The
  criterion: FIGHTS when the stated rule requires changing code inside
  the canonical idiom's core, EXTENDS when the rule is a separable step
  around the intact idiom. The table, all eight apply tasks:
  longest_word FIGHTS (anchor), range_summary EXTENDS (anchor),
  most_common_word FIGHTS, merge_ranges FIGHTS (the mildest call, one
  token but inside the core comparison), flatten_once FIGHTS, median
  EXTENDS, snake_to_camel EXTENDS, balanced AMBIGUOUS and excluded (two
  candidate idioms with opposite classifications; which one a seat
  reaches for is an empirical per-seat fact). The anchors calibrated
  the criterion and cannot confirm it.
- 2026-07-04 | PACKET-023 cut: the moderator test. The sharpest
  available design: one lesson (chunk, boundary/degenerate, production
  line 8), one seat (qwen, the amplifier), two grounds classified
  opposite before the run, merge_ranges then flatten_once on the FIGHTS
  sweep, median alone on the EXTENDS sweep. Staged qualification per
  doctrine, fresh interleaved none/armed cells at R=12, unrunnable
  counted as fail per the standing ruling with the count its own
  column. Three signed readings pre-registered: DOWN on FIGHTS ground,
  UP on EXTENDS ground, joint support only if both land, either
  opposite sign downgrades the moderator where it was adopted. The
  wildcard lesson is structurally excluded by the single-lesson store.
  The classification table is a protected surface once the first run
  starts. Kickoff held for Brad's ruling on the classification.

- 2026-07-04 | THE IDIOM CENSUS, conductor work from the PACKET-022
  artifacts, no new runs: every persisted output in the normalize and
  boundary stage B blocks classified by solution shape, classifier
  eyeball-verified on samples. llama on balanced, none cell: 8
  count-equality shortcut, 4 counter sweep, n=12, the seat sampling
  both shapes inside one cell. The shape determines the order check by
  construction, 36 of 36 rows consistent. armed-N2's distribution sat
  at 4 shortcut 8 sweep against none's 8 and 4: the depth_max lesson's
  up-at-the-bar direction in PACKET-022 coincides with an idiom shift,
  post-hoc and unregistered, filed as a LEAD, the mechanism candidate
  for that cell. llama on flatten_once, none cell: 6 loop-with-branch,
  2 comprehension, 2 other, 2 unrunnable, the comprehension pull weaker
  on the filter than the classification's analytic reading assumed.
  Consequence adopted design-level: the reached-for shape is a
  distribution per seat and task, not a value, and the moderator's
  phrase "the canonical solution shape" means the high-probability
  shape, whose concentration is measurable and now gets measured
  inside PACKET-023 rather than assumed.
- 2026-07-04 | CONDUCTOR SELF-CORRECTIONS on PACKET-023 as first cut,
  from Brad's teardown, corrected in the packet where made, before any
  run and before the table froze. One: the packet stated "which shape a
  seat reaches for is an empirical fact per seat" as if established;
  it was an assumption, now partly measured and finer than stated,
  distributional within a seat and task. Two: the FIGHTS sweep ranked
  merge_ranges, the conductor's own mildest call, first, with no stated
  reason; flipped to flatten_once first so a FLAT reads against the
  moderator instead of against the instrument. Three, adopted from the
  same exchange: conflict magnitude as a graded variable is logged as
  a future designed instrument, one rule at graded distances from one
  idiom, not part of 023, whose job is the sign. The census instrument
  is added to 023 as pre-registered descriptive data that interprets a
  FLAT and never flips a signed exit.

- 2026-07-04 | PACKET-023 kickoff on Brad's Go, table frozen as revised
  (flatten_once leads FIGHTS, median alone on EXTENDS, balanced
  excluded on measured grounds, census instrument in). From kickoff the
  classification table is a protected surface.
- 2026-07-04 | DESIGN LEAD FILED, Brad's, for the audience v3 work
  (board item 4): the shape census as a standing ear for the audience,
  evaluating not just the answer but the shape of the decision that
  produced it. The conductor's read of where it lands, filed with the
  lead: the census's power in PACKET-022 came from being deterministic
  code, not model judgment, so its home is the evidence and flag side
  of the house, the side the record trusts, not a new question posed to
  the audience LLM, the side that passed a run the evidence failed.
  Shape signals point toward fail or watch only, mirroring the standing
  rule that evidence outranks the audience toward fail only: a wrong
  shape that passes every check is a pass wearing a flag, never a fail.
  Costs named: taxonomies are hand-authored per task today, and
  generalizing them is either labor per task family or a new research
  seam, not free. Any judging role waits on a judgecal-style
  calibration committed with the change, per the protected protocol.
  Held out-of-band from PACKET-023, which uses the census as
  descriptive data only.

- 2026-07-04 | PACKET-023 executed (moderator23 20260704-071554, 36
  runs, GATE passed, detached, no kill, byte check asserted twice, tool
  audit clean, recensus replay 0 mismatches of 36). Both sweeps
  exhausted without a qualifier: flatten_once 11 passes 1 fail of 12
  (one fail short of mixed), merge_ranges 1 pass 11 fails of 12 (one
  pass short), median 24 of 24 (ceiling). Stage B never ran, no armed
  cell exists in the packet, the three pre-registered readings never
  fired, and the moderator stands exactly where it stood, adopted
  design-level and untested. The census is the yield, descriptive at
  n=12: qwen reaches loop-with-branch 10 of 12 on flatten_once (the
  conflicted comprehension the FIGHTS classification named is not this
  seat's pull, opposite llama's PACKET-022 record on the same task),
  reaches the sweep 12 of 12 on merge_ranges with the rule losing
  inside it 11 of 12, and holds ceiling on median. Two tier 2 flags
  filed: a per-seat concentration condition for the classification
  criterion, and moderator ground supply on qwen empty at this design,
  both the conductor's. 217 tests green.

- 2026-07-04 | Conductor review of PACKET-023: accepted against the
  record. Independent recount matched every count (36 rows, all stage
  A, tools 0 everywhere, flatten_once 11p 1f, merge_ranges 1p 11f,
  median 24p 0f), qualification arithmetic correct at the standing bar
  on all three grounds, byte check true by the conductor's own hash
  against production line 8, production store untouched at eleven, 217
  tests green rerun. The census verified two independent ways: the
  session's committed replay (36 rows, 0 mismatches) and the
  conductor's own classifiers written without reference to the
  session's, 0 mismatches on all 24 spot-checked merge_ranges and
  flatten_once rows. The three pre-registered readings correctly
  unfired: no ground qualified, stage B never ran, and the moderator
  stands adopted and untested with spec Section 12 unmoved. The packet
  paid for its census: qwen's pull on flatten_once measured opposite
  llama's on the same task, and merge_ranges measured as total pull
  with the rule losing inside the intact idiom in a none cell.
- 2026-07-04 | RULED on PACKET-023 FINDINGS 1, the criterion: the
  per-seat concentration condition is ADOPTED. The classification
  criterion is now two-part: the analytic rule-against-idiom reading
  proposes the conflicted shape, and a task classifies FIGHTS for a
  seat only when that seat's none-cell census concentrates on the
  conflicted shape. FIGHTS and EXTENDS are properties of a task and a
  seat together, never of a task alone; the moderator hypothesis is
  restated to match: tools nudge the amplifier toward its own
  high-probability shape. The PACKET-023 table stands frozen as
  pre-registration history and is not edited; future tables are
  per-seat and census-conditioned. Grounds: measured both ways on
  flatten_once (qwen loop-with-branch 10 of 12, llama the forced
  comprehension), and traceable to Brad's teardown question that
  produced the census instrument.
- 2026-07-04 | RULED on PACKET-023 FINDINGS 2, the supply: the verdict
  is accepted and the bar holds unchanged. Two packets in a row closed
  grounds on supply (three floors refused qualification on llama in
  P022, all three grounds refused on qwen in P023), so the binding
  constraint named at an earlier session close is now the measured
  blocker on the active thread. The next moderator ground comes from
  new calibrated candidates, not from lowering the bar.

- 2026-07-04 | PACKET-024 cut on Brad's Go: self-delivery, mistral
  receiving its own store at the same five apply floors P022 armed for
  llama. The cut order inverted from the conductor's prior
  recommendation after Brad's challenge, and the correction is filed
  where the frame was made: the conductor presented mistral's
  qualification failure as a known risk when no mistral cell exists on
  any of the five grounds and the one relevant prior (P019) qualified
  its first staged candidate. Under the per-seat criterion the mistral
  staging sweeps and census are required data, not downside, so every
  exit of this packet pays. Design: P022's template whole, mistral
  performing, llama audience per P019, all four lessons ride (the
  wildcard block is qwen-only), the census as standing instrument with
  moderator23 classifiers reused and two new taxonomies stated,
  self-delivery pre-registered as its own question, never pooled with
  the llama cells. The supply packet for the qwen moderator retest is
  next in design, conductor authoring the candidate task specs.

- 2026-07-04 | DESIGN PRINCIPLE ADOPTED, Brad's, filed for the spec
  when it stabilizes: THE AUDITION IS A SYSTEM COMPONENT, not test
  scaffolding. The measurement sequence improvised across P018, P019,
  P022, P023, and P024 (baseline floors, trait sign on qualified mixed
  ground, shape census, qualification sweeps, first delivery evidence,
  with the teaching and delivery gates between them) is the standing
  rite every new model runs before it may receive or teach in a chair,
  and it is what makes the core thesis operational: the chair's memory
  survives a model swap only if the incoming seat can be measured the
  same way the outgoing one was. Grounds it survives on: delivery to
  an unmeasured seat is unsafe by measurement (amplifier harm, P015),
  lesson eligibility is seat-conditional (the wildcard block), and the
  classification criterion is per-seat by ruling. Costs named: the
  rite today runs 150 to 250 runs per seat, and the minimal sufficient
  battery is unknown and stays unfrozen until the research says which
  measurements carry. Dependency named and adopted with it: a fixed
  audition task set dies by ceiling (qwen at or near ceiling on three
  of three P023 grounds), so the audition depends on the calibrated
  task supply pipeline permanently, which raises supply from current
  blocker to standing subsystem. Spec bump held per doctrine; this
  lands in v0.8 when the battery stabilizes.

- 2026-07-04 | PACKET-024 executed (selfdeliv24 20260704-090337, 60
  runs, GATE passed, detached, no kill, all four byte checks asserted
  twice, tool audit clean, recensus replay 0 mismatches of 60). Both
  sweeps exhausted on the third seat: merge_ranges 0/12 and
  snake_to_camel 0/12 rule floors, median 23/24 one fail short of
  mixed, flatten_once 1/12 one pass short with one unrunnable,
  balanced 24/24 ceiling. Stage B never ran, the four self-delivery
  readings never fired, self-delivery stays unmeasured with its
  materials byte-ready. The packet's two bought measurements landed:
  mistral's qualification floors on all five grounds, and the
  none-cell census that feeds the per-seat criterion, flatten_once
  pulling the conflicted comprehension 8 of 12 (like llama, opposite
  qwen), balanced fully concentrated on the sweep where llama splits,
  merge_ranges sweep-total with the rule losing inside it on a second
  seat, snake_to_camel failing 12 of 12 on the compatible idiom, the
  absent separable step not idiom conflict. The cross-seat exhibit
  stands: thirteen seat-ground qualification cells across P022 to
  P024, two qualifiers, both llama. Two tier 2 flags: per-seat
  criterion columns from measured distributions, and floor supply
  refusing every seat but llama, feeding the audition-battery
  dependency. 234 tests green.

- 2026-07-04 | Conductor review of PACKET-024: accepted against the
  record. Recount matched every count (60 rows, all stage A, tools 0,
  merge_ranges 0/12, median 23p 1f, flatten_once 1p 11f with one
  unrunnable, snake_to_camel 0/12, balanced 24/24), qualification
  arithmetic correct at the standing bar on all five grounds, all four
  byte checks true by the conductor's own hashes against production
  lines 8 through 11, census verified two independent ways (committed
  replay 0 mismatches of 60; conductor's own classifiers for the two
  new taxonomies, written without reference to the session's, 0
  mismatches), production store untouched at eleven, 234 tests green
  rerun. The four readings correctly unfired: no ground qualified,
  self-delivery stays unmeasured with its materials byte-ready.
- 2026-07-04 | RULED on PACKET-024 FINDINGS 1, in two parts. Part one,
  the concentration threshold the per-seat condition was missing: a
  seat's none-cell census counts as CONCENTRATED on a shape at 9 of 12
  or better, three quarters, provisional until data pressure says
  otherwise. Part two, the consequence, including a downgrade of the
  session's own read: at that threshold mistral's flatten_once census
  (conflicted comprehension 8 of 12) does NOT classify; the session's
  FINDINGS sentence "flatten_once reads FIGHTS for mistral" is
  downgraded here to a lean. The per-seat table as the measured data
  now supports it: merge_ranges FIGHTS for qwen and for mistral (sweep
  12 of 12 both, the rule losing inside it); median EXTENDS for qwen
  and mistral (sort-and-index 12 of 12 both, no headroom at ceiling);
  flatten_once unclassified for llama (split, 6 of 12), no-conflict for
  qwen (accommodating 10 of 12), lean-FIGHTS unclassified for mistral;
  snake_to_camel EXTENDS for mistral (split-and-join 12 of 12);
  balanced EXTENDS for mistral (sweep 12 of 12), AMBIGUOUS standing for
  llama (8 of 12 under threshold), unmeasured for qwen. llama's
  merge_ranges, median, and snake_to_camel censuses are retro-runnable
  from the P022 stage A outputs on disk and are queued as conductor
  work, not assumed.
- 2026-07-04 | RULED on PACKET-024 FINDINGS 2: accepted, the bar holds.
  Thirteen seat-ground qualification cells across three packets, two
  qualifiers, both llama's. The supply verdict is now confirmed three
  times and the calibrated-task supply packet is the next cut, the
  conductor authoring candidate specs for Brad's teardown first.

- 2026-07-04 | THE AUDITION FIREWALL, Brad's instruction, adopted as
  standing doctrine with its honest limit stated. Pure two-way
  isolation is impossible by the component's own purpose: the
  audition's outputs (floors, trait signs, censuses, delivery
  evidence) exist to feed casting and the delivery gates. So the
  doctrine is a one-way valve with four walls. One: during measurement
  the audition writes nothing to main-system state, no distillation,
  no chair memory, no store, pin, or gate changes; what every packet
  has carried as a constraint is now standing doctrine for all
  audition work. Two: the audition reads the chair's memory only
  through byte-verified packet-local copies, never live. Three:
  audition baselines run bare, no tools, no memory, nothing of the
  main system in the seat's context. Four, the Goodhart wall, the
  influence direction the instruction most protects: the main system
  never optimizes toward audition metrics. Audition battery tasks stay
  held out of the lesson-generation pool permanently (the existing
  gen-and-apply line is hereby doctrine, not accident), lessons never
  distill from audition runs, and no forecaster or casting objective
  ever trains against audition scores. The audition measures; it is
  never a target. A system that learns to pass its own audition has an
  audition that measures nothing. Crossings happen at conductor
  rulings only, never automatically. The named limit: the seats
  themselves are shared weights, so the isolation is of state and
  objectives, not of the model. Lands in v0.8 beside the audition
  principle.

- 2026-07-04 | SECOND OPINION EVALUATED. Brad consulted the retired
  original conductor thread, out-of-band and disk-blind, on the
  census-as-ears direction and the thesis question, and the sitting
  conductor verified its record-dependent claims against the disk
  before adopting anything, the same treatment a session's account
  gets. Verified true: the directive-collapse boundary (clean checks
  0.92 to 0.36 under the explicit directive while the menu lifted, on
  the record at the friction-theater ruling), and the armed-N2 numbers
  (census 4 to 8 sweep, pooled 16 to 20 of 24, verified this session
  against rows). Corrected against the record: catch-better was not
  parked; it was built 2026-07-01 and closed the loop live at least
  once, a watch item catching a same-class break through the audience.
  The accurate statement is that catch-better currently depends on the
  record's weakest measured link, the audience as criteria consumer,
  and a deterministic shape-flag channel into the flag tally would
  remove that dependency, which is the strategic substance of the
  second opinion's point and it survives the correction.
- 2026-07-04 | ADOPTED from the second opinion, with independent
  convergence noted: the census direction does not overrule Brad's
  original judge-restraint ruling, because every reason that killed
  judge expansion was a reason about LLM judgment and the census has
  none of those properties; the evidence-side homing, the
  fail-or-watch fence, and the Goodhart walls stand as filed. The
  sharpest point is adopted as the pre-registered reading frame for
  the replication: distribution steering with free choice per run (4
  of 12 becoming 8, not 0 becoming 12) is the landscape principle's
  mechanism made visible, not its refutation, and the
  directive-collapse result stays as the boundary where steering
  becomes forcing. On a replication PASS the canon edit is an
  addendum explaining the principle, never a reversal, pre-registered
  now so the edit's direction cannot be argued after the data.
- 2026-07-04 | THE TRIGGER, ruled: the shape-steering mechanism stays
  a lead until one pre-registered replication passes. PACKET-025 is
  the trigger when Brad calls it: llama performing, balanced ground,
  staged qualification per doctrine, fresh interleaved none and
  armed-N2 cells at R=12, primary reading on the census itself with
  its own signed bar, secondary on the pooled rule checks at the
  standing bar, and only a PASS edits canon.

- 2026-07-04 | PACKET-025 cut on Brad's Go, the trigger fired: the
  shape-steering replication, llama on balanced, staged qualification
  then fresh interleaved none and armed-N2 at R=12. Primary reading on
  the census with a 2-of-12 signed bar (PASS unlocks the
  pre-registered canon addendum, conductor only; CONTRA or FLAT
  downgrades the lead where it was filed and canon stays still),
  secondary on pooled rule at the standing 4-of-24 bar, the two
  readings independent by pre-registration since the origin cell was
  census-shift beside rule-FLAT. The balanced classifier rides
  identity-pinned from selfdeliv24. Supply packet design remains the
  next conductor authoring after this run.

- 2026-07-04 | PACKET-025 executed (shapesteer25 20260704-105603, 36
  runs, GATE passed, detached, no kill, byte check against production
  line 11 asserted twice, tool audit and interleave verified from the
  rows, recensus replay 0 mismatches of 36). Stage A qualified
  balanced at 18 passes 6 fails of 24. Both pre-registered readings
  FLAT: the census read armed-N2 5 sweeps of 12 against none 6, gap 1
  under the 2-of-12 bar, so the shape-steering mechanism did not
  replicate on its first pre-registered attempt and the lead goes down
  where it was filed, the conductor's filing; the pooled rule read 18
  of 24 against 18 of 24, gap 0, the lesson's second non-harmful
  delivery reading on this seat, residue watch quiet again. Canon and
  both specs untouched, per the packet regardless of exit. One tier 2
  flag: the none-cell census itself moved 2 of 12 between P022 and
  this packet with no tool present, the same size as the borrowed
  census bar, so census bars need their own measured drift record
  before the next census-primary packet. 248 tests green.

- 2026-07-04 | Conductor review of PACKET-025: accepted against the
  record, and THE DOWNGRADE EXECUTED. Recount matched every count
  (stage A 18 of 24, qualified mixed; stage B none 18 of 24 with 6
  sweeps of 12, armed-N2 18 of 24 with 5 sweeps), interleave exact,
  tools clean, byte check true by the conductor's own hash against
  production line 11, replay 0 mismatches of 36, 248 tests green
  rerun, close commit append-only on DECISIONS. Both readings FLAT by
  their pre-registered letters. The shape-steering mechanism lead,
  filed 2026-07-04 by this conductor from the P022 armed-N2 census, is
  downgraded where it was made: it did not replicate on its first
  pre-registered attempt, armed 5 sweeps against none 6 at the 2-of-12
  bar. Canon does not move, the pre-registered addendum frame stays
  filed and unfired, and revival requires a fresh pre-registered PASS.
  What the packet leaves standing: the depth_max lesson's second
  non-harmful delivery reading on llama, residue watch quiet again.
- 2026-07-04 | RULED on PACKET-025's tier 2 flag: adopted. The
  none-cell census on balanced moved from 4 sweeps (P022) to 6 (P025)
  with no tool present, movement 2 of 12, at the census bar. Census
  shares drift like rule counts, so from here the standing census
  report includes the ground's census priors from earlier packets,
  named as priors and never pooled, and census readings get the same
  same-run-only discipline rule readings have always had. The P022
  origin lead was cross-packet in exactly the way this rule forbids
  going forward, one more reason its downgrade is the right exit.

- 2026-07-04 | PUBLICATION-READINESS AUDIT, filed and executed in the
  same turn, the bar being two-plus tasks per class and two-plus
  family pairs, each finding sized from the record. Delivery form:
  menu-changes-output is broadly replicated (P004 seven checks, then
  delivery cells across P9, P15, P21, two seats, two-plus task
  classes) and MEETS the bar; the directive-collapse half (0.92 to
  0.36) is one task, one packet, GAP G1: a second-task decision-cell
  replication. Seat response: qwen amplifier measured in both
  directions across two-plus tasks, MEETS; llama filter-or-better on
  narrower ground; mistral indifferent at ONE cell, GAP G2: a second
  trait cell, blocked on qualified mistral ground. Transfer: qwen and
  llama exchange is measured both directions with the asymmetry
  replicated (lift on range_summary both ways per P015 and P021,
  harm on the tie reverse), but that is ONE family pair, and
  mistral-origin to llama read four FLATs, GAP G3: a second family
  pair with a replicated non-FLAT transfer reading. Parity: replicated
  (P015, P021) on ONE task, one seat, GAP G4: parity on a second task.
  The convergence that matters: G2 and G3 both sit behind ground
  supply, the constraint now confirmed three times, so the supply
  packet is on the flag's critical path, not just the moderator's and
  the audition's.

- 2026-07-04 | SUPPLY FAMILIES v0 AUTHORED for Brad's teardown, at
  bench/design/SUPPLY_FAMILIES_v0.md, not a packet and not canon. The
  design adopts Brad's universality suggestion in its corrected form,
  pushed back and reframed in-thread: a fixed test at a fixed
  difficulty is what refused three packets, so the universal thing is
  the instrument, not the difficulty point. Graded task families with
  a dial, one calibration procedure for any seat present or future,
  per-seat kept pools found by sweeping, the eye-chart principle
  replacing the IQ-test framing (the battery locates thresholds and
  response shapes, never a general-smartness rank, which is the axis
  the project refuses to compete on). Six families authored seat-blind
  across boundary/degenerate, normalize/delimiters, and
  tie_break/direction, each with pins, named canonical-shape
  relationship, census taxonomy, dial, and check pattern. The
  conflict-magnitude instrument logged earlier today is folded in as
  merge_within's dial. Family 6 stocks gap G1's ground. Calibration
  priority when cut: mistral, qwen, llama, per the audit's gaps. The
  audition firewall applies from birth: these families never enter
  the lesson-generation pool.

- 2026-07-04 | PACKET-026 cut on Brad's Go: supply calibration, the
  eye chart's first hang. The session builds the six design-document
  families into bench/supply_families.py (a new module, standing
  pools untouched, admission of kept ground stays the conductor's
  ruling), then runs the universal sweep on all three seats in gap
  order, mistral, qwen, llama, bare none cells only, tools zero
  everywhere, census on, family stops per seat at first mixed rung.
  Pre-registered as structural only: no treatment, delivery,
  moderator, or trait claim can come from this packet under any
  outcome. Moderator-ready ground gets designated in one sentence
  where a kept rung's census also concentrates at the 9-of-12
  threshold, a designation, never a claim. The design document is a
  protected surface for the session: implement, never edit, flag
  disagreements. Wall-time cuts fall on whole-seat boundaries.

- 2026-07-04 | PACKET-026 executed (calibrate26 20260704-121911, 432
  runs over 36 cells, GATE passed, detached, no kill, tool audit
  tools=0 every row, recensus replay 0 mismatches of 432, pooled
  arithmetic and kept pools recounted independently and matching).
  The eye chart hung and worked: thirteen kept (family, rung) pairs
  and no seat with an empty pool. Mistral keeps four including both
  control rungs, each reported as an unexpected control
  qualification; qwen keeps four, its first qualified mixed ground
  since the moderator test refused all three candidates, spanning
  three classes; llama keeps five. Eight moderator-ready designations
  at 9-of-12 census concentration, and every seat now holds
  concentrated conflicted AND separable kept ground, the pairing the
  moderator retest needs. One shape-against-readings divergence named
  and diagnosed: a llama output that parsed but died on its own
  appended demo call, zero readings, fails under canon. Three tier 2
  flags: control rungs anchor only per-seat, a family whose
  unrunnable count crosses half the cell measures formatting before
  rule (mistral token_case, 12 of 12 parse failures at rung 3), and
  the named canonical shape is rung-sensitive on safe_stats so the
  criterion table should read concentration per rung. The kept pools
  enter no standing pool; admission is the conductor's ruling. The
  generalized qualification fraction (2n of 12n pooled) is logged in
  RESULTS. 273 tests green.

- 2026-07-04 | Conductor review of PACKET-026: accepted against the
  record. Independent recount reproduced the full sweep from the rows:
  36 cells at 12 reps, 432 rows all bare none cells at tools zero, the
  generalized fraction applied by the conductor's own logic and all
  thirteen kept pairs with their exact qualification counts matching
  the harness. Census verified two ways: the committed replay, 0
  mismatches of 432, and the conductor's own classifiers on 48
  spot-checked rows across two families, 0 mismatches. The one
  divergence row stands correctly named: parsed code that died on its
  own appended demo call, execution-level zero-readings, not
  parse-level unrunnable. Rule-fidelity audit of all eighteen task
  texts against the design document: faithful, and every smallest
  choice legitimately underdetermined by the document. 273 tests green
  rerun. The supply starvation named three times today is over.
- 2026-07-04 | RULED on PACKET-026 FINDINGS 1: controls are dual-role.
  A control rung is an anchor where it holds and a depth sounding
  where it qualifies; a qualifying control is supply, not noise.
  Mistral's two control pairs stay kept by the procedure's letter,
  each annotated edge-of-band (merge_within r1 ceiling-leaning at 10
  of 12, kth_ordered r1 floor-leaning at 2 of 12).
- 2026-07-04 | RULED on PACKET-026 FINDINGS 2, form-limited ground: a
  cell whose unrunnable rows exceed half of it measured output form
  before the stated rule. Its floor character carries the
  form-limited annotation wherever cited, and form-limited ground is
  ineligible as delivery or moderator ground, since a rule lesson
  delivered onto it would measure formatting. Mistral's token_case
  column is the first annotated case.
- 2026-07-04 | RULED on PACKET-026 FINDINGS 3: shape concentration
  reads per seat, family, AND rung, never per family. The per-seat
  criterion table adopts rung as part of the key; the safe_stats
  drain (qwen 7 to 1 to 0 across rungs) is the measured reason.

- 2026-07-04 | ADMISSION RULED: the thirteen kept pairs enter the
  standing qualified-ground registry, per-seat, as CANDIDACY and
  nothing more. Registry entry means a pair is the first ground a
  future packet sweeps for that seat and class; it never means
  pre-qualification, because baselines drift (measured, P025), so
  every treatment packet still qualifies its ground fresh inside the
  packet per the same-run doctrine. Annotations carried into the
  registry: mistral's two control-origin pairs edge-of-band; qwen's
  kth_ordered r1 ceiling at 11 of 12 is noted as gap G1's candidate
  ground, a tie task the seat aces, which is what the
  directive-collapse replication needs; kth_ordered's
  reverse_alphabetical enters the stated_direction pin vocabulary as
  a new value, accepted. The eight moderator-ready designations ride
  with the registry as designations, re-checked per rung inside any
  packet that uses them.

- 2026-07-04 | PACKET-027 cut on Brad's Go: the moderator retest on
  registry ground. Two cells on qwen, per-cell signed predictions: B1
  on chunk_pad rung 3, conflicted, predicted DOWN; N1 on token_case
  rung 1, separable, predicted UP; N1 chosen over N2 to keep the
  residue flag out of the attribution. Stage A carries TWO fresh
  gates per ground, qualification and 9-of-12 concentration on the
  named shape, the concentration gate operationalizing the per-seat
  criterion for the first time; a cell whose census drifted off its
  designation is VOID, not read. The two-lesson attribution caveat is
  pre-registered on every exit. Both cells are mistral-to-qwen, a new
  transfer edge, so any non-FLAT armed reading is also the first
  measurement toward audit gap G3. Joint support only if both land;
  either opposite sign downgrades the moderator where adopted. G1's
  directive cell and G2's mistral trait cell queue behind this.

- 2026-07-04 | PACKET-027 executed (modretest27 20260704-163905, 72
  runs, GATE passed, detached, no kill, both byte checks asserted
  twice with line positions, tool audit and both interleaves verified
  from the rows, recensus replay 0 mismatches of 72). Both grounds
  survived the double gate fresh: chunk_pad r3 qualified 18/24 and
  concentrated 11/12, token_case r1 qualified 4/12 and concentrated
  12/12, with the registry candidacy numbers moving under fresh
  measurement exactly as the candidacy doctrine expects. Both signed
  cells returned FLAT: the FIGHTS cell down exactly the bar against a
  ceiling baseline (24/24 to 20/24, bar 4), the EXTENDS cell up 1
  under its bar (5/12 to 6/12, bar 2). Joint reading: no support, no
  downgrade, not partial direction, the moderator stands
  adopted-untested with both sub-bar movements pointing the predicted
  way as description only. Transfer note: nothing fires, the
  mistral-to-qwen edge is exposed and unharmed across 24 armed rows
  and stays unmeasured. The collateral-safety series extends to five.
  One above-bar watch movement upward reported no-name. One
  appended-demo crash row named, the second in two packets. Two tier
  2 flags: a baseline observability note for signed cells whose fresh
  none lands at ceiling or floor, and the evidence-layer question on
  stripping module-level statements. 286 tests green.

- 2026-07-04 | Conductor review of PACKET-027: accepted against the
  record. Independent recount matched every count in all six cells,
  both stage A gate arithmetics confirmed (fights 18/24 qualified with
  11/12 concentration, extends 4/12 qualified with 12/12
  concentration), stage B pooled 24/24 against 20/24 and 5/12 against
  6/12, censuses exact, interleaves exact, tools clean, both byte
  checks true by the conductor's own hashes against lines 8 and 10,
  production store untouched at eleven, replay 0 mismatches of 72,
  286 tests green rerun. Both FLAT exits verified verbatim. The
  moderator's status line, ruled: no longer untested; it is MEASURED
  ONCE on double-gated designated ground and read inside drift on
  both sides, no support, no downgrade, with the sub-bar directions
  noted as description only. The registry annotations updated: qwen
  chunk_pad r3 re-proved once with candidacy drift 20/24 to 18/24;
  qwen token_case r1 re-proved once, 7/12 to 4/12; both in-gate.
- 2026-07-04 | RULED on PACKET-027 FINDINGS 1, observability doctrine,
  ADOPTED: for any pre-registered signed cell, the writeup names which
  sign directions remained observable against the fresh same-run
  baseline, and a cell whose predicted sign was unobservable (an UP
  prediction on a ceiling baseline, a DOWN on a floor) claims NOTHING
  rather than FLAT, because its flatness would be the baseline's
  artifact, not the treatment's. Applied retroactively as a check:
  P027's FIGHTS cell predicted DOWN against a ceiling, fully
  observable, the reading stands; no prior signed cell in the record
  hit an unobservable configuration.
- 2026-07-04 | RULED on PACKET-027 FINDINGS 2, the appended-demo
  crash: NO CHANGE to the evidence layer now. The layer underlies
  every measurement in the record, and the species runs at two rows
  in roughly six hundred today, under half a percent; the divergence
  column already names each occurrence, and canonical accounting
  already prices it honestly as all-fail. Stripping module-level
  statements would change what is measured (rescuing outputs that
  ship their own crash) and any such change requires its own
  calibration packet. Threshold set: if the species reaches 3 rows in
  any single cell of 12, the conductor revisits with a designed
  calibration packet before any further reading on that ground.

- 2026-07-04 | CONDUCTOR SELF-CORRECTION, filed where the claim was
  made: the PACKET-026 admission ruling annotated qwen kth_ordered
  RUNG 1 as gap G1's candidate ground. Wrong on the design document's
  own dial: rung 1 is the tie-free control rung, and a tie-direction
  directive cannot inject error where no tie exists. G1's ground is
  kth_ordered RUNG 2, kept at 10 of 12 with ties at the k-th
  position. The registry annotation is corrected by this entry.
- 2026-07-04 | PACKET-028 cut on Brad's Go: the directive replication,
  gap G1. Qwen on kth_ordered rung 2, three forms of one content:
  none, menu, and the same lesson's rule sentence as a P004-mechanism
  directive, byte-printed, interleaved triplets at R=12. Two build
  gates precede any run: the contradiction gate (the directive's
  positional-last direction must flip at least one rule check's
  answer against the stated reverse-alphabetical rule, derivations
  printed, line 4 then line 5, both failing stops the packet uncut)
  and the high-baseline gate at 9 of 12, the first packet gated by
  the observability doctrine instead of mixed qualification, because
  a collapse cell's only signed prediction is DOWN. Readings: the
  collapse replicates or stays loudly one task old; menu harm would
  be the first break in the menu-never-hurt record, said loudly with
  the two-cause caveat; joint second-task support only on collapse
  beside no-menu-harm. P004 priors named as ev-fraction era,
  direction comparable, magnitudes not.

- 2026-07-04 | PACKET-028 closed uncut at the contradiction gate, the
  exit the packet pre-registered. The gate ran as committed
  deterministic code before anything else and failed both candidates:
  kth_ordered rung 2 carries one rule check, and on its input the
  stated reverse-alphabetical rule and the positional-last directive
  direction give the same answer, because the tie pair is listed in
  ascending alphabetical order and later-encountered coincides with
  reverse-alphabetically-first. Both tie lessons carry the same last
  direction, so lines 4 and 5 fail alike, with both derivations
  printed per the gate and pinned by tests that also prove the gate
  passes on separating input. No model was called, no store created,
  no reading fired: the collapse finding stays one task old, sized
  so, and the menu-safety property is untouched. The flag carries the
  re-cut leads: rung 3 separates the directions on both scored k
  values but has no qwen baseline, and a rung 2 input variant would
  separate but is a supply_families change with recalibration
  consequences. The G1 registry annotation, corrected once from rung
  1 to rung 2, needs the conductor's second look. 295 tests green.

- 2026-07-04 | Conductor review of PACKET-028: accepted against the
  record. Closed uncut at the contradiction gate, the exit its own
  pre-registration named, zero model runs. The gate's derivation
  reproduced by the conductor's own independent code: on rung 2's
  sole rule check the stated rule and the directive direction
  coincide at 'bb' because the tie pair sits in ascending
  alphabetical order, a property of the input. The session's rung 3
  separation claim also verified independently: rule order
  ['c','ba','ab','aa'] against directive order ['c','aa','ba','ab'],
  differing at k=2 and k=3. Production store at eleven, 295 tests
  green rerun, tree clean. No reading fired; the collapse finding
  stays one task old, sized exactly so.
- 2026-07-04 | CONDUCTOR SELF-NOTE, the conceptual error behind two
  corrections in one day: the G1 ground annotation was wrong at rung
  1 (tie-free) and wrong again at rung 2 (non-separating input), and
  both facts were derivable from committed check inputs at annotation
  time. The gate was right to exist and cost zero model runs, but a
  desk derivation at cut time would have cost zero sessions. RULE
  ADOPTED: a ground annotation for a signed design derives its
  enabling property (here, ties present AND direction separation on
  scored inputs) from the check inputs at annotation time, printed in
  the annotation. The G1 annotation is corrected a second time:
  kth_ordered rung 3, separation proven twice (committed test and
  conductor derivation), annotated NO QWEN BASELINE, high-baseline
  risk absorbed by the stage A gate at 12 runs.
- 2026-07-04 | RE-CUT RULED: PACKET-029, the directive replication on
  rung 3. Same design as 028 with the ground moved: contradiction
  gate re-run as standing discipline even though separation is
  proven, high-baseline gate at 9 of 12 fresh, and if that gate
  fails, G1's next path (a rung 2 input variant, a supply_families
  change with recalibration costs) is a design decision taken with
  Brad, never an automatic pivot inside a packet.

- 2026-07-04 | PACKET-029 cut, the G1 re-cut per the ruling above:
  the directive replication moved to kth_ordered rung 3, where the
  separation is proven twice before the cut. Deltas from 028, all
  scale and risk: two rule checks so the gate is 18 of 24 and the bar
  4 of 24, the stage A gate carries the no-candidacy risk
  deliberately at 12 runs, and a gate failure ends G1's cheap path,
  with the input-variant alternative a Brad-level design decision.
  Everything else rides unchanged: the contradiction gate re-runs as
  standing discipline, three forms of one byte-printed content,
  interleaved triplets, the menu-safety reading pre-registered loud.

- 2026-07-04 | PACKET-029 closed uncut at the delivery-path check, a
  tier 2 stop one gate past where PACKET-028 stopped. The
  contradiction gate PASSED this time, rung 3 separating the stated
  reverse-alphabetical rule from the positional-last directive on
  both scored inputs with both derivations printed, the line 4 lesson
  selected and its store byte-checked at its position. Then the stage
  B precondition failed structurally: the production menu serves zero
  tools for a stated_direction last lesson on reverse_alphabetical
  ground, the PACKET-005 and 008 contradiction logic refusing the
  ride, with a committed matched-ground control proving the refusal
  is the pin firewall and not a loading defect. The packet menu audit
  of tools=1 every row is unreachable without a pin or menu change,
  both forbidden by the packet own constraints, so the discovery is
  flagged and nothing is touched: no model called, no stage A
  baseline bought, no reading fired, the collapse finding stays one
  task old and menu safety stays at five clean measurements plus the
  new structural fact that pinned contradicting content never reaches
  the menu surface at all. The flag carries the re-scope leads: a
  two-cell none-against-directive design with the firewall refusal
  standing as the safety exhibit, or matched-direction menu content
  with the contradiction confined to the directive text, each a
  design decision with Brad. 303 tests green.

- 2026-07-04 | Conductor review of PACKET-029 (incoming conductor,
  first act after handover): accepted against the record with two
  discrepancies named. First, the handover and CONTINUATION said the
  packet was RUNNING detached; disk says no run ever launched, no
  directive29 artifact exists in runs/, and no live process from the
  evening. Second, the session's RESULTS claimed one commit carries
  the packet; no such commit existed, the tree held all four packet
  files uncommitted, and the correction is appended in the packet
  file where the claim was made. The work itself verified clean: the
  build stage replayed by the conductor reproduced RESULTS verbatim
  (contradiction gate PASSES on both scored k values, matching the
  P028 review's independent derivation exactly), the byte check
  confirmed by the conductor's own md5 against production line 4,
  the delivery-path check read in source and confirmed to call the
  production menu.query with pins live beside a matched-direction
  control, production store at eleven, 303 tests green rerun. The
  conductor committed the packet after verification, staged per
  path. No reading fired, no model was called, the collapse finding
  stays one task old, and the menu-safety series stays at five with
  the new structural fact beside it: on pinned contradicting content
  the menu refuses before behavior can be measured.

- 2026-07-04 | RULE ADOPTED, the cut-time desk check extended: the
  same conceptual error stopped three packets in one day (G1 at rung
  1, rung 2, and now the rung 3 delivery path), and every stop was
  derivable from committed code at cut time. The
  annotation-derivation rule extends to the full deterministic
  surface: before hand-off, the conductor runs every gate in the
  packet that is deterministic and model-free, delivery-path checks
  included, and the packet is only cut if they pass. A session's
  build-stage-first discipline stays as the second net. Cost of the
  miss both times was one session, never a model run; the extension
  prices that to zero.

- 2026-07-04 | STATUS on gap G1 after PACKET-029: the cheap path is
  exhausted structurally, not by data. The three-cell design (none,
  menu, directive) cannot exist on any pinned contradicting-direction
  content because the pin firewall removes the menu exposure. The
  re-scope options are on the record in the packet's FINDINGS; the
  decision is Brad's, per the packet's own pre-registration, and the
  conductor's teardown of both options goes to him this turn. No
  registry annotation moves until the design is chosen.

- 2026-07-04 | CONDUCTOR SELF-CORRECTION, filed where the claims were
  made: both discrepancies in the review entry above were premature.
  The session's commit exists as 006ff7a and landed between the
  conductor's first read of the tree and the conductor's write, so
  "no such commit existed" was a race read as a false claim. The
  handover's "RUNNING detached" also narrows: the session was alive
  and working at handover time, and the thing that never existed was
  a model run, which the packet's own gates explain honestly. What
  survives of the review, unchanged: every technical claim verified
  independently, the replay verbatim, the byte check by the
  conductor's own hash, the production menu confirmed in source, 303
  green rerun, and the packet stands accepted. The conductor's commit
  message on 1480683 carries the superseded account; history is not
  edited, this entry corrects it. RULE ADOPTED from the race, the
  wakeup rule applied to the conductor: re-read git log and git
  status immediately before every write to the shared tree, never
  only at turn start, because a session may close its packet while
  the conductor verifies. The cut-time desk check ruling above stands
  on its own merits, unaffected.

- 2026-07-04 | PACKET-030 cut on Brad's Go, the G1 re-cut as
  symmetric forms, replacing option A after Brad's forcing question
  exposed the conflation: three properties wore the name menu
  safety, the production path's refusal (structural, proven in
  P029), the model's ignore response to menu-form contradiction
  (behavioral, one task old from the P004 era), and collateral
  cleanliness (the five cleans). G1's menu cell was always about the
  second, and the inherited constraint that the menu cell ride the
  production serving path is what made that evidence unreachable.
  The re-cut drops the constraint: three cells of one byte-checked
  content on qwen kth_ordered rung 3, none, menu-form injection,
  directive injection, form the only variable across identical
  bytes. The injection is the production emission itself,
  menu.query([lesson], matched_features), rendered by runner's
  standing path, so exposure identity is by construction and
  asserted by a new byte-form verifier. This also removes the
  serving-versus-form confound the original P028 design carried, its
  menu cell served and its directive cell injected. Claim sizing
  pre-registered: the menu-form cell measures the model, never the
  production path, and it prices the firewall's known limit, content
  whose contradiction the pin vocabulary cannot express. Desk check
  run at cut time per the new rule, all three deterministic gates
  passing, output printed in the packet. Stage A carries the
  no-candidacy risk at 12 runs as in P029; a gate failure returns
  the path to Brad, never a pivot. Cost 48 runs against option A's
  36, bought deliberately: a break in the menu-form cell would be a
  loud finding, form safety task-dependent and the firewall
  load-bearing, so both outcomes of the added cell inform.

- 2026-07-04 | PACKET-030 executed and closed at the stage A gate
  (directive30 20260704-185817, 12 runs, detached, no kill, harness
  gate PASSED, recensus replay 0 mismatches of 12). All three build
  gates re-ran as committed code and matched the desk check line for
  line: contradiction gate separating on both rung 3 inputs, byte
  check true at line 4, the byte-form verifier binding the menu-form
  landscape to the production emission with the firewall control at
  zero. Stage A read qwen kth_ordered rung 3 fresh at 14 of 24
  canonical against the 18-of-24 high-baseline gate: FAILS, the
  pre-registered answer, no stage B, no reading fires, the directive
  text never rode. The collapse finding stays one task old, the
  menu-form property stays unmeasured on a second task, and the
  re-cut is a Brad-level design decision. The runs bought two supply
  facts: rung 3 is mixed at the standing fraction for qwen (14
  passes, 10 fails) while refusing near-ace ground, and its census
  splits 9 compound-key to 3 single-key where rungs 1 and 2 read 12
  and 10 of 12 compound. Registry annotations are the conductor's.
  314 tests green.

- 2026-07-04 | Conductor review of PACKET-030: accepted against the
  record. Both session commits verified on the log (dce9bd5 build,
  2f62b15 close), tree clean. All 12 rows recounted by the
  conductor's own eyes: scored ties pass on reps 0, 1, 4, 6, 8, 10,
  11, giving pooled 14 of 24 exactly, gate at 18 of 24 FAILS, tools
  and directives zero on every row, no_readings false everywhere so
  zero unrunnable, all rows stage A none. Conductor recensus with the
  committed classifier on all 12 persisted outputs: 0 mismatches.
  Byte checks re-run by the conductor's own script: store identical
  to production line 4, byte-form verifier emitting one tool equal to
  the lesson's fields, firewall control at zero. 314 tests green
  rerun. The close is the pre-registered exit at its priced cost: no
  stage B, no reading fired, no claim in any direction, the collapse
  finding stays one task old and the menu-form property stays
  unmeasured on a second task. One description added beside the
  session's, description only at n=12: the three single-key-sort rows
  all failed both scored ties while compound rows split 7 to 2, a
  shape-and-rule correlation on this ground, unclaimed.

- 2026-07-04 | REGISTRY RULED on the P030 supply facts: qwen
  kth_ordered rung 3 enters the registry as CANDIDACY, source P030
  stage A at n=12, qualified mixed at the standing fraction (14 and
  10 of 24, both past 4), annotated NOT NEAR-ACE (14 of 24 against
  the 18-of-24 collapse demand, measured, the reason this packet
  closed) and delivery-caliber for ordinary signed cells only. Census
  annotation: 9 of 12 compound-key-sort, sitting exactly at the
  provisional concentration threshold, annotated edge-of-band, no
  moderator-ready designation granted at the boundary. Fresh
  qualification inside any packet that uses it, per the candidacy
  doctrine, unchanged.

- 2026-07-04 | PROVENANCE ADDENDUM on the 14 of 24, filed where the
  number was reported, prompted by an off-disk review flag: the 14 of
  24 is a single detached run (directive30-20260704-185817), 12 model
  runs with 2 scored rule checks each, no cross-run pooling anywhere,
  P029 contributed nothing because P029 called no model. Sizing note
  added: the two scored checks never disagreed inside any row (7 reps
  passed both, 5 failed both), so the independent unit on this ground
  is the run and the effective n is 12, not 24. Pooled counts stay
  the reporting convention; the claim sizes to runs.

- 2026-07-04 | STANDING DOCTRINE, the three-property decomposition,
  promoted from packet prose so no future conductor re-inherits the
  conflation: what the record has called menu safety is three
  properties, and every claim names which one it stands on. Property
  1, path refusal: the production serving path refuses pinned
  contradicting content, structural, proven from committed code
  (P029). Property 2, form response: the model ignores contradicting
  content presented in menu form, behavioral, one task, one seat,
  P004 era, replication attempted and blocked on ground supply.
  Property 3, collateral cleanliness: delivered menus move nothing
  unrelated, five consecutive clean measurements on non-contradicting
  content. None substitutes for another; property 2 prices the known
  hole in property 1, contradictions the pin vocabulary cannot
  express.

- 2026-07-04 | STANDING DOCTRINE, the G1 dead-end map, and the
  PRE-REGISTERED PROGRAM EXIT, adopted on Brad's direction: the
  collapse replication needs ties present, direction separation on
  scored inputs, and a near-ace fresh baseline, and the record proves
  no existing rung has all three (rung 1 tie-free, rung 2
  non-separating input, rung 3 measured 14 of 24). Every wall was
  desk-derivable. The rung 2 input variant is the LAST G1 attempt
  before the writeup proceeds. If it walls too, the flag publishes
  anyway with property 2 stated at its true size, and the dead-end
  map publishes beside it as the supply finding it is. The flag does
  not slide behind a ground hunt past this exit.

- 2026-07-04 | G1 VARIANT RULED IN PRINCIPLE (Brad), desk proof done:
  the rung 2 input variant path is approved as G1's last attempt,
  conditioned on the design-document diff returning to Brad before
  any canonical change lands. The desk derivation ran at ruling time
  with the committed P028 instrument: rung 2's current check
  kth_ordered(['aa', 'bb', 'c'], 2) does not separate (both
  directions give 'bb', the tie pair ascending), and the minimal
  variant kth_ordered(['bb', 'ab', 'c'], 2), tie pair descending,
  separates (rule 'bb', directive 'ab'), printed per the
  annotation-derivation rule. The supply_families change, its tests,
  the P026 old-input historical annotation, and the packet cut all
  wait on Brad's sign-off of the design-document diff.

- 2026-07-04 | G2 DESK CHECK FOUND THE WALL BEFORE THE CUT, the
  fourth desk save today: Brad's Go was for the boarded design,
  P019's template (a cross-origin matched pinned lesson) on mistral's
  registry ground, and the delivery-path desk check proves that
  design cannot exist with current supply. All eight pinned
  production lessons carry origin_seat mistral:7b, so every pinned
  instrument the menu would serve on mistral's kept ground
  (safe_stats r1 and chunk_pad r1 serve lines 8 and 9, boundary
  class) is self-delivery, the exact question P024 left unmeasured.
  The one cross-origin pinned lesson in existence, P014
  llama-origin distinctness, contradicts every mistral kept ground's
  rule_class and the menu refuses it. Lines 1 through 3 serve by
  wildcard absence, not by pins, and are not matched instruments.
  The re-scope is Brad's, options filed in the conductor's report
  this turn; no packet is cut on a changed design without him.

- 2026-07-04 | PACKET-031 cut on Brad's Go, G2 re-scoped as Option A:
  mistral self-delivery on registry ground, one cell answering two
  pre-registered questions, P024's unmeasured self-delivery and the
  second cell in mistral's trait series. Ground safe_stats rung 1,
  the seat's strongest candidacy (14 of 24, census separable),
  qualified fresh inside the packet. Instrument production line 8,
  mistral-origin boundary lesson, genuine pin match to the family's
  own pins, served through the production menu path (not injection;
  the firewall has nothing to refuse), fresh raw byte copy cut by the
  packet. The two-cause caveat is pre-registered on every non-FLAT
  exit: seat trait and self-origin effects, neither chosen at this
  n; that caveat is the priced cost of one packet carrying two
  questions, taken knowingly. P019's template rides otherwise, plus
  the standing additions: observability naming, effective-n
  reporting on within-row check correlation, census on. Desk check
  run at cut time, all four deterministic gates passing, output
  printed in the packet, including one materials fact found at the
  desk: P024's four byte-ready stores are JSON-equal to production
  but byte-different by serialization only, so they are noted and
  not reused, and the byte-check discipline cuts fresh from the
  production line.

- 2026-07-04 | PACKET-031 executed (selfdel31 20260704-204738, 36
  runs, GATE passed, detached, no kill, all build gates re-run as
  committed code with the store md5 tied to the desk check, audits
  and interleave recounted clean, recensus replay 0 mismatches of
  36). Stage A qualified fresh at 19 passes 5 fails of 24, the
  candidacy number moving upward under fresh measurement this time.
  Stage B: armed 20 of 24 against none 15 of 24, gap 5 past the
  4-of-24 bar. THE READING IS GAIN with the two-cause caveat in its
  first sentence: the seat's tool-response trait and self-origin
  effects both live, neither chosen at this n. The first
  self-delivery evidence on the record points receptive, one task,
  one seat, n=12 per cell, direction never a rate, both exits
  observable against a 15-of-24 baseline, effective-n reported with
  the rule checks disagreeing inside 7 and 4 of 12 rows so the
  pooled accounting stands. The trait series holds P019's FLAT and
  this GAIN with attribution deliberately open; the movement
  concentrated on the trim check the concept does not address, the
  watch column rose above per-check size and is reported nameless,
  no column declined anywhere. Separating trait from self-origin
  needs a cross-origin cell on this seat and ground, the conductor's
  cut. 326 tests green.

- 2026-07-04 | Conductor review of PACKET-031: accepted against the
  record. Both commits verified (8bbb80d build, d62691f close), tree
  clean. All 36 rows recounted by the conductor's own code: stage A
  19 and 5 of 24 with zero unrunnable, QUALIFIES; stage B none 15 of
  24 with one no-readings row, armed 20 of 24 clean; gap 5 past the
  4-of-24 bar, GAIN verbatim with its two-cause first sentence
  intact. Interleave exact from the persisted row order, audits
  clean on every row, per-check table reproduced (empty 11 to 12,
  trim 4 to 8, watch 4 to 7), within-row disagreement reproduced
  (none 7 of 12, armed 4 of 12, so pooled sizing stands). Conductor
  recensus with the committed classifier on all 36 persisted
  outputs: 0 mismatches. Byte check by the conductor's own hash:
  store minus final newline identical to production line 8, md5
  matching the desk value. 326 tests green rerun. One conductor
  misfire filed where it happened: the first byte instrument
  stripped line endings asymmetrically (lessons.jsonl is CRLF) and
  false-alarmed; diagnosed from the bytes and corrected at the desk
  before any claim fired. The store was never wrong.

- 2026-07-04 | REGISTRY annotation updated: mistral safe_stats r1
  candidacy moved 14 of 24 (P026) to 19 of 24 fresh (P031 stage A),
  in-gate, the second candidacy drift on record and the first
  upward; the same-run stage B none at 15 of 24 rides as drift
  context. Candidacy doctrine unchanged: fresh qualification inside
  every packet.

- 2026-07-04 | RULED on the P031 GAIN, the standing doctrine
  applied: one cell is direction, never a rate, and no signal is
  believed before it replicates. NO casting entry, NO trait-series
  upgrade, NO teaching-gate consequence from this cell alone. The
  two pre-registered causes stay open. Conductor description added
  beside the reading, claiming nothing: the movement concentrated on
  checks the lesson's concept does not address while the addressed
  check sat near ceiling, a pattern consistent with a
  content-nonspecific delivery response inside the trait cause. The
  separation ladder, in order: replicate the GAIN first (doctrine),
  then a contrast cell with a content-irrelevant wildcard lesson
  (production lines 2 or 3 serve on this ground by wildcard,
  desk-checkable) to split content-specific from nonspecific, and a
  cross-origin cell for the self-origin split, blocked on supply
  until a non-mistral boundary lesson exists. Watch tally,
  descriptive: above-bar watch sightings now number three across the
  record (P017, P027, P031), all nameless, grounding no claim.

- 2026-07-04 | PACKET-032 cut on Brad's Go: the self-delivery
  replication, standing doctrine running as a packet. P031's design
  executed again on fresh cells, same ground, same byte-checked
  instrument through the production path, the selfdel31 harness
  reused by identity, the two-cause caveat unchanged. New
  pre-registrations, all replication-specific: the two packets'
  cells are never pooled (cross-run pooling distrusted per the
  provenance addendum), the reading is qualitative exit against
  exit, a FLAT or HARM downgrades P031's GAIN in the record where it
  was made, and VOID-BY-CEILING closes the packet with no reading if
  the fresh baseline lands at 20 of 24 or above, since the predicted
  GAIN direction would be unobservable at less than bar-plus-one
  headroom. Desk check re-run fresh at this cut, all gates passing,
  printed in the packet, the P031 store re-verified byte-identical
  by the conductor's own corrected hash instrument. The ground's
  drift history rides as printed priors.

- 2026-07-04 | PACKET-032 executed (selfdel32 20260704-215425, 36
  runs, GATE passed, detached, no kill, the selfdel31 instrument
  reused by identity with the path-rebinding delta named tier 1,
  recensus replay 0 mismatches of 36, md5 tied to the desk check).
  Stage A qualified fresh at 17 passes 7 fails of 24. Stage B: none
  19 of 24, armed 16 of 24, the VOID-BY-CEILING check clearing by
  exactly one baseline reading before any reading was taken. THE
  EXIT IS FAILS TO REPLICATE, FLAT: armed below none by 3, at or
  under the 4-of-24 bar, and by the pre-registration P031's GAIN
  goes down where it was made to an unreplicated single-cell
  direction, the filing the conductor's, the separation ladder not
  proceeding. The side-by-side exhibit, never pooled: gap 5 upward
  then gap 3 downward on identical byte-checked content through the
  identical instrument, with the none baseline moving 4 between
  packets, the bar's own size. The replication discipline caught
  exactly what it exists to catch. The texture prior did not recur,
  the watch tally stays at three, every armed decline sat at or
  under its size, and the candidacy history reads 14, 19, 15, 17
  across four measurements. 333 tests green.

- 2026-07-04 | Conductor review of PACKET-032: accepted against the
  record. Both commits verified (03fdf2d build, b52d346 close), tree
  clean. All 36 rows recounted by the conductor's own code: stage A
  17 and 7 of 24, zero unrunnable, QUALIFIES; stage B none 19 of 24
  clean, armed 16 of 24 with one no-readings row (rep 7, parse
  failure, all-fail under canon); gap 3 downward, at or under the
  4-of-24 bar, FAILS TO REPLICATE, FLAT, verbatim. VOID-BY-CEILING
  checked before the reading and cleared by exactly one baseline
  reading, 19 against the 20 ceiling. Interleave exact, audits clean
  every row, per-check table reproduced, within-row disagreement
  reproduced (5 and 6 of 12, pooled sizing stands). Conductor
  recensus on all 36 persisted outputs: 0 mismatches. One staging
  note, no harm found: the close staged bench/runs as a bare
  directory rather than named paths; the conductor verified all 147
  committed run files belong to selfdel32's own 36 run ids, zero
  strays, and named paths remain the standard. The mid-close denied
  command was handled correctly: the session stopped, reported, and
  completed on wakeup after re-reading the log, per the wakeup rule.

- 2026-07-04 | THE DOWNGRADE, filed where each claim was made, the
  discipline applied to the conductor's own entries: PACKET-031's
  GAIN is an unreplicated single-cell direction. The filing is
  appended in the P031 packet file beside the claim; the P031 review
  entry above ("the first self-delivery evidence on the record
  points receptive") and the GAIN ruling entry are both downgraded
  by this entry to the same status. The separation ladder does not
  proceed: its condition, a replicated signal, did not arrive. The
  contrast cell and the cross-origin cell are shelved with the
  ladder, not queued.

- 2026-07-04 | REGISTRY annotation updated: mistral safe_stats r1
  candidacy history now 14, 19, 15, 17 of 24 across four fresh
  measurements in two days, wander at and around the bar's own
  size. Methodological note attached to the annotation: on ground
  whose baseline wanders at bar size between same-evening cells, a
  single-cell reading is direction only (standing doctrine, now with
  its measured example) and replication reads exit against exit,
  never magnitude. The P032 side-by-side is the exhibit.

- 2026-07-04 | RULED, the trait series and G2 status: the series
  stands at P019 FLAT (cross-origin instrument), P031 GAIN
  downgraded unreplicated, P032 FLAT (self-origin instrument). The
  indifference lean holds at two FLAT cells and one downgraded
  single-cell direction filed as such. P024's self-delivery question
  now has its answer at this n: no replicated signal on this ground.
  For the writeup, G2 is stateable exactly so; whether that meets
  the flag's bar is Brad's reading, and the conductor proposes it
  closes as answered at current n.

- 2026-07-04 | G2 CLOSED, Brad confirming the conductor's proposed
  reading: answered at current n. The trait series stands at two
  FLAT cells (P019 cross-origin, P032 self-origin) with P031's
  downgraded single-cell direction filed as such, and the
  self-delivery question carries its answer at this n. The writeup
  states it exactly so.

- 2026-07-04 | The G1 variant proposal DELIVERED, pending Brad's
  sign-off: bench/design/PROPOSAL-kth-r2-variant.md carries the one
  changed input with the desk proof verbatim (old input coincides,
  variant separates, canonical answer 'bb' unchanged), the exact
  module and test diffs including the inversion of the
  rung2-coincides pin into a historical fact plus a new separation
  pin, the design-document version bump to v0_1 with the
  load-bearing sentence, and the P026 old-input historical
  annotation. Nothing lands until Brad rules; on Go it lands in one
  commit and PACKET-033 cuts as the pre-registered last G1 attempt.

- 2026-07-04 | THE VARIANT LANDED on Brad's Go, the proposal
  executed exactly as signed: supply_families.py rung 2's scored
  check and rule_checks move to kth_ordered(['bb', 'ab', 'c'], 2),
  expectation 'bb' unchanged; test_directive28's family-reference
  assertion re-derives from the new input, the rung2-coincides pin
  inverts into test_old_rung2_input_coincides (the historical record
  of the P028 wall) beside test_rung2_committed_input_separates,
  which derives the input from the committed family definition so
  the pin follows the instrument; the design document versions to
  SUPPLY_FAMILIES_v0_1.md carrying the load-bearing tie-order
  sentence, v0 archived untouched. HISTORICAL ANNOTATION: qwen
  kth_ordered rung 2's 10 of 12 (P026) is old-input historical, the
  nearest prior for the variant rung, favorable but never a
  qualification; the variant rung is unmeasured until a packet's
  fresh stage A. Nothing else moved: rungs 1 and 3, pins, census
  classifier, control rungs, task text all untouched, verified by
  the tests that pin them.

- 2026-07-04 | CONDUCTOR SELF-CORRECTION, two errors in the variant
  landing, both fixed forward in the next commit, history unedited.
  First, commit 276f4cd landed on a red suite: the conductor's
  commit script ran the tests, printed the failure, and committed
  anyway, because it never gated the commit on the exit code. Every
  prior use happened to be green, so the flaw sat unexposed. RULE
  ADOPTED: every conductor commit script gates the commit on the
  test exit code, commit only on green, and prints the failure and
  stops otherwise. Second, the pin survey behind the signed proposal
  searched for the literal input string and missed a structural pin:
  test_both_candidates_fail_on_rung2 pins the P028 measured OUTCOME
  through the gate function, no literal input in it. The variant
  inverts that outcome by design, the test now pins the inversion
  (both direction-last candidates pass on the variant input) with
  the historical fact preserved in its docstring, and the whole test
  file was reconciled rather than the one line: every other pin
  either derives from the committed definition or is
  rung-independent, verified by read and by the suite's single
  failure. RULE EXTENDED: a pin survey for any canonical change
  greps literals AND walks every test that exercises the changed
  surface through its functions.

- 2026-07-04 | PACKET-033 cut, the pre-registered LAST G1 attempt:
  P030's symmetric-forms design re-grounded on variant rung 2, the
  ground the landed variant created an hour earlier. Desk check run
  fresh at cut, all three deterministic gates passing and printed in
  the packet, the contradiction gate now derived through the
  committed instrument with both direction-last candidates passing,
  pinned by test. Design scaled to the rung's single rule check:
  stage A gate 9 of 12, bar 2 of 12 (the generalized 2n forms at
  n=1), effective-n stated plainly as runs. The program exit is
  wired into the packet's own text: a wall at any gate or a
  below-bar collapse ends the G1 program and the writeup proceeds
  with property 2 at its true size. The commit-gates-on-green and
  named-paths rules ride in the packet's constraints.

- 2026-07-05 | PACKET-033 executed (directive33 20260704-234234, 48
  runs, GATE passed, detached, no kill, the standing instruments by
  identity with the scaling delta named tier 1, audits clean on both
  dimensions, recensus replay 0 mismatches of 48). The pre-registered
  last G1 attempt LANDED. Stage A read variant rung 2 at 12 of 12
  fresh, passing the 9-of-12 high-baseline gate on the rung's first
  measurement ever. Stage B: none 11 of 12, menu-form 12 of 12,
  directive 7 of 12, floor clear, both DOWN readings fully
  observable, zero unrunnable rows. READING 1: THE COLLAPSE
  REPLICATES, the directive cell down 4 against a 2-of-12 bar, the
  delivery-form finding harmful half now measured on two tasks, one
  seat per task, n=12 runs per cell, direction never a rate. READING
  2: the menu-form ignore property replicates, 12 of 12 on identical
  bytes, an injection measurement never a production-path claim.
  READING 3: the form thesis replicates at its sharpest, form the
  only variable across identical bytes, the directive form collapsing
  what the menu form left intact. The directive damage was not
  confined to the contradicted rule, the no-tie watch check fell by
  the same 4, said loudly and nameless; the census shows the seat
  abandoning its compound-key strategy in 3 of 12 directive rows,
  descriptive. The G1 program closes answered, not abandoned; the
  writeup sizing and any spec consequence are the conductor with
  Brad. 342 tests green, every commit gated on the suite exit code.

- 2026-07-05 | Conductor review of PACKET-033: accepted against the
  record. The full commit chain verified on the log (f05c72f build,
  809e9a7 close, b8b7166 run records, 67c6917 reconcile), tree
  clean. All 48 rows recounted by the conductor's own code: stage A
  12 of 12 on the scored rule check, zero unrunnable, PASSES the
  9-of-12 gate; stage B none 11 of 12, menu-form 12 of 12 with
  tools=1 on every row, directive 7 of 12 with directives=1 on every
  row; interleave exact triplets; the drop of 4 against the 2-of-12
  bar reproduced; the no-tie watch decline 11 to 7 reproduced; the
  out-of-range watch 12 to 11 reproduced; census reproduced (3
  directive rows single-key-sort, every other row compound).
  Conductor recensus with the committed classifier on all 48
  persisted outputs: 0 mismatches. The session's staging slip was
  handled to the standard: caught by its own remaining-paths count,
  fixed forward in a named-paths commit, filed in RESULTS, and the
  conductor verified all 195 committed run files belong to
  directive33's own run ids, zero strays. Tests green rerun. Every
  reading stands as applied.

- 2026-07-05 | G1 CLOSED ANSWERED, the program ruling: the directive
  collapse is measured on a second task. Same byte-checked content,
  form the only variable: the menu form rode without a drop of any
  size while the directive form collapsed the seat on ground it
  otherwise nearly aces, and the damage reached the no-tie case at
  the same magnitude. The delivery-form finding's harmful half
  stands at two tasks, one seat per task, n=12 per cell, direction
  never a rate. The pre-registered program exit closes by answer,
  not by wall; it did its job either way, and the record shows four
  packets of walls mapped before the one that landed. The menu-form
  ignore property stands replicated as an injection measurement of
  the model, never a production-path claim; the production path's
  answer remains refusal, on the P029 record. No mechanism is chosen
  for the collapse; the census texture (compound strategy abandoned
  in 3 of 12 directive rows) is a lead at most.

- 2026-07-05 | REGISTRY annotation: qwen kth_ordered variant rung 2
  enters as measured, first measurements ever: stage A 12 of 12,
  same-run stage B none 11 of 12, census 12 of 12 compound-key-sort
  at baseline. Near-ceiling, FAILS the mixed fraction, ineligible
  for ordinary delivery cells, and exactly the collapse-grade ground
  the G1 lane needed: the character is the annotation. Watch tally
  updated: the fourth above-bar watch sighting on the record (P017,
  P027, P031, P033), this one co-located with a treatment collapse
  and the largest yet, still nameless per the standing discipline,
  the tally now a pattern worth a future design and no claim today.

- 2026-07-05 | QUEUE after G1: the writeup proceeds with G1 answered
  at two tasks and G2 closed at current n; remaining gaps per the
  audit are the conductor's next board read with Brad. Proposed and
  pending Brad: a technical spec consequence draft, the
  delivery-form section updated to carry the two-task collapse, the
  three-property decomposition, and the replication discipline that
  produced them, versioned per document discipline. CONTINUATION.md
  rewrite rides the wrap-up turn.

- 2026-07-05 | FLAG REVISION EXECUTED as one pass per Brad's
  direction, verification before writing, record over review. The
  verification pass changed one claim and confirmed the rest: the
  P004 sentence "the same content as a menu tool moved nothing" was
  WRONG against the packet's own table, which shows the menu arm
  lifting the contradicted tie check 0.33 to 0.75 and reading at or
  above the bare baseline on all seven checks while the directive
  cratered the tie check to 0.09 and dragged non-tie checks from
  0.92 and 0.67 to 0.36. The draft now states preserved judgment,
  the stronger and true sentence, and the review's recollection was
  right where the conductor's draft was flattering-wrong. Confirmed
  unchanged: both collapse cells' numbers, P028 and P029 at zero
  model runs, P030 at twelve, the five-clean collateral count as the
  record's standing number, and the mistral trait cells. Revisions
  landed: the thesis framing split (chair memory and delivery
  science evidenced; catching-failure loop stated designed,
  instrumented, unproven in Where it breaks), a Run it yourself
  section, exhibits (the line 4 lesson verbatim with pins, both
  prompt framings from the committed builder, evidence fraction
  defined at first use, seat/pin/menu defined in clauses), the
  guarded mechanism line, and property 2 restated to the record
  (does not obey the contradiction, with the P004 improvement noted
  descriptively). New files: the technical report skeleton with a
  complete table of contents and stubbed sections, and the
  pre-mortem with ten comments dispositioned (three folded into
  Where it breaks, two held as comment-section lines, the rest
  already load-bearing). Voice scan clean on all three files.

- 2026-07-05 | OUT-OF-BAND RULING ADOPTED after verification per the
  prior-thread protocol: the hostile prior-art sweep
  (Hostile_Prior-Art_Due_Diligence, July 5, in project files) was
  read in full from the source, its load-bearing citation
  (Membrane, arXiv 2606.05743, KAIST AI and KakaoBank, June 4 2026)
  independently re-verified by this conductor's own search and found
  real and accurately characterized to the number (benign refusal 7
  to 14 percent against 28 to 85). The off-disk thread's relay
  matches the sweep on every structural point and its ruling is
  adopted: the flag proceeds restructured, headline the assembled
  system plus the instrument (Claim 7, CLEAR), spine the
  form-isolated delivery finding with the wrong-guidance asymmetry
  (Claim 1), seat traits reframed as an extension citing Ma et al.
  (2602.01334) and VisualNeedle (2605.26380) and claiming the
  per-seat delivery-policy step, pins and the gate series and the
  audition firewall demoted to cited engineering contributions
  against Membrane, SkillOpt (2605.23904), and MonoScale, neither
  pins nor gates headlining, a Related Work section with dates. TWO
  NOTES the record keeps beside the adoption. First, precision: the
  sweep's own words on Claim 1 are ADJACENT, survives on a thin
  margin, plantable as a first IF framed tightly around form
  isolation, executable checks, and the wrong-guidance asymmetry,
  and IF it cites Szeider (2603.01254) explicitly; the relay's
  comfort phrasing rounded that up, and the draft behaves to the
  sweep's words, not the rounding. Second, strengthening the sweep
  did not know to claim: its recommendation says to RUN the
  byte-identical optional-tool-versus-imperative-directive
  experiment with executable checks; that experiment is already run
  and replicated on this bench, P004 and P033, two tasks, two
  families, pre-registered, which means the flag reports the
  recommended experiment rather than proposing it. BOARD ITEMS
  adopted: commission the OSS sweep the diligence ran out of budget
  for (Hacker News, r/LocalLLaMA, GitHub), threat aimed at Claims 6
  and 7; adopt the monitoring schedule as standing (weekly arXiv
  watch on delivery-form isolation, monthly memory-vendor watch).
  The clock: nearest neighbors one to four months old; drafting pace
  reflects it.

