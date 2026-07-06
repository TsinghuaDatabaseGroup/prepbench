# Evaluation

PrepBench evaluates generated result tables against per-case ground truth.
Inference and evaluation are separate: run your own agent first, then point the
evaluator at the mode run root.

## Modes

All public modes share the same output contract and comparison semantics.

| Mode | Workspace input | Extra tool |
| --- | --- | --- |
| `clarified` | clarified `query.md` + `inputs/` | none |
| `interactive` | original `query.md` + `inputs/` | user simulator |
| `workflow` | original `query.md` + `inputs/` | user simulator + workflow executor |

The evaluator requires `--mode`, and the value must match the last path segment
of `--run-root`.

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

Evaluate all GT cases for one mode:

```bash
python scripts/evaluate_submission.py \
  --mode interactive \
  --run-root @runs/my_agent/interactive
```

Evaluate one case for debugging:

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

When `--case` is omitted, the evaluator checks every GT case. The command exits
with code 0 only when every evaluated case passes. Missing case folders or
missing result files are marked as `NOT_FOUND`.

Use `--case` for single-case debugging. Omit it only for a complete mode run.

## Comparison Semantics

Each output file has a `config.json` entry that declares the columns to compare,
their matcher types, and the key columns used for row alignment. Maintainer
checks require the configured columns to match the GT output columns exactly.

Numeric columns use a general-purpose tolerance. Nonzero numeric values match
when `abs(gt - cand) / max(abs(gt), abs(cand)) < 0.02`; if either side is zero,
they match when `abs(gt - cand) < 0.02`. The same numeric matcher is used for
numeric key columns, because many PrepBench configs use all output columns as an
unordered row signature rather than a separate database-style primary key.

## Programmatic API

For one candidate directory:

```python
from evaluate.core import evaluate

passed, first_error = evaluate(
    gt_dir="src/evaluate/gt/case_001",
    cand_dir="@runs/my_agent/clarified/case_001/result",
)
```

For the public run-root layout:

```python
from prepbench.submission_eval import evaluate_submission

summary = evaluate_submission(
    mode="clarified",
    run_root="@runs/my_agent/clarified",
)
```

`first_error` is `None` when the candidate passes. Otherwise, it contains the
first meaningful mismatch. Use `evaluation/summary.csv` to inspect one row per
case.
