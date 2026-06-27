# Evaluation

PrepBench evaluates generated output tables against per-case ground truth.

## Tracks

PrepBench uses three public tracks. They differ only in what the agent is allowed
to see and whether it can ask clarification questions.

| Track | Agent input | Interaction | Main question |
| --- | --- | --- | --- |
| `interactive` | `query.md` + `inputs/*.csv` | May call `LocalUserSimulatorAPI` | Can the agent resolve ambiguity through clarification and prepare the tables? |
| `direct` | `query.md` + `inputs/*.csv` | No simulator | Can the agent prepare the tables from the original instruction alone? |
| `oracle` | `query_full.md` + `inputs/*.csv` | No simulator | Can the agent prepare the correct tables when the instruction is clarified? |

The evaluator itself is track-agnostic. Put each run under a track-named results
root, such as `@output/my_agent/interactive`.

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
missing cases are marked as `NOT_FOUND`.

## Single-Case Debugging

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
first meaningful mismatch.

## Disambiguation Metrics

If your agent stores clarify artifacts, run:

```bash
PYTHONPATH=src python -m evaluate.disamb --results-root @output/my_agent/interactive
```

Generated files:

```text
@output/my_agent/interactive/disamb_summary.csv
@output/my_agent/interactive/disamb_by_type.csv
@output/my_agent/interactive/disamb_metrics.json
@output/my_agent/interactive/disamb_f1.txt
```

## Reporting

For each run, report:

- track name: `interactive`, `direct`, or `oracle`
- method or model name
- number of evaluated cases
- table accuracy from `acc.txt`
- disambiguation metrics, if the `interactive` track used clarification logs
