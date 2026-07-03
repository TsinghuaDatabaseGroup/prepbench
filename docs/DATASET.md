# Dataset

PrepBench contains 306 data-preparation cases. Each case pairs public task inputs
with benchmark-side assets used for evaluation and user simulation. The current
public release is `v0.1.0`.

## Public Case Inputs

For `direct` and `interactive` settings, participant agents should read only:

```text
data/case_xxx/query.md
data/case_xxx/inputs/*.csv
```

`query.md` is the natural-language request available to the model-under-test.
`inputs/*.csv` are the raw input tables.

For the `oracle` setting, the agent may use:

```text
data/case_xxx/query_full.md
data/case_xxx/inputs/*.csv
```

`query_full.md` is the clarified instruction. It should not be used in `direct`
or `interactive` runs. It is not an answer file and does not expose GT outputs.

## Additional Case Assets

The following files are included to support benchmark execution, but they must not
be used as model inputs except where explicitly allowed by the `oracle` setting:

```text
data/case_xxx/query_full.md
data/case_xxx/amb_kb.json
src/evaluate/gt/case_xxx/config.json
src/evaluate/gt/case_xxx/output_*.csv
reference/solutions/case_xxx/solution.py
```

Meanings:

- `query_full.md`: clarified specification used by benchmark-side components.
- `amb_kb.json`: ambiguity slots used by the user simulator and paper-side
  ambiguity analysis.
- `config.json`: typed output-comparison rules for the evaluator.
- `output_*.csv`: ground-truth prepared tables.
- `reference/solutions/`: reference implementations used for reproducibility
  checks and simulator evidence.

## Model-Input Policy

These assets are included in the repository so the benchmark is self-contained.
The table below describes what the model-under-test may read for each setting.

| Asset | `oracle` | `direct` | `interactive` | Purpose |
| --- | --- | --- | --- | --- |
| `query.md` | Optional | Allowed | Allowed | Original task instruction |
| `query_full.md` | Allowed | Not allowed | Not allowed | Clarified task instruction |
| `inputs/*.csv` | Allowed | Allowed | Allowed | Raw input tables |
| `amb_kb.json` | Not allowed | Not allowed | Not allowed | Simulator and ambiguity metadata |
| `src/evaluate/gt/` | Not allowed | Not allowed | Not allowed | Evaluation target |
| `reference/solutions/` | Not allowed | Not allowed | Not allowed | Reference implementation |

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

reference/solutions/
  case_001/
    solution.py
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
- one reference solution per data case

Expected summary:

```text
cases=306 input_tables=829 gt_cases=306 solution_cases=306 errors=0
```

## Source Links

`data/case_links.txt` records source challenge links used by the benchmark authors.
It has one link per case and is metadata for traceability, not an execution input.

The benchmark cases are derived from public Preppin' Data challenge materials.
PrepBench code is MIT-licensed; benchmark data and source-derived assets should
retain source attribution. See [../NOTICE.md](../NOTICE.md) for the repository
attribution note.
