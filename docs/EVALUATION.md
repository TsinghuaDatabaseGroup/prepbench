# Evaluation

PrepBench evaluates generated output tables against per-case ground truth.

## Settings

PrepBench uses three public settings, ordered from easiest to hardest. They
differ only in what the agent may read and whether it can ask clarification
questions. Evaluation is identical in all settings: compare candidate output
tables with the expected output tables.

| Setting | Agent input | Interaction | Main question |
| --- | --- | --- | --- |
| `oracle` | `query_full.md` + `inputs/*.csv` | No simulator | Can the agent prepare the tables from a clarified instruction? |
| `direct` | `query.md` + `inputs/*.csv` | No simulator | Can the agent prepare the tables from the original instruction alone? |
| `interactive` | `query.md` + `inputs/*.csv` | May call `LocalUserSimulatorAPI` | Can the agent resolve ambiguity through clarification and prepare the tables? |

`oracle` means the instruction is clarified. It does not allow access to GT
outputs, reference solutions, or simulator metadata.

The evaluator itself is setting-agnostic. Put each run under a setting-named
results root, such as `@output/my_agent/interactive`.

## Candidate Layout

Write outputs under:

```text
@output/my_agent/interactive/
  case_001/
    solution/
      cand/
        output_01.csv
```

Rules:

- Case folders must use `case_xxx` names.
- Candidate CSVs must live under `solution/cand/`.
- Candidate output file names must match the expected GT names, such as
  `output_01.csv`.

## Comparison Semantics

Each output file has a `config.json` entry that declares the columns to compare,
their matcher types, and the key columns used for row alignment. Maintainer
checks require the configured columns to match the GT output columns exactly.

Numeric columns use a general-purpose tolerance. Nonzero numeric values match
when `abs(gt - cand) / max(abs(gt), abs(cand)) < 0.02`; if either side is zero,
they match when `abs(gt - cand) < 0.02`. The same numeric matcher is used for
numeric key columns, because many PrepBench configs use all output columns as an
unordered row signature rather than a separate database-style primary key.

## Batch Evaluation

```bash
PYTHONPATH=src python -m evaluate.batch --results-root @output/my_agent/interactive
```

Generated files:

```text
@output/my_agent/interactive/evaluation_summary.csv
@output/my_agent/interactive/acc.txt
```

The batch evaluator iterates every GT case. If your run contains only a subset,
missing cases are marked as `NOT_FOUND`, and `acc.txt` still uses all GT cases as
the denominator. Use subset runs for local debugging only; official leaderboard
submissions should include all 306 cases for one setting.

## Single-Case Debugging

For a known-correct smoke test:

```bash
python examples/evaluate_demo.py
```

For your own candidate output:

```bash
PYTHONPATH=src python -m evaluate.batch --results-root @output/my_agent/interactive
rg '^case_001,' @output/my_agent/interactive/evaluation_summary.csv
```

## Programmatic API

```python
from evaluate.core import evaluate

passed, first_error = evaluate(
    gt_dir="src/evaluate/gt/case_001",
    cand_dir="@output/my_agent/interactive/case_001/solution/cand",
)
```

`first_error` is `None` when the candidate passes. Otherwise, it contains the
first meaningful mismatch. This API is fail-fast within one case; use
`evaluation_summary.csv` from batch evaluation to inspect one result row per
case.

## Reporting

For leaderboard submission, provide candidate outputs for all 306 cases in one
setting. The leaderboard score is the table accuracy written to `acc.txt` by the
public evaluator; participants do not need to compute additional metrics.
