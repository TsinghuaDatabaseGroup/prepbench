# User Simulator

PrepBench provides a local user simulator for agents that ask clarification
questions before producing prepared tables.

In prepared workspaces, `interactive` and `workflow` mode include a
`simulator.md` file with the minimal case-specific API reminder.

The simulator uses an OpenAI-compatible chat-completions endpoint. Configure the
model, endpoint, API key, and temperature with environment variables or a local
`.env` file.

Recommended native DeepSeek setup for comparable runs:

```bash
PREPBENCH_SIMULATOR_BASE_URL=https://api.deepseek.com
PREPBENCH_SIMULATOR_MODEL=deepseek-v4-flash
PREPBENCH_SIMULATOR_TEMPERATURE=0
PREPBENCH_SIMULATOR_API_KEY=your_api_key
```

OpenRouter alternative:

```bash
PREPBENCH_SIMULATOR_BASE_URL=https://openrouter.ai/api/v1
PREPBENCH_SIMULATOR_MODEL=deepseek/deepseek-v4-flash
PREPBENCH_SIMULATOR_TEMPERATURE=0
PREPBENCH_SIMULATOR_API_KEY=your_openrouter_api_key
```

Other optional settings:

```bash
PREPBENCH_SIMULATOR_MAX_TOKENS=8192
PREPBENCH_SIMULATOR_TIMEOUT=120
```

The simulator checks API keys in this order: `PREPBENCH_SIMULATOR_API_KEY`,
`OPENROUTER_API_KEY`, then `OPENAI_API_KEY`.

`PREPBENCH_SIMULATOR_TEMPERATURE` defaults to `0` when omitted.

Public import:

Install the repo with `python -m pip install -e .` first, or set
`PYTHONPATH=/path/to/prepbench/src`, so `simulator` is importable from `@runs/...`.

```python
from simulator import LocalUserSimulatorAPI
```

## Session Flow

```python
from simulator import LocalUserSimulatorAPI

api = LocalUserSimulatorAPI(
    model_name="your-model-name",
    data_root="data",
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
- `next_round`
- `parse_error`

`round` is optional. If omitted, `ask(...)` uses the next expected round. If a
caller provides `round`, it must match the next expected round or the API raises
`ValueError`.

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

## Reference Solutions

The simulator uses reference solutions as benchmark-side evidence. The public
repository includes them under `reference/solutions/` for reproducibility and
local simulator use.

The default path is repository-relative, so run the simulator from a source
checkout. The reference-solution root can be overridden with:

```bash
export PREPBENCH_SOLUTIONS_ROOT=/absolute/path/to/reference_solutions
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
reference/solutions/
```

Reference solutions are answer artifacts. Do not provide them as model input or
use them as submission assistance when evaluating an agent.

## Detailed Contract

See `docs/contracts/USER_SIMULATOR_LOCAL.md` for exact fields, classification
values, and error behavior.
