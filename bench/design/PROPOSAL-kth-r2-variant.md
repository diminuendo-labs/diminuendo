# PROPOSAL: kth_ordered rung 2 input variant (G1's last attempt)

Status: PENDING BRAD'S SIGN-OFF. Nothing below lands until he rules.
This is a canonical-adjacent change to the committed supply
instrument, conductor-and-Brad work per document discipline, never a
packet's.

## What changes and why

One input string. Rung 2's scored check moves from
kth_ordered(['aa', 'bb', 'c'], 2) to kth_ordered(['bb', 'ab', 'c'],
2). The old input's tie pair is encountered in ascending alphabetical
order, which makes last-encountered coincide with
reverse-alphabetical-first, so the stated rule and the P004-mechanism
directive give the same answer and G1's collapse design cannot use
the rung (proven at P028's gate). The variant lists the tie pair
descending, the directions separate, and the rung keeps everything
else: one tie pair at the k-th position, the same task text, and the
same canonical answer 'bb' under the stated rule.

This is the pre-registered LAST G1 attempt. If its packet walls, the
writeup proceeds with property 2 at its true size, per the program
exit in DECISIONS.

## Desk proof, the committed instrument, verbatim

OLD (current rung 2): input ['aa', 'bb', 'c']
  rule order      ['c', 'bb', 'aa'] -> k=2 'bb'
  directive order ['c', 'bb', 'aa'] -> k=2 'bb'
  SEPARATES: False
NEW (variant): input ['bb', 'ab', 'c']
  rule order      ['c', 'bb', 'ab'] -> k=2 'bb'
  directive order ['c', 'ab', 'bb'] -> k=2 'ab'
  SEPARATES: True
canonical expectation under the stated rule: 'bb' both, unchanged.

## The exact diffs, ready to land on Go

### 1. bench/supply_families.py, two lines inside the rung 2 entry

Line 493:
  OLD: {"call": "kth_ordered(['aa', 'bb', 'c'], 2)",
  NEW: {"call": "kth_ordered(['bb', 'ab', 'c'], 2)",
  (the "expect": "'bb'" line beneath it is unchanged)

Line 499:
  OLD: "rule_checks": ["kth_ordered(['aa', 'bb', 'c'], 2)"]},
  NEW: "rule_checks": ["kth_ordered(['bb', 'ab', 'c'], 2)"]},

Nothing else in the module moves: the task text, rungs 1 and 3, the
pins, the census classifier, and CONTROL_RUNGS are all untouched.

### 2. bench/tests/test_directive28.py, three touch points

test_rule_order_matches_the_family_reference: the rung 2 assertion
re-derives from the NEW committed input (['bb', 'ab', 'c'] at k=2
gives 'bb'), keeping the test true to its name.

test_rung2_input_coincides: its premise inverts. It becomes two
tests: test_old_rung2_input_coincides pins the historical fact on
['aa', 'bb', 'c'] with a comment naming it the input that walled
P028 (the instrument-level record of why the variant exists), and
test_rung2_committed_input_separates pins that the NEW committed
rung 2 rule check separates (rule 'bb', directive 'ab').

test_directive_order_prefers_later_encountered and
test_gate_logic_can_pass_on_separating_input: unchanged, they test
the instrument, not the family pin.

### 3. bench/design/SUPPLY_FAMILIES_v0_1.md, the version bump

The lesson is load-bearing, so the design document versions: v0
stays on disk untouched (P026's calibration reads against it), and
v0_1 is the copy with two amendments to Family 6: the dial line for
rung 2 gains "tie pair listed against the stated direction" and the
section gains one sentence: "Scored tie inputs must not list ties in
the encounter order that coincides with the stated tie direction, or
the rung cannot serve the G1 lane; rung 2's original input taught
this at the cost of a packet."

### 4. bench/DECISIONS.md, the historical annotation on landing

Qwen kth_ordered rung 2's 10 of 12 (P026) is annotated old-input
historical: the nearest prior for the variant rung, favorable but
not a qualification, since the input changed. The variant rung is
unmeasured until a packet's fresh stage A, per candidacy doctrine.

## What the change does NOT do

It does not touch rung 2's difficulty structure (one tie pair at
the k-th position, canonical answer unchanged), does not touch any
other family or rung, does not touch the census classifier, and does
not qualify anything: the G1 packet's stage A gate still decides,
now betting with a neighbor prior instead of against a void.

## On Go

The conductor lands items 1 through 4 in one commit with tests
green, then cuts PACKET-033, the G1 last attempt: the P030 symmetric
forms design re-grounded on variant rung 2, the 18-of-24 high
baseline gate carrying the same 12-run price, VOID and observability
doctrine as written there.
