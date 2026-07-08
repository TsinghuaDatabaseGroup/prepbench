# Workflow Execution

Workflow mode asks the agent to produce a workflow JSON file, execute it, and
leave the final scored tables under `result/output_*.csv`. The workflow JSON is
a working artifact; PrepBench evaluates only the final CSVs.

## Workspace

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
  clarification_guide.md
  workflow_prompt.md
  result/
```

`workflow_prompt.md` is the operator guide the agent should use when producing
the workflow JSON.

## Minimal JSON Shapes

A minimal complete workflow reads from `inputs/` and writes to `result/`:

```json
{
  "id": "minimal_flow",
  "name": "Minimal flow",
  "nodes": {
    "src": {
      "kind": "input",
      "params": {"path": "inputs/input_01.csv"}
    },
    "keep_cols": {
      "kind": "project",
      "inputs": {"in": "src"},
      "params": {"select": ["*"]}
    },
    "out": {
      "kind": "output",
      "inputs": {"in": "keep_cols"},
      "params": {"path": "output_01.csv"}
    }
  }
}
```

Union nodes take `inputs.items`, not `left`/`right`:

```json
{
  "id": "union_flow",
  "name": "Union flow",
  "nodes": {
    "a": {"kind": "input", "params": {"path": "inputs/input_01.csv"}},
    "b": {"kind": "input", "params": {"path": "inputs/input_02.csv"}},
    "all_rows": {
      "kind": "union",
      "inputs": {"items": ["a", "b"]},
      "params": {"distinct": false, "align": "by_name", "fill_missing": "null", "type_coerce": "error"}
    },
    "out": {
      "kind": "output",
      "inputs": {"in": "all_rows"},
      "params": {"path": "output_01.csv"}
    }
  }
}
```

## Execute from Code

Agent harnesses should call the Python API and return any structured error to
the agent for revision:

```python
from py2flow.api import run_flow_file

result = run_flow_file(
    flow_path="@runs/my_agent/workflow/case_099/workflow.json",
    input_root="@runs/my_agent/workflow/case_099/inputs",
    output_root="@runs/my_agent/workflow/case_099/result",
    require_outputs=True,
)
```

On success, `result["ok"]` is `True`. On failure, `result["ok"]` is `False` and
`result["error"]` contains fields such as `node_id`, `step_kind`, `field`,
`error_code`, and `help`. Use `require_outputs=True` in workflow-mode harnesses
so execution is treated as failed when no scored `output_*.csv` files are written.

## Execute from CLI

For manual debugging, run the same workflow from the repository root:

```bash
python scripts/execute_workflow.py \
  --flow-path @runs/my_agent/workflow/case_099/workflow.json \
  --input-root @runs/my_agent/workflow/case_099/inputs \
  --output-root @runs/my_agent/workflow/case_099/result
```

Add `--explain` to validate and print a node summary without executing
(`--dry-run` is an alias). Add `--json-errors` to print structured errors to
stderr. Normal execution fails if no `output_*.csv` files are written directly
under `--output-root`.

For a minimal reference runner that wires together clarification, workflow
generation, execution, and optional evaluation, see `examples/run_workflow_agent.py`.
Set `PREPBENCH_AGENT_BASE_URL`, `PREPBENCH_AGENT_MODEL`, and
`PREPBENCH_AGENT_API_KEY` for that example. It is an example harness, not a
required agent framework. To keep the example short, it prompts for workflow
JSON directly; replace that generation step with your own code-to-workflow
logic if that is what your agent evaluates.

## Evaluate

After execution, evaluate the run root:

```bash
python scripts/evaluate_submission.py \
  --mode workflow \
  --run-root @runs/my_agent/workflow \
  --case case_099
```

## Limits

- `workflow_prompt.md` contains the operator contract and generation rules.
- A workflow may use at most 3 `script` nodes.
- Each `script.inline_code` must be at most 1500 characters.
- Workflow execution is a trusted-code path, not a sandbox for untrusted code.
