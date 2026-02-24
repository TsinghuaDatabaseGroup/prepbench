# py2flow

py2flow is a lightweight, pandas-based DAG executor for data preparation/ETL.
It executes a flow (DAG) defined as a Python dict / JSON with a fixed set of operators.

## Supported StepKinds

`input`, `project`, `filter`, `join`, `union`, `aggregate`, `dedup`, `sort`, `pivot`, `output`, `script`

## JSON Schema

Machine-readable flow contract:

- `py2flow/flow.schema.json`

Use it for pre-validation before calling py2flow runtime. Runtime validation in `py2flow/ir.py` remains authoritative.

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

## Python API (file-based inputs)

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

CLI takes explicit `flow.json` and input directory paths.
Input node paths are resolved from `--input-root`.
Other relative paths (for example output files) are resolved relative to `flow.json` directory.

```bash
python -m py2flow.exec_flow \
  --flow-path /path/to/case_dir/flow.json \
  --input-root /path/to/case_dir/inputs
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

py2flow does not sandbox scripts; do not run untrusted code.
