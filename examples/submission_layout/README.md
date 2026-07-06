# Minimal Submission Layout

PrepBench expects candidate output tables under a mode run root:

```text
@runs/<agent>/<mode>/
  case_001/
    query.md
    inputs/
    result/
      output_01.csv
  case_002/
    query.md
    inputs/
    result/
      output_01.csv
```

Use one of three public mode names:

- `clarified`
- `interactive`
- `workflow`

Run evaluation with:

```bash
python scripts/evaluate_submission.py \
  --mode <mode> \
  --run-root @runs/<agent>/<mode>
```

Candidate CSV names must match the expected ground-truth output names for each
case, such as `output_01.csv`. Missing outputs are reported as `NOT_FOUND`.
