# Minimal Submission Layout

PrepBench expects candidate output tables under a results root:

```text
@output/<method>/<setting>/
  case_001/
    solution/
      cand/
        output_01.csv
  case_002/
    solution/
      cand/
        output_01.csv
```

Use one of three setting names, ordered from easiest to hardest:

- `oracle`: clarified instruction, no simulator.
- `direct`: original instruction, no simulator.
- `interactive`: original instruction plus user-simulator clarification.

Run evaluation with:

```bash
PYTHONPATH=src python -m evaluate.batch --results-root @output/<method>/<setting>
```

Candidate CSV names must match the expected ground-truth output names for each
case, such as `output_01.csv`.

Official leaderboard submissions should include all 306 cases for one setting.
Subset folders are useful for debugging, but missing cases count as `NOT_FOUND`
in the evaluator output.
