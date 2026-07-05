# bench, the Diminuendo minimal build

The code home for the first build: the minimal loop, the two-level handoff, and the
transfer probe. The plan is BENCH_BUILD_PLAN.md at the repo root. Every architecture
call lands in DECISIONS.md with one reason.

Layout:
- score.py, ledger.py, breadcrumb.py, contracts.py, evidence.py, flagtally.py:
  the tested primitives.
- runner.py: one task through the loop. lesson.py and menu.py: the lesson
  engine and the landscape.
- minimal_loop.py, cascade.py, probe.py: the three harnesses, each printing a
  computed gate line and logging itself to runs/.
- tests/ holds the tests, 39 and green. runs/ holds every run's records:
  breadcrumbs, ledgers, traces, summaries, flags, probe reports. The records
  are the data and are committed.

Run with the py launcher, Python 3.14. Models come from local Ollama:
qwen2.5-coder:7b and llama3.1:8b, audience always the other family from the
performer. Never stream a long model run through a live pipe: launch with
output to a file and poll the file. CONTINUATION.md at the repo root carries
the full state.
