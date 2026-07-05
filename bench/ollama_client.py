"""Minimal Ollama client. Standard library only, local HTTP, no dependencies.

Returns the text plus the cost facts Ollama reports: prompt tokens, output
tokens, and wall time. Those numbers flow to the ledger and breadcrumb on the
audience side of the firewall. The performer never sees them.
"""

import json
import urllib.request

BASE = "http://localhost:11434"


def generate(model, prompt, timeout_s=300, options=None):
    payload = {"model": model, "prompt": prompt, "stream": False}
    if options:
        payload["options"] = options
    body = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        BASE + "/api/generate", data=body,
        headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout_s) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    return {
        "text": data.get("response", ""),
        "prompt_tokens": data.get("prompt_eval_count", 0),
        "output_tokens": data.get("eval_count", 0),
        "time_s": data.get("total_duration", 0) / 1e9,
    }
