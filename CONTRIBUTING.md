# Contributing

Thanks for helping improve PrepBench. This file is for people who want to
report issues, edit the dataset/docs, or change the evaluator, simulator, or
workflow executor.

## Setup

```bash
git clone https://github.com/TsinghuaDatabaseGroup/prepbench.git
cd prepbench
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m pip install -e .
cp .env.example .env
```

The `.env` file is only needed for simulator-backed runs that call an
OpenAI-compatible model endpoint. Basic dataset and evaluator checks do not need
API credentials.

## Project Areas

- Dataset layout: `docs/DATASET.md`
- User simulator contract: `docs/USER_SIMULATOR.md`
- Evaluation: `docs/EVALUATION.md`
- Workflow execution: `docs/WORKFLOW_EXECUTION.md`

Benchmark-side answer artifacts live under `src/evaluate/gt/` and
`reference/solutions/`. Keep them available for validation and reproducibility,
but do not use them as model input when evaluating an agent.

## Checks

```bash
make check
```

This compiles the public Python modules, runs unit tests, validates the dataset,
and checks that the submission evaluator CLI imports correctly.

If a change touches `data/`, `src/evaluate/gt/`, `reference/solutions/`,
`src/evaluate/`, or simulator evidence loading, run the full release gate:

```bash
make check-all
```

`make release-validate` is an alias for the full maintainer gate.

## Reference Verification

Maintainers can verify public reference solutions against the public evaluator:

```bash
make verify-reference-outputs
```

## Reporting Issues

Include:
- command used
- full error output
- expected behavior
- minimal reproduction path
