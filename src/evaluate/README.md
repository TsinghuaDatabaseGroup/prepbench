# Evaluator

Minimal evaluator for comparing a candidate output directory against a ground-truth (GT) directory using a GT-provided `config.json`.

## Scope
- Input: `gt_dir` (must contain `config.json`) and `cand_dir`.
- Output: a boolean pass/fail plus **only the first mismatch** detail.
- Fail-fast: evaluation stops at the first meaningful mismatch.
- Includes a batch CLI for evaluating all case outputs under one results root.

## Public API

```python
from evaluate.core import evaluate

passed, first_error = evaluate(gt_dir, cand_dir, config_path=None)
```

Return value:
- `passed`: `True` if all files match.
- `first_error`: `None` on success, otherwise a dict describing the first mismatch.

`first_error` schema (example):
```json
{
  "error_type": "ROW_COUNT_MISMATCH",
  "message": "File output_01.csv: gold=100, cand=99",
  "file": "output_01.csv",
  "detail": {
    "...": "optional fields depending on error"
  }
}
```

## config.json
The GT directory must include `config.json` with this shape:

```json
{
  "files": {
    "output_01.csv": {
      "ignore_order": true,
      "key": ["id"],
      "columns": {
        "id": "number",
        "name": "text_norm",
        "created_at": "datetime"
      }
    }
  }
}
```

Notes:
- `key` is required and must be non-empty.
- `columns` defines types for **all** columns used in comparison.
- `ignore_order` affects **non-key** column comparison only.

## Matching rules (high-level)
- Files must exist on both sides and counts must match.
- Rows are aligned by key; key comparison is type-aware and tolerant for `number`.
- If a GT key has multiple candidate matches, this is an error (fail-fast).
- First mismatch returned could be one of:
  - `CONFIG_MISSING`, `FILE_COUNT_MISMATCH`, `MISSING_FILE`, `READ_ERROR`,
  - `MISSING_COLUMNS`, `ROW_COUNT_MISMATCH`, `NON_UNIQUE_KEY`, `KEY_MISMATCH`,
  - `VALUE_MISMATCH`, `ALIGNMENT_ERROR`, `EXCEPTION`.

For `KEY_MISMATCH`, `detail.reason` can be:
- `missing_key`
- `multiple_matches`
- `extra_keys`

## Dependencies
- `pandas`

## Examples

```python
from evaluate.core import evaluate

ok, err = evaluate("/path/to/gt", "/path/to/cand")
if ok:
    print("PASS")
else:
    print("FAIL", err)
```

## Batch CLI

Batch mode evaluates all `case_*` folders under a results root and writes one CSV.

```bash
python -m evaluate.batch --results-root @output/<model>/<run_mode>
```

Behavior:
- GT is always loaded from `evaluate/gt/case_xxx`.
- Every GT case is written to the summary CSV. Missing run outputs are marked as `NOT_FOUND`.
- Candidate directory is auto-detected per case:
  - prefer `solution/flow_cand` when present with CSV files
  - otherwise use `solution/cand`
- Candidate selection can be forced:
  - `--candidate-kind auto` (default): prefer `flow_cand`, then `cand`
  - `--candidate-kind code`: only `solution/cand`
  - `--candidate-kind flow`: only `solution/flow_cand`
- Output CSV is written to:
  - `<results_root>/evaluation_summary.csv`
- Accuracy scalar is written to:
  - `<results_root>/acc.txt`

Examples:

```bash
python -m evaluate.batch --results-root @output/<model>/<run_mode> --candidate-kind auto
python -m evaluate.batch --results-root @output/<model>/<run_mode> --candidate-kind code
python -m evaluate.batch --results-root @output/<model>/<run_mode> --candidate-kind flow
```

CSV columns:
- `case_name`
- `execution` (`success` | `fail`)
- `evaluation` (`correct` | `false`)
- `candidate_dir`
- `gt_dir`
- `error_type`
- `error_message`

## Disambiguation CLI

Computes disambiguation precision/recall/F1 from clarify artifacts (`clarify/summary.json`)
against ambiguity slots from `data/case_xxx/amb_kb.json`.

Scoring note:
- Aggregate precision uses `unique_hit_slots / questions_used`.
- Per-type question counts are based on hit answers with resolvable slot ids.

```bash
python -m evaluate.disamb --results-root @output/<model>/<run_mode>
```

Optional:

```bash
python -m evaluate.disamb --results-root @output/<model>/<run_mode> --data-root /path/to/data
```

Generated files:
- `<results_root>/disamb_summary.csv` (per-case metrics and status)
- `<results_root>/disamb_by_type.csv` (per ambiguity type metrics)
- `<results_root>/disamb_metrics.json` (aggregate metrics)
- `<results_root>/disamb_f1.txt` (single scalar F1)
