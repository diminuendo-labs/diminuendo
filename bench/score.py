"""The Score: deterministic dependency graph and scheduler.

Tech Spec Section 2. The score on the stand, not a second conductor. It encodes
dependencies and enforces ordering, refusing to release a node until its
predecessors are complete. Deterministic, decorrelated from the conductor.

Rules built in:
- add_edge runs a cycle check on every add. A cycle is rejected, never stored.
- Dynamic growth is one direction only: a running node may spawn children
  downstream. A mid-run discovery of a missing upstream parent is a break, not a
  live edit, and the caller handles it as one (stop, schedule, re-run, add the
  edge for next time).
- Edge sources are recorded (structural, semantic, missing) because the three
  carry different trust, per the spec.
"""

PENDING = "pending"
DONE = "done"
EDGE_SOURCES = ("structural", "semantic", "missing")


class CycleError(Exception):
    """Raised when an edge would create a cycle."""


class UnknownNodeError(Exception):
    """Raised when an edge references a node the score does not hold."""


class Score:
    """A queryable dependency graph with release gating."""

    def __init__(self):
        self._state = {}      # node_id -> PENDING | DONE
        self._parents = {}    # node_id -> set of node_ids it depends on
        self._children = {}   # node_id -> set of node_ids that depend on it
        self._edge_meta = {}  # (parent, child) -> source string

    # ---- nodes ----

    def add_node(self, node_id, depends_on=(), source="semantic"):
        """Add a node, optionally with its dependencies in one call."""
        if node_id in self._state:
            raise ValueError(f"node already in score: {node_id}")
        self._state[node_id] = PENDING
        self._parents[node_id] = set()
        self._children[node_id] = set()
        for dep in depends_on:
            self.add_edge(dep, node_id, source=source)

    def mark_complete(self, node_id):
        if node_id not in self._state:
            raise UnknownNodeError(node_id)
        self._state[node_id] = DONE

    def state(self, node_id):
        return self._state[node_id]

    # ---- edges ----

    def add_edge(self, parent, child, source="semantic"):
        """Declare that child depends on parent. Rejects cycles and unknowns."""
        if source not in EDGE_SOURCES:
            raise ValueError(f"unknown edge source: {source}")
        if parent not in self._state:
            raise UnknownNodeError(parent)
        if child not in self._state:
            raise UnknownNodeError(child)
        if parent == child or self._reaches(child, parent):
            raise CycleError(f"edge {parent} -> {child} would create a cycle")
        self._parents[child].add(parent)
        self._children[parent].add(child)
        self._edge_meta[(parent, child)] = source

    def _reaches(self, start, target):
        """True if target is reachable downstream of start."""
        stack = [start]
        seen = set()
        while stack:
            n = stack.pop()
            if n == target:
                return True
            if n in seen:
                continue
            seen.add(n)
            stack.extend(self._children[n])
        return False

    def edge_source(self, parent, child):
        return self._edge_meta[(parent, child)]

    # ---- queries ----

    def ready_nodes(self):
        """Pending nodes whose every dependency is done. The release gate."""
        out = []
        for node_id, st in self._state.items():
            if st != PENDING:
                continue
            if all(self._state[p] == DONE for p in self._parents[node_id]):
                out.append(node_id)
        return sorted(out)

    def blocked_by(self, node_id):
        """The incomplete dependencies holding a node back. Diagnostics."""
        if node_id not in self._state:
            raise UnknownNodeError(node_id)
        return sorted(p for p in self._parents[node_id]
                      if self._state[p] != DONE)

    def nodes(self):
        return sorted(self._state)

    def is_done(self):
        return all(st == DONE for st in self._state.values())

    def to_dict(self):
        """Plain-data snapshot, for persistence and inspection."""
        return {
            "state": dict(self._state),
            "edges": [
                {"parent": p, "child": c, "source": s}
                for (p, c), s in sorted(self._edge_meta.items())
            ],
        }
