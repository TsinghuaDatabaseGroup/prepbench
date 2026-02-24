# PrepAgent Reference (E2E)

This is a reference implementation for participants who want to build and evaluate their own agent framework on PrepBench.

Pipeline order is fixed and self-contained in this folder:
1. profile
2. clarify/interact (via local user simulator API)
3. code generation + execution
4. flow generation + execution (only when code outputs exist)

## Folder Structure

- `run_prepagent.py`: entrypoint and pipeline orchestration.
- `prompts/*.yaml`: PrepAgent-owned prompt configs.
- `prompts/templates/*.jinja2`: PrepAgent-owned prompt templates.
  - `prep_profile*`: profile stage
  - `prep_interact*`: interact stage
  - `prep_code*`: code stage
  - `prep_flow*`: flow stage

PrepAgent does not reuse the benchmark cache/reuse policy in `run.py`.
Each case run starts from a clean output directory to keep behavior deterministic for external users.

## Run

```bash
./scripts/run_prepagent.sh --case 1 --model openai/gpt-5.2
```

Outputs follow the standard evaluation layout under `@output/<model_info>/prepagent/case_xxx/solution/`:
- `cand/*.csv` (code track)
- `flow_cand/*.csv` (flow track)

`<model_info>` is derived from the last segment of model name and sanitized for paths.
Example: `openai/gpt-5.2` -> `gpt-5.2`.

## Evaluate

```bash
PYTHONPATH=src python -m evaluate.batch --results-root @output/<model_info>/prepagent --candidate-kind auto
```

## Notes

- This reference implementation reuses core executors/parsers, but uses its own prompt assets under `methods/prepagent/prompts`.
- User simulator and flow mode require reference solutions in `src/simulator/assets/solutions/case_xxx.py`.
