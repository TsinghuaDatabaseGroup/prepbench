# Evaluation

PrepBench evaluates generated result tables against per-case ground truth.
Inference and evaluation are separate: run your own agent first, then point the
evaluator at the run root for that mode, such as `@runs/my_agent/interactive`.
All public modes share the same result-file contract and comparison rules.

## Candidate Layout

Write result tables under:

```text
@runs/<agent>/<mode>/
  case_001/
    result/
      output_01.csv
  case_002/
    result/
      output_01.csv
```

This `result/` directory is the only scoring input.

Rules:

- Case folders must use `case_xxx` names.
- Candidate CSVs must live directly under `result/`.
- Candidate output file names must match the expected GT names, such as
  `output_01.csv`.

## Run Evaluation

For a complete mode run, prepare the workspaces, run your agent, then evaluate
the run root:

```bash
python scripts/prepare_run.py \
  --mode interactive \
  --all \
  --run-root @runs/my_agent/interactive
```

```bash
python scripts/evaluate_submission.py \
  --mode interactive \
  --run-root @runs/my_agent/interactive
```

For single-case debugging, add `--case`:

```bash
python scripts/evaluate_submission.py \
  --mode interactive \
  --run-root @runs/my_agent/interactive \
  --case case_001
```

Generated files:

```text
@runs/my_agent/interactive/evaluation/summary.json
@runs/my_agent/interactive/evaluation/summary.csv
```

Single-case runs also write stable per-case copies, for example
`evaluation/case_001.summary.json` and `evaluation/case_001.summary.csv`, so
debugging another case does not overwrite the previous case-specific summary.

When `--case` is omitted, the evaluator checks every GT case. The command exits
with code 0 only when every evaluated case passes. Missing case folders or
missing result files are marked as `NOT_FOUND`.

The evaluator requires `--mode`, and the value must match the final path segment
of `--run-root`, for example `interactive` for `@runs/my_agent/interactive`.

## Comparison Semantics

Each output file has a `config.json` entry that declares the columns to compare,
their matcher types, and the key columns used for row alignment.

Numeric columns use a general-purpose tolerance. Nonzero numeric values match
when `abs(gt - cand) / max(abs(gt), abs(cand)) < 0.02`; if either side is zero,
they match when `abs(gt - cand) < 0.02`. The same numeric matcher is used for
numeric key columns, because many PrepBench configs use all output columns as an
unordered row signature rather than a separate database-style primary key.

## Programmatic API

```python
from prepbench.submission_eval import evaluate_submission

summary = evaluate_submission(
    mode="clarified",
    run_root="@runs/my_agent/clarified",
)
```

The returned summary has the same aggregate and per-case fields written to
`evaluation/summary.json`. Use `evaluation/summary.csv` to inspect one row per
case.
