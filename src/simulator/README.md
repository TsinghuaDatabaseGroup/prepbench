# Simulator Package

This package contains benchmark-provided simulator components. It is not part of the model-under-test agent set.

## Layout

- `user_simulator.py`: user simulator implementation.
- `local_api.py`: local session-based interface (`LocalUserSimulatorAPI`) for BYOA integration.
- `prompts/`: simulator prompt configs and templates.
- `assets/solutions/`: optional local mount point for private reference solutions.

## Notes

- Reference solutions are benchmark-internal runtime assets distributed privately.
- The public repository intentionally does not ship a reference-solutions folder.
- Set `PREPBENCH_SOLUTIONS_ROOT` to the unpacked private solutions directory.
- Recommended layout is `case001/solution.py` (legacy forms such as `case_001.py` are also supported).
- These files must not be used as method inputs for BYOA evaluation.
- Default question budget policy in `LocalUserSimulatorAPI` is ratio-based:
  - `max_questions = ceil(question_ratio * ambiguity_count)` with defaults `question_ratio=2.5`, `max_questions_cap=25`.
