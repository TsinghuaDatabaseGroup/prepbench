# Data Synthesis

This module builds benchmark assets under:

- `src/data_synthesis/output/`

It does **not** overwrite `data/case_xxx/*` by default.

## Quick Start

From repository root:

```bash
PYTHONPATH=src python -m data_synthesis.run --help
```

Run a single mode:

```bash
PYTHONPATH=src python -m data_synthesis.run build_gt_code --case 4 --model deepseek/deepseek-v3.2 --force
```

Run the three main builders in sequence:

```bash
bash src/data_synthesis/scripts/run_case_artifacts.sh 4 deepseek/deepseek-v3.2
```

## Output Layout

- `output/gt_codegen/<model_dir>/case_xxx/`
- `output/workflow/<model_dir>/case_xxx/`
- `output/disamb_build/<model_dir>/case_xxx/`
- `output/full/<model_dir>/case_xxx/`
- `output/amb/<model_dir>/case_xxx/`

`<model_dir>` is model name with `/` replaced by `__`.

## Notes

- `build_flow` writes back to `data/case_xxx/flow.json` only with `--publish-flow`.
- `build_gt_code` publishes to simulator assets only with `--publish-solution`.
