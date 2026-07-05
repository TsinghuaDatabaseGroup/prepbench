# Workflow Execution

This page documents the experimental PrepBench workflow-execution path:

```text
clarify -> generate solution.py -> translate solution.py to flow.json -> execute flow.json -> evaluate output_*.csv
```

The public leaderboard interface is still the table-output evaluator described
in `docs/EVALUATION.md`. Workflow execution is an experimental internal path for
checking whether an agent-produced workflow can reproduce candidate tables.

## Files

- Workflow-generation prompt: `src/agents/prompts/flow_agent.yaml`
- Prompt template: `src/agents/prompts/templates/flow_agent.jinja2`
- Runtime executor package: `src/py2flow/`
- Wrapper CLI: `scripts/execute_workflow.py`
- Example workflow fixture: `data/case_099/flow_compressed.json`

## Workflow Contract

A workflow is a JSON DAG with top-level `id`, `name`, and `nodes`.

Supported node kinds:

```text
input, project, filter, join, union, aggregate, dedup, sort, pivot, output, script
```

Runtime path rules:

- Input nodes should read `inputs/<file>.csv`.
- Output nodes should write `flow_cand/output_*.csv`.
- The wrapper maps `inputs/...` to the provided `--input-root`.
- The wrapper maps `flow_cand/...` to the provided `--output-root`.

## Execute One Workflow

```bash
PYTHONPATH=src python scripts/execute_workflow.py \
  --flow-path data/case_099/flow_compressed.json \
  --input-root data/case_099/inputs \
  --case-id case_099 \
  --evaluate \
  --clean-output
```

Default generated outputs go under:

```text
@output/workflow_execution/<case_id>/workflow/cand/output_*.csv
```

The command prints a JSON summary containing generated output files and, when
`--evaluate` is set, the evaluator result.

## Direct Executor

Use the lower-level py2flow CLI when evaluation is not needed:

```bash
PYTHONPATH=src python -m py2flow.exec_flow \
  --flow-path data/case_099/flow_compressed.json \
  --input-root data/case_099/inputs \
  --output-root @output/workflow_execution/case_099/workflow/cand
```

## Limitations

- The restored fixture coverage is one case: `case_099`.
- Expressions and `script` nodes restrict imports to trusted data-prep modules,
  but workflow execution is still a trusted-code path, not a sandbox.
- Workflow execution is separate from the public table-output evaluator.
