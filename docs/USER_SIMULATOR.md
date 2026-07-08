# User Simulator

PrepBench provides a local user simulator for `interactive` and `workflow` mode.
Agents use it when they need clarification before producing final
`result/output_*.csv` tables.

Prepared `interactive` and `workflow` workspaces include
`clarification_guide.md`, which reminds the agent how to call the simulator and
what kinds of questions are allowed.

## Configure

Install PrepBench first; see the [README install steps](../README.md#install).
The `simulator` package must be importable from `@runs/...` workspaces.
The simulator backend is configured through environment variables or a local
`.env` file, not through `LocalUserSimulatorAPI(...)`.

Recommended setup for comparable runs, not a requirement:

```bash
PREPBENCH_SIMULATOR_BASE_URL=https://api.deepseek.com
PREPBENCH_SIMULATOR_MODEL=deepseek-v4-flash
PREPBENCH_SIMULATOR_THINKING=disabled
PREPBENCH_SIMULATOR_TEMPERATURE=0
PREPBENCH_SIMULATOR_API_KEY=your_api_key
```

Store API keys in your shell environment or a local `.env` file. Do not commit
`.env` or API keys.

Any OpenAI-compatible provider can be used. Change `PREPBENCH_SIMULATOR_BASE_URL`,
`PREPBENCH_SIMULATOR_MODEL`, and `PREPBENCH_SIMULATOR_API_KEY` to match it. For
OpenRouter, use `https://openrouter.ai/api/v1` and the namespaced model id
`deepseek/deepseek-v4-flash`.

Provider endpoints must accept non-streaming chat-completions requests and
return JSON responses. `PREPBENCH_SIMULATOR_THINKING` is a provider-specific
DeepSeek option; leave it unset for endpoints that do not support it.

Optional settings:

```bash
PREPBENCH_SIMULATOR_MAX_TOKENS=8192
PREPBENCH_SIMULATOR_TIMEOUT=120
PREPBENCH_SIMULATOR_REASONING_EFFORT=high
```

API keys are checked in this order:
`PREPBENCH_SIMULATOR_API_KEY`, `OPENROUTER_API_KEY`, then `OPENAI_API_KEY`.

For official DeepSeek V4 endpoints, PrepBench defaults thinking mode to
`disabled` when it is omitted. Set `PREPBENCH_SIMULATOR_THINKING=enabled` only
for a separate thinking-mode experiment.

Check the configured backend before running `interactive` or `workflow`:

```bash
python scripts/check_simulator.py --case case_001
```

## Session Flow

```python
from simulator import LocalUserSimulatorAPI

api = LocalUserSimulatorAPI()
session = api.start_session(case_id="case_001", run_id="my_agent")

reply = api.ask(
    session_id=session["session_id"],
    questions=[
        "Should the monthly date be represented as the first day of each month?"
    ],
)
```

`api.ask(...)` accepts a list of atomic clarification questions. Each item should
ask one decision that could change the implementation. Answers are returned in
the same order.

Common case-id forms are normalized:

```text
1 -> case_001
001 -> case_001
case001 -> case_001
case_001 -> case_001
```

## Question Rules

Ask only atomic requirement clarifications that can change implementation
behavior. The simulator may refuse questions about hidden data, code, target
outputs, full hidden specifications, unrelated topics, or multiple unrelated
decisions bundled into one question.

Budget defaults: at most 10 questions per `ask(...)` call; per-case total budget
is `ceil(2.5 * ambiguity_count)`, capped at 25 but never lower than the case's
own `ambiguity_count`.

## Harness Contract

Harness developers who need exact constructor options, response fields,
classification values, and error behavior can use
[contracts/USER_SIMULATOR_LOCAL.md](contracts/USER_SIMULATOR_LOCAL.md).
