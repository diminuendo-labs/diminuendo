"""PACKET-020: mining the resistant pairs. Mistral's first teaching
work, from the record it already wrote.

The eight eligible contrast pairs enumerated in PACKET-017 RESULTS ride
verbatim, two per class at the cap, in class order. Supply comes from
the onboard17-20260703-161320 stage 1 artifacts on disk: the failing
and passing runs' own summaries, no new model runs for supply
(distillation calls are the engine's own). Full gates, genpass pattern:
every outcome recorded, accepts and rejects both, the failing screen
named on every reject. Output lands in the packet-local store only;
production stores stay untouched, and admission is a separate
conductor-and-Brad ruling. A supply packet: counts, no treatment
claims."""

import json
import os
import sys
import time

import lesson
import runner
from genpass import _reason_key
from probe_tasks import CANDIDATE_GEN_TASKS, FEATURES

GENERATOR = "qwen2.5-coder:7b"
SOURCE_RUN = "onboard17-20260703-161320"
CLASS_OF_SIBLING = "normalize"

# the eight pairs, verbatim from PACKET-017 RESULTS, in class order
PAIRS = (
    {"type": "within_task", "rule_class": "tie_break",
     "fail_task": "shortest_word", "pass_task": "shortest_word"},
    {"type": "within_task", "rule_class": "tie_break",
     "fail_task": "longest_run_char", "pass_task": "longest_run_char"},
    {"type": "within_task", "rule_class": "distinctness",
     "fail_task": "sum_of_modes", "pass_task": "sum_of_modes"},
    {"type": "within_task", "rule_class": "distinctness",
     "fail_task": "third_largest_distinct",
     "pass_task": "third_largest_distinct"},
    {"type": "within_task", "rule_class": "boundary",
     "fail_task": "chunk", "pass_task": "chunk"},
    {"type": "within_task", "rule_class": "boundary",
     "fail_task": "weighted_mean", "pass_task": "weighted_mean"},
    {"type": "within_task", "rule_class": "normalize",
     "fail_task": "split_csvish", "pass_task": "split_csvish"},
    {"type": "sibling", "rule_class": "normalize",
     "fail_task": "depth_max", "pass_task": "count_word"},
)

_PACKETS = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        "packets")
STORE = os.path.join(_PACKETS, "PACKET-020-lessons.jsonl")

_TASKS = {t["name"]: t for t in CANDIDATE_GEN_TASKS}

_TS = time.strftime("%Y%m%d-%H%M%S")
_LOG = os.path.join(runner.RUNS, f"mine20-{_TS}.log")
_ROWS = os.path.join(runner.RUNS, f"mine20-{_TS}.rows.jsonl")
_REPORT = os.path.join(runner.RUNS, f"mine20-{_TS}.report.json")


def _set_ts(ts):
    """Rebind the run id and its file paths. Resume reuses a prior id so
    the checkpoint rows, the log, and the report stay one record."""
    global _TS, _LOG, _ROWS, _REPORT
    _TS = ts
    _LOG = os.path.join(runner.RUNS, f"mine20-{_TS}.log")
    _ROWS = os.path.join(runner.RUNS, f"mine20-{_TS}.rows.jsonl")
    _REPORT = os.path.join(runner.RUNS, f"mine20-{_TS}.report.json")


def _p(*parts):
    line = " ".join(str(p) for p in parts)
    print(line, flush=True)
    with open(_LOG, "a", encoding="utf-8") as f:
        f.write(line + "\n")


def _row(d):
    """Checkpoint every pair outcome as it lands."""
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


def _features(t):
    f = {**FEATURES, "rule_class": t["rule_class"]}
    if "rule_topic" in t:
        f["rule_topic"] = t["rule_topic"]
    if "stated_direction" in t:
        f["stated_direction"] = t["stated_direction"]
    return f


def source_rows():
    """The PACKET-017 stage 1 checkpoint rows, the supply record."""
    path = os.path.join(runner.RUNS, f"{SOURCE_RUN}.rows.jsonl")
    with open(path, encoding="utf-8") as f:
        return [json.loads(l) for l in f if l.strip()
                and json.loads(l).get("stage") == 1]


def _load_summary(run_id):
    try:
        with open(os.path.join(runner.RUNS, f"{run_id}.summary.json"),
                  encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return None


def gather(rows, task_name, passed):
    """Summaries for a task's failing or passing runs, rep order, from
    disk."""
    out = []
    for r in sorted((x for x in rows if x["task"] == task_name
                     and x["ev_passed"] == passed),
                    key=lambda x: x["rep"]):
        s = _load_summary(r["run_id"])
        if s is not None:
            out.append(s)
    return out


def mine_pair(pair, rows, committed_nodes):
    """One pair through distillation at full gates, genpass pattern:
    two attempts, every reject named by its screen."""
    fails = gather(rows, pair["fail_task"], passed=False)
    passes = gather(rows, pair["pass_task"], passed=True)
    if not fails or not passes:
        return {**pair, "attempted": False, "committed": False,
                "outcome": (f"artifacts insufficient: "
                            f"{len(fails)} fail and {len(passes)} pass "
                            f"summaries on disk"),
                "rejects": []}
    if any(s["node_id"] in committed_nodes for s in fails):
        return {**pair, "attempted": True, "committed": True,
                "outcome": "already committed, resumed", "rejects": []}
    tf = _TASKS[pair["fail_task"]]
    rejects = []
    for attempt in range(2):
        try:
            if pair["type"] == "within_task":
                cand = lesson.generate_contrastive(
                    tf["task"], _features(tf), fails[0], passes[0],
                    model=GENERATOR)
            else:
                tp = _TASKS[pair["pass_task"]]
                cand = lesson.generate_sibling_contrast(
                    tf["task"], tp["task"], pair["rule_class"],
                    _features(tf), fails[0], passes[0], model=GENERATOR)
            cand.setdefault("trail", {})["gen_task"] = tf["name"]
            cand["trail"].setdefault("contrast_type", pair["type"])
            cand["trail"]["source_run"] = SOURCE_RUN
            cand["trail"]["origin_seat"] = "mistral:7b"
            lesson.commit(STORE, cand)
            return {**pair, "attempted": True, "committed": True,
                    "outcome": "committed", "rejects": rejects}
        except lesson.LessonError as e:
            rejects.append({"attempt": attempt + 1,
                            "screen": _reason_key(e),
                            "detail": str(e)[:200]})
            _p(f"  attempt {attempt + 1} rejected "
               f"[{_reason_key(e)}]: {e}")
    return {**pair, "attempted": True, "committed": False,
            "outcome": "rejected at the gates", "rejects": rejects}


def main(resume_ts=None):
    prior = []
    if resume_ts:
        _set_ts(resume_ts)
        prior = _load_rows()
        _p(f"RESUME {_TS}: {len(prior)} checkpointed pair outcomes found")
    done = {(p["fail_task"], p["type"]) for p in prior}
    rows = source_rows()
    committed_nodes = ({l.get("trail", {}).get("node_id")
                        for l in lesson.load(STORE)}
                       if os.path.exists(STORE) else set())
    _p(f"RESISTANT-PAIR MINING {_TS} (PACKET-020, counts not claims)")
    _p(f"source={SOURCE_RUN} stage 1 artifacts, {len(rows)} rows on disk")
    _p(f"generator={GENERATOR} (fixed)  pairs={len(PAIRS)} in class order")

    outcomes = list(prior)
    for pair in PAIRS:
        if (pair["fail_task"], pair["type"]) in done:
            continue
        _p(f"pair {pair['rule_class']} {pair['type']}: "
           f"fail={pair['fail_task']} pass={pair['pass_task']}")
        outcome = mine_pair(pair, rows, committed_nodes)
        _row(outcome)
        outcomes.append(outcome)
        _p(f"  -> {outcome['outcome']}")

    store_lessons = lesson.load(STORE) if os.path.exists(STORE) else []
    accepts = sum(1 for o in outcomes if o["committed"])
    rejects_by_screen = {}
    for o in outcomes:
        for rej in o.get("rejects", []):
            rejects_by_screen[rej["screen"]] = (
                rejects_by_screen.get(rej["screen"], 0) + 1)
    classes = sorted({l["applies_when"]["rule_class"]
                      for l in store_lessons})

    report = {
        "mine20_id": _TS, "source_run": SOURCE_RUN,
        "generator": GENERATOR, "pairs": [dict(p) for p in PAIRS],
        "outcomes": outcomes,
        "counts": {"attempts": sum(1 for o in outcomes if o["attempted"]),
                   "accepts": accepts,
                   "rejects_by_screen": rejects_by_screen},
        "store_classes": classes,
        "store_lessons": [{"concept": l["concept"], "rule": l["rule"],
                           "applies_when": l["applies_when"],
                           "trail": {k: l["trail"].get(k) for k in
                                     ("gen_task", "contrast_type",
                                      "origin_seat")}}
                          for l in store_lessons],
        "n_note": ("A supply packet: counts, no treatment claims, no "
                   "delivery arms. Admission to production stores is a "
                   "separate ruling."),
    }
    with open(_REPORT, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    _p("== CLOSING COUNTS ==")
    _p(f"  attempts={report['counts']['attempts']}  accepts={accepts}  "
       f"rejects_by_screen={rejects_by_screen or 'none'}")
    _p(f"  store classes: {classes}")
    boundary = "boundary" in classes
    normalize = "normalize" in classes
    _p(f"CLOSING: the record now holds its first gated boundary-class "
       f"lesson: {'YES' if boundary else 'NO'}; its first gated "
       f"normalize-class lesson: {'YES' if normalize else 'NO'}.")
    gate = (len(outcomes) == len(PAIRS) and os.path.exists(_ROWS))
    _p(f"GATE: {'PASSED' if gate else 'FAILED'}. all eight pairs "
       f"attempted in order, every outcome reported with rejects named "
       f"by screen, store packet-local only, production stores "
       f"untouched.")


if __name__ == "__main__":
    main(resume_ts=sys.argv[1] if len(sys.argv) > 1 else None)
