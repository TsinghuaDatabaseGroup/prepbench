# Contributing

## Setup

```bash
git clone https://github.com/zzzbitz/prepbench.git
cd prepbench
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
cp .env.example .env
```

## Scope

- Dataset layout: `docs/DATASET.md`
- User simulator contract: `docs/USER_SIMULATOR.md`
- Evaluation: `docs/EVALUATION.md`

## Pull Request Checklist

```bash
python -m compileall src/evaluate src/simulator examples scripts/validate_dataset.py
python scripts/validate_dataset.py
PYTHONPATH=src python -m evaluate.batch --help
```

## Reporting Issues

Include:
- command used
- full error output
- expected behavior
- minimal reproduction path
