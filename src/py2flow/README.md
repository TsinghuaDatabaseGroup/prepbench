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

## Operator Contract Summary

The versioned prompt in `src/agents/prompts/flow_agent.yaml` is the generation-time
operator contract. This section is the human-readable runtime summary. Each entry
lists what the operator is for, when to reach for it, and the one gotcha that most
often bites a generated flow.

### input

- **Purpose:** Read a CSV/line file or materialize inline rows.
- **When to use:** Every source table. Use `mode="line"` only for true line-based
  text (single `raw` column); use `data`/`source_type="inline"` for fixtures.
- **Key params:** `path`, `mode`, CSV read options (`delimiter`, `encoding`,
  `header`, `na_values`, `parse_dates`, `dtype`, `skiprows`, `on_bad_lines`, etc.),
  `data`, `source_type`.
- **Gotcha:** When the source data can be mistaken for a header row, set
  `header: null` and address columns positionally (`df.iloc[:, i]`) downstream.
  `encoding` may be a list; the runtime tries each until one succeeds.

### project

- **Purpose:** Select, rename, compute, cast, map, and scaffold-expand columns.
- **When to use:** The default shaping operator. Prefer it over `script` for any
  per-column transform.
- **Key params:** `select`, `rename`, `compute`, `cast`, `map`, `expand`,
  `promote_row_to_header`, `on_error`, `error_cols`.
- **Execution order (fixed):**
  `promote_row_to_header -> select -> rename -> compute -> cast -> map -> expand`.
- **Gotcha:** `select` runs *before* `compute`, so a column produced by `compute`
  cannot be named in the same node's `select`. Split into two project nodes.

### filter

- **Purpose:** Keep rows matching a boolean expression.
- **When to use:** Row predicates over one table.
- **Key params:** `predicate` (required), `null_as_false` (default `true`).
- **Gotcha:** The predicate must return a boolean Series aligned to the frame. For
  row-wise cross-column logic use vectorized boolean ops, not a Series-valued
  string method call.

### join

- **Purpose:** Relational joins, semi/anti joins, and narrow substring fuzzy joins.
- **When to use:** Combining two tables. Use `semi`/`anti` to filter the left table
  by key membership; use a cross join (`on=["k"]` with a constant `k=1`) for
  cartesian products.
- **Key params:** `how`, `on` or `left_on`/`right_on`, `null_equal`, `suffixes`,
  `select_left`, `select_right`, `validate`, `fuzzy_match`.
- **Gotcha:** `select_left`/`select_right` do **not** apply to `semi`/`anti` (those
  return left rows only). `fuzzy_match` is intentionally narrow; see subcontracts.

### union

- **Purpose:** Stack two or more tables by column name.
- **When to use:** Concatenating same-shaped results (e.g. branch outputs).
- **Key params:** `distinct` (required bool), `align` (`by_name` only),
  `fill_missing` (`null|error`), `type_coerce` (`error` only).
- **Gotcha:** `distinct` is required; validation fails without it. `align` is
  by-name only; there is no positional union.

### aggregate

- **Purpose:** Grouped or scalar aggregation.
- **When to use:** Counts/sums/etc. per group, or a single scalar row when
  `group_keys` is empty.
- **Key params:** `group_keys` (list, may be empty), `aggs` (required),
  `having`, `null_group` (default `true`).
- **Gotcha:** Every `aggs` item needs `expr` except `func="count"`. `null_group`
  keeps null keys as their own group.

### dedup

- **Purpose:** Drop duplicate rows or duplicate keys with deterministic tie-breaks.
- **When to use:** Collapsing to one row per key. Use `output="keys_only"` to get
  the distinct key set (handy as an anti-join right side).
- **Key params:** `keys` (null or list), `output` (`all_cols|keys_only`), `keep`
  (`first|last|none`), `order_by`.
- **Gotcha:** `keep` in `first|last` with `output="all_cols"` **requires** a
  non-empty `order_by` tiebreaker, or validation fails (nondeterministic result).

### sort

- **Purpose:** Stable global or per-group ordering.
- **When to use:** Ordering the final output, or ranking within a group.
- **Key params:** `order_by` (required), `stable` (default `true`), `limit`,
  `partition_by`, `limit_per_group`.
- **Gotcha:** `partition_by` only takes effect when `limit_per_group` is also set;
  alone it does nothing.

### pivot

- **Purpose:** Wide/long reshaping plus dirty-table layout-repair macros.
- **When to use:** `pivot_longer`/`pivot_wider` for clean relational reshapes;
  `pivot_longer_from_rows`/`pivot_longer_paired` only for repairing messy source
  layouts that a plain melt/pivot cannot express; reach for these before `script`.
- **Key params:** `mode` plus mode-specific params.
- **Gotcha:** The `_from_rows`/`_paired` macros are layout repair, not general
  relational algebra; do not use them where a standard `pivot_longer` works.

### output

- **Purpose:** Write a CSV output table.
- **When to use:** Terminal node(s); every flow needs at least one.
- **Key params:** `path`, `schema` (`columns`/`order`/`dtype`), `schema_enforce`,
  `write_order` (default `true`), `datetime_format`, `encoding`, `lineterminator`.
- **Gotcha:** Column order is only enforced when `schema.order`/`schema.columns` is
  given. Evaluation is key-based, but if final order matters, sort upstream and set
  the schema order explicitly.

### script

- **Purpose:** Last-resort trusted Python transform.
- **When to use:** Only when no combination of the operators above can express the
  step. Keep `inline_code` short (target <= 1500 chars).
- **Key params:** `inline_code`, optional `deterministic`, optional `side_effects`.
- **Gotcha:** `inline_code` must define `transform(df, pd, np) -> DataFrame`.
  Imports are restricted to the trusted allowlist (same as expressions).

### Important subcontracts

- `project.map` primitive transforms: `trim`, `lower`, `upper`, `regex_replace`, `regex_extract`, `html_strip`, `squeeze_whitespace`, `split`, `tokenize`, `explode`, `fillna`, `map_values`.
- `project.map` convenience macros: `complete_calendar`, `parse_date_multi`, `date_range`, `date_range_to_start`, `date_year_only`, `group_cumcount`, `format_number`.
- `project.map[].when` is a row-level condition and should be emitted as a top-level map item field. It is not supported for `explode`, `regex_extract`, or `complete_calendar`.
- `project.expand` requires `keys`, `from_col`, `expand_col`, and exactly one of `to_col`, `to_value`, or `to_value_expr`. Prefer it over `script` for calendar/range scaffold generation.
- `join.fuzzy_match=true` is intentionally narrow: one key per side, `how` in `left|inner`, substring containment only, shortest containing right-side string wins, and right-row order breaks ties.
- `pivot_longer_from_rows` and `pivot_longer_paired` are layout-repair macros for dirty source tables, not general relational algebra.
- `script.inline_code` must define `transform(df, pd, np) -> DataFrame`; `deterministic` defaults to `true` and `side_effects` defaults to `false`.

### Cross-operator gotchas (most common failures)

- **project:** `select` precedes `compute`; never select a not-yet-computed column.
- **union:** `distinct` is mandatory.
- **dedup:** `keep=first/last` needs an `order_by` tiebreaker.
- **sort:** `partition_by` is inert without `limit_per_group`.
- **join:** `select_left`/`select_right` are ignored for `semi`/`anti`.
- **script vs operators:** reach for `expand` (scaffolds), `pivot_*` (layout repair),
  and `map` macros before writing a `script` node.

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
