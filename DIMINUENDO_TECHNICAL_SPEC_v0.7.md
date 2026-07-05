# Diminuendo Technical Spec v0.7

Purpose of this document. The concept spec says what Diminuendo is and why. This says how the known pieces are built, concretely enough to break before code, and now against code that ran. Every section has a Spec and a Where it breaks. The second is the point. Specify, attack, build the survivors. v0.7 folds in the second bench window: transfer measured in both directions and replicated, the task revealed as the delivery moderator, and a third model seat onboarded, teaching, and profiled. The evidence behind every claim marked measured lives in bench/packets and bench/DECISIONS.md.

Scope. Known, buildable machinery only. Not governance, not the grand system. The two centers that were open research are narrower now. The score-to-lesson engine is specified as a concept curriculum with named remainders, and learned-catching has a measurable signature with one irreducible floor. What's still open is marked in Section 12, and it closes by running, not on paper.

---

## 1. Roles and instances

Spec.
- Three instance types, never sharing state: Performer (does the work), Audience (fresh blind instance, scores only), Conductor (holds state, never scores).
- Four roles: Patron (the human, top, ground-truth verdict, the final decorrelated detector sitting outside the whole performance, steps in on highest blast radius), Conductor (holds composition, goal, tempo, releases work, never scores), Principal (section-scoped, QAs musician output before it reaches the conductor), Musician (single scoped task, waits for the baton).
- A "role" is the persistent unit. A model fills a chair. Memory belongs to the chair. Swap the model, the chair's memory stays.
- An instance is one running model with a defined input contract and output contract. A Performer instance receives: the task, the criteria, and a queried landscape of tools to choose from. It returns: output, the tools it chose, breadcrumb. It never receives raw scores or the metric.
- The system shapes the landscape, never the choice. Terrain, not steps. It sets what tools are available and how they're weighted, and the instance still picks and still reasons. Same principle as the menu changing while the chooser stays free, the flag that signals without pulling, the verdict left to the upper level. Shape the conditions, never take the agent's hands.
- The system's job toward the Patron is not to catch the last error. It's to lower the noise until the one error it couldn't catch clears the floor and becomes audible. Resolve every disharmony it can, so the residual is the only sound left. Diminuendo, until the off-note is findable by the detector outside the room.

Where it breaks.
- "Never shares state" is easy to write and easy to violate by accident through a shared file, a logging side channel, or a lesson that smuggles the metric. Needs an explicit boundary I can test, not a principle.
- Chair-holds-memory assumes the chair's memory stays coherent across model swaps with different context windows and formats. A lesson written against model A's behavior may not transfer to model B. The rig runs, and the evidence now goes both ways. Forward: four consistent measurements of one family's lessons lifting another through the production menu. Reverse: a machine-born lesson with a no-hands lineage (one family's break, full-gate distillation, pins, menu) lifted the other family's seat, measured twice on the same design against fresh same-run baselines, with origin parity replicating beside it, the inherited lesson matching the seat's best hand-authored content both times. Sized honestly: one task per direction, small n, direction never a rate. The transfer bet rides on the memory being concepts, which are close to model-invariant, not procedures, which aren't, and the build enforces that line with shape screens after measuring a procedure-shaped lesson behave like a command. If transfer fails at scale anyway, the fallback is shared concepts with a thin per-model grounding layer.
- Principal QA adds a hop on every section. If the principal is weak, it becomes a rubber stamp that adds cost and catches nothing.
- The quiet room surfaces the disharmony a person can hear. The wrong note that happens to sound in tune stays inaudible even in silence, and only the world refutes it. The Patron is the last detector, not an omniscient one.

---

## 2. The Score (deterministic dependency map)

Spec.
- Two jobs, kept separate. The graph encodes dependencies, which is a claim about the task, and enforces ordering, which is a mechanism. The decorrelation is real for enforcement and earned for encoding. A scheduler that refuses to release a node until its predecessors are marked complete is deterministic and genuinely independent of the conductor. That is the decorrelated check on timing, and it stands.
- The edges, the claims themselves, come from three sources, layered like feature capture (Section 3):
  - Structural edges, where a node reads what another writes, extracted by a deterministic script watching the data flow. Decorrelated, cheap, forward. Strong wherever the data flow is legible.
  - Semantic edges, where a node should weigh another's conclusion without reading its file, asserted by the conductor. Correlated, provisional, the forward pass.
  - Missing edges, discovered by breaks. A node that ran without an input it needed produces a break, and the lesson is a new edge. The backward pass, decorrelated by reality.
- Error types are asymmetric. A false edge costs time only, you waited for nothing, and it retires like a marginal rule once it never changes the result. A missing edge risks correctness and is the one to catch. So the graph's content is learned the way concepts are, the conductor's guess forward, breaks correcting backward.
- Dynamic growth, one direction only. A running node may spawn children downstream, which can't make a cycle because a child is strictly later and nothing points at it yet. That's a live, deterministic, safe operation, with a cheap cycle check on every edge add as backstop. A node discovering mid-run that it needed an undeclared upstream parent is not a live edit. That's a break. Stop, schedule the parent, re-run, add the edge for next time.
- Cross-level flow and escalation live in Section 10.
- API surface: `ready_nodes()` returns releasable nodes, `mark_complete(node)` updates state, `add_node`, `add_edge`, `blocked_by(node)` for diagnostics.

Where it breaks.
- The latent missing edge. A real dependency that never gets exercised stays invisible until it bites. The same floor as everything else, inherited not added.
- Structural extraction only sees legible data flow. Where work passes freeform text, the structural layer goes quiet and the conductor's correlated semantic authorship carries more of the load. Strong for file-ops domains, weak for pure reasoning.
- Replanning. A node finding the plan above it is wrong, rather than an edge missing, is not a graph fix. It routes up through the escalation mechanism in Section 10.
- Pruning false edges costs a re-check to confirm the edge never mattered. Tolerable, because false edges are cost and not correctness.

---

## 3. The Breadcrumb (the data record)

Spec. The load-bearing record. One per node. Triple duty: forecasting features, credit-assignment trail, novelty inheritance. Fields:
- `node_id`, `parent_concept_id` (the trail upward)
- `model`, `role`
- `work_features` (a vector, not one label: operation, target, size, structure, constraints, and whatever the schema captures). Grain is chosen at read time by which features a consumer groups on, never committed at write time.
- `cost_time`, `cost_tokens` (kept separate, never summed)
- `outcome` (provisional forward score, then hindsight-corrected)
- `error_class` (populated in hindsight if a miss is found)
- `novelty_flag` (set at cast time, can be re-set retroactively)
- `trace_ref` (the distilled reasoning trace, the kept thing, not the raw input. The error lives in the process, and the trace is where it's visible. Distilled to its load-bearing steps, the same cut that makes the lesson and strips the content for pooling)

Grain is a projection, not a setting. One feature vector, three reads. The forecaster groups on a couple of coarse features for a stable baseline. Discrimination holds a concept's stated conditions fixed and varies one candidate feature against the comparison set. Attribution localizes at whatever altitude the break lives. No single grain, so no coarse-versus-fine dilemma. The curse of dimensionality doesn't bite because no query matches the whole vector, every query is a low-dimensional projection.

Capture is layered, like detection.
- A deterministic schema pulls structural features forward and cheap, decorrelated from the performer because a script reads them. The reference layer seeds the schema, the same seed that stocks the concept vocabulary.
- Back-fill adds the feature a break exposes, paid once, then logged ahead.
- Retention sets how much of the trace you keep so a newly found feature can be re-derived across past runs. Keep enough and the comparison set enriches retroactively. Keep too much and storage and privacy both suffer.

Where it breaks.
- Feature selection replaces grain as the hard problem. You can't capture every dimension, so the schema is a prior, and the prior is wrong at the edges where novel breaks live. Back-fill covers the reconstructable misses. What's neither captured nor reconstructable is the floor, the unrecoverable latent dimension, the same floor Section 5 lands on.
- Trace fidelity. The trace is the model's self-report, not a recording. A confabulated clean trace over a broken process hides the error better than the bare output, and the infidelity correlates with the bad reasoning you're hunting. The trace needs a decorrelated reader, and a shared blind spot in one model family still survives.
- Retention timing. Distill a trace before you know which step mattered and you can discard the one that did. So keep traces raw in the novel and recent window, distill only after the work-type goes quiet. Decay decides when.

---

## 4. The Scoring Ledger

Spec.
- Two axes, time and tokens, recorded separately for every node. Never combined into one number.
- Clean run posts positive. A caught problem posts the cost of the failure plus its correction as a minus, then a catch-bonus as a plus. The problem's cost self-quantifies through the rework it caused, which scales the penalty to blast radius without hand-grading.
- The metric (time, tokens, raw score) lives only with the blind Audience. The Performer sees criteria and lessons. Never the metric.
- A third axis, accuracy, is not live. It enters only in hindsight (Section 6), which is the correct place for the correctness measure.

Where it breaks.
- Catch-bonus calibration. Set it too high and the system manufactures catchable problems to earn bonuses. Set it too low and catching isn't worth the inspection cost. The number is unknown and it's gameable.
- "Cost is not correctness" is stated and then leaned on anyway. The live score is provisional and biased high (it only knows what got caught). Every downstream consumer of the live score has to treat it as a lower bound on trouble, and nothing yet enforces that.
- Self-quantifying penalty assumes rework is measurable and attributable to the original miss. When a miss causes diffuse downstream slowdown rather than a clean redo, the penalty undercounts.

---

## 5. The Lesson Engine (score → lesson)

Spec.
- A score is not a lesson, and a lesson is not a procedure. A lesson is a guiding concept plus the conditions on when it applies. The engine issues coarse concepts and sharpens their boundaries over time. A concept curriculum, not a scalar inversion.
- Three altitudes, three horizons, three languages. The musician's lesson is task-shaped and fast. The principal's is section-and-combination-shaped and medium. The conductor's is composition-shaped and slow. The same run gets read three ways, and the three are decorrelated views that cross-check each other's attribution. A concept that didn't carry can be invisible to the musician and obvious to the conductor.
- Most updates are not rewrites, they narrow applicability. Running is fine, running with scissors is dangerous, running scissors to a surgeon who needs them is necessary. The lesson is never don't run. It's the edge of the rule, the when and the how and the with-what. A break almost always annotates a rule that was right. It rarely deletes one.
- The clean corner. Don't ask is the rule wrong, which is confounded. Ask what context-feature separates this misfire from the prior times the same rule worked. That's a bounded discrimination and it yields the valuable lesson, the how-and-when. Within-task model substitution is the cleanest case (only the model varied) but it yields only casting lessons, which player. Applicability-discrimination is the general case and yields procedural ones, the half that was supposed to have no clean corner.
- Contrast is scarce in practice, measured. At small retry counts a model is nearly deterministic per task: it passes every run or fails every run, and the within-task fail-and-pass pair rarely exists. Sibling contrast widens the source, a fail on one task and a pass on its same-class sibling, same seat, still one seat's own experience, with within-task pairs keeping precedence. Lessons come from breaks, never from averages, and a class that never breaks yields no lesson, which makes failure supply the binding input of the engine. A strong seat that rarely breaks in-band accumulates memory slowly, the entry-fee economics seen from the supply side.
- Committed lessons pass gates in series: required shape and provenance, the metric screen, the platitude screen, the aim screen (the rule must share ground with the failing check that produced it), and the imperative screens on concept and rule. Crude screens by design, each one paid for by a measured failure.
- A committed lesson contains: the concept, its applicability conditions, the work_features and breadcrumb trail it came from, and a confidence that says how far it generalizes. No metric, no raw task content.
- The trace is the substrate. Process-features and the silent errors that never show in output, the right answer reached by wrong reasoning, live there and nowhere else. Distilling a trace to its load-bearing steps is one cut that does three jobs at once: shrinks it for storage, extracts the lesson, strips the content for pooling.

Delivery as a landscape, not a rule set.
- Lessons reach the performer as tools to choose from, queried at the start of a task, never as corrections after it. The friction finding is that models resist post-hoc correction. Guidance offered upfront as an option shapes the response as it forms instead of fighting one already committed. No prior output to defend, and the method is self-authored.
- The landscape has a duality. The same query returns directional tools (approaches), cautionary tools (pitfalls, recovery moves), and provocations (lateral prompts, the strategy-and-psychology texture from the reference layer). A field to work in, not a track with the turns pre-decided.
- Confidence-graded. Narrowed, earned tools are the exploit half. Provocations are the explore half, unvalidated and high variance, offered as a fallback when the reliable moves aren't working. Explore and exploit live in the menu's own structure.
- The menu is the applicability conditions rendered as a query result. The conditions are the engine's view, the menu is the performer's view, one object. A wrong pick is a break, the break re-scopes the tool, and the tool resurfaces in the context where it fits. The fresh instance has no memory of the prior menu, so curation never reads as correction. Role-holds-memory is what makes it invisible.
- Re-scope, don't demote. A failure sharpens where a tool applies, it doesn't lower its standing. Demotion is the cruder fallback for when the distinguishing feature is unknown. Convergence stays gradual, with a re-check budget that resurfaces a pruned tool to test whether it was wrongly cut.
- Measured, not assumed: delivery changes output. The same lesson as a menu tool lifts the rule checks it teaches, and as an explicit directive it gets obeyed even when wrong, collapsing work the performer otherwise did correctly. The menu is the safer surface because a performer can decline a tool and cannot decline an order.
- Tool response is a casting trait, and three seats now read as three responses. One seat filters its tools, ignoring the wrong ones and gaining modestly from the right ones. One amplifies them, posting the largest measured lifts under a right tool and real harm under a wrong one. A third sat indifferent on its first valid cell, unmoved in either direction by a matched tool on qualified ground, a lean, not a profile. Pins are necessary and not sufficient: applicability pins (rule class, stated direction, rule topic) block topic contradictions, and harm still occurred under fully pinned, matched tools on ground where the stated rule fights the canonical solution shape. The task moderates delivery: the same seat through the same menu gained on a rule that extends the idiom and collapsed on a rule that replaces it, inside one interleaved run. The idiom-conflict moderator is the leading hypothesis, design-level and untested, and if it holds it is forward-classifiable, a casting input the forecaster family can consume. Trait ground carries its own doctrine: a trait cell conditions on ground that proves itself mixed at the rule-check level at R=12 inside the same packet, never on a small-n label, which two null cells paid for.
- The menu carries the concept and its applicability conditions, nothing else. That makes the concept text the safety surface: the imperative screens (declarative, never a recipe) guard it, and the rule field, which never rides, is screened for distillation quality rather than delivery safety.

Two coupled loops.
- Do-better. Applicability edits cut the breaks the performer produces.
- Catch-better. When hindsight finds a break the audience missed, that's a lesson to the audience about what to watch. The criteria sharpen, and next time the break is caught live instead of in hindsight. This loop is the one that lowers the detection floor. See Section 12.

Four detectors, four latencies.
- Route deviation, in-flight. With the trace, the forecaster predicts the route a model takes (Section 7), and a run going off its predicted path flags before the output exists. The earliest catch and the cheapest, caught while it's still correctable instead of paying the rework. Matures with data, and a legitimately novel route trips it, which raises the guard, not a gate.
- Criteria, fast. The audience catches breaks it knows to look for, at the output. Arbitration is one-directional: executable evidence outranks the audience toward fail on the checks it covers, and an audience fail is never overridden by an evidence pass, because evidence covers correctness, not every criterion, and silence is not safety. Measured at small model scale: the criteria detector is weak on its own, one local judge fails clean work, the other passes everything, and demanding substantiation traded away the true catches. Execution carries the catching load. The designed cure is a three-way verdict, pass, fail with cited evidence, or uncertain escalating into the flag tally at low weight, an escalator instead of a forced binary. Unbuilt, queued.
- Forecast residual, medium. A score under the forecaster's estimate by a margin flags something is wrong here even when no criterion fired. Reality below prediction is visible when the cause isn't. The surprise fires a breadcrumb trail that localizes the gap and updates both the concept and the forecaster.
- Real world and audit, slow. The only signal that reveals a steady silent loss, the kind the forecaster has normalized into its own baseline.

Grain heals, it isn't fixed at write time.
- A break can write its own missing feature into the record. This broke, why were we running it, asked in hindsight, recovers context that wasn't logged forward and records it. First time a feature matters it costs a break to find. After that it's logged ahead. Same entry-fee shape as the economics, pay once per feature.

Retraction is emergent.
- A genuinely false rule isn't found and deleted by a special faculty. Its applicability window narrows everywhere it's tried until it's obsolete, then it retires into lessons-from-failure. Slow, because you can't know a rule is false everywhere without the breaks that prove it. The retired rule becomes a negative concept, a marked trap, which feeds new concepts from the failure side.

Where it breaks.
- Genesis. A break that no existing concept covers needs a concept that wasn't there. Narrowing is bounded, genesis is open-ended. This is where the reference layer and slow abstraction have to carry the weight, and it's unbuilt.
- Unrecoverable latent context. Back-fill only recovers what hindsight can reconstruct from the surviving record plus the outcome. A distinguishing feature that was never captured and can't be recovered leaves the rule narrowing coarsely instead of cleanly. The true grain floor, smaller than Section 3 implied, not zero.
- Stationary silent loss. The forecast-residual detector measures deviation from prediction, not from truth. A failure that's always present gets absorbed into the baseline and stops making surprise. Only the slow channel catches it, and the slow channel is the latest and least timely.
- The marginal rule. Narrowing drives a false rule to zero cleanly. It leaves a mostly-wrong-occasionally-right rule alive at a narrow window that costs more to judge than it returns. Whether to retire it anyway is an economics call, the effort selector's, not a new mechanism.
- Craft-shaped automation. Concepts are in the language of the work by nature, which mostly closes the old metric-leak. Mostly is doing work in that sentence. The screens now mechanize part of it: a misaimed, metric-shaped, platitude, or procedure-shaped lesson dies at the gate, each screen paid for by a measured failure. What no screen catches still needs the human read, and that remainder is unproven.
- Transfer across models. A concept learned from model A's failure may not bind on model B. The three-layer cross-check helps. Measured in both directions through the production menu, and the reverse direction and origin parity are each replicated at two measurements on the same design against fresh same-run baselines. The magnitudes are real and check-local, one task per direction, direction never a rate. The failure-supply constraint that capped the evidence eased when the third seat's onboarding supplied gated lessons in all four rule classes, including the two no other seat could break; the constraint now sits at delivery evidence rather than existence.
- Friction theater, measured and retired as stated. The three-arm test ran, none against menu against directive, and delivery changes output. What replaces the question: response style differs by seat, the effects are check-local and vanish inside coarse task means, and contradictions no applicability pin can express remain the amplifier seat's exposure.
- Landscape breadth. Too rich a landscape becomes noise and context rot. Too thin becomes a cage that strips the model's own problem-solving. How wide to surface is a knob, tuned in the loop, the grain tension again.
- The menu converges against detection. Curation rewards tools that don't visibly break, so a tool that fails silently can stay on the menu and get reinforced while the dashboard reads healthy. The direction is measurable. Its correctness is only as good as detection.
- Corner cleanliness tracks detection. Discrimination compares a misfire against prior successes, but success is the live label, only as honest as detection. Silent misfires wearing a success label poison the set. So the clean procedural corner is clean as a function of the local detection rate, not a constant. High-detection work-types hold, leaky ones degrade quietly.

---

## 6. The Hindsight Pass

Spec.
- Runs at project end. Re-evaluates the run with outcome knowledge the live pass didn't have.
- Produces a casting profile per role: model × seat × work-features → accuracy, token cost, time, error rate, and tool response, filter, amplifier, or indifferent, the measured trait that sets how tightly a seat's menu gets pinned, read only from cells whose ground qualified as mixed at the rule-check level. Correlating the cost columns against final accuracy is the casting sheet for future orchestras.
- The unobserved-miss problem (you can't measure your own false-negative rate) gets a layered estimator, not a single number:
  - Project-end hindsight: fast, rich, a strong lower bound. Accuracy % here is an upper bound on true accuracy.
  - Slow real-world outcomes: reveal silent misses over time, lower the estimated ground.
  - Sampled independent audit: puts error bars on the estimate.

Where it breaks.
- "Project end" assumes a clean end. Continuous or open-ended work has no end to trigger the pass. Needs a windowing rule.
- The slow real-world signal is the truest and the latest. By the time it arrives, the model that earned the profile may be retired and the lesson stale. The most reliable data is the least timely.
- The estimator gives a lower bound that tightens, never the true false-negative rate. But discovery latency gives the slope a measurable signature even so. The absolute floor stays unmeasurable, the rest is trackable. See Section 12.

---

## 7. The Forecaster (the Analyst)

Spec.
- Statistical, not an LLM. Decorrelated from the agents by construction.
- Inputs: breadcrumb features (work_features, model, parent_concept, historical cost and accuracy) and the distilled traces. Outputs: predicted cost, predicted accuracy, confidence, and once traces accumulate the predicted route, the shape of the attempt.
- Route prediction. After enough traces the forecaster predicts not just the endpoint but the path a given model takes on a work-type, where it branches, where it stalls, what it burns getting there. That powers the in-flight detector in Section 5, a run off its predicted route flags mid-attempt.
- Makes casting predict-then-cast instead of react.
- Four rules: confidence-weighted not authoritative; confidence picks the player but never lowers the guard (live checks run full-strength regardless of forecast); explore as well as exploit; multi-dimensional and statistical. Confidence is calibrated in the hindsight loop.
- Cold-start: borrowed benchmarks first, own hindsight takes over as it accumulates.

Where it breaks.
- Garbage in. The forecaster is only as good as work_features (Section 3). If the capture is wrong, the features are wrong, and a confident wrong forecast is worse than no forecast.
- Route prediction is data-hungry and cold-starts empty, so the in-flight detector doesn't exist early. It arrives once a model has enough traces on a work-type. And a novel-but-correct route reads as deviation, a false alarm the system has to treat as guard-raising, not gating.
- "Never lowers the guard" is the safety rule and also the cost problem. If the forecast never reduces inspection, what is the forecast for. The answer is casting and exploration, not guard reduction, and that has to be enforced or the cost savings everyone wants will quietly come from lowering the guard.
- Calibration needs volume. Early on it's uncalibrated and its confidence is itself untrustworthy. The system has to distrust its own confidence number until it's earned, and nothing yet does that.

---

## 8. The Novelty Flag

Spec.
- Catches the forecaster's blind spot: a task that looks routine but isn't.
- Tier-appropriate, forced by context scoping. Musician judges task novelty. Principal judges concept-plus-combination novelty. Conductor judges concept novelty.
- Inherits down the breadcrumb trail. A routine-looking task gets re-flagged novel if its parent concept is novel. Proactive at cast time, retroactive via hindsight.
- A slider, not a switch. Never zero.
- Three rules: escalator never a gate (firing raises the guard, silence never lowers it, silence is not safety); decorrelated ownership (not the forecaster, instead statistical outlier plus conductor judgment plus human for high blast radius); orthogonal check-areas tuned by blast radius.

Where it breaks.
- Everything is novel at the start. With no baseline, the flag fires constantly and correctly, which means maximum cost exactly when there's no money and no data. Cold-start cost is real and front-loaded.
- "Silence is not safety" makes the flag a one-way ratchet. It can only raise cost, never lower it. Combined with the never-lower-the-guard rule, the system has two mechanisms that only add inspection and none that confidently remove it except decay (Section 9). Decay is carrying a lot of weight.

---

## 9. The Effort Selector (economics)

Spec.
- Novelty plus forecast set inspection depth per node. Breadcrumbs aim the focus at the few risky nodes. The rest runs light.
- Effort = floor + escalation. The floor is decorrelated baseline inspection that runs on everything regardless, scales with blast radius, and is never cut. The floor is what catches novel-disguised-as-routine.
- Decay is the economic engine. First encounter of a pattern pays full inspection. Then novelty fades and cost drops. A one-time entry fee per novel pattern, not a recurring tax. Overhead high early, trends down.
- Re-checks keep decay honest against non-stationarity. A decayed pattern gets re-sampled occasionally in case the world moved.
- Cheap or local models on high-count low-judgment roles, frontier models on judgment and high-stakes.
- Decorrelation comes mostly from different kinds of checker, not different LLMs. Large studies find model errors are substantially correlated, and that the strongest models correlate most, even across providers, so a panel of LLMs is less independent than it looks. Source decorrelation from the deterministic graph, the statistical forecaster, the human patron, and executable evidence. Treat model diversity as a minor contributor, and down-weight judges by measured entanglement so two entangled judges don't count as two independent hands.

Where it breaks.
- Decay rate is unknown and it's the whole economic model. Too fast and the system stops inspecting things that still fail (the floor drifts up in false confidence). Too slow and the entry fee never ends, overhead stays high, the cost story dies.
- Non-stationarity beats decay in the limit. If models and tasks keep shifting, re-checks have to fire often enough to catch drift, which eats the savings decay produced. This is a steady-state tension, not a solved thing.
- "Free" local models cost hardware and ops. The cheap-model lever is less free than it reads.

---

## 10. Cascade Control

Spec.
- Loops: upward flow is pull-initiated and read-only. A level reads a lower level's committed pieces when it needs them. Lower levels never push up. A downward commit never re-triggers an upward evaluation. This terminates by construction, no level can start a chain reaction in another.
- Drift: concept indicators broadcast from the source only, never relayed re-derivations. Each level commits its own pieces. A changed concept signals once from where it changed. Levels don't echo each other's interpretations back and forth.
- Escalation by ambient tally, not by push. A lower break raises a flag, and a flag is a raised hand, not a bell. It never initiates a pull. It adds to a per-concept tally the upper level watches, and attention flows to the tally, so a swell of flags draws the upper level's eye without any upward causation. The upper level still acts only on its own read, which keeps termination, and it verifies the flag against the trail before acting, real problem or false claim, which keeps decorrelation. The flag is a claim, never a verdict.
- Flag weight is blast radius times credibility times surprise, floored above zero.
  - Blast radius, how much rides on the flagging node, read off the DAG, deterministic.
  - Credibility, the flagger's record of true flags. A habitual false-flagger's weight decays.
  - Surprise, how far the flag sits from the monitored baseline. A known, watched problem flagging at its expected rate is low surprise even at high count, the roof you already put a bucket under. An orphan, breadcrumbless and conceptless, is maximal surprise, no baseline at all. A known problem flagging far above its rate is surprise again, the drip becoming a flood.
  - Floored above zero. The discount on a known problem never reaches zero, or the slow flood inside the baseline walks past.
- Surprise sensitizes, then decays. A surprising flag doesn't pull, it raises the gain on that region so the next hand there counts for more and corroboration crosses sooner. The gain decays without corroboration. A glance, a raised watch, a fade if nothing follows.
- Connectivity sets latency. A break on a known edge flags instantly along it, deterministic graph propagation, zero latency. A break with no known edge is an orphan, logged and visible, routed to genesis (Section 5), explained as fast as genesis allows. So the scheduled backward pass stops being the detector and drops to patient work, mining orphans and pruning false edges.
- Residual: fan-out cost, an optimization, not a correctness issue.

Where it breaks.
- Broadcast-from-source assumes a clean source for every indicator. When two sources change the same concept near-simultaneously, "from source only" is ambiguous about which broadcast wins.
- Threshold calibration. How high the tally must swell before attention moves is a number nobody knows yet, tuned in the loop like the catch-bonus and the decay rate.
- The severe-but-quiet problem at a structurally-trivial node gets under-weighted on blast radius and stays under threshold until it spreads and more hands go up. A latency that shrinks as the problem grows, not a permanent miss. Unless it never grows, in which case it's the floor.

---

## 11. The Minimal First Build

Spec. The smallest thing that tests the spine.
Status: built. The loop, the two-level cascade, the transfer rig, the delivery arms, and the controls ran and passed their gates in July 2026. The record lives in bench/packets and bench/DECISIONS.md. The design below stands as what it was built from, and one prediction in it came true exactly: the first probe's improvement was noise, and only the controls said so.
- One task. One Performer. One blind Audience scorer. The score plus the trace plus the standard produce one lesson. A second run consumes the lesson. I check whether the second run improved.
- Then add one two-level handoff (a Principal over two Musicians) to confirm the cascade terminates without drift.
- This exercises Section 4 (ledger), Section 5 (the lesson engine, dragged out of hand-wave), Section 10 (cascade), and gives the first read on Section 12.
- Built on my own existing stack so the engineering serves real work instead of competing with it.
- Scope discipline. Most of this document is forward design. The first build needs almost none of it. Not the landscape, not the confidence-graded menu, not the four detectors, not route prediction, not the economics. It needs the small loop and the two-level handoff, nothing more. The spec's weight is not the build's weight, and the elaborateness here is not a license to keep designing instead of building.

Where it breaks.
- "I check whether it improved" hides Section 12. On one task with one lesson, improvement could be noise. The first build can show the loop runs. It cannot yet show the loop learns. Don't confuse the two.
- The lesson engine (Section 5) is the part most likely to be a stub here. If the first build's "lesson" is hand-shaped by me rather than produced by the engine, I've tested the plumbing, not the idea. I need to be honest in the build about which it is.

---

## 12. Open research nubs (named, not specified)

These do not close on paper. They close by running, and the first two are partway closed by it.
- Score → lesson (Section 5). The common case runs: contrastive distillation with sibling widening, gated in series, applicability pinned by class, direction, and topic. Transfer evidence is bidirectional and replicated (Section 1). What the running exposed: contrast scarcity made failure supply the binding input until a third seat's breadth eased it, and the genesis remainder stands untouched, concepts that weren't there still have no source but the reference layer. Craft-shape is partly mechanized by the screens, with the unscreenable remainder still open.
- The delivery moderator (new, named by the second window). Whether the stated rule fights or extends the canonical solution shape appears to decide whether a matched lesson helps or harms a seat, and it moderated delivery inside a single interleaved run. Leading hypothesis, untested: classify tasks by idiom conflict in advance and measure the moderator directly. Alongside it, three smaller named remainders: a boundary-behavior disturbance seen once at content floor and deliberately unnamed until a designed measurement, a wildcard-pin gate gap logged as a lead for a future screen, and delivery evidence for the newly admitted production lessons, none of which has yet ridden a menu.
- Measuring learned catching (Seam 3). The signature is implemented: the discovery-latency mix computes from the run record, caught live versus caught by evidence versus clean. What running added is the discipline the signature demands: treatment claims come from pre-registered focused arms at fixed n, probes measure supply and structure only, and no signal is believed before it replicates. Four premature signals were executed under that rule and one result survived it, which is the rule working. The absolute floor stays unmeasurable, the miss silent to every detector at once, the hot stove. Open at the floor, trackable above it, and now actually tracked.

---

## How to use this document

Poke holes in the Where it breaks sections. The ones that survive get built in the order of Section 11. The nubs in Section 12 don't get argued into submission, they get run. When the build teaches me something, it lands first in bench/DECISIONS.md and the packet record, and this spec gets versioned when the lessons are load-bearing. v0.5 taught the design. The first build graded it. v0.7 records the second window: the transfer bet measured both ways and replicated, the task revealed as the delivery moderator, and the moderator named as the next open center.
