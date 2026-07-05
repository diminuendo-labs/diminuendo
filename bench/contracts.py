"""Instance contracts and the blind-metric firewall. Tech Spec Sections 1 and 4.

The state boundary as code, not policy. A Performer receives task, criteria,
landscape. It never receives raw scores or the metric. The Audience holds the
metric. The firewall here is a hard gate: any performer-bound payload passes
guard_no_metric, which walks the whole structure and raises on any metric-shaped
key. The known limit, stated in the spec and repeated here: a key check cannot
catch metric advice laundered into lesson prose. That risk lives on the
score-to-lesson translation and is tested there, not silently assumed away.
"""

METRIC_KEYS = {
    "time", "time_s", "tokens", "cost_time", "cost_tokens",
    "score", "raw_score", "metric", "ledger", "totals",
}


class FirewallError(Exception):
    """A metric-shaped field tried to cross into a performer context."""


def guard_no_metric(obj, path="context"):
    """Recursively verify no metric-shaped key exists anywhere in obj."""
    if isinstance(obj, dict):
        for k, v in obj.items():
            if str(k).lower() in METRIC_KEYS:
                raise FirewallError(f"metric key '{k}' at {path}")
            guard_no_metric(v, f"{path}.{k}")
    elif isinstance(obj, (list, tuple)):
        for i, v in enumerate(obj):
            guard_no_metric(v, f"{path}[{i}]")
    return obj


def performer_context(task, criteria, landscape=None):
    """Everything a Performer is allowed to see, and nothing else.
    Guarded on the way out, so a metric can never ride in on a lesson dict."""
    ctx = {
        "task": task,
        "criteria": list(criteria),
        "landscape": list(landscape or []),
    }
    return guard_no_metric(ctx)


def validate_performer_output(out):
    """A Performer returns output, the tools it chose, work features, and a
    trace. Missing pieces are a contract break, caught here, not downstream."""
    required = ("output", "tools_chosen", "work_features", "trace")
    missing = [k for k in required if k not in out]
    if missing:
        raise ValueError(f"performer output missing: {missing}")
    return out


def audience_packet(task, criteria, output):
    """Everything the blind Audience sees: the task, the criteria, the output.
    Fresh instance, no chair memory, no performer trace. It holds the metric
    on its side, it does not need one handed in."""
    return {
        "task": task,
        "criteria": list(criteria),
        "output": output,
    }
