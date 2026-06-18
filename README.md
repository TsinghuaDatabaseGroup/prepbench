# PrepBench

**PrepBench: How Far Are We from Natural-Language-Driven Data Preparation?**

[Dataset](docs/DATASET.md) |
[Evaluation](docs/EVALUATION.md) |
[User Simulator](docs/USER_SIMULATOR.md) |
[Simulator Contract](docs/contracts/USER_SIMULATOR_LOCAL.md) |
[Citation](CITATION.cff)

PrepBench is a benchmark for evaluating natural-language-driven table preparation.
Given a task instruction and raw CSV inputs, an agent must produce prepared output
tables. For tasks with ambiguous requirements, PrepBench also provides a local user
simulator API for clarification-style interaction.

![PrepBench overview](docs/assets/prepbench_overview.png)

## Task Formulation

For each case, an agent receives a natural-language instruction and one or more
raw CSV tables. It must produce the prepared output CSVs expected by the task.

```text
query.md + inputs/*.csv  ->  solution/cand/output_*.csv
```

The evaluator compares candidate outputs with per-case ground truth tables.
Interactive agents may ask clarification questions through the local user
simulator before producing outputs.

## At a Glance

| Item | Value |
| --- | --- |
| Dataset version | v0.1.0 |
| Tasks | 306 |
| Input tables | 829 |
| Primary input | `query.md` + `inputs/*.csv` |
| Candidate output | `solution/cand/*.csv` |
| Ground truth | `src/evaluate/gt/case_xxx/` |
| Optional interaction | `simulator.LocalUserSimulatorAPI` |

## Repository Layout

```text
data/                         # public benchmark cases
src/evaluate/                  # output-table evaluator
src/evaluate/gt/               # ground-truth outputs and comparison configs
src/simulator/                 # local user simulator API
docs/                          # dataset, evaluation, and simulator docs
examples/                      # small integration examples
scripts/validate_dataset.py    # local integrity check
```

The public repository intentionally excludes internal data-construction scripts,
plotting scripts, paper experiment runners, and private reference solutions.

## Evaluation Tracks

PrepBench keeps the public evaluation surface small. Use one of three tracks:

| Track | Agent input | Interaction | Purpose |
| --- | --- | --- | --- |
| `interactive` | `query.md` + `inputs/*.csv` | May call `LocalUserSimulatorAPI` | Full ambiguous-task setting with clarification |
| `direct` | `query.md` + `inputs/*.csv` | No simulator | Tests whether the agent can solve from the original instruction alone |
| `oracle` | `query_full.md` + `inputs/*.csv` | No simulator | Tests table preparation under the clarified instruction |

All tracks use the same candidate-output contract:

```text
@output/<method>/<track>/case_xxx/solution/cand/output_*.csv
```

## Install

```bash
git clone https://github.com/zzzbitz/prepbench.git
cd prepbench
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

## Dataset

Each case has this shape:

```text
data/case_001/
  query.md
  query_full.md
  amb_kb.json
  inputs/
    input_01.csv
```

Asset visibility:

| Asset | Visible to agents? | Purpose |
| --- | --- | --- |
| `query.md` | Yes | Original task instruction |
| `inputs/*.csv` | Yes | Raw input tables |
| `query_full.md` | Only in `oracle` track | Clarified task instruction |
| `amb_kb.json` | No | Simulator and disambiguation metadata |
| `src/evaluate/gt/case_xxx/` | No | Ground-truth outputs and comparison config |
| private reference solutions | No | Simulator-side evidence only |

Validate the local dataset:

```bash
python scripts/validate_dataset.py
```

Expected summary:

```text
cases=306 input_tables=829 gt_cases=306 errors=0
```

More details: `docs/DATASET.md`.

## Evaluate an Agent

Write candidate outputs under a results root:

```text
@output/my_agent/interactive/
  case_001/
    solution/
      cand/
        output_01.csv
```

Run:

```bash
PYTHONPATH=src python -m evaluate.batch --results-root @output/my_agent/interactive
```

The evaluator writes:

```text
@output/my_agent/interactive/evaluation_summary.csv
@output/my_agent/interactive/acc.txt
```

More details: `docs/EVALUATION.md`.

## Use the Local User Simulator

Set simulator credentials in `.env` or the process environment:

```bash
PREPBENCH_SIMULATOR_MODEL=openai/gpt-5.2
OPENROUTER_API_KEY=your_openrouter_api_key
```

Provide private reference solutions locally:

```bash
export PREPBENCH_SOLUTIONS_ROOT=/absolute/path/to/private_solutions
```

Then call the local API:

```python
from simulator import LocalUserSimulatorAPI

api = LocalUserSimulatorAPI(max_rounds=3, question_ratio=2.5)
session = api.start_session(case_id="case_001", run_id="demo")
response = api.ask(
    session_id=session["session_id"],
    questions=["Should the monthly date be the first day of each month?"],
    round=1,
)
print(response["answers"])
```

More details: `docs/USER_SIMULATOR.md` and
`docs/contracts/USER_SIMULATOR_LOCAL.md`.

## Reporting Results

Report the track, model or agent name, table accuracy from `acc.txt`, and whether
disambiguation metrics were used. If only a subset of cases was run, report the
case range explicitly.

## Minimal Example

`examples/user_simulator_demo.py` shows the local simulator API. For submission
layout only, see `examples/submission_layout/README.md`.

## FAQ

**Which track should I use?** Use `interactive` for the full benchmark,
`direct` for no-clarification agents, and `oracle` when you want to isolate
table preparation under clarified instructions.

**Why is my case marked `NOT_FOUND`?** The evaluator expects candidate CSVs under
`case_xxx/solution/cand/`.

**Why does the simulator fail before answering?** Set a simulator API key and make
sure `PREPBENCH_SOLUTIONS_ROOT` points to private reference solutions.

## Private Assets

Reference solutions are used only by benchmark-side simulation. They are not part
of the public repository and are ignored by Git.

Supported local layouts:

```text
case001/solution.py
case_001/solution.py
case001.py
case_001.py
```

Default local mount point:

```text
src/simulator/assets/solutions/
```

## Citation

If you use PrepBench in research, cite the paper and this repository. Citation
metadata is available in `CITATION.cff`.
