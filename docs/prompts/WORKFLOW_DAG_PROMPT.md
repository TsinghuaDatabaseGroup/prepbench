# Workflow DAG Prompt

This page summarizes the public py2flow workflow contract used by PrepBench
`workflow` mode agents.

Canonical source files:

- `src/agents/prompts/flow_agent.yaml`
- `src/agents/prompts/templates/flow_agent.jinja2`

The YAML file is the versioned operator contract. The workspace symlink
`workflow_prompt.yaml` points to that YAML file.

## Required Output

The agent may produce one JSON object:

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
      "params": {"path": "output_01.csv"}
    }
  }
}
```

## Core Rules

- Use only supported node kinds: `input`, `project`, `filter`, `join`, `union`,
  `aggregate`, `dedup`, `sort`, `pivot`, `output`, and `script`.
- Keep the graph acyclic and make every node contribute to at least one output.
- Read input tables from `inputs/`.
- Write final output tables as `output_*.csv`.
- Prefer standard operators over `script`.
- Use `script` only as a last resort; it must define
  `transform(df, pd, np) -> DataFrame`.
- Return only valid JSON.
