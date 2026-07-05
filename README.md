# Diminuendo

Diminuendo is a multi-agent orchestration framework that competes on
catching failure rather than on making agents smarter. It treats the
role, not the model, as the persistent unit, so the memory belongs to
the chair and survives a model swap. This repository is the research
bench: a small running system with a deterministic score, a cost
ledger, and the instrument that measures whether a lesson learned by
one model transfers to another.

## What is here

- `bench/`: the code, the tests, the work packets, and the run
  records. The run records are the data and are committed.
- `DIMINUENDO_TECHNICAL_SPEC_v0.7.md`: how the known pieces are built,
  each section with a Spec and a Where it breaks.
- `DIMINUENDO_FLAG_DRAFT_v0.md`: the writeup of what the bench
  measured, in draft.
- `DIMINUENDO_TECH_REPORT_SKELETON_v0.md`: the technical report
  outline.
- `bench/DECISIONS.md`: the decisions log, one line per architecture
  call. This is a redacted public copy; see its header.

## What it measured

Form is a variable. The same lesson handed to a model as a menu tool
behaves differently from the same bytes handed to it as a directive:
the menu form preserved the model's judgment while the directive form
collapsed work the model otherwise did correctly. Measured on two
tasks and two model families, small n, direction not rate. Tool
response reads as a per-model casting trait. Transfer across models is
consistent with the field and sized to n. The catching-failure loop
is designed and instrumented, not yet proven. The details, with every
measured claim traced to the run record, are in the flag draft and
the technical spec.

## Running the bench

Python runs as `py` (3.14). Models are served locally through Ollama.
From `bench/`:

- Tests: `py -m unittest discover -s tests`
- Minimal loop: `py minimal_loop.py llama3.1:8b`
- Transfer probe: `py probe.py`

See `bench/README.md` for the full set of entry points.

## Status

This is a concept plus a first build, not proof. The seams close by
running, and what has run is in the bench record.

## License

AGPL-3.0. See `LICENSE`.
