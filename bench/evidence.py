"""Executable evidence: run the generated code against concrete checks.

One of the decorrelated checker kinds from the spec. The audience reads the
output and forms an opinion. This module executes it, and execution does not
share a blind spot with any language model. For the checks it covers, evidence
outranks the audience: an audience pass over an evidence fail is a fail.

Containment, stated honestly: the code runs in a subprocess with a timeout,
which contains hangs and crashes. It is not a sandbox. Acceptable for synthetic
tasks authored here. Revisit before any untrusted task enters the loop.
"""

import json
import os
import re
import subprocess
import sys
import tempfile

_FENCE = re.compile(r"```(?:python)?\s*\n(.*?)```", re.DOTALL)


def extract_python(text):
    """The first fenced python block, else the text as-is."""
    m = _FENCE.search(text)
    return m.group(1).strip() if m else text.strip()

_HARNESS = """
import json as _json
_checks = _CHECKS
_results = []
for _c in _checks:
    try:
        _got = eval(_c["call"])
        _results.append({"call": _c["call"], "ok": repr(_got) == _c["expect"],
                         "got": repr(_got), "expect": _c["expect"]})
    except Exception as _e:
        _results.append({"call": _c["call"], "ok": False,
                         "got": "raised " + repr(_e), "expect": _c["expect"]})
print(_json.dumps(_results))
"""


def run_checks(code, checks, timeout_s=15):
    """checks: [{"call": "f(args)", "expect": "<repr of expected value>"}].
    Returns {"passed": bool, "results": [...], "error": str or None}."""
    script = code + "\n" + _HARNESS.replace(
        "_CHECKS", json.dumps(checks))
    fd, path = tempfile.mkstemp(suffix=".py")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(script)
        try:
            proc = subprocess.run([sys.executable, path],
                                  capture_output=True, text=True,
                                  timeout=timeout_s)
        except subprocess.TimeoutExpired:
            return {"passed": False, "results": [],
                    "error": f"timeout after {timeout_s}s"}
    finally:
        os.unlink(path)

    if proc.returncode != 0:
        return {"passed": False, "results": [],
                "error": (proc.stderr or "nonzero exit").strip()[-500:]}
    line = proc.stdout.strip().splitlines()[-1] if proc.stdout.strip() else ""
    try:
        results = json.loads(line)
    except json.JSONDecodeError:
        return {"passed": False, "results": [],
                "error": "harness produced no parseable results"}
    return {"passed": all(r["ok"] for r in results),
            "results": results, "error": None}
