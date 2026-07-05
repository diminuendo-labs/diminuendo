# PACKET-008: Screen the field that rides, pin the topic

Status: DONE
Owner: any Claude Code session. Read /CLAUDE.md first, then this, whole.

## Goal

Close PACKET-007's two approved hands. The menu delivers concept plus
applies_when only, so the imperative screen moves to the field that rides,
and the amplifier-seat exposure gets narrowed by applicability instead of
delivery bans: the deferred rule_topic key (PACKET-005 FINDINGS 2, approved)
comes live.

## Work item 1: the concept-field shape screen

Extend the imperative screen (same pattern list, same crudeness discipline)
to the concept field, keeping the rule-field screen as is. Reject fixture:
the PACKET-006 harm lesson's concept text ("ensure that pairs are stored in
a way that disregards order"). Pass fixtures: the PACKET-005 tie and
title_words lessons' concepts. Both distiller prompts gain the matching
line: the concept states what the task requires, never how to code it.
Pinned by tests. Note the fallout pattern from PACKET-007 and handle it the
same way: any instrument store now dying at the gates is superseded, pinned,
and said plainly.

## Work item 2: the rule_topic applicability key

The stated_direction move, generalized. Tasks in probe_tasks.py gain a
rule_topic naming the thing their stated rule governs, one word from a
fixed vocabulary per class (tie_break: direction; distinctness: pairs,
values; boundary: empty, degenerate; normalize: case, whitespace,
punctuation, delimiters). Exposed in work_features. Both distiller prompts
require the lesson to pin rule_topic when its content is topic-specific,
wildcard when genuinely general. The menu's existing contradiction logic
does the rest. Pin by tests: a punctuation lesson never surfaces on a
delimiters task; a wildcard lesson rides everywhere in its class.

## Work item 3: prove it end to end, small

One contrastive generation pass per seat on the existing generation pool
(R_G=3, the standing machinery), gates at full strength including both new
screens, then report: how many candidates the new screens rejected and
why, the committed lessons quoted with their pins. No probe, no transfer
arms: this packet ships mechanism, the next measurement uses it.

## Gate

- Concept screen: fixtures pinned, both prompts updated, tests green.
- rule_topic: every task carries one, vocabulary pinned, mismatch never
  surfaces, wildcard rides, tests green.
- The generation pass ran, screen accounting reported (rejected counts by
  reason), committed lessons quoted with pins.
- Honest RESULTS and FINDINGS, commits, detached runs read from disk.

## Constraints

- Protected surfaces, tier 2: judge protocol v1, firewall, watch gates,
  lessons.jsonl, watchlist.jsonl, canonical documents. The two lesson-gate
  changes are conductor-approved and in scope.
- Do not weaken any screen to raise the lesson count. Fewer, cleaner
  lessons is the intended direction.
- If wall time forces a cut, cut the generation pass R_G, never the tests.

## FINDINGS

One tier 2 observation, evidence for a standing deferred ruling rather
than a new hand: the aim screen is now the binding screen, and it binds
against within-task phrasing specifically. All five rejections this
pass were aim-screen kills of count_token within-task candidates (both
seats, both attempts), while the sibling path's class-level phrasing
passed the same screen on the same contrast material and committed in
both seats. This is live evidence for the already-approved-and-deferred
preference for class-level phrasing (PACKET-004 FINDINGS 2 lineage),
and it is the first time the sibling machinery committed lessons in
production conditions: built in PACKET-003, stub-proven since, it fired
here as the rescue path. What I would do: nothing unilateral; when the
conductor revisits the deferred phrasing ruling, this pass is the data.

## RESULTS

Executed 2026-07-03 by a Claude Code session. Commits: bc758a9 (work
items 1 and 2), 9b56e50 (work item 3 harness), and the closing commit
carrying this section. Run 20260703-053623 ran detached start to
finish, no kill, resume unused. 122 tests green throughout.

Work item 1, delivered:
- The imperative screen now covers the concept field, the field that
  rides the menu, with the same pattern list and the same crudeness
  discipline. One inflection was added to the shared pattern
  ("stored in" beside "store in"), without which the packet's own
  reject fixture would have slipped through.
- Fixtures pinned by test: the PACKET-006 harm lesson's concept text is
  rejected verbatim; the PACKET-005 tie and title_words concepts pass
  verbatim. Both distiller prompts carry the matching line, pinned by
  the prompt-capture test.
- Fallout, checked the PACKET-007 way: no further instrument store dies
  at the new screen. The PACKET-004 delivery store and the PACKET-006
  store A load clean; store B was already superseded at the rule-field
  screen. The full suite pins all of it.

Work item 2, delivered:
- Every task in probe_tasks.py (31: the full generation and apply
  candidate pools) carries rule_topic, one word from the fixed
  per-class vocabulary in RULE_TOPICS (tie_break: direction;
  distinctness: pairs, values; boundary: empty, degenerate; normalize:
  case, whitespace, punctuation, delimiters). Vocabulary and coverage
  pinned by test.
- rule_topic rides work_features in every generation-side harness, both
  distiller prompts require pinning when topic-specific and wildcard
  when general, and the menu tests pin both directions: a punctuation
  lesson never surfaces on a delimiters task, a wildcard lesson rides
  every topic in its class. The PACKET-006 pairing-3 mismatch
  (punctuation lessons on an underscores task) is now unservable by
  construction.

Work item 3, what ran (genpass 20260703-053623, R_G=3 per task per
seat, both seats, full gates, 48 runs checkpointed, GATE passed):
- Contrast accounting. Seat A: both tie_break siblings mixed, two
  within-task lessons; normalize count_token mixed, within-task
  distillation rejected at the gates, sibling contrast (count_token
  failing, title_words passing) committed on retry; distinctness and
  boundary all_pass, nothing broke. Seat B: both tie_break siblings
  all_fail for the third consecutive run, no passing partner, no
  lesson; distinctness count_distinct_pairs mixed, one within-task
  lesson; normalize the same sibling rescue as seat A; boundary
  all_pass.
- Screen accounting: five rejections, every one aim_screen, every one
  a count_token within-task or first sibling attempt. Zero imperative
  rejections and zero platitudes: the strengthened prompts appear to
  teach shape upstream, at one pass of evidence.
- The five committed lessons, quoted with their pins:
  1. A, max_index, within-task. Concept: "When the task states to
     return the index of the last occurrence of the largest value,
     ensure your function follows this direction." Rule: "if the
     largest value appears more than once, return the index of its
     last occurrence." Pins: rule_class=tie_break,
     rule_topic=direction, stated_direction=last.
  2. A, shortest_word, within-task. Concept: "When the task states to
     return the last word in case of a tie, prioritize returning the
     last word among those with the shortest length." Rule: "If there
     are multiple words with the same minimum length, follow the
     direction the task states by returning the last such word." Pins:
     tie_break, direction, last.
  3. A, count_token, SIBLING (vs title_words). Concept: "When a task
     states that you should normalize or strip certain elements (like
     punctuation), always follow the stated direction before
     proceeding with the core operation." Rule: "Follow any stated
     direction for normalization (e.g., removing leading/trailing
     punctuation) when processing input strings in your function."
     Pins: normalize, punctuation.
  4. B, count_distinct_pairs, within-task. Concept: "When the task
     states that distinct pairs should be counted, ensure that each
     pair is unique regardless of how many times its values repeat in
     the input list." Rule: "Follow the direction the task states to
     count distinct unordered value pairs only once." Pins:
     distinctness, pairs.
  5. B, count_token, SIBLING (vs title_words). Concept: "When the task
     states to normalize text, follow the stated direction for
     handling punctuation." Rule: "Follow the direction the task
     states regarding punctuation normalization." Pins: normalize,
     punctuation.

Findings, sized to what a supply pass can claim:
This packet ships mechanism, and the mechanism held end to end: five
lessons, every one conditionally phrased, declaratively shaped, and
topic-pinned, with the direction pin on both tie lessons. The two new
screens rejected nothing that deserved to live and the aim screen did
all the gatekeeping, concentrated on one task's within-task phrasing,
where the sibling path then delivered its first live commits in both
seats. llama's tie_break all_fail is now three runs consistent, so
tie-lesson supply still comes only from qwen at this pool difficulty.
No treatment claim is made or implied; the next measurement uses these
stores.

Repository note: a v0.6 technical spec draft was present untracked
during this packet. It was swept into the first commit by a git add
-A, caught immediately, and removed by a soft reset before anything
else happened; the recommit (bc758a9) carries only packet files, and
the conductor later committed the spec as canon (cdee935). Explicit
per-path staging from that point on.

Fixed under tier 1: the "stored in" inflection gap in the new screen,
found because the packet's own fixture demanded it, fixed and pinned
before the fixture test was ever green.

NOT done:
- Nothing cut: R_G=3 ran in full on both seats, all tests written.
- Protected surfaces beyond the two approved gate changes: untouched.
- Not attempted: any treatment measurement (explicitly out of the
  packet's scope), and any change to within-task phrasing (FINDINGS,
  the conductor's standing deferred ruling).
