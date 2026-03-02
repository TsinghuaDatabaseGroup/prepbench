# Local User Simulator Contract

This is the local (in-process) contract for benchmark-side user simulation.

Implementation:
- `simulator/local_api.py`
- `simulator.LocalUserSimulatorAPI`

Reference-solution dependency:
- `start_session(...)` requires benchmark-private reference solutions.
- Set `PREPBENCH_SOLUTIONS_ROOT` to your private solutions directory.
- Recommended layout: `case001/solution.py` (legacy `case_001.py` style is also accepted).

## API

### `start_session(case_id: str, run_id: str) -> dict`

Input:
- `case_id`: benchmark case id, for example `case_001`
- `run_id`: caller-defined run identifier

Output:
- `session_id`
- `case_id`
- `run_id`
- `max_rounds`
- `max_questions`
- `max_questions_per_ask`

### `ask(session_id: str, questions: list[str], round: int) -> dict`

Input:
- `session_id`: value from `start_session`
- `questions`: list of sub-questions for this round
- `round`: current round index (1-based)

Output:
- `session_id`
- `case_id`
- `run_id`
- `round`
- `answers`: list of answer items
- `budget`: round/question budget state
- `done`: whether the session has reached its budget limit
- `parse_error`: parser error from simulator model output (if any)

Behavior notes:
- If the session is already done, `ask(...)` returns `done=true` with empty `answers` (no exception).
- If `round` does not match the expected next round, `ask(...)` raises a `ValueError`.

Answer item fields:
- `sub_question`
- `classification`
- `source`
- `answer`
- `ref`
- `canonical_value`: normalized slot identifier for a `hit` answer (defaults to `ref` when omitted).  
  For non-`hit` answers this should be treated as nullable and ignored.
- `details`

## Classification Enum

Strict enum (no `unknown`):
- `hit`
- `fallback`
- `refuse_need_data`
- `refuse_too_broad`
- `refuse_illegal`
- `refuse_irrelevant`
