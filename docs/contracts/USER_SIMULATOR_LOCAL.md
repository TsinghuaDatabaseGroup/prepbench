# Local User Simulator Contract

This is the local, in-process contract for benchmark-side user simulation.

Implementation:
- `simulator/local_api.py`
- `simulator.LocalUserSimulatorAPI`

Reference-solution dependency:
- `start_session(...)` requires reference solutions.
- The public repository ships them under `reference/solutions/`.
- Set `PREPBENCH_SOLUTIONS_ROOT` only when overriding the default path.
- Recommended layout: `case_001/solution.py` (legacy `case001.py` style is also accepted).
- The default data and reference-solution paths are repository-relative; run the
  API from a source checkout unless explicit paths are provided.

This API is the supported external interface. It is preferable to calling
`UserSimulator` directly, because it owns session state, question budgets, and
response normalization.

## API

### `LocalUserSimulatorAPI(...)`

Constructor options:
- `model_name`:
  - OpenAI-compatible model name used by the simulator backend
  - required unless provided by `PREPBENCH_SIMULATOR_MODEL` or legacy model envs
- `api_key`, `base_url`, `temperature`, `thinking_type`, `reasoning_effort`:
  - optional backend overrides; otherwise environment variables are used
- `data_root` (default repository `data/`):
  - path to the public `data/case_xxx` directories
- `question_ratio` (default `2.5`):
  - case budget formula: `max_questions = ceil(question_ratio * ambiguity_count)`
- `max_questions_cap` (default `25`):
  - cap is applied after ratio, but effective cap is at least `ambiguity_count`
- `max_questions` (default `None`):
  - optional explicit override for fixed budget
- `max_rounds` (default `3`)
- `max_questions_per_ask` (default `10`)

Credential lookup order:
- `PREPBENCH_SIMULATOR_API_KEY`
- `OPENROUTER_API_KEY`
- `OPENAI_API_KEY`

Backend environment:
- `PREPBENCH_SIMULATOR_BASE_URL`
- `PREPBENCH_SIMULATOR_MODEL`
- `PREPBENCH_SIMULATOR_THINKING` (`enabled` or `disabled`)
- `PREPBENCH_SIMULATOR_TEMPERATURE` (defaults to `0`)
- `PREPBENCH_SIMULATOR_MAX_TOKENS` (defaults to `8192`)
- `PREPBENCH_SIMULATOR_TIMEOUT` (defaults to `120`)
- `PREPBENCH_SIMULATOR_REASONING_EFFORT` (sent only when thinking is enabled)

Thinking-mode behavior:
- For official DeepSeek V4 models (`deepseek-v4-*` at `https://api.deepseek.com`),
  the simulator defaults to `PREPBENCH_SIMULATOR_THINKING=disabled`.
- Other OpenAI-compatible endpoints do not receive a `thinking` field unless
  `PREPBENCH_SIMULATOR_THINKING` is set explicitly.
- Use non-thinking mode for comparable benchmark simulator runs, because DeepSeek
  thinking mode ignores sampling controls such as temperature.

Budget examples (default ratio/cap):
- if `ambiguity_count=4`: ratio budget = `ceil(2.5*4)=10`, cap=25 -> final `max_questions=10`
- if `ambiguity_count=20`: ratio budget = `50`, cap=25 -> final `max_questions=25`
- if `ambiguity_count=30`: ratio budget = `75`, cap=25 but effective cap is at least ambiguity count -> final `max_questions=30`

### `start_session(case_id: str, run_id: str) -> dict`

Input:
- `case_id`: benchmark case id, for example `case_001`; numeric forms such as
  `1`, `001`, and `case001` are normalized to `case_001`
- `run_id`: caller-defined run identifier

Output:
- `session_id`
- `case_id`
- `run_id`
- `max_rounds`
- `max_questions`
- `max_questions_per_ask`
- `ambiguity_count`
- `question_ratio`
- `max_questions_cap`

### `ask(session_id: str, questions: list[str], round: int | None = None) -> dict`

Input:
- `session_id`: value from `start_session`
- `questions`: list of sub-questions for this round
- `round`: optional current round index (1-based). If omitted, the API uses the
  next expected round.

Output:
- `session_id`
- `case_id`
- `run_id`
- `round`
- `answers`: list of answer items
- `budget`: round/question budget state
- `done`: whether the session has reached its budget limit
- `next_round`: next expected round number, or `null` when `done=true`
- `parse_error`: parser error from simulator model output (if any)

Behavior notes:
- If the session is already done, `ask(...)` returns `done=true` with empty `answers` (no exception).
- If `round` is provided and does not match the expected next round, `ask(...)` raises a `ValueError`.
- If `questions` exceeds `max_questions_per_ask` or remaining budget, it is truncated in order.

Answer item fields:
- `sub_question`
- `classification`
- `source`: derived from `classification` (`hit`→`lib`, `fallback`→`fallback`, `refuse_*`→`refuse`). The model no longer outputs this directly.
- `answer`
- `ref`: ambiguity id for a `hit` answer, otherwise `null`.

## Classification Enum

Strict enum (no `unknown`):
- `hit`
- `fallback`
- `refuse_need_data`
- `refuse_too_broad`
- `refuse_illegal`
- `refuse_irrelevant`

## Question Contract

Ask only business-rule clarifications that can change implementation behavior.

Typical allowed topics:
- aggregation method and grouping granularity
- join key choice / join policy
- missing-value handling
- tie-breaking / dedup policy
- boundary semantics (inclusive/exclusive)

Disallowed topics:
- requests to inspect/enumerate raw dataset contents
- requests for code, output examples, or full hidden spec
- broad multi-topic questions bundled into one sub-question

Formatting guidance:
- `ask(...)` accepts `questions: list[str]`; each item should be one atomic question.
- Keep question order stable within one call; answers are returned in the same order.
