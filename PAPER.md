# The chair holds the memory

## Lessons that move between AI models, and the delivery form that decides whether bad advice is survivable: measurements from a small reproducible bench

Brad Hunt, Diminuendo LLC. July 2026. Code, tests, and every run
record cited below live in this repository; everything marked
measured traces to them.

DOI: https://doi.org/10.5281/zenodo.21212666

Here is the finding in plain terms. Take one piece of advice and
hand it to a small AI model two ways. Phrased as a command, the
model obeys it even when it contradicts the task, and work the model
does correctly on its own collapses. Phrased as an option on a menu,
the identical bytes cause no harm anywhere: the model uses what fits
and declines what does not. Same advice, same model, same task. The
framing alone decides whether bad advice is survivable, and I
measured it, on two tasks and two model families, with executable
checks. This document is that measurement, the system it came from,
and the record that lets you rerun it on a consumer machine.

A word on the name. Diminuendo is the musical mark for growing
quieter, and that is the whole job. The system does not try to catch
the last error. It resolves every disharmony it can so the noise
floor drops, until the one error it could not catch clears the floor
and becomes audible to the person outside the room. Quiet the
orchestra until the off-note is findable. That frame is what the
rest of this hangs on.

## What I built

I run a small research bench that asks one question about AI agents:
when a lesson has to move from one model to another, what carries
it? My answer is the chair, not the model. Diminuendo treats every
model as a musician who sits down, plays, and leaves. A seat is a
position in the system a model occupies, and the memory stays with
the seat: distilled lessons in a store, served through a menu (the
delivery path that offers lessons as tools beside a task), gated by
pins (stated applicability conditions a lesson must match before it
reaches the prompt). The larger bet is that you compete on catching
failure, not on model intelligence. What this document evidences is
the layer under that bet: chair memory works, and delivery form is a
measured variable. The catching-failure loop itself is designed and
instrumented, not yet proven; that status is stated plainly in Where
it breaks.

This is a concept plus a first build, not proof. The seams close by
running, and what has run is in the bench record. Everything below
marked measured traces to that record or it does not get said.

The claim of this document, stated once so the rest can be checked
against it: the assembled system is the first of its kind. I rest
that priority on the public record, not on assertion: the dated
bench artifacts in this repository and this document's archival DOI
(10.5281/zenodo.21212666). The full development history behind those
dated artifacts is available to referees on request. A hostile
prior-art sweep (July 2026) found every ingredient published
somewhere, and the assembly published nowhere in the academic record or, per an
extended sweep of shipped open-source projects, in the OSS space,
with the claim sized to the sweep's reach: role-persistent chair
memory across swappable models, break-mined gated lessons, form-safe
menu delivery, per-model casting (choosing which model to seat for a task), and the measurement discipline, in
one running system with the instrument that measures it. The
neighbors are cited by name in Related Work below, because the
second thing this document claims, the delivery finding, survives on
a thin margin in a valley that is filling in monthly, and the honest
way to hold thin ground is to name every neighbor and build exactly
where they are not.

## The finding: form is the variable

Take one lesson and hand it to a model two ways. As a menu tool, an
approach offered beside the task. As a directive, a rule commanded.
Same content. The forms behave differently, and the difference is
the safety story.

Measured on two tasks and two model families. Each measured
condition is a cell: one task by one seat by one delivery form, at n
runs. In the first cell a llama seat took a lesson whose tie
direction contradicted the task's stated rule. Commanded as a directive, the seat cratered the
contradicted tie check from 0.33 to 0.09 evidence fraction (the
share of a run's checks that pass, scored by executable code, the
blind listener that hears only the output), and the damage spread: the
task's non-tie checks fell from 0.92 and 0.67 to 0.36. Offered as a
menu tool, the identical content hurt nothing on any of the seven
checks measured, and the contradicted tie check rose from 0.33 to
0.75. The menu arm never read below the bare baseline anywhere. The
seat kept the task's stated rule, declined the contradicting
direction, and did better with the tool present than without it,
which is a stronger sentence than the one I first wrote here: the
menu did not sit inert, it preserved the seat's judgment.

In the second cell, on a fresh task and a different family, a qwen
seat read 11 of 12 runs correct bare, 12 of 12 with the identical
byte-checked lesson in menu form, and 7 of 12 under the directive
form, with the damage again reaching a check the directive did not
contradict. Counts in runs; the counters differ across the two eras,
so the cross-cell comparison is direction, not magnitude. One seat
per task, n=12 runs per cell, small numbers stated as directions.

The nearest published neighbor measures something else. Szeider
(arXiv 2603.01254) isolates framing of a task-irrelevant tool and
reads self-reported aversion, with per-model splits; instruction
hierarchy work (Wallace et al., arXiv 2404.13208) trains models to
rank conflicting instructions; instructional-distraction work
(DIM-Bench, arXiv 2502.04362) shows models obeying embedded
instructions against the task. None isolates delivery form of
byte-identical guidance as the only variable, and none reports the
asymmetry above: wrong guidance collapses performance when
imperative and is harmless when optional, under executable checks.
That asymmetry is this bench's contribution, and it is the exact
experiment the field's own diligence recommends running next.

## Exhibit: the lesson and the two framings

The committed lesson that rode both collapse designs, quoted
verbatim from the production store with its pins:

    "concept": "When handling ties in the task, always return the
    last word with the shortest length.",
    "applies_when": {"operation": "write_code", "target":
    "function", "language": "python", "size": "small", "rule_class":
    "tie_break", "rule_topic": "direction", "stated_direction":
    "last"}

The two framings the model actually sees, from the committed prompt
builder. Menu form:

    APPROACHES available to you (choose what fits):
    - {"concept": "...", "applies_when": {...}}

Directive form:

    APPLY THESE RULES:
    - When handling ties in the task, always return the last word
      with the shortest length.

Same bytes ride both. The framing is the only variable, and the
framing is what decides whether a wrong lesson is survivable.

## Three properties, kept apart on purpose

The phrase menu safety hid three different claims until the bench
forced them apart. I keep them named.

Property 1, path refusal. The production menu refuses to serve a
lesson whose stated conditions contradict the task. Structural,
proven from committed code and reproduced at every packet cut since (a packet is one scoped unit of bench work, its readings fixed before the run).
On pinned contradicting content the exposure cannot occur. The
structural idea has a published neighbor: Membrane (arXiv
2606.05743) pairs blocking and permitting conditions on safety
memory and proves the gate is what blocks harm, in jailbreak
defense. What this bench claims is the craft-lesson instantiation:
conditions carrying rule class, stated direction, and rule topic on
advice rather than attacks, refusing a wrong-direction lesson before
it reaches a working seat.

Property 2, form response. When contradicting content reaches a
model in menu form anyway, the model does not obey the
contradiction. Behavioral, measured on two tasks and two families.
In the first cell the seat declined the wrong direction and improved
beside the tool; in the second, injection reproducing the production
emission byte for byte read 12 of 12 with no drop of any size. This
property prices the known hole in property 1: a contradiction the
pin vocabulary cannot express sails past the refusal, and the
model's own form response is the layer behind it.

Property 3, collateral cleanliness. Delivered lessons that do apply
move nothing unrelated. Five consecutive clean measurements on
non-contradicting content.

None of the three substitutes for another. A system that reports
them as one number is hiding which layer failed.

## Seats respond differently, and that is castable

The same delivery instrument reads differently per model. My llama
seat filters: it takes matched tools and declines mismatched
directions. My qwen seat amplifies, leaning into whatever tool it is handed. My mistral seat has read
indifferent in two cells, one cross-origin and one self-origin, with
one early gain that failed replication and is filed as exactly that.
The measurement has published parents and a frontier-scale echo: the
Gain/Harm decomposition (Ma et al., arXiv 2602.01334) counts what a
tool fixes against what it breaks per model, and VisualNeedle
(arXiv 2605.26380) finds the same amplify-versus-filter split across
frontier families. That corroboration is a gift: independent groups
at scale this bench cannot afford confirm the trait reads true. What
this bench claims is the step neither paper takes: measuring the
trait per seat, before seating, and using it to set the delivery
policy for that chair. Seat response to tools is a casting trait you
measure, not a property you assume from a benchmark.

## Transfer, sized honestly

Lessons distilled from one model family change the output of
another. On my bench that replicated in both directions, at parity
with hand-authored content, at small n. The 2026 literature says the
field has the same ingredient: cross-model memory transfer (arXiv
2604.14004), Rosetta Memory (arXiv 2606.07711), ExpGraph (arXiv
2605.30712), and the MemAgents workshop framing (ICLR 2026) all
confirm that distilled experience moves between
models. I state
my transfer results as consistent with that field, sized to my n.
Nothing here claims a first on transfer. This work stands on what
the field has not published: the delivery science. Which form carries a
lesson safely, measured at byte identity. Which seats amplify,
filter, or sit indifferent, measured as traits. Where the serving
path refuses, proven from code. And an instrument that produces
those answers on a schedule.

## Related work, with dates

A hostile prior-art sweep ran before this document froze, built to
kill each claim, and its map is reproduced here so a reader can
check the claims against the neighborhood. MemCollab (arXiv
2603.23234) distills cross-model memory from contrastive
trajectories and reports that naive cross-model reuse can degrade a
seat, which is the hazard the form finding above prices and the menu
form survives. Membrane (arXiv
2606.05743, June 2026) publishes conditional gating of safety memory
as the harm-blocking mechanism, and published first; this bench
claims the craft-lesson instantiation. Szeider (arXiv 2603.01254,
March 2026)
is the closest method neighbor to the form finding, with a different
dependent variable and no wrong-guidance result. Ma et al. (arXiv
2602.01334, February 2026) and VisualNeedle (arXiv 2605.26380, May
2026) publish the Gain/Harm measurement and the per-family split;
this bench claims the per-seat policy step. Wallace et al. (arXiv
2404.13208, 2024) and DIM-Bench (arXiv 2502.04362, 2025) anchor
instruction hierarchy and instructional distraction. SkillOpt (arXiv
2605.23904) and the ExpeL and Reflexion lineage cover gated skill
distillation; the exact gate series here (declarative shape
enforced, imperative phrasing rejected, aim matched to the failing
check) is claimed as an engineering contribution, not a discovery.
MonoScale (2026) covers onboarding batteries; the one-way audition
firewall, audition tasks permanently outside the lesson pool and the
system never optimizing toward audition metrics, is claimed as
architecture. Springdrift (arXiv 2604.04660) is the closest partial
assembly and lacks casting and form-safe delivery. Where this
bench's measurements predate or parallel these works, the packet
dates in the public record say so; where they follow, the citation
says that instead.

## Run it yourself

The record is the argument, so it ships with the code. Three seats,
all local Ollama on one consumer Windows machine: qwen2.5-coder:7b,
llama3.1:8b, mistral:7b. Python 3.14, invoked as py. The repo layout
that matters: bench/packets/ holds every work packet with its
pre-registered readings and appended RESULTS; bench/DECISIONS.md is
the ruling log, corrections included; bench/runs/ holds every run's
persisted rows, summaries, and logs, committed. Each packet names
its harness, and a cell reproduces from the bench directory with the
harness's staged commands, for example: py directive33.py build,
then its run stage, artifacts landing in bench/runs. The suite runs
with py -m unittest discover -s tests. Every claim above has a
packet, and every packet has rows on disk you can recount without
trusting me.

## The instrument is the product of the method

The bench runs one discipline end to end. Readings are
pre-registered before any run and applied verbatim after. No signal
is believed before it replicates, and premature leads get downgraded
in the record where they were made, mine included. Every packet's
claims are verified against the run artifacts on disk, never against
the session's account. The same evening this paper's central result
landed, the same machinery buried a promising gain three hours
earlier because its replication came back flat. The machine that
killed the result I liked is the machine vouching for the one I am
publishing.

The dead ends are part of the finding. Reaching the second collapse
measurement took four packets: two closed at deterministic desk
checks for zero model runs, one closed at a measured gate for
exactly the twelve runs it priced, and the fourth landed. The walls
were supply facts, each one mapped, and the fixes are now standing
doctrine. If you want the negative space, it is in the record too.

## Where it breaks

The catching-failure thesis, the project's larger bet, is designed
and instrumented but unproven: the loop that turns caught failures
into lessons at production scale is the open half, and this document
does not claim it. The mechanism behind the directive collapse is
observed only descriptively (the census, a deterministic classifier
that reads each output's solution shape rather than its correctness,
shows the seat abandoning its compound strategy in a quarter of the
collapse cell's runs) and is not claimed. Effects at this model scale are real, check-local,
and small: they vanish inside coarse means, which is why the
readouts are per-check. The trace is a strong signal, not a clean
one. The production path's refusal is proven only where pins can
express the contradiction. Every number above is one seat per cell
at n=11 or 12: directions, not rates, and replication here means a
second task on a second family under pre-registration, not a
population claim. The next tier needs more seats, more tasks, and
larger n, and the bench is built to buy them one packet at a time.

The musician will keep playing wrong notes. That was always the
assumption. The work is everything else in the room going quiet
enough that the person outside it can hear which note fell, and who
played it.

Diminuendo is a project of Diminuendo LLC (Arizona). The code and
record publish under AGPL-3.0-or-later; commercial licenses are
available from the LLC, contact via the diminuendo-labs organization
on GitHub.
