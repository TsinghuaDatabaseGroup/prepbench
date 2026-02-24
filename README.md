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

## Quick Start for Evaluating Your Agent (Primary Path)

For most users, PrepBench should be used as an **E2E benchmark/evaluator**.

1) Set API key in `.env`.
2) Run the reference `PrepAgent` on one case:

```bash
./scripts/run_prepagent.sh --case 1 --model openai/gpt-5.2
```

3) Evaluate outputs:

```bash
PYTHONPATH=src python -m evaluate.batch --results-root @output/<model_info>/prepagent --candidate-kind auto
```

4) Read results:

```bash
@output/<model_info>/prepagent/evaluation_summary.csv
@output/<model_info>/prepagent/acc.txt
```

`<model_info>` is derived from the last segment of `--model` and sanitized for paths.
Example: `openai/gpt-5.2` -> `gpt-5.2`.

What third-party frameworks need to produce:
- code track: `case_xxx/solution/cand/*.csv`
- flow track: `case_xxx/solution/flow_cand/*.csv`

Public per-case inputs:
- `data/case_xxx/query.md`
- `data/case_xxx/inputs/*.csv`

Integration contract:
- `docs/BYOA_E2E.md`
- `docs/ARCHITECTURE.md`

Reference implementation:
- `methods/prepagent/run_prepagent.py`
- `methods/prepagent/README.md`
- `methods/prepagent/prompts/`

PrepAgent output root is isolated from benchmark run modes:
- `@output/<model_info>/prepagent/case_xxx/solution/...`

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
- Path: `src/simulator/assets/solutions/case_XXX.py`
- Not bundled publicly to reduce data leakage risk
- Request access: `j1n9zhe@gmail.com`

## Troubleshooting

- `API key not provided`:
  - Ensure `.env` exists at repo root and contains a valid key (for example `OPENROUTER_API_KEY=...`).
- `run_mode is empty`:
  - Pass `--run_mode` explicitly or set `experiment.run_mode` in `config/experiment.yaml`.
- `Reference solution not found` (usually in `flow` mode):
  - Prepare `src/simulator/assets/solutions/case_XXX.py` first. For access, contact `j1n9zhe@gmail.com`.
- `No candidate directory with CSV outputs found` during batch evaluation:
  - The run did not produce result CSV files under `solution/cand` or `solution/flow_cand` for that case.
- Many `NOT_FOUND` rows in `evaluation_summary.csv`:
  - `evaluate.batch` always iterates all GT cases; if you only run a subset, missing cases are expected.
  - For single-case debugging, filter one row (example): `rg '^case_001,' @output/<model_info>/<run_mode>/evaluation_summary.csv`

## Contributing and Citation

- Contribution guide: `CONTRIBUTING.md`
- Citation metadata: `CITATION.cff`
