# User Simulator

PrepBench provides a local user simulator for agents that ask clarification
questions before producing prepared tables.

Implementation:

```text
src/simulator/local_api.py
src/simulator/user_simulator.py
```

The simulator uses an OpenAI-compatible chat-completions endpoint. Configure it
with environment variables or a local `.env` file:

```bash
PREPBENCH_SIMULATOR_MODEL=openai/gpt-5.2
OPENROUTER_API_KEY=your_openrouter_api_key
# Optional:
# PREPBENCH_SIMULATOR_BASE_URL=https://openrouter.ai/api/v1
# PREPBENCH_SIMULATOR_MAX_TOKENS=8192
# PREPBENCH_SIMULATOR_TIMEOUT=120
```

Public import:

```python
from simulator import LocalUserSimulatorAPI
```

## Session Flow

```python
from simulator import LocalUserSimulatorAPI

api = LocalUserSimulatorAPI(
    max_rounds=3,
    question_ratio=2.5,
    max_questions_cap=25,
    max_questions_per_ask=10,
)

session = api.start_session(case_id="case_001", run_id="agent_run_001")

response = api.ask(
    session_id=session["session_id"],
    questions=[
        "Should the monthly date be represented as the first day of each month?"
    ],
    round=1,
)
```

`start_session(...)` returns:

- `session_id`
- `case_id`
- `run_id`
- `max_rounds`
- `max_questions`
- `max_questions_per_ask`
- `ambiguity_count`
- `question_ratio`
- `max_questions_cap`

`ask(...)` returns:

- `answers`
- `budget`
- `done`
- `parse_error`

## Question Budget

By default:

```text
max_questions = ceil(question_ratio * ambiguity_count)
```

The default cap is `25`, but the effective cap is never lower than the ambiguity
count. This keeps full ambiguity coverage possible on cases with many slots.

## Case ID Normalization

The API accepts common case forms and normalizes them internally:

```text
1 -> case_001
001 -> case_001
case001 -> case_001
case_001 -> case_001
```

## Allowed Questions

Ask only requirement clarifications that can change implementation behavior.

Good examples:

- aggregation method and output grain
- join key choice or join policy
- missing-value handling
- tie-breaking or deduplication policy
- inclusive/exclusive boundary semantics

Disallowed examples:

- asking to inspect or enumerate hidden data
- asking for code, target outputs, or a full hidden specification
- bundling multiple unrelated decisions into one sub-question

## Private Reference Solutions

The simulator uses private reference solutions as benchmark-side evidence. They
are not shipped in the public repository.

Configure them with:

```bash
export PREPBENCH_SOLUTIONS_ROOT=/absolute/path/to/private_solutions
```

Supported layouts:

```text
case001/solution.py
case_001/solution.py
case001.py
case_001.py
```

Default local mount point:

```text
src/simulator/assets/solutions/
```

That directory is ignored by Git.

## Detailed Contract

See `docs/contracts/USER_SIMULATOR_LOCAL.md` for exact fields, classification
values, and error behavior.
