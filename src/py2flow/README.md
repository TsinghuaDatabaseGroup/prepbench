# py2flow

py2flow is a lightweight, pandas-based DAG executor for data preparation/ETL.
It executes a flow (DAG) defined as a Python dict / JSON with a fixed set of operators.

## Supported StepKinds

`input`, `project`, `filter`, `join`, `union`, `aggregate`, `dedup`, `sort`, `pivot`, `output`, `script`

## JSON Schema

Machine-readable flow contract:

- `py2flow/flow.schema.json`

Use it for pre-validation before calling py2flow runtime. Runtime validation in `py2flow/ir.py` remains authoritative.

## Contract Notes

- `project.expand` is one object, not an array: `{keys, from_col, expand_col, ...}`.
- `project.map[].when` is a top-level row condition beside `col/op/args`. Legacy `args.when` is still accepted when it does not conflict.
- `output.write_order=true` writes columns according to `schema.order` or `schema.columns` when provided.
- `project.map` contains primitive transforms plus benchmark convenience macros. `pivot_longer_from_rows` and `pivot_longer_paired` are layout-repair macros for dirty tables.

## Operator Contract

The canonical operator contract lives in `src/agents/prompts/flow_agent.yaml`
(the file symlinked into workflow workspaces as `workflow_prompt.yaml`). It
defines supported node kinds, parameters, execution order, and common pitfalls.

Supported kinds: `input`, `project`, `filter`, `join`, `union`, `aggregate`,
`dedup`, `sort`, `pivot`, `output`, `script`.

Refer to `flow_agent.yaml` for full parameter specs and the operator cookbook.

## Python API (in-memory inputs)

Use `input_tables` to inject pandas DataFrames by input node id.
This takes precedence over file reads for those nodes.

```python
import pandas as pd
from py2flow.api import execute_flow_dict

flow = {
    "id": "demo",
    "name": "demo",
    "nodes": {
        "in": {"kind": "input", "params": {"path": "ignored.csv"}},
        "p": {
            "kind": "project",
            "inputs": {"in": "in"},
            "params": {"compute": [{"as": "total", "expr": "df['qty'] * df['price']"}]},
        },
        "o": {"kind": "output", "inputs": {"in": "p"}, "params": {"path": "out.csv"}},
    },
}

orders = pd.DataFrame({"qty": [2, 1], "price": [5, 10]})

result = execute_flow_dict(
    flow,
    base_path="/tmp",  # optional, used by Output to resolve paths
    input_tables={"in": orders},
    keep="outputs",
)
```

## Python API (workspace flow file)

PrepBench workflow mode uses `execute_flow_file` from inside a prepared case
workspace. By default it reads inputs from `./inputs` and writes outputs to
`./result`.

```python
from py2flow.api import execute_flow_file

execute_flow_file(flow_path="workflow.json")
```

Use explicit roots when debugging outside a workspace:

```python
from py2flow.api import execute_flow_file

execute_flow_file(
    flow_path="tests/fixtures/workflows/case_099_workflow.json",
    input_root="data/case_099/inputs",
    output_root="@runs/debug/workflow/case_099/result",
)
```

## Python API (file-based flow dict)

```python
from py2flow.api import execute_flow_dict

flow = {
    "id": "demo",
    "name": "demo",
    "nodes": {
        "in": {"kind": "input", "params": {"path": "inputs/orders.csv"}},
        "f": {"kind": "filter", "inputs": {"in": "in"}, "params": {"predicate": "df['qty'] > 0"}},
        "o": {"kind": "output", "inputs": {"in": "f"}, "params": {"path": "output/result.csv"}},
    },
}

execute_flow_dict(flow, base_path="/data", keep="outputs")
```

## CLI (path-based)

CLI takes explicit paths for the workflow JSON, input directory, and output
directory. Input node paths are resolved under `--input-root`; output node paths
are resolved under `--output-root`. Other relative paths are resolved relative to
the workflow JSON directory.

```bash
PYTHONPATH=src python -m py2flow.exec_flow \
  --flow-path tests/fixtures/workflows/case_099_workflow.json \
  --input-root data/case_099/inputs \
  --output-root @runs/workflow_execution/case_099/result
```

PrepBench also provides a wrapper that can evaluate generated workflow outputs
against GT:

```bash
PYTHONPATH=src python scripts/execute_workflow.py \
  --flow-path tests/fixtures/workflows/case_099_workflow.json \
  --input-root data/case_099/inputs \
  --case-id case_099 \
  --evaluate \
  --clean-output
```

## Errors

- `FlowValidationError`: invalid DAG structure or parameters.
- `FlowExecutionError`: operator execution failed (includes node id, kind, params, and cause).

## Script node

`script` nodes execute trusted inline Python code. The code must define:

```python
def transform(df, pd, np):
    return df
```

`deterministic` defaults to `true`; `side_effects` defaults to `false`. Scripts and expressions share the same trusted import allowlist (`math`, `datetime`, `pandas`, `numpy`, `re`, and other standard data-prep modules). py2flow is still a trusted-workflow executor, not a general sandbox; do not run untrusted workflows.

Runtime validation allows at most 3 `script` nodes per workflow, and each
`inline_code` value must be at most 1500 characters.
