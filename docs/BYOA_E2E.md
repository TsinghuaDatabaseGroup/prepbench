# BYOA E2E Integration (Local Protocol)

This document defines the local (non-network) integration contract for third-party agent frameworks.

For BYOA, PrepBench uses a single setting: **E2E**.  
A framework can submit either:
- **code track** outputs (`solution/cand/*.csv`), or
- **flow track** outputs (`solution/flow_cand/*.csv`).

## Minimal 3-Step Checklist

1) Read public inputs only:
- `data/case_xxx/query.md`
- `data/case_xxx/inputs/*.csv`

2) Write outputs under:
- `@output/<your_framework>/e2e/case_xxx/solution/cand/*.csv`
- or `@output/<your_framework>/e2e/case_xxx/solution/flow_cand/*.csv`

3) Run evaluator:

```bash
PYTHONPATH=src python -m evaluate.batch --results-root @output/<your_framework>/e2e --candidate-kind auto
```

## Reference Implementation

PrepBench provides a reference `PrepAgent` pipeline for E2E:

```bash
./scripts/run_prepagent.sh --case 1 --model openai/gpt-5.2
```

PrepAgent writes to an isolated root:
- `@output/<model_info>/prepagent/case_xxx/solution/...`

`<model_info>` is derived from the last segment of model name and sanitized for paths.
Example: `openai/gpt-5.2` -> `gpt-5.2`.

And can be evaluated with:

```bash
PYTHONPATH=src python -m evaluate.batch --results-root @output/<model_info>/prepagent --candidate-kind auto
```

Source:
- `methods/prepagent/run_prepagent.py`
- `methods/prepagent/README.md`
- `methods/prepagent/prompts/` (PrepAgent-owned prompts/templates)

## 1) Public Inputs Per Case

Only these public inputs are required by participants:
- `data/case_xxx/query.md`
- `data/case_xxx/inputs/*.csv`

`query_full.md`, `amb_kb.json`, GT files, and reference solutions are benchmark-internal assets.
They may exist in the repository for runtime/evaluation, but they are not allowed as method inputs.

## 2) Local User Simulator Interface

Use `simulator.LocalUserSimulatorAPI` (not HTTP).

```python
from simulator import LocalUserSimulatorAPI

api = LocalUserSimulatorAPI()
session = api.start_session(case_id="case_001", run_id="run_001")
resp = api.ask(
    session_id=session["session_id"],
    questions=["What does 'recent' mean in this task?"],
    round=1,
)
```

Notes:
- `start_session(...)` requires internal reference solution for the case.
- Reference solutions are private benchmark assets and are **not** included in this public repository.
- The public repository intentionally does not ship a reference-solutions folder.
- Request access via `j1n9zhe@gmail.com` (see `README.md` for a suggested email format).
- Put the received folder at your local target path, then set `PREPBENCH_SOLUTIONS_ROOT=/absolute/path/to/<solutions_root>`.
- Recommended layout from the distributed package: `case001/solution.py` (legacy forms are also supported).

Response fields include:
- `round`: current round index (required for debugging/audit).
- `answers`: list of answer objects.
- `budget`: round/question usage stats.
- `done`: whether the session reached its budget limits.

`classification` is a strict enum:
- `hit`
- `fallback`
- `refuse_need_data`
- `refuse_too_broad`
- `refuse_illegal`
- `refuse_irrelevant`

No `unknown` fallback class is used in this protocol.

Detailed local contract:
- `docs/contracts/USER_SIMULATOR_LOCAL.md`

## 3) Flow Contract (Machine-Readable)

For flow-track systems, validate generated `flow.json` against:
- `src/py2flow/flow.schema.json`

Runtime validation and execution are still authoritative in:
- `src/py2flow/ir.py`
- `src/py2flow/executor.py`

Operator semantics prompt used by the reference translator:
- `src/agents/prompts/flow_agent.yaml`
- This prompt describes operator constraints and repair policy used by the benchmark reference flow generation.

## 4) Submission Layout

Put generated results under one root (example: `@output/my_framework/e2e/`):

```text
@output/my_framework/e2e/
  case_001/
    solution/
      cand/          # code track (optional)
        output_01.csv
      flow_cand/     # flow track (optional)
        output_01.csv
  case_002/
    solution/
      ...
```

Rules:
- Case folder must be named `case_xxx`.
- CSV file names should match expected names (for example `output_01.csv`).
- A single run root should contain one primary track (code or flow).

## 5) Evaluation

Run local batch evaluation:

```bash
PYTHONPATH=src python -m evaluate.batch --results-root @output/my_framework/e2e --candidate-kind auto
PYTHONPATH=src python -m evaluate.batch --results-root @output/my_framework/e2e --candidate-kind code
PYTHONPATH=src python -m evaluate.batch --results-root @output/my_framework/e2e --candidate-kind flow
```

Generated files:
- `@output/my_framework/e2e/evaluation_summary.csv`
- `@output/my_framework/e2e/acc.txt`

Scoring fields:
- `execution`: `success` | `fail`
- `evaluation`: `correct` | `false`

Ground truth source:
- `evaluate.batch` automatically loads GT from `src/evaluate/gt/case_XXX`.

Important:
- `evaluate.batch` always iterates all GT cases.
- If your framework only generated a subset of cases, the missing cases will be marked `NOT_FOUND`.

Track mapping for `acc.txt`:
- `--candidate-kind code` -> code-track accuracy
- `--candidate-kind flow` -> flow-track accuracy
- `--candidate-kind auto` -> flow first, fallback to code

If your framework includes interactive disambiguation, compute disambiguation precision/recall/F1 with:

```bash
PYTHONPATH=src python -m evaluate.disamb --results-root @output/my_framework/e2e
```

Metric note:
- Aggregate precision uses `unique_hit_slots / questions_used`.
