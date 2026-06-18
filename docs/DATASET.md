# Dataset

PrepBench contains 306 data-preparation cases. Each case pairs public task inputs
with benchmark-side assets used for evaluation and user simulation.

## Public Case Inputs

For `interactive` and `direct` tracks, participant agents should read only:

```text
data/case_xxx/query.md
data/case_xxx/inputs/*.csv
```

`query.md` is the natural-language request available to the model-under-test.
`inputs/*.csv` are the raw input tables.

For the `oracle` track, the agent may use:

```text
data/case_xxx/query_full.md
data/case_xxx/inputs/*.csv
```

`query_full.md` is the clarified instruction. It should not be used in
`interactive` or `direct` runs.

## Additional Case Assets

The following files are included to support benchmark execution, but they must not
be used as model inputs except where explicitly allowed by the `oracle` track:

```text
data/case_xxx/query_full.md
data/case_xxx/amb_kb.json
src/evaluate/gt/case_xxx/config.json
src/evaluate/gt/case_xxx/output_*.csv
```

Meanings:

- `query_full.md`: clarified specification used by benchmark-side components.
- `amb_kb.json`: ambiguity slots used by the user simulator and disambiguation
  metrics.
- `config.json`: typed output-comparison rules for the evaluator.
- `output_*.csv`: ground-truth prepared tables.

## Asset Visibility

| Asset | `interactive` | `direct` | `oracle` | Purpose |
| --- | --- | --- | --- | --- |
| `query.md` | Visible | Visible | Optional | Original task instruction |
| `query_full.md` | Hidden | Hidden | Visible | Clarified task instruction |
| `inputs/*.csv` | Visible | Visible | Visible | Raw input tables |
| `amb_kb.json` | Hidden | Hidden | Hidden | Simulator and disambiguation metadata |
| `src/evaluate/gt/` | Hidden | Hidden | Hidden | Evaluation target |
| private reference solutions | Hidden | Hidden | Hidden | Simulator-side evidence |

## Expected Layout

```text
data/
  case_001/
    query.md
    query_full.md
    amb_kb.json
    inputs/
      input_01.csv
  ...

src/evaluate/gt/
  case_001/
    config.json
    output_01.csv
  ...
```

## Integrity Check

Run:

```bash
python scripts/validate_dataset.py
```

The validator checks:

- contiguous `case_xxx` numbering
- required public and benchmark-side files
- readable JSON files
- at least one input CSV per case
- at least one GT output CSV per case
- one GT directory per data case

Expected summary:

```text
cases=306 input_tables=829 gt_cases=306 errors=0
```

## Source Links

`data/case_links.txt` records source challenge links used by the benchmark authors.
It is metadata for traceability, not an execution input.
