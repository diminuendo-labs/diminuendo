"""PACKET-028: the directive replication, gap G1, second task. This
module carries the packet's two build gates; nothing here calls a
model. The contradiction gate is deterministic: for each rule check
input of kth_ordered rung 2 it derives the answer under the stated
rule (reverse-alphabetical among equal lengths) and under the
directive's direction (later-encountered among equal lengths), prints
both, and passes a candidate only when at least one rule check's
answers differ. Candidates in the packet's order: the production tie
lesson at line 4 (shortest_word), fallback line 5 (longest_run_char),
both carrying stated_direction last. If both fail, the packet closes
uncut and the conductor re-cuts; this harness stops, it does not
reinterpret.

Run the gate: py directive28.py gate"""

import ast
import json
import os
import sys

import supply_families as sf

_BENCH = os.path.dirname(os.path.abspath(__file__))
LESSONS_PROD = os.path.join(_BENCH, "lessons.jsonl")

GROUND_FAMILY = "kth_ordered"
GROUND_RUNG = 2

# Candidate content in the packet's order: (production line, gen_task).
CANDIDATES = ((4, "shortest_word"), (5, "longest_run_char"))


def load_candidate(prod_line, gen_task):
    """The candidate lesson from its production line, position
    asserted, rule sentence returned byte-verbatim for printing."""
    with open(LESSONS_PROD, "rb") as f:
        lines = [l for l in f.read().split(b"\n") if l.strip()]
    if prod_line > len(lines):
        raise SystemExit(f"production store has {len(lines)} lines, "
                         f"candidate names line {prod_line}")
    obj = json.loads(lines[prod_line - 1])
    trail = obj.get("trail") or {}
    if trail.get("gen_task") != gen_task:
        raise SystemExit(f"line {prod_line} carries gen_task "
                         f"{trail.get('gen_task')}, the packet names "
                         f"{gen_task}")
    return {"prod_line": prod_line, "gen_task": gen_task,
            "rule": obj["rule"], "concept": obj["concept"],
            "stated_direction": obj["applies_when"]
            .get("stated_direction")}


def rule_order(words):
    """The stated rule: increasing length, reverse-alphabetical among
    equal lengths."""
    return sorted(sorted(words, reverse=True), key=len)


def directive_order(words):
    """The directive's direction: increasing length, later-encountered
    first among equal lengths (the positional-last preference ranks
    the later-encountered word ahead of its tie partners)."""
    indexed = sorted(enumerate(words), key=lambda p: -p[0])
    ordered = sorted(indexed, key=lambda p: len(p[1]))
    return [w for _, w in ordered]


def kth(order, k):
    return order[k - 1] if 1 <= k <= len(order) else None


def _parse_call(call):
    node = ast.parse(call, mode="eval").body
    words = ast.literal_eval(node.args[0])
    k = ast.literal_eval(node.args[1])
    return words, k


def derivations():
    """Both derivations for every rule check of the ground rung.
    Deterministic, the conductor's replay surface."""
    rung = sf.get_rung(GROUND_FAMILY, GROUND_RUNG)
    out = []
    for call in rung["rule_checks"]:
        words, k = _parse_call(call)
        r_ord = rule_order(words)
        d_ord = directive_order(words)
        r_ans = kth(r_ord, k)
        d_ans = kth(d_ord, k)
        out.append({"call": call, "words": words, "k": k,
                    "rule_order": r_ord, "rule_answer": r_ans,
                    "directive_order": d_ord, "directive_answer": d_ans,
                    "differs": r_ans != d_ans})
    return out


def contradiction_gate():
    """The packet's build gate, run per candidate in order. The
    derivation depends only on the directive's direction, which both
    candidates state as last; each candidate is still evaluated and
    printed on its own line with its rule sentence."""
    derivs = derivations()
    results = []
    for prod_line, gen_task in CANDIDATES:
        cand = load_candidate(prod_line, gen_task)
        if cand["stated_direction"] != "last":
            raise SystemExit(f"line {prod_line} stated_direction is "
                             f"{cand['stated_direction']}, the gate "
                             f"derivation presumes last")
        passes = any(d["differs"] for d in derivs)
        results.append({"candidate": cand, "derivations": derivs,
                        "passes": passes})
    return results


def main():
    print(f"PACKET-028 CONTRADICTION GATE (build stage, no model): "
          f"{GROUND_FAMILY} rung {GROUND_RUNG}")
    rung = sf.get_rung(GROUND_FAMILY, GROUND_RUNG)
    print(f"rule checks (the standing annotation): "
          f"{rung['rule_checks']}")
    results = contradiction_gate()
    for res in results:
        c = res["candidate"]
        print(f"candidate line {c['prod_line']} ({c['gen_task']}, "
              f"stated_direction {c['stated_direction']}):")
        print(f"  rule sentence (the would-be directive text, "
              f"byte-verbatim): {c['rule']}")
        for d in res["derivations"]:
            print(f"  {d['call']}:")
            print(f"    stated rule (reverse-alphabetical among equal "
                  f"lengths): order {d['rule_order']} -> "
                  f"{d['rule_answer']!r}")
            print(f"    directive direction (later-encountered among "
                  f"equal lengths): order {d['directive_order']} -> "
                  f"{d['directive_answer']!r}")
            print(f"    DIFFERS: {d['differs']}")
        print(f"  GATE: {'PASSES' if res['passes'] else 'FAILS'}")
    if not any(r["passes"] for r in results):
        print("BOTH CANDIDATES FAIL THE CONTRADICTION GATE: the packet "
              "closes uncut per its own pre-registration, no store is "
              "selected, no model run happens, the conductor re-cuts.")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
