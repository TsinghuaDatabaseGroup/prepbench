# Workflow DAG Prompt

This is the prompt contract for the workflow-generation step in the experimental
PrepBench e2e path.

Canonical source files:

- `src/agents/prompts/flow_agent.yaml`
- `src/agents/prompts/templates/flow_agent.jinja2`

Use the YAML file as the versioned prompt body because it carries the full
operator contract. The template injects `solution.py` and optional retry
feedback.

## System Prompt

```text
You are a senior data engineer translating pandas/Python ETL code into a py2flow DAG.

Task: convert the given solution.py into a single flow.json that py2flow can
validate and execute to produce the same output CSV files.

Output ONLY a valid JSON object. No markdown, no explanation, no extra text.
```

## Required Output

The model must return one JSON object:

```json
{
  "id": "case_xxx_flow",
  "name": "Case xxx workflow",
  "nodes": {
    "input_node": {
      "kind": "input",
      "params": {"path": "inputs/input_01.csv"}
    },
    "output_node": {
      "kind": "output",
      "inputs": {"in": "upstream_node"},
      "params": {"path": "flow_cand/output_01.csv"}
    }
  }
}
```

## Core Rules

- Use only supported node kinds: `input`, `project`, `filter`, `join`, `union`,
  `aggregate`, `dedup`, `sort`, `pivot`, `output`, and `script`.
- Keep the graph acyclic and make every node contribute to at least one output.
- Read from `inputs/<file>.csv`.
- Write to `flow_cand/output_*.csv`.
- Prefer standard operators over `script`.
- Use `script` only as a last resort; it must define
  `transform(df, pd, np) -> DataFrame`.
- Use top-level `project.map[].when` for row conditions; do not emit legacy
  `args.when`.
- Treat `project.expand` as one object, not an array.
- `script.deterministic` and `script.side_effects` are optional metadata with
  defaults `true` and `false`.
- Return only valid JSON.

## Retry Feedback

When a previous attempt fails, pass feedback into the template as:

```json
{
  "type": "json_parse | validation | execution | no_outputs",
  "message": "human-readable error",
  "details": {}
}
```

The model should fix only the failed layer:

- `json_parse`: fix JSON syntax and escaping.
- `validation`: fix schema, unsupported kinds, missing params, or references.
- `execution`: fix the failed node path and immediate dependencies.
- `no_outputs`: add connected `output` nodes writing `flow_cand/output_*.csv`.
