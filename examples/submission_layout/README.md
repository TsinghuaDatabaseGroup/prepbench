# Minimal Submission Layout

PrepBench expects candidate output tables under a results root:

```text
@output/<method>/<track>/
  case_001/
    solution/
      cand/
        output_01.csv
  case_002/
    solution/
      cand/
        output_01.csv
```

Use one of three track names:

- `interactive`: original instruction plus user-simulator clarification.
- `direct`: original instruction, no simulator.
- `oracle`: clarified instruction, no simulator.

Run evaluation with:

```bash
PYTHONPATH=src python -m evaluate.batch --results-root @output/<method>/<track>
```

Candidate CSV names must match the expected ground-truth output names for each
case, such as `output_01.csv`.
