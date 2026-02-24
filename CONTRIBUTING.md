# Contributing

## Setup

```bash
git clone https://github.com/zzzbitz/prepbench.git
cd prepbench
pip install -r requirements.txt
cp .env.example .env
```

## Scope

- BYOA benchmark path: `docs/BYOA_E2E.md`
- Paper reproduction path: `docs/REPRO.md`

## Pull Request Checklist

```bash
python -m py_compile run.py methods/prepagent/run_prepagent.py src/core/orchestrator.py src/core/orchestration/code_phase.py
./scripts/run_prepagent.sh --list 1
PYTHONPATH=src python -m evaluate.batch --help
```

## Reporting Issues

Include:
- command used
- full error output
- expected behavior
- minimal reproduction path
