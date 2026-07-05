"""The Tool Menu: committed lessons rendered as a landscape at task start.

The performer's-side view of applicability conditions. Queried before the
work, never delivered as a correction after it. Matching is deliberately
simple: a lesson surfaces when its applies_when conditions overlap the task's
work features, wildcards match anything, and results sort by confidence.
Narrow beats broad later. Simple first.
"""


def matches(conditions, features):
    """Public matcher, shared with the audience watchlist. Score of equal
    key-values, wildcards match anything, a contradiction disqualifies."""
    score = 0
    for k, v in conditions.items():
        if k not in features:
            continue
        if str(v) == "*" or str(v).lower() == str(features[k]).lower():
            score += 1
        else:
            return -1  # a stated condition that contradicts the task
    return score


_matches = matches


def query(lessons, work_features, limit=5):
    """Return landscape tools for the performer: concept + applies_when only.
    No confidence number crosses (it is derived from outcomes), no trail.
    A lesson missing the fields the menu consumes is declined, never a
    crash (PACKET-013 tier 1, conductor-ruled): the menu serves what it
    can rank and silently shelves what it cannot."""
    scored = []
    for les in lessons:
        if any(k not in les for k in ("concept", "applies_when",
                                      "confidence")):
            continue
        s = _matches(les["applies_when"], work_features)
        if s >= 1:
            scored.append((s, float(les["confidence"]), les))
    scored.sort(key=lambda t: (-t[0], -t[1]))
    return [{"concept": les["concept"], "applies_when": les["applies_when"]}
            for _, _, les in scored[:limit]]
