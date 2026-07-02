# Contributing

## Setup

```bash
git clone https://github.com/TsinghuaDatabaseGroup/prepbench.git
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
make check
```

## Reference Verification

Maintainers can verify public reference solutions against the public evaluator:

```bash
make verify-reference-outputs
```

## Reporting Issues

Include:
- command used
- full error output
- expected behavior
- minimal reproduction path
