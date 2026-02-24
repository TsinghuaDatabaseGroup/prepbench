# Simulator Package

This package contains benchmark-provided simulator components. It is not part of the model-under-test agent set.

## Layout

- `user_simulator.py`: user simulator implementation.
- `local_api.py`: local session-based interface (`LocalUserSimulatorAPI`) for BYOA integration.
- `prompts/`: simulator prompt configs and templates.
- `assets/solutions/`: reference solutions for each case (`case_XXX.py`).

## Notes

- `assets/solutions/` is a benchmark-internal runtime asset directory.
- Files under `assets/solutions/case_XXX.py` are used by simulator alignment and flow translation.
- These files must not be used as method inputs for BYOA evaluation.
