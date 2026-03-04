# PrepBench: How Far Are We from Natural-Language-Driven Data Preparation?

This repository contains the benchmark dataset and experimental runner for the paper
"PrepBench: How Far Are We from Natural-Language-Driven Data Preparation?".

## Installation

1) Clone and enter the repo:

```bash
git clone https://github.com/zzzbitz/prepbench.git
cd prepbench
```

2) Install dependencies:

```bash
pip install -r requirements.txt
```

## Prerequisites

- Python 3.9+ (recommended)
- Network access to your configured LLM provider endpoint
- A valid API key in `.env`

## Configuration

- `config/experiment.yaml` holds experiment/runtime defaults (tracked).
- `config/llm.yaml` holds provider/model routing defaults (tracked).
- Optional local override (gitignored): `config/config.local.yaml`
- For the built-in OpenRouter provider, API keys must be set in `.env` (do not put keys in YAML).

Important notes:
- YAML values are **not** environment-variable expanded. Do not use `${OPENROUTER_API_KEY}` inside YAML.
- Set `experiment.run_mode` in `config/experiment.yaml` and model/provider in `config/llm.yaml` if you want defaults.

### Minimal OpenRouter example

`config/experiment.yaml`:

```yaml
experiment:
  run_mode: "orig"
```

`config/llm.yaml`:

```yaml
llm:
  active_provider: "openrouter"
  providers:
    openrouter:
      type: "openrouter"
      model: "openai/gpt-5.2"
      # OpenRouter API keys are read from .env only.
```

`.env` (local, not committed):

```bash
cp .env.example .env
# then edit .env:
OPENROUTER_API_KEY=your-key
```

## Reference Solutions Access (Private)

Benchmark-internal `run.py` modes (`flow`, `interact`, `e2e`) and the local user simulator require benchmark-private reference solutions.
These files are **not** included in the public repository.
The public repository intentionally does not ship a reference-solutions folder.

Request access by email:
- Contact: `j1n9zhe@gmail.com`
- Required subject: `PrepBench Reference Solutions Request`

After approval, you will receive a solutions directory, typically like:

```text
<solutions_root>/
  case001/solution.py
  case002/solution.py
  ...
```

Place this folder at your preferred local path (example: `<repo>/private/prepbench_solutions`),
then set:

```bash
export PREPBENCH_SOLUTIONS_ROOT=/absolute/path/to/<solutions_root>
```

This solutions directory is required for:
- interactive disambiguation via local user simulator
- benchmark-internal `interact` / `flow` / `e2e` runs

Supported reference-solution layouts include:
- `case001/solution.py`
- `case_001/solution.py`
- `case001.py`
- `case_001.py`

## Quick Start for Evaluating Your Own Agent (Primary Path)

For most users, PrepBench is an **evaluator** for their own framework (BYOA).
You do **not** need to run `PrepAgent` to evaluate your system.

What PrepBench provides:
- Public per-case inputs:
  - `data/case_xxx/query.md`
  - `data/case_xxx/inputs/*.csv`
- Evaluation tools:
  - `evaluate.batch` (code/flow output correctness)
  - `evaluate.disamb` (interactive disambiguation metrics, if available)

Private reference solutions are needed only when your framework uses local user-simulator clarify.
If you only run code/flow generation and batch evaluation, private solutions are not required.

What your framework needs to produce:
- code track: `@output/<your_framework>/e2e/case_xxx/solution/cand/*.csv`
- flow track: `@output/<your_framework>/e2e/case_xxx/solution/flow_cand/*.csv`

Single-case smoke test (recommended for first integration):
1) Run your framework on one case (for example `case_001`) and write CSV outputs under:
   - `@output/<your_framework>/e2e/case_001/solution/cand/`
   - or `@output/<your_framework>/e2e/case_001/solution/flow_cand/`
2) If your framework uses local clarify, configure private solutions first:
   - `export PREPBENCH_SOLUTIONS_ROOT=/absolute/path/to/<solutions_root>`
3) Run batch evaluator and inspect only the case you just ran:
   - `PYTHONPATH=src python -m evaluate.batch --results-root @output/<your_framework>/e2e --candidate-kind auto`
   - `rg '^case_001,' @output/<your_framework>/e2e/evaluation_summary.csv`
4) Optional disambiguation metrics (only when clarify artifacts exist):
   - `PYTHONPATH=src python -m evaluate.disamb --results-root @output/<your_framework>/e2e`
   - `rg '^case_001,' @output/<your_framework>/e2e/disamb_summary.csv`

Evaluate your outputs:

```bash
PYTHONPATH=src python -m evaluate.batch --results-root @output/<your_framework>/e2e --candidate-kind auto
```

Optional (only if your run includes clarify artifacts like `clarify/summary.json`):

```bash
PYTHONPATH=src python -m evaluate.disamb --results-root @output/<your_framework>/e2e
```

Read results:

```bash
@output/<your_framework>/e2e/evaluation_summary.csv
@output/<your_framework>/e2e/acc.txt
```

Single-case quick check (recommended during integration):

```bash
rg '^case_001,' @output/<your_framework>/e2e/evaluation_summary.csv
```

Integration contract and architecture:
- `docs/BYOA_E2E.md`
- `docs/ARCHITECTURE.md`
- `docs/contracts/USER_SIMULATOR_LOCAL.md` (clarify interaction format, budget, and allowed/disallowed question scope)

## Quick Start for PrepAgent Reference Pipeline (Secondary Path)

Use this path only if you want to run the benchmark's reference implementation.
Its main purpose is to show a practical BYOA chain:
read inputs -> optional profile (recommended) -> user simulator clarify -> generate/execute code -> output CSV.

1) Set API key in `.env`.
2) Run PrepAgent on one case:

```bash
./scripts/run_prepagent.sh --case 1 --model openai/gpt-5.2
```

3) Evaluate PrepAgent outputs:

```bash
PYTHONPATH=src python -m evaluate.batch --results-root @output/<model_info>/prepagent --candidate-kind auto
```

Optional disambiguation metric:

```bash
PYTHONPATH=src python -m evaluate.disamb --results-root @output/<model_info>/prepagent
```

4) Read results:

```bash
@output/<model_info>/prepagent/evaluation_summary.csv
@output/<model_info>/prepagent/acc.txt
```

`<model_info>` is derived from the last segment of `--model` and sanitized for paths.
Example: `openai/gpt-5.2` -> `gpt-5.2`.

PrepAgent output root is isolated from benchmark run modes:
- `@output/<model_info>/prepagent/case_xxx/solution/...`

Reference implementation:
- `methods/prepagent/run_prepagent.py`
- `methods/prepagent/README.md`
- `methods/prepagent/prompts/`

## Reproduce Paper Experiments (Secondary Path)

`run.py` is the experiment reproducer for internal multi-mode runs.

Quick example:

```bash
python run.py --case 1 --run_mode orig --model openai/gpt-5.2
```

Mode scripts:

```bash
./scripts/run_orig.sh --case 1 --model openai/gpt-5.2
./scripts/run_disamb.sh --case 1 --model openai/gpt-5.2
./scripts/run_interact.sh --case 1 --model openai/gpt-5.2
./scripts/run_disamb_only.sh --case 1 --model openai/gpt-5.2
./scripts/run_flow.sh --case 1 --model openai/gpt-5.2
./scripts/run_e2e.sh --case 1 --model openai/gpt-5.2
```

Full reproduction guide:
- `docs/REPRO.md`

## Output Layout

Results are written under:

```bash
@output/<model_info>/<run_mode>/<case_name>/
```

`<model_info>` is derived from the last segment of model name (`openai/gpt-5.2` -> `gpt-5.2`).

Typical structure:

```text
@output/<model_info>/<run_mode>/<case_name>/
├── rounds/
└── solution/
    ├── final_status.json
    ├── cand/        # code track outputs
    └── flow_cand/   # flow track outputs
```

### Reference Solutions for Flow/User Simulator

Flow mode and user simulator alignment require benchmark reference solutions:
- They are distributed privately on request (see "Reference Solutions Access (Private)").
- Configure `PREPBENCH_SOLUTIONS_ROOT` to the unpacked solutions directory.
- Benchmark-internal asset: do not use as method input in BYOA evaluation

## Troubleshooting

- `API key not provided`:
  - Ensure `.env` exists at repo root and contains a valid key (for example `OPENROUTER_API_KEY=...`).
- `run_mode is empty`:
  - Pass `--run_mode` explicitly or set `experiment.run_mode` in `config/experiment.yaml`.
- `Reference solution not found` (usually in `flow` mode):
  - Ensure `PREPBENCH_SOLUTIONS_ROOT` points to the private solutions directory.
  - Ensure the target case exists (for example `case001/solution.py`).
- `No candidate directory with CSV outputs found` during batch evaluation:
  - The run did not produce result CSV files under `solution/cand` or `solution/flow_cand` for that case.
- Many `NOT_FOUND` rows in `evaluation_summary.csv`:
  - `evaluate.batch` always iterates all GT cases; if you only run a subset, missing cases are expected.
  - For single-case debugging, filter one row (example): `rg '^case_001,' @output/<model_info>/<run_mode>/evaluation_summary.csv`
- Need disambiguation F1 (paper metric):
  - Run `PYTHONPATH=src python -m evaluate.disamb --results-root @output/<model_info>/<run_mode>`

## Contributing and Citation

- Contribution guide: `CONTRIBUTING.md`
- Citation metadata: `CITATION.cff`
