# Reproducing Paper Experiments

This document is for the internal reproduction track (`run.py` + multi-mode runs).
If you are evaluating your own framework, use `docs/BYOA_E2E.md` instead.

## Prerequisites

- Install and configure environment as in `README.md`.
- `flow`, `interact`, and `e2e` use benchmark reference solutions at:
  - `src/simulator/assets/solutions/case_XXX.py`
- In this repository snapshot, reference solutions are already included.
- They are benchmark-internal assets for runtime/evaluation alignment, not public inputs for method design.

## Entry Point

Main runner:

```bash
python run.py --case 1 --run_mode orig --model openai/gpt-5.2
```

Shortcut scripts:

```bash
./scripts/run_orig.sh --case 1 --model openai/gpt-5.2
./scripts/run_disamb.sh --case 1 --model openai/gpt-5.2
./scripts/run_interact.sh --case 1 --model openai/gpt-5.2
./scripts/run_disamb_only.sh --case 1 --model openai/gpt-5.2
./scripts/run_flow.sh --case 1 --model openai/gpt-5.2
./scripts/run_e2e.sh --case 1 --model openai/gpt-5.2
```

## Run Modes

- `orig`: raw query + profile + code
- `disamb`: disambiguated/full query + profile + code
- `interact`: raw query + clarify + profile + code
- `disamb_only`: disambiguated/full query + code (no profile)
- `e2e`: interact pipeline + code-to-flow
- `flow`: flow-only execution (translates `src/simulator/assets/solutions/case_XXX.py`)

## Common Selectors

Run one case:

```bash
python run.py --case 52 --run_mode disamb --model openai/gpt-5.2
```

Run a range:

```bash
python run.py --case 5-8 --run_mode orig --model openai/gpt-5.2
```

Run all cases:

```bash
python run.py --run_mode orig --model openai/gpt-5.2
```

Use config defaults (omit `--run_mode` and `--model`):

```bash
python run.py --case 52
```

## Output Root Naming

`<model_info>` in output paths is derived from the last segment of model name and sanitized for filesystem usage.

Example:
- model: `openai/gpt-5.2`
- output root prefix: `@output/gpt-5.2/`

## Notes

- `e2e` can run directly and reuses compatible interact artifacts when available.
- `flow` / `interact` / `e2e` depend on benchmark reference solutions under `src/simulator/assets/solutions/`.

## Evaluate Reproduction Runs

Evaluate one run root:

```bash
PYTHONPATH=src python -m evaluate.batch --results-root @output/<model_info>/<run_mode>
```

Generated:
- `@output/<model_info>/<run_mode>/evaluation_summary.csv`
- `@output/<model_info>/<run_mode>/acc.txt`

Important:
- `evaluate.batch` always evaluates against all GT cases.
- If you only ran a subset of cases, the rest will be marked `NOT_FOUND` in `evaluation_summary.csv`.
- GT for code/workflow evaluation is loaded from `src/evaluate/gt/case_XXX`.

Track mapping:
- `--candidate-kind code` -> code accuracy (`solution/cand/*.csv`)
- `--candidate-kind flow` -> workflow accuracy (`solution/flow_cand/*.csv`)
- `--candidate-kind auto` -> prefer flow track, then code track

Disambiguation metric (paper Table 5, third metric):

```bash
PYTHONPATH=src python -m evaluate.disamb --results-root @output/<model_info>/<run_mode>
```

Generated:
- `@output/<model_info>/<run_mode>/disamb_summary.csv`
- `@output/<model_info>/<run_mode>/disamb_by_type.csv`
- `@output/<model_info>/<run_mode>/disamb_metrics.json`
- `@output/<model_info>/<run_mode>/disamb_f1.txt`

Metric note:
- Aggregate precision uses `unique_hit_slots / questions_used`.
