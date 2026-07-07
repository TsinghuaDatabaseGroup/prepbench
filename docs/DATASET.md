# Dataset

PrepBench contains 306 data-preparation cases. Each case pairs public task inputs
with benchmark-side assets used for evaluation and user simulation. The current
public release is `v0.1.0`.

## Case Files

Each case has this shape:

```text
data/case_001/
  query.md
  query_full.md
  amb_kb.json
  inputs/
    input_01.csv
```

Ground truth lives separately:

```text
src/evaluate/gt/case_001/
  config.json
  output_01.csv
```

Reference solutions live under `reference/solutions/` and support reproducibility
checks and simulator evidence.

## Public Workspaces

Participants should run agents from prepared workspaces rather than reading case
files directly:

```bash
python scripts/prepare_run.py \
  --mode clarified \
  --case case_001 \
  --run-root @runs/my_agent/clarified
```

For a complete mode run, prepare all evaluator cases:

```bash
python scripts/prepare_run.py \
  --mode clarified \
  --all \
  --run-root @runs/my_agent/clarified
```

`--all` uses the GT case set and requires matching `data/case_xxx` directories.

Workspace contents by mode:

| Mode | `query.md` points to | Other files |
| --- | --- | --- |
| `clarified` | `data/case_xxx/query_full.md` | `inputs/`, `result/` |
| `interactive` | `data/case_xxx/query.md` | `inputs/`, `simulator.md`, `result/` |
| `workflow` | `data/case_xxx/query.md` | `inputs/`, `simulator.md`, `workflow_prompt.yaml`, `result/` |

`inputs/` is a real workspace directory containing per-file symlinks to the case
input CSVs. This keeps the agent-facing workspace simple while avoiding a
directory symlink back to the full case directory.

## Allowed-Input Policy

The benchmark is self-contained, so files used by the simulator and evaluator
remain in the repository. The model-under-test should only read the assets
present in its prepared workspace.

| Asset | `clarified` | `interactive` | `workflow` | Purpose |
| --- | --- | --- | --- | --- |
| workspace `query.md` | Allowed | Allowed | Allowed | Task instruction for the selected mode |
| workspace `inputs/` | Allowed | Allowed | Allowed | Raw input tables |
| workspace `simulator.md` | Not present | Allowed | Allowed | Local simulator usage note |
| workspace `workflow_prompt.yaml` | Not present | Not present | Allowed | Workflow/operator contract |
| `data/case_xxx/query_full.md` outside workspace | Already exposed through workspace | Not allowed | Not allowed | Clarified instruction |
| `data/case_xxx/amb_kb.json` | Not allowed | Not allowed | Not allowed | Simulator metadata |
| `src/evaluate/gt/` | Not allowed | Not allowed | Not allowed | Evaluation target |
| `reference/solutions/` | Not allowed | Not allowed | Not allowed | Reference implementation |

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

`data/case_links.txt` records source challenge links used by the benchmark
authors. It has one link per case and is metadata for traceability, not an
execution input.

The benchmark cases are derived from public Preppin' Data challenge materials.
PrepBench code is MIT-licensed; benchmark data and source-derived assets should
retain source attribution. See [../NOTICE.md](../NOTICE.md) for the repository
attribution note.
