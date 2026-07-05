"""PACKET-029: the directive replication re-cut, gap G1, kth_ordered
rung 3. This module carries the packet's build stage; the sequence it
enforces is the packet's own: the contradiction gate first, then
candidate selection and the byte check with line position, then the
delivery-path check that stage B's menu cell presumes. Nothing here
calls a model.

The contradiction gate reuses the PACKET-028 derivation instrument
unchanged, imported not copied, pinned by identity test: for each rule
check input of kth_ordered rung 3, both derivations print, and the
gate passes a candidate when at least one rule check's answers differ.
Rung 3 separates on both scored k values, proven twice before this cut.

The delivery-path check is where this packet's build stage found its
stop: the menu cell requires the selected lesson served through the
production menu path at tools=1 every row, and the production menu's
contradiction logic (PACKET-005 and 008, a protected surface) refuses
a stated_direction last lesson on ground whose features state
reverse_alphabetical. The check prints the refusal beside a matched-
ground control proving the refusal is the pin firewall, not a loading
defect. Per the tier rules the discovery is flagged, never fixed:
bypassing it would be a pin change or a menu change, both forbidden.

Run the build stage: py directive29.py build"""

import json
import os
import sys

import menu
import supply_families as sf
from directive28 import (derivations as _p028_derivations,
                         directive_order, kth, load_candidate,
                         rule_order)
from probe_tasks import FEATURES

_BENCH = os.path.dirname(os.path.abspath(__file__))
LESSONS_PROD = os.path.join(_BENCH, "lessons.jsonl")
STORE = os.path.join(_BENCH, "packets", "PACKET-029-lesson_tie.jsonl")

GROUND_FAMILY = "kth_ordered"
GROUND_RUNG = 3
STORE_PROD_LINE = 4
STORE_GEN_TASK = "shortest_word"

# The packet's candidate order, as in PACKET-028.
CANDIDATES = ((4, "shortest_word"), (5, "longest_run_char"))

# The census classifier this packet's cells would use, unchanged from
# supply_families, pinned by identity test. No cell runs in this
# packet; the pin documents what stage B would have consumed.
CENSUS_SHAPE = sf.census_shape


def _features():
    return {**FEATURES, **sf.FAMILIES[GROUND_FAMILY]["pins"]}


def derivations():
    """Both derivations for every rule check of rung 3, using the
    PACKET-028 instrument's functions on this rung's annotation."""
    import ast
    rung = sf.get_rung(GROUND_FAMILY, GROUND_RUNG)
    out = []
    for call in rung["rule_checks"]:
        node = ast.parse(call, mode="eval").body
        words = ast.literal_eval(node.args[0])
        k = ast.literal_eval(node.args[1])
        r_ord = rule_order(words)
        d_ord = directive_order(words)
        out.append({"call": call, "words": words, "k": k,
                    "rule_order": r_ord, "rule_answer": kth(r_ord, k),
                    "directive_order": d_ord,
                    "directive_answer": kth(d_ord, k),
                    "differs": kth(r_ord, k) != kth(d_ord, k)})
    return out


def contradiction_gate():
    """The packet's first build gate, candidates in order, stopping at
    the first that passes."""
    derivs = derivations()
    results = []
    for prod_line, gen_task in CANDIDATES:
        cand = load_candidate(prod_line, gen_task)
        passes = any(d["differs"] for d in derivs)
        results.append({"candidate": cand, "derivations": derivs,
                        "passes": passes})
        if passes:
            break
    return results


def byte_check():
    """The selected lesson's packet-local store byte-identical to its
    production line, position asserted."""
    with open(LESSONS_PROD, "rb") as f:
        lines = [l for l in f.read().split(b"\n") if l.strip()]
    src = lines[STORE_PROD_LINE - 1]
    obj = json.loads(src)
    if (obj.get("trail") or {}).get("gen_task") != STORE_GEN_TASK:
        raise SystemExit(f"line {STORE_PROD_LINE} is not the "
                         f"{STORE_GEN_TASK} lesson")
    with open(STORE, "rb") as f:
        ok = f.read() == src + b"\n"
    if not ok:
        raise SystemExit("byte check failed, the lesson was touched")
    return ok


def menu_delivery_check():
    """The stage B menu cell's structural precondition, checked
    against the production path with pins live, beside a matched-
    ground control. Deterministic, no model."""
    with open(LESSONS_PROD, encoding="utf-8") as f:
        lessons = [json.loads(l) for l in f if l.strip()]
    selected = [lessons[STORE_PROD_LINE - 1]]
    ground_tools = menu.query(selected, _features())
    control_features = {**FEATURES, "rule_class": "tie_break",
                        "rule_topic": "direction",
                        "stated_direction": "last"}
    control_tools = menu.query(selected, control_features)
    return {"ground_tools": len(ground_tools),
            "ground_stated_direction": _features()["stated_direction"],
            "lesson_stated_direction": selected[0]["applies_when"]
            .get("stated_direction"),
            "control_tools": len(control_tools)}


def main():
    print(f"PACKET-029 BUILD STAGE (no model): {GROUND_FAMILY} rung "
          f"{GROUND_RUNG}")
    rung = sf.get_rung(GROUND_FAMILY, GROUND_RUNG)
    print(f"rule checks (the standing annotation): "
          f"{rung['rule_checks']}")

    print("GATE 1, THE CONTRADICTION GATE:")
    results = contradiction_gate()
    selected = None
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
        if res["passes"]:
            selected = c
    if not selected:
        print("BOTH CANDIDATES FAIL: the packet closes uncut.")
        return 1
    print(f"SELECTED: line {selected['prod_line']} "
          f"({selected['gen_task']})")

    print("GATE 2, THE BYTE CHECK:")
    ok = byte_check()
    print(f"  store byte-identical to production line "
          f"{STORE_PROD_LINE}, position asserted: {ok}")

    print("THE STAGE B DELIVERY-PATH CHECK (the menu cell's "
          "precondition, tools=1 every row):")
    chk = menu_delivery_check()
    print(f"  production menu serves the selected lesson on "
          f"{GROUND_FAMILY} ground: {chk['ground_tools']} tools "
          f"(lesson stated_direction {chk['lesson_stated_direction']} "
          f"against ground stated_direction "
          f"{chk['ground_stated_direction']})")
    print(f"  matched-ground control (stated_direction last): "
          f"{chk['control_tools']} tools")
    if chk["ground_tools"] != 1:
        print("THE MENU CELL IS STRUCTURALLY UNREACHABLE: the "
              "production menu's contradiction logic refuses the "
              "contradicting-direction lesson on this ground, the "
              "control proves the refusal is the pin firewall, and "
              "the packet's menu audit (tools=1 every row) cannot be "
              "met without a pin or menu change, both forbidden. "
              "FLAG in FINDINGS and STOP: no model run happens, the "
              "conductor rules.")
        return 2
    return 0


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "build":
        sys.exit(main())
    sys.exit(main())
