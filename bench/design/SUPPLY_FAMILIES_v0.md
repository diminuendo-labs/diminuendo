# SUPPLY FAMILIES v0 (draft for Brad's teardown, not yet a packet)

The supply instrument: graded task families, one instrument for every
seat, current and future. Each family is a single stated-rule task
with a difficulty dial, authored seat-blind. Calibration finds each
seat's mixed band by sweeping the dial bottom-up with bare none cells,
the standing qualification bar unchanged. The instrument is universal;
the operating point is per-seat and always measured, never assumed.
This is the eye-chart principle: same chart on the wall for every
patient, the output is where your rows blur.

Every family carries at authoring time: pins (rule_class, rule_topic),
the stated rule, the canonical shape and its named relationship to the
rule (conflicted or separable, the moderator criterion's input), a
census taxonomy, the dial with its rungs, and the check pattern (rule
checks plus watch checks). Nothing in any family names a model.

## The calibration procedure (one procedure, any seat)

For a target seat: sweep each family from rung 1 upward, none cell at
R=12 per rung, no tools, census on, canonical unrunnable-as-fail
accounting. Stop the family for that seat at its first rung that
qualifies mixed at the standing fraction; that (family, rung) pair
enters the seat's kept pool. A family whose rungs exhaust unmixed
records the seat's floor or ceiling on it and keeps nothing. Kept
pools are per-seat by measurement. New model arrives: run the same
sweep, nothing gets respecced.

## Family 1: chunk_pad (boundary/degenerate, FIGHTS candidate)

Rule: split a list into chunks of size k; a final short chunk is
padded with None to exactly k. Canonical shape: the range-step
comprehension, which naturally leaves the tail short; the pad rule
must change the chunk expression itself, conflicted. Census taxonomy:
range-step comprehension, explicit loop-with-pad, other, unrunnable.
Dial: rung 1, inputs are exact multiples of k plus one ragged tail;
rung 2, ragged tails throughout plus k larger than the list; rung 3,
rung 2 plus empty list and k equal to 1 degenerates in the same check
set. Rule checks probe the padded tail; watch checks probe an exact
multiple and the empty list.

## Family 2: merge_within (boundary/degenerate, FIGHTS candidate, and
the conflict-magnitude instrument)

Rule: merge ranges that overlap or sit within distance d of each
other, d stated in the task text. Canonical shape: the sort-and-sweep
with the overlap comparison; any d above zero changes the comparison
inside the sweep. The dial IS the conflict magnitude, the graded
instrument logged 2026-07-04: rung 1, d=0, pure idiom, no conflict, a
control rung; rung 2, d=1, the P022 touch conflict, one token; rung
3, d stated as a parameter with mixed values across checks, the rule
living further from the idiom. Census taxonomy: sort-and-sweep,
pairwise-other, unrunnable. Rule checks probe d-dependent merges;
watch checks probe plain overlap and the empty list. This family
doubles as the moderator's magnitude probe: if the moderator is real
and graded, armed harm should grow with the rung.

## Family 3: safe_stats (boundary/degenerate, EXTENDS candidate)

Rule: a small statistic (trimmed mean: drop one min and one max, then
average) with stated degenerate handling: empty and one-element and
two-element lists return None. Canonical shape: sort, slice, average;
the degenerate guards are separable prepended steps. Census taxonomy:
sort-slice-average, loop-accumulate, other, unrunnable. Dial: rung 1,
degenerates limited to empty; rung 2, all three degenerate sizes in
the check set; rung 3, rung 2 plus all-equal values where the trim is
ambiguous and the rule states the resolution. Rule checks probe the
degenerates and the trim; watch checks probe a plain well-formed list.

## Family 4: collapse_delims (normalize/delimiters, FIGHTS candidate)

Rule: split a string on any of a stated set of delimiters, collapsing
runs, dropping leading and trailing empties, and the output rejoins
with a single canonical delimiter. Canonical shape: single-character
split, which mishandles mixed delimiters and produces empties; the
rule forces either a pre-normalization or a character walk, so at
mixed-delimiter rungs the plain split is the conflicted shape. Census
taxonomy: single-split, multi-split-or-regex, char-walk, other,
unrunnable. Dial: rung 1, one delimiter type with runs; rung 2, two
delimiter types mixed; rung 3, three types plus leading and trailing
runs plus the empty string. Rule checks probe mixed runs and edges;
watch checks probe the single-delimiter clean case.

## Family 5: token_case (normalize/delimiters, EXTENDS candidate)

Rule: convert delimited tokens to a stated case convention (first
token lower, rest capitalized), where tokens appearing in a stated
exception list keep their exact given form. Canonical shape: the
split-capitalize-join; the exception handling is a separable lookup
step around the intact join. Census taxonomy: split-capitalize-join,
regex, char-walk, other, unrunnable. Dial: rung 1, no exceptions in
inputs, the list merely stated; rung 2, one exception appearing
mid-token-stream; rung 3, exceptions at first position, colliding
with the first-token-lower rule, resolution stated in the task text.
Rule checks probe exception preservation and the collision; watch
checks probe the plain conversion.

## Family 6: kth_ordered (tie_break/direction, breadth and the G1 lane)

Rule: return the k-th item under a stated ordering where ties break
by a stated secondary direction that differs from stable-sort
default. Canonical shape: sorted with a single key; the stated tie
direction changes the key or demands a compound key, conflicted.
Census taxonomy: single-key-sort, compound-key-sort, manual-scan,
other, unrunnable. Dial: rung 1, no ties in inputs, a control rung;
rung 2, one tie pair at the k-th position; rung 3, dense ties and k
inside a tie run. Rule checks probe tie positions; watch checks probe
the no-tie case. This family also stocks ground for gap G1, the
directive-collapse second-task replication, which needs a
tie-directional task the seat otherwise aces.

## Calibration priority when this becomes a packet

The gaps rank the sweeps: mistral first (G2, the trait's second cell,
and G3, the second transfer pair, both need qualified mistral
ground), qwen second (the moderator retest needs census-concentrated
mixed ground), llama third (its pool holds the only two current
qualifiers, least starved). Wall-time bound: complete a seat's whole
sweep before starting the next seat; a finished seat's kept pool
stands alone. Worst case per seat at six families and three rungs is
18 none cells, 216 runs, and the expected case is far smaller because
each family stops at its first mixed rung.

## What this document is not

Not a packet, not canon, not run. It is the conductor's authored
draft for Brad's teardown. The rungs, the named conflicted shapes,
and the taxonomies are analytic claims of exactly the species the
census corrected once already, and calibration measures them rather
than trusts them. Nothing here names a model, and the audition
firewall applies from birth: these families are audition and
qualification ground, permanently held out of the lesson-generation
pool.
