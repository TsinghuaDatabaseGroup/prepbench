from __future__ import annotations

import json
import logging
import os
import random
import re
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Optional

import requests
import yaml
from jinja2 import Environment, FileSystemLoader

logger = logging.getLogger(__name__)
PROMPT_DIR = Path(__file__).parent / "prompts"
REPO_ROOT = Path(__file__).resolve().parents[2]


@dataclass(frozen=True)
class UserSimulatorAnswerItem:
    sub_question: str
    classification: str
    source: str
    answer: str
    canonical_value: Optional[str] = None
    details: Optional[dict[str, Any]] = None
    ref: Optional[str] = None


@dataclass(frozen=True)
class UserSimulatorResult:
    answers: list[UserSimulatorAnswerItem]
    raw_response: str
    messages: list[dict[str, str]]
    parse_error: Optional[str] = None
    raw_attempts: Optional[list[str]] = None

    @property
    def combined_answer(self) -> str:
        parts = []
        for i, item in enumerate(self.answers, 1):
            if len(self.answers) == 1:
                parts.append(item.answer)
            else:
                parts.append(f"{i}. {item.answer}")
        return "\n".join(parts)

    @property
    def classification(self) -> str:
        return self.answers[0].classification if self.answers else "fallback"

    @property
    def source(self) -> str:
        return self.answers[0].source if self.answers else "refuse"

    @property
    def answer(self) -> str:
        return self.combined_answer

    @property
    def ref(self) -> Optional[str]:
        return self.answers[0].ref if self.answers else None

    @property
    def canonical_value(self) -> Optional[str]:
        return self.answers[0].canonical_value if self.answers else None

    @property
    def details(self) -> Optional[dict[str, Any]]:
        return self.answers[0].details if self.answers else None


_JSON_CODE_FENCE_RE = re.compile(r"```(?:json)?\s*([\s\S]*?)```", re.MULTILINE)
_ANSWER_REQUIRED_FIELDS = ("sub_question", "classification", "source", "answer")
_MAX_FEEDBACK_CHARS = 2000
_ALLOWED_CLASSIFICATIONS = {
    "hit",
    "fallback",
    "refuse_need_data",
    "refuse_too_broad",
    "refuse_illegal",
    "refuse_irrelevant",
}
_RETRYABLE_STATUS_CODES = {429, 500, 502, 503, 504}
_DOTENV_LOADED = False


def _load_dotenv() -> None:
    global _DOTENV_LOADED
    if _DOTENV_LOADED:
        return
    env_path = REPO_ROOT / ".env"
    if env_path.exists():
        for line in env_path.read_text(encoding="utf-8").splitlines():
            stripped = line.strip()
            if not stripped or stripped.startswith("#") or "=" not in stripped:
                continue
            if stripped.startswith("export "):
                stripped = stripped[len("export ") :].strip()
            key, value = stripped.split("=", 1)
            key = key.strip()
            value = value.strip().strip("'\"")
            if key and key not in os.environ:
                os.environ[key] = value
    _DOTENV_LOADED = True


def _env(name: str, default: str = "") -> str:
    _load_dotenv()
    value = os.getenv(name, default)
    return value.strip() if isinstance(value, str) else default


def _load_prompt_yaml(name: str) -> dict[str, Any]:
    path = PROMPT_DIR / f"{name}.yaml"
    if not path.exists():
        raise FileNotFoundError(f"Prompt config not found: {path}")
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(data, dict):
        raise ValueError(f"Prompt config must be a YAML mapping: {path}")
    return data


def _chat_completions_url(base_url: str) -> str:
    trimmed = (base_url or "").strip().rstrip("/")
    if not trimmed:
        raise ValueError("base_url must be non-empty")
    if trimmed.endswith("/chat/completions"):
        return trimmed
    return f"{trimmed}/chat/completions"


class OpenAICompatibleClient:
    def __init__(
        self,
        *,
        api_key: str,
        model_name: str,
        base_url: str,
        timeout: int,
        max_retries: int = 2,
    ) -> None:
        if not api_key:
            raise RuntimeError(
                "Simulator API key is missing. Set PREPBENCH_SIMULATOR_API_KEY, "
                "OPENROUTER_API_KEY, or OPENAI_API_KEY."
            )
        if not model_name:
            raise RuntimeError("Simulator model is missing. Set PREPBENCH_SIMULATOR_MODEL.")
        self.api_key = api_key
        self.model_name = model_name
        self.url = _chat_completions_url(base_url)
        self.timeout = timeout
        self.max_retries = max_retries
        self.session = requests.Session()

    def _backoff(self, attempt: int, retry_after: str | None = None) -> float:
        if retry_after:
            try:
                return min(float(retry_after), 30.0)
            except ValueError:
                pass
        return min(1.5 * (2**attempt) * random.uniform(0.8, 1.2), 30.0)

    def generate(
        self,
        messages: list[dict[str, str]],
        *,
        temperature: float,
        max_tokens: int,
    ) -> str:
        payload = {
            "model": self.model_name,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
        }
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        last_error: Exception | None = None
        for attempt in range(self.max_retries + 1):
            try:
                response = self.session.post(
                    self.url,
                    headers=headers,
                    data=json.dumps(payload),
                    timeout=self.timeout,
                )
                if response.status_code in _RETRYABLE_STATUS_CODES and attempt < self.max_retries:
                    time.sleep(self._backoff(attempt, response.headers.get("Retry-After")))
                    continue
                response.raise_for_status()
                data = response.json()
                choices = data.get("choices") or []
                if not choices:
                    raise RuntimeError(f"LLM response has no choices: {str(data)[:500]}")
                content = ((choices[0].get("message") or {}).get("content") or "").strip()
                if not content:
                    raise RuntimeError(f"LLM response content is empty: {str(data)[:500]}")
                return content
            except requests.RequestException as exc:
                last_error = exc
                if attempt < self.max_retries:
                    time.sleep(self._backoff(attempt))
                    continue
                raise RuntimeError(f"LLM request failed: {exc}") from exc
        raise RuntimeError(f"LLM request failed: {last_error}")


def _extract_json_object(text: str) -> Optional[dict[str, Any]]:
    if not text:
        return None

    try:
        result = json.loads(text.strip())
        if isinstance(result, dict):
            return result
    except Exception:
        pass

    for fence_match in _JSON_CODE_FENCE_RE.finditer(text):
        try:
            result = json.loads(fence_match.group(1).strip())
            if isinstance(result, dict):
                return result
        except Exception:
            pass

    candidates: list[dict[str, Any]] = []
    i = 0
    while i < len(text) and len(candidates) < 5:
        if text[i] == "{":
            depth = 0
            start = i
            in_string = False
            escape_next = False
            for j in range(i, len(text)):
                c = text[j]
                if escape_next:
                    escape_next = False
                    continue
                if c == "\\" and in_string:
                    escape_next = True
                    continue
                if c == '"' and not escape_next:
                    in_string = not in_string
                    continue
                if in_string:
                    continue
                if c == "{":
                    depth += 1
                elif c == "}":
                    depth -= 1
                    if depth == 0:
                        try:
                            obj = json.loads(text[start : j + 1])
                            if isinstance(obj, dict):
                                candidates.append(obj)
                        except Exception:
                            pass
                        i = j
                        break
        i += 1

    if not candidates:
        return None
    with_answers = [c for c in candidates if isinstance(c.get("answers"), list)]
    if with_answers:
        return max(with_answers, key=lambda c: len(c.get("answers") or []))
    return candidates[0]


def _sanitize_answer(answer: str) -> str:
    return (answer or "").replace("```", "").strip()


def _normalize_classification(classification: str) -> str:
    value = (classification or "").strip()
    if value == "hit_amb_kb":
        return "hit"
    if value in {"fallback_flow", "fallback_solution"}:
        return "fallback"
    if value == "illegal":
        return "refuse_illegal"
    if value in _ALLOWED_CLASSIFICATIONS:
        return value
    return "fallback"


def _normalize_ref_for_classification(
    classification: str,
    ref: Optional[str],
    canonical_value: Optional[str],
) -> tuple[Optional[str], Optional[str]]:
    if classification != "hit":
        if canonical_value == ref:
            canonical_value = None
        ref = None
    return ref, canonical_value


def _source_for_classification(classification: str) -> str:
    if classification == "hit":
        return "lib"
    if classification == "fallback":
        return "fallback"
    if classification in {"refuse_need_data", "refuse_too_broad", "refuse_illegal", "refuse_irrelevant"}:
        return "refuse"
    return "fallback"


def _parse_single_answer(data: dict[str, Any], sub_question: str = "") -> UserSimulatorAnswerItem:
    details = data.get("details") if isinstance(data.get("details"), dict) else None

    classification = _normalize_classification(str(data.get("classification") or "fallback"))
    source = data.get("source") or _source_for_classification(classification)

    ref = data.get("ref")
    if ref is None and isinstance(details, dict):
        ref = details.get("slot_id")

    canonical_value = data.get("canonical_value")
    if canonical_value is None:
        canonical_value = ref
    ref, canonical_value = _normalize_ref_for_classification(classification, ref, canonical_value)

    return UserSimulatorAnswerItem(
        sub_question=sub_question or str(data.get("sub_question", "")),
        classification=classification,
        source=str(source),
        answer=_sanitize_answer(str(data.get("answer") or "")),
        canonical_value=canonical_value,
        details=details,
        ref=ref,
    )


def _validate_parsed_answers(
    parsed: Optional[dict[str, Any]],
    expected_sub_questions: list[str],
) -> Optional[str]:
    if not isinstance(parsed, dict):
        return "json_parse_failed"
    answers = parsed.get("answers")
    if not isinstance(answers, list):
        return "answers_missing_or_not_list"
    if not answers:
        return "answers_empty"
    if expected_sub_questions and len(answers) != len(expected_sub_questions):
        return f"answer_count_mismatch: expected={len(expected_sub_questions)} got={len(answers)}"
    for i, ans in enumerate(answers):
        if not isinstance(ans, dict):
            return f"answer_not_object: index={i}"
        missing = [k for k in _ANSWER_REQUIRED_FIELDS if k not in ans]
        if missing:
            return f"answer_missing_fields: index={i} missing={missing}"
        if not isinstance(ans.get("sub_question"), str):
            return f"sub_question_not_string: index={i}"
        if not isinstance(ans.get("classification"), str):
            return f"classification_not_string: index={i}"
        if not isinstance(ans.get("source"), str):
            return f"source_not_string: index={i}"
        if not isinstance(ans.get("answer"), str):
            return f"answer_not_string: index={i}"
        ref_val = ans.get("ref")
        if ref_val is not None and not isinstance(ref_val, str):
            return f"ref_not_string_or_null: index={i}"
        if expected_sub_questions and ans.get("sub_question") != expected_sub_questions[i]:
            return (
                "sub_question_mismatch: "
                f"index={i} expected={expected_sub_questions[i]!r} got={ans.get('sub_question')!r}"
            )
    return None


def _format_runtime_feedback(error: str, raw: str) -> str:
    snippet = raw or ""
    truncated = False
    if len(snippet) > _MAX_FEEDBACK_CHARS:
        snippet = snippet[:_MAX_FEEDBACK_CHARS]
        truncated = True
    suffix = "\n[truncated]" if truncated else ""
    return "ParseError: " + error + "\nPreviousOutput:\n" + snippet + suffix


def _default_base_url() -> str:
    explicit = _env("PREPBENCH_SIMULATOR_BASE_URL") or _env("OPENAI_BASE_URL")
    if explicit:
        return explicit
    if _env("OPENROUTER_API_KEY"):
        return "https://openrouter.ai/api/v1"
    return "https://api.openai.com/v1"


class UserSimulator:
    def __init__(
        self,
        model_name: Optional[str] = None,
        *,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        timeout: Optional[int] = None,
    ) -> None:
        self.model_name = (
            model_name
            or _env("PREPBENCH_SIMULATOR_MODEL")
            or _env("LLM_USER_SIMULATOR_MODEL")
            or _env("LLM_MODEL")
            or "openai/gpt-5.2"
        )
        self.api_key = (
            api_key
            or _env("PREPBENCH_SIMULATOR_API_KEY")
            or _env("OPENROUTER_API_KEY")
            or _env("OPENAI_API_KEY")
        )
        self.base_url = base_url or _default_base_url()
        self.temperature = float(
            temperature if temperature is not None else (_env("PREPBENCH_SIMULATOR_TEMPERATURE") or "0")
        )
        self.max_tokens = int(
            max_tokens if max_tokens is not None else (_env("PREPBENCH_SIMULATOR_MAX_TOKENS") or "8192")
        )
        self.timeout = int(timeout if timeout is not None else (_env("PREPBENCH_SIMULATOR_TIMEOUT") or "120"))
        self.client = OpenAICompatibleClient(
            api_key=self.api_key,
            model_name=self.model_name,
            base_url=self.base_url,
            timeout=self.timeout,
        )
        template_dir = PROMPT_DIR / "templates"
        self.jinja_env = Environment(loader=FileSystemLoader(template_dir), trim_blocks=True, lstrip_blocks=True)
        self.template = self.jinja_env.get_template("clarify_agent.jinja2")

    def _build_prompt(self, ctx: dict[str, Any]) -> str:
        cfg = _load_prompt_yaml("clarify_agent")
        for key in ("system", "guidelines"):
            if not isinstance(cfg.get(key), str) or not cfg[key].strip():
                raise ValueError(f"Prompt config missing required key: {key}")
        return self.template.render(
            system_prompt_text=cfg["system"],
            guidelines_text=cfg["guidelines"],
            context=ctx,
        )

    def _generate(self, messages: list[dict[str, str]]) -> str:
        return self.client.generate(
            messages,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
        )

    def answer(
        self,
        *,
        query_full_text: str,
        amb_kb_json: Optional[dict[str, Any]],
        solution_text: str,
        question: str,
        expected_sub_questions: Optional[list[str]] = None,
        runtime_feedback: Optional[str] = None,
    ) -> UserSimulatorResult:
        ctx = {
            "query_full_text": query_full_text,
            "question": question,
            "amb_kb_json": amb_kb_json or {},
            "solution_text": solution_text,
            "expected_sub_questions": expected_sub_questions or [],
            "runtime_feedback": runtime_feedback or "",
        }
        prompt_content = self._build_prompt(ctx)
        messages = [{"role": "user", "content": prompt_content}]
        raw = self._generate(messages)

        def parse_answers(raw_text: str) -> tuple[Optional[UserSimulatorResult], Optional[str]]:
            parsed = _extract_json_object(raw_text or "")
            error = _validate_parsed_answers(parsed, expected_sub_questions or [])
            if error:
                return None, error
            items = []
            for ans_data in parsed.get("answers", []):
                if isinstance(ans_data, dict):
                    item = _parse_single_answer(ans_data)
                    if not item.answer:
                        item = UserSimulatorAnswerItem(
                            sub_question=item.sub_question,
                            classification="refuse_illegal" if item.classification == "fallback" else item.classification,
                            source="refuse" if item.source == "fallback" else item.source,
                            answer="I cannot answer that question.",
                            canonical_value=item.canonical_value,
                            details=item.details,
                            ref=item.ref,
                        )
                    items.append(item)
            if not items:
                return None, "answers_empty_after_parse"
            return UserSimulatorResult(answers=items, raw_response=raw_text or "", messages=messages), None

        result, error = parse_answers(raw or "")
        if error:
            ctx["runtime_feedback"] = _format_runtime_feedback(error, raw or "")
            retry_prompt = self._build_prompt(ctx)
            retry_messages = [{"role": "user", "content": retry_prompt}]
            raw_retry = self._generate(retry_messages)
            result, error = parse_answers(raw_retry or "")
            if result:
                return UserSimulatorResult(
                    answers=result.answers,
                    raw_response=result.raw_response,
                    messages=result.messages,
                    parse_error=None,
                    raw_attempts=[raw or "", raw_retry or ""],
                )

            fallback_questions = expected_sub_questions or [question]
            answers = [
                UserSimulatorAnswerItem(
                    sub_question=q,
                    classification="refuse_illegal",
                    source="refuse",
                    answer="I cannot answer this because the user simulator response was invalid.",
                )
                for q in fallback_questions
            ]
            return UserSimulatorResult(
                answers=answers,
                raw_response=raw_retry or "",
                messages=retry_messages,
                parse_error=error,
                raw_attempts=[raw or "", raw_retry or ""],
            )

        return UserSimulatorResult(
            answers=result.answers,
            raw_response=result.raw_response,
            messages=result.messages,
            parse_error=None,
            raw_attempts=[raw or ""],
        )
