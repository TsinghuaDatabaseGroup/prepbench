<h1 align="center">PrepBench</h1>

<p align="center">
  <strong>How far are we from natural-language-driven data preparation?</strong>
</p>

<p align="center">
  <a href="https://arxiv.org/abs/2605.08687"><img alt="arXiv" src="https://img.shields.io/badge/arXiv-2605.08687-b31b1b.svg"></a>
  <a href="https://github.com/TsinghuaDatabaseGroup/prepbench/actions/workflows/ci.yml"><img alt="CI" src="https://github.com/TsinghuaDatabaseGroup/prepbench/actions/workflows/ci.yml/badge.svg"></a>
  <img alt="Python 3.9+" src="https://img.shields.io/badge/python-3.9%2B-blue.svg">
  <a href="LICENSE"><img alt="License: MIT" src="https://img.shields.io/badge/license-MIT-green.svg"></a>
</p>

<p align="center">
  <a href="https://arxiv.org/abs/2605.08687">Paper</a> |
  <a href="docs/DATASET.md">Dataset</a> |
  <a href="docs/EVALUATION.md">Evaluation</a> |
  <a href="docs/USER_SIMULATOR.md">User Simulator</a> |
  <a href="docs/WORKFLOW_EXECUTION.md">Workflow Execution</a> |
  <a href="docs/RESULTS.md">Results</a> |
  <a href="CITATION.cff">Citation</a>
</p>

PrepBench evaluates whether an agent can prepare correct output tables from a
natural-language request and CSV inputs. The benchmark gives each case as a
workspace. Your agent runs as a black box in that workspace and writes
`result/output_*.csv`; PrepBench evaluates those files.

## At a Glance

| Item | Value |
| --- | --- |
| Release version | v0.1.0 |
| Cases | 306 |
| Input tables | 829 |
| Public modes | `clarified`, `interactive`, `workflow` |
| Case workspace | `@runs/<agent>/<mode>/<case_id>/` |
| Candidate output | `result/output_*.csv` |
| Ground truth | `src/evaluate/gt/case_xxx/` |
| Optional tools | `simulator.LocalUserSimulatorAPI`, `py2flow.api.execute_flow_file` |

## Public Modes

PrepBench exposes exactly three public modes, ordered from simplest to most
end-to-end.

| Mode | Workspace input | Extra tool | Goal |
| --- | --- | --- | --- |
| `clarified` | clarified `query.md` + `inputs/` | none | Prepare tables from a disambiguated request |
| `interactive` | original `query.md` + `inputs/` | user simulator | Clarify the request, then prepare tables |
| `workflow` | original `query.md` + `inputs/` | user simulator + workflow executor | Clarify, build/run a workflow, then produce tables |

All modes are evaluated the same way: PrepBench reads
`@runs/<agent>/<mode>/<case_id>/result/output_*.csv` and compares those files
with the expected output tables.

## Install

```bash
git clone https://github.com/TsinghuaDatabaseGroup/prepbench.git
cd prepbench
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m pip install -e .
```

Commands below assume this virtualenv is activated; use `python` from the
activated environment.

PrepBench is intended to run from a source checkout because the dataset,
simulator assets, workflow prompt, and evaluator ground truth live in the repo.
The editable install makes `simulator` and `py2flow` importable when your agent
runs from `@runs/...`; alternatively set `PYTHONPATH=/path/to/prepbench/src`.

> **Note:** The editable install registers a package named `evaluate`. If you
> have HuggingFace `evaluate` installed in the same environment, the two will
> conflict. Use a dedicated virtualenv for PrepBench.

## Basic Flow

```text
prepare workspace -> run your agent -> write result/output_*.csv -> evaluate
```

## Agent Integration Contract

- PrepBench does not call your agent.
- You run your agent once per prepared case workspace.
- The agent input is the workspace path, not copied file contents.
- The agent may inspect and write files inside that workspace.
- The final scored files are `result/output_*.csv`.
- The evaluator reads only those result CSVs.

## Prepare a Workspace

Create one case workspace under a run root:

```bash
python scripts/prepare_run.py \
  --mode clarified \
  --case case_001 \
  --run-root @runs/my_agent/clarified
```

The workspace layout is:

```text
@runs/my_agent/clarified/case_001/
  query.md
  inputs/
  result/
```

`interactive` workspaces also contain `simulator.md`. `workflow` workspaces
contain both `simulator.md` and `workflow_prompt.yaml`.

Repeat this command for each case you want to run. Workspace files are symlinks
where possible, so setup is cheap.

Prepare every GT case for a complete mode run:

```bash
python scripts/prepare_run.py \
  --mode clarified \
  --all \
  --run-root @runs/my_agent/clarified
```

`--all` uses the evaluator GT case set, then requires matching `data/case_xxx`
directories for workspace setup.

PrepBench is an honor-system benchmark. The repository still contains evaluator
and simulator assets, but the model-under-test should only read files exposed in
its prepared workspace.

## Run Your Agent

Run your agent inside the case workspace. Give it the workspace path, not copied
file contents. It can inspect `query.md`, read `inputs/`, write code or other
working files, and finally write result tables:

```text
@runs/my_agent/<mode>/<case_id>/result/output_*.csv
```

For `interactive`, the agent may use `simulator.md` and the Python API:

```python
from simulator import LocalUserSimulatorAPI

api = LocalUserSimulatorAPI()
session = api.start_session(case_id="case_001", run_id="my_agent")
reply = api.ask(
    session_id=session["session_id"],
    questions=["Should the monthly date be the first day of each month?"],
)
```

For comparable interactive runs, keep the simulator backend fixed. A practical
default is official `deepseek-v4-flash` in non-thinking mode with
`PREPBENCH_SIMULATOR_TEMPERATURE=0`; see `docs/USER_SIMULATOR.md` for
provider-specific settings.

For `workflow`, the agent may read `workflow_prompt.yaml`, generate a py2flow
JSON DAG at any workspace path, and execute it from the workspace:

```python
from py2flow.api import execute_flow_file

execute_flow_file(flow_path="workflow.json")
```

The workflow executor defaults to `./inputs` and `./result`, so a workflow run in
the case workspace writes the same `result/output_*.csv` files that the evaluator
scores.

## Evaluate

Evaluate a full mode run:

```bash
python scripts/evaluate_submission.py \
  --mode clarified \
  --run-root @runs/my_agent/clarified
```

For single-case debugging:

```bash
python scripts/evaluate_submission.py \
  --mode clarified \
  --run-root @runs/my_agent/clarified \
  --case case_001
```

The evaluator writes:

```text
@runs/my_agent/clarified/evaluation/summary.json
@runs/my_agent/clarified/evaluation/summary.csv
```

When `--case` is omitted, the evaluator checks every GT case. Missing case
folders or missing result tables are reported as `NOT_FOUND`. The command exits
with code 0 only when every evaluated case passes.

If you prepared only one case, pass `--case`. Omit `--case` only for a complete
mode run.

## Minimal Smoke Tests

Validate the dataset:

```bash
python scripts/validate_dataset.py
```

Expected summary:

```text
cases=306 input_tables=829 gt_cases=306 solution_cases=306 errors=0
```

Run an evaluator demo that copies known-correct GT output for one case into the
public result layout:

```bash
python examples/evaluate_demo.py
```

Run the repository checks:

```bash
PYTHON=python3 make check
```

## More Documentation

- Dataset and allowed-input policy: [docs/DATASET.md](docs/DATASET.md)
- Evaluation details: [docs/EVALUATION.md](docs/EVALUATION.md)
- User simulator API: [docs/USER_SIMULATOR.md](docs/USER_SIMULATOR.md)
- Workflow executor: [docs/WORKFLOW_EXECUTION.md](docs/WORKFLOW_EXECUTION.md)
- Paper figures and historical analysis: [docs/RESULTS.md](docs/RESULTS.md)

## FAQ

**Which mode should I start with?** Use `clarified` first to check basic table
preparation, then `interactive`, then `workflow` if you want to evaluate an
agent's workflow-generation path.

**What does the evaluator score?** Only final result tables under
`result/output_*.csv`.

**Where should local runs go?** Use `@runs/<agent>/<mode>/`; this directory is
ignored by git.
