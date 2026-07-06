# Workflow Execution

Workflow mode gives the agent a py2flow operator contract and an executor. The
agent may generate a workflow JSON DAG, execute it, inspect failures, edit the
workflow, and finally leave scored result tables under `result/output_*.csv`.

The workflow JSON itself is a working artifact. PrepBench evaluates only the
final result CSVs.

## Workspace Files

Prepare a workflow workspace:

```bash
python scripts/prepare_run.py \
  --mode workflow \
  --case case_099 \
  --run-root @runs/my_agent/workflow
```

The workspace contains:

```text
@runs/my_agent/workflow/case_099/
  query.md
  inputs/
  simulator.md
  workflow_prompt.yaml
  result/
```

`workflow_prompt.yaml` is a symlink to
`src/agents/prompts/flow_agent.yaml`, which documents the operator contract.

## Workflow Contract

A workflow is a JSON DAG with top-level `id`, `name`, and `nodes`.

Supported node kinds:

```text
input, project, filter, join, union, aggregate, dedup, sort, pivot, output, script
```

Runtime path rules:

- Input nodes read paths such as `inputs/input_01.csv`.
- Output nodes write filenames such as `output_01.csv`.
- The executor maps input paths to the workspace `inputs/` directory.
- The executor maps output filenames to the workspace `result/` directory.

## Python API

Run from inside the case workspace:

Install the repo with `python -m pip install -e .` first, or set
`PYTHONPATH=/path/to/prepbench/src`, so `py2flow` is importable from `@runs/...`.

```python
from py2flow.api import execute_flow_file

execute_flow_file(flow_path="workflow.json")
```

Defaults:

```text
input_root = ./inputs
output_root = ./result
```

Both roots can be overridden when debugging outside a workspace:

```python
execute_flow_file(
    flow_path="workflow.json",
    input_root="data/case_099/inputs",
    output_root="@runs/debug/workflow/case_099/result",
)
```

## CLI Debugging

The CLI is kept as a maintenance/debug entry point:

```bash
PYTHONPATH=src python scripts/execute_workflow.py \
  --flow-path tests/fixtures/workflows/case_099_workflow.json \
  --input-root data/case_099/inputs \
  --case-id case_099 \
  --evaluate \
  --clean-output
```

Default CLI outputs go under:

```text
@runs/workflow_execution/<case_id>/result/output_*.csv
```

## Limitations

- The restored workflow fixture coverage is one case:
  `tests/fixtures/workflows/case_099_workflow.json`.
- Workflows may use at most 3 `script` nodes, and each `script.inline_code`
  must be at most 1500 characters.
- Expressions and `script` nodes restrict imports to trusted data-prep modules,
  but workflow execution is still a trusted-code path, not a sandbox.
