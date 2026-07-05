"""PACKET-014: the supply probe on the liftable ground. Does llama
supply breaks and contrast pairs in the distinctness class, the material
the clean reverse-transfer test needs.

A probe measures supply and structure: counts, not claims. Performer
llama, evidence execution as the label, R=6 per task across every
distinctness-class task in both pools, the enumeration printed before
any run. Contrast enumeration follows the standing engine rules,
within-task pairs first, sibling pairs second, with the conjunction
filter (breaks for the seat AND carries an in-pool topic) applied and
printed per task. Generation material is generation-pool tasks only:
the apply-pool distinctness tasks are probed for supply knowledge and
excluded from distillation by the standing disjointness rule, and
range_summary itself is the apply target. If eligible pairs exist,
distillation runs at full gates into the packet-local store only, every
gate outcome reported, accepts and rejects both. No treatment arms, no
qwen runs, no signed readings."""

import json
import os
import sys
import time

import lesson
import runner
from probe_tasks import (APPLY_TASKS, CANDIDATE_APPLY_TASKS,
                         CANDIDATE_GEN_TASKS, CRITERIA, FEATURES)

PERFORMER = "llama3.1:8b"
AUDIENCE = "qwen2.5-coder:7b"
GENERATOR = "qwen2.5-coder:7b"
R = 6
CLASS = "distinctness"

_PACKETS = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        "packets")
STORE = os.path.join(_PACKETS, "PACKET-014-lessons.jsonl")

_TS = time.strftime("%Y%m%d-%H%M%S")
_LOG = os.path.join(runner.RUNS, f"probe14-{_TS}.log")
_ROWS = os.path.join(runner.RUNS, f"probe14-{_TS}.rows.jsonl")
_REPORT = os.path.join(runner.RUNS, f"probe14-{_TS}.report.json")


def _set_ts(ts):
    """Rebind the run id and its file paths. Resume reuses a prior id so
    the checkpoint rows, the log, and the report stay one record."""
    global _TS, _LOG, _ROWS, _REPORT
    _TS = ts
    _LOG = os.path.join(runner.RUNS, f"probe14-{_TS}.log")
    _ROWS = os.path.join(runner.RUNS, f"probe14-{_TS}.rows.jsonl")
    _REPORT = os.path.join(runner.RUNS, f"probe14-{_TS}.report.json")


def _p(*parts):
    line = " ".join(str(p) for p in parts)
    print(line, flush=True)
    with open(_LOG, "a", encoding="utf-8") as f:
        f.write(line + "\n")


def _row(d):
    """Checkpoint every run as it lands. A dead pipe strands nothing."""
    with open(_ROWS, "a", encoding="utf-8") as f:
        f.write(json.dumps(d) + "\n")


def _load_rows():
    rows = []
    try:
        with open(_ROWS, encoding="utf-8") as f:
            rows = [json.loads(l) for l in f if l.strip()]
    except FileNotFoundError:
        pass
    return rows


def _load_summary(run_id):
    try:
        with open(os.path.join(runner.RUNS, f"{run_id}.summary.json"),
                  encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return None


def ev_fraction(ev):
    results = (ev or {}).get("results") or []
    if not results:
        return 0.0
    return sum(1 for r in results if r["ok"]) / len(results)


def _features(t):
    f = {**FEATURES, "rule_class": t["rule_class"]}
    if "rule_topic" in t:
        f["rule_topic"] = t["rule_topic"]
    if "stated_direction" in t:
        f["stated_direction"] = t["stated_direction"]
    return f


def enumerate_tasks():
    """Every distinctness-class task in both pools, with pool membership
    and generation eligibility. Printed before any run."""
    apply_topics = {t["rule_topic"] for t in APPLY_TASKS}
    out = []
    for t in CANDIDATE_GEN_TASKS:
        if t["rule_class"] != CLASS:
            continue
        out.append({"name": t["name"], "pool": "generation",
                    "rule_topic": t["rule_topic"],
                    "generation_eligible": True,
                    "topic_in_apply_pool": t["rule_topic"] in apply_topics})
    for t in CANDIDATE_APPLY_TASKS:
        if t["rule_class"] != CLASS:
            continue
        out.append({"name": t["name"], "pool": "apply",
                    "rule_topic": t["rule_topic"],
                    "generation_eligible": False,
                    "topic_in_apply_pool": t["rule_topic"] in apply_topics})
    return out


def _task(name):
    for t in CANDIDATE_GEN_TASKS + CANDIDATE_APPLY_TASKS:
        if t["name"] == name:
            return t
    raise KeyError(name)


def run_probe(enum, repeats=R, prior_rows=None):
    """R runs per enumerated task, evidence as the label."""
    prior = list(prior_rows or [])
    done = {(r["task"], r["rep"]) for r in prior}
    if prior:
        _p(f"resuming past {len(prior)} checkpointed runs")
    rows = list(prior)
    for entry in enum:
        t = _task(entry["name"])
        for rep in range(repeats):
            if (t["name"], rep) in done:
                continue
            r = runner.run_once(t["task"], CRITERIA, _features(t),
                                model=PERFORMER, audience_model=AUDIENCE,
                                evidence_checks=t["checks"])
            row = {"task": t["name"], "pool": entry["pool"], "rep": rep,
                   "run_id": r["run_id"], "verdict": r["verdict"],
                   "ev": ev_fraction(r["evidence"]),
                   "ev_passed": bool((r["evidence"] or {}).get("passed")),
                   "checks": {c["call"]: bool(c["ok"]) for c in
                              (r["evidence"] or {}).get("results") or []}}
            _row(row)
            rows.append(row)
            _p(f"{t['name']} rep {rep}: ev={row['ev']:.2f} "
               f"passed={row['ev_passed']}")
    return rows


def supply_table(enum, rows):
    """Per task: pass/fail counts at R from evidence, the case, and the
    conjunction verdict for generation-eligible tasks."""
    table = []
    for entry in enum:
        task_rows = [r for r in rows if r["task"] == entry["name"]]
        fails = sum(1 for r in task_rows if not r["ev_passed"])
        passes = len(task_rows) - fails
        case = ("mixed" if fails and passes else
                "all_pass" if not fails else "all_fail")
        breaks = fails > 0
        conjunction = (entry["generation_eligible"] and breaks
                       and entry["topic_in_apply_pool"])
        table.append({**entry, "runs": len(task_rows), "fails": fails,
                      "passes": passes, "case": case,
                      "breaks_for_seat": breaks,
                      "conjunction_eligible": conjunction})
    return table


def contrast_pairs(table):
    """The standing engine rules over the generation-eligible tasks:
    within-task pairs first, sibling pairs second, conjunction filter
    applied. Every eligible pair listed."""
    gen = [e for e in table if e["generation_eligible"]]
    pairs = []
    for e in gen:
        if e["case"] == "mixed" and e["conjunction_eligible"]:
            pairs.append({"type": "within_task", "fail_task": e["name"],
                          "pass_task": e["name"],
                          "rule_topic": e["rule_topic"]})
    mined = {p["fail_task"] for p in pairs}
    for e in gen:
        if len(pairs) >= 2:
            break
        if e["name"] in mined or not e["fails"]:
            continue
        if not e["conjunction_eligible"]:
            continue
        partner = next((x for x in gen if x["name"] != e["name"]
                        and x["passes"]), None)
        if partner is None:
            continue
        pairs.append({"type": "sibling", "fail_task": e["name"],
                      "pass_task": partner["name"],
                      "rule_topic": e["rule_topic"]})
        mined.add(e["name"])
    return pairs[:2]  # the standing per-class cap


def distill(pairs, rows):
    """Full-gate distillation into the packet-local store, genpass
    pattern: every outcome recorded, accepts and rejects both."""
    outcomes = []
    by_task = {}
    for r in rows:
        by_task.setdefault(r["task"], []).append(r)

    def summaries(name, passed):
        picked = [r for r in by_task.get(name, [])
                  if r["ev_passed"] == passed]
        out = []
        for r in picked:
            s = _load_summary(r["run_id"])
            if s is not None:
                out.append(s)
        return out

    for pair in pairs:
        fails = summaries(pair["fail_task"], passed=False)
        passes = summaries(pair["pass_task"], passed=True)
        if not fails or not passes:
            outcomes.append({**pair, "committed": False,
                             "outcome": "summaries missing on disk"})
            continue
        tf = _task(pair["fail_task"])
        committed = False
        rejects = []
        for attempt in range(2):
            try:
                if pair["type"] == "within_task":
                    cand = lesson.generate_contrastive(
                        tf["task"], _features(tf), fails[0], passes[0],
                        model=GENERATOR)
                else:
                    tp = _task(pair["pass_task"])
                    cand = lesson.generate_sibling_contrast(
                        tf["task"], tp["task"], CLASS, _features(tf),
                        fails[0], passes[0], model=GENERATOR)
                cand.setdefault("trail", {})["gen_task"] = tf["name"]
                cand["trail"].setdefault("contrast_type", pair["type"])
                lesson.commit(STORE, cand)
                committed = True
                break
            except lesson.LessonError as e:
                rejects.append(f"attempt {attempt + 1}: {e}")
                _p(f"  {pair['type']} {pair['fail_task']} rejected: {e}")
        outcomes.append({**pair, "committed": committed,
                         "rejects": rejects,
                         "outcome": ("committed" if committed else
                                     "rejected at the gates")})
        _p(f"distill {pair['type']} {pair['fail_task']}: "
           f"{'committed' if committed else 'REJECTED'}")
    return outcomes


def main(repeats=R, resume_ts=None):
    prior_rows = []
    if resume_ts:
        _set_ts(resume_ts)
        prior_rows = _load_rows()
        _p(f"RESUME {_TS}: {len(prior_rows)} checkpointed rows found")
    enum = enumerate_tasks()
    _p(f"SUPPLY PROBE {_TS} (PACKET-014, counts not claims)")
    _p(f"performer={PERFORMER}  audience={AUDIENCE} (v1, production)")
    _p(f"class={CLASS}  R={repeats} per task  tasks={len(enum)}")
    _p("== ENUMERATION (printed before any run) ==")
    for e in enum:
        _p(f"  {e['name']:24s} pool={e['pool']:10s} "
           f"topic={e['rule_topic']:7s} "
           f"gen_eligible={e['generation_eligible']} "
           f"topic_in_apply={e['topic_in_apply_pool']}")
    if sum(1 for e in enum) < 2:
        _p("fewer than two tasks in the class: that is a supply answer, "
           "stopping")
        return

    rows = run_probe(enum, repeats, prior_rows)
    table = supply_table(enum, rows)
    pairs = contrast_pairs(table)
    _p("== SUPPLY TABLE ==")
    for e in table:
        _p(f"  {e['name']:24s} {e['case']:9s} "
           f"({e['fails']}/{e['runs']} failed) "
           f"conjunction={'YES' if e['conjunction_eligible'] else 'no'}"
           f"{'' if e['generation_eligible'] else ' (apply pool, excluded from generation)'}")
    _p(f"== ELIGIBLE CONTRAST PAIRS: {len(pairs)} ==")
    for p in pairs:
        _p(f"  {p['type']}: fail={p['fail_task']} pass={p['pass_task']} "
           f"topic={p['rule_topic']}")

    outcomes = distill(pairs, rows) if pairs else []
    store_lessons = lesson.load(STORE) if os.path.exists(STORE) else []

    reachable = any(
        l.get("applies_when", {}).get("rule_class") == CLASS
        and l.get("applies_when", {}).get("rule_topic") in
        ("values", "*")
        for l in store_lessons)

    report = {
        "probe14_id": _TS, "performer": PERFORMER, "audience": AUDIENCE,
        "rule_class": CLASS, "repeats": repeats,
        "enumeration": enum, "supply_table": table,
        "eligible_pairs": pairs, "distill_outcomes": outcomes,
        "store_lessons": [{"concept": l["concept"], "rule": l["rule"],
                           "applies_when": l["applies_when"]}
                          for l in store_lessons],
        "reverse_on_liftable_ground_reachable": reachable,
        "n_note": (f"R={repeats} per task. A supply probe: counts, not "
                   f"claims, no treatment readings."),
    }
    with open(_REPORT, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    counts_ok = all(
        sum(1 for r in rows if r["task"] == e["name"]) == repeats
        for e in enum)
    gate = counts_ok and os.path.exists(_ROWS)
    _p(f"CLOSING: a gated llama-origin distinctness lesson with an "
       f"in-pool topic {'EXISTS' if reachable else 'DOES NOT EXIST'}; "
       f"the reverse cell on liftable ground is "
       f"{'REACHABLE' if reachable else 'NOT REACHABLE'}.")
    _p(f"GATE: {'PASSED' if gate else 'FAILED'}. enumeration printed "
       f"before any run, {len(enum)} tasks at R={repeats}, every run "
       f"checkpointed, report persisted, store packet-local only.")


if __name__ == "__main__":
    main(repeats=int(sys.argv[1]) if len(sys.argv) > 1 else R,
         resume_ts=sys.argv[2] if len(sys.argv) > 2 else None)
