"""The Breadcrumb store. Tech Spec Section 3.

One record per node, the load-bearing record: forecaster features, credit
assignment trail, novelty inheritance. Append-only JSONL. Hindsight never edits
history, it appends an amendment, and load() resolves the latest value per
field. That is the grain-heals-by-back-fill rule made concrete: the original
forward record survives, the correction sits after it, both are readable.
"""

import json
import time as _time

REQUIRED = ("node_id", "model", "role", "work_features",
            "cost_time", "cost_tokens", "outcome")
OPTIONAL = ("parent_concept_id", "error_class", "novelty_flag", "trace_ref")


def write(path, record):
    """Append one forward breadcrumb. Required fields enforced."""
    missing = [k for k in REQUIRED if k not in record]
    if missing:
        raise ValueError(f"breadcrumb missing fields: {missing}")
    unknown = [k for k in record if k not in REQUIRED + OPTIONAL]
    if unknown:
        raise ValueError(f"breadcrumb has unknown fields: {unknown}")
    row = dict(record)
    row["ts"] = _time.time()
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(row) + "\n")
    return row


def amend(path, node_id, **updates):
    """Append a hindsight amendment for a node. Typical fields: outcome
    (hindsight-corrected), error_class, novelty_flag (retroactive re-set),
    and new work_features a break exposed (back-fill)."""
    bad = [k for k in updates if k not in REQUIRED + OPTIONAL]
    if bad:
        raise ValueError(f"amendment has unknown fields: {bad}")
    row = {"node_id": node_id, "_amend": True, "ts": _time.time()}
    row.update(updates)
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(row) + "\n")
    return row


def load(path):
    """Resolve the file to one merged record per node_id, later values
    overriding earlier ones field by field. work_features merge by key so
    back-fill adds features without erasing the forward ones."""
    merged = {}
    with open(path, encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            row = json.loads(line)
            nid = row["node_id"]
            cur = merged.setdefault(nid, {})
            for k, v in row.items():
                if k in ("_amend", "ts"):
                    continue
                if k == "work_features" and isinstance(cur.get(k), dict):
                    cur[k] = {**cur[k], **v}
                else:
                    cur[k] = v
    return merged
