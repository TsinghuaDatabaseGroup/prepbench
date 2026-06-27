from __future__ import annotations

from dataclasses import dataclass
import math
from pathlib import Path
import re
from typing import Any, Dict, List, Optional
from uuid import uuid4

from simulator.user_simulator import UserSimulator
from simulator.case_views import InternalCaseView, load_internal_case_view


@dataclass
class _SessionState:
    session_id: str
    run_id: str
    case_id: str
    case_view: InternalCaseView
    max_rounds: int
    max_questions: int
    max_questions_per_ask: int
    used_rounds: int = 0
    used_questions: int = 0
    done: bool = False


class LocalUserSimulatorAPI:
    """
    Local (non-network) user simulator interface for external-agent integration.

    This API hides benchmark-private assets (query_full/amb_kb/reference solution)
    behind a simple session-based interface:
      - start_session(case_id, run_id)
      - ask(session_id, questions, round)
    """

    def __init__(
        self,
        *,
        model_name: Optional[str] = None,
        data_root: Optional[str | Path] = None,
        max_rounds: int = 3,
        question_ratio: float = 2.5,
        max_questions_cap: Optional[int] = 25,
        max_questions: Optional[int] = None,
        max_questions_per_ask: int = 10,
    ) -> None:
        self.user_simulator = UserSimulator(model_name=model_name)
        if data_root is not None:
            self.data_root = Path(data_root).resolve()
        else:
            # Local simulator defaults to repository-level public cases under `data/`.
            self.data_root = (Path(__file__).resolve().parents[2] / "data").resolve()
        self.max_rounds = int(max_rounds)
        if question_ratio <= 0:
            raise ValueError(f"question_ratio must be positive, got {question_ratio}")
        self.question_ratio = float(question_ratio)
        if max_questions_cap is not None and int(max_questions_cap) <= 0:
            raise ValueError(f"max_questions_cap must be positive, got {max_questions_cap}")
        self.max_questions_cap = int(max_questions_cap) if max_questions_cap is not None else None
        self.max_questions_override = int(max_questions) if max_questions is not None else None
        if self.max_questions_override is not None and self.max_questions_override <= 0:
            raise ValueError(f"max_questions must be positive, got {max_questions}")
        self.max_questions_per_ask = int(max_questions_per_ask)
        if self.max_questions_per_ask <= 0:
            raise ValueError(f"max_questions_per_ask must be positive, got {max_questions_per_ask}")
        self._sessions: Dict[str, _SessionState] = {}

    @staticmethod
    def normalize_case_id(case_id: str) -> str:
        raw = str(case_id or "").strip().lower()
        if not raw:
            raise ValueError("case_id must be a non-empty string")
        match = re.fullmatch(r"case[_-]?(\d+)", raw)
        if match:
            return f"case_{int(match.group(1)):03d}"
        if raw.isdigit():
            return f"case_{int(raw):03d}"
        return raw

    def _resolve_case_dir(self, case_id: str) -> Path:
        normalized_case_id = self.normalize_case_id(case_id)
        case_dir = (self.data_root / normalized_case_id).resolve()
        if not case_dir.is_dir():
            raise FileNotFoundError(f"Case directory not found: {case_dir}")
        return case_dir

    def _compute_max_questions(self, amb_kb_json: Dict[str, Any]) -> tuple[int, int]:
        ambiguities = amb_kb_json.get("ambiguities")
        amb_count = len(ambiguities) if isinstance(ambiguities, list) else 0

        if self.max_questions_override is not None:
            return self.max_questions_override, amb_count

        max_questions = max(1, math.ceil(self.question_ratio * amb_count))
        if self.max_questions_cap is not None:
            # Cap is raised to ambiguity count so full coverage remains possible.
            effective_cap = max(self.max_questions_cap, amb_count)
            max_questions = min(max_questions, effective_cap)
        return max_questions, amb_count

    def start_session(self, *, case_id: str, run_id: str) -> Dict[str, Any]:
        case_dir = self._resolve_case_dir(case_id)
        normalized_case_id = case_dir.name
        case_view = load_internal_case_view(case_dir, require_reference_solution=True)
        max_questions, ambiguity_count = self._compute_max_questions(case_view.amb_kb_json)
        session_id = f"sess_{uuid4().hex[:16]}"
        state = _SessionState(
            session_id=session_id,
            run_id=run_id,
            case_id=normalized_case_id,
            case_view=case_view,
            max_rounds=self.max_rounds,
            max_questions=max_questions,
            max_questions_per_ask=self.max_questions_per_ask,
        )
        self._sessions[session_id] = state
        return {
            "session_id": session_id,
            "case_id": state.case_id,
            "run_id": run_id,
            "max_rounds": state.max_rounds,
            "max_questions": state.max_questions,
            "max_questions_per_ask": state.max_questions_per_ask,
            "ambiguity_count": ambiguity_count,
            "question_ratio": self.question_ratio,
            "max_questions_cap": self.max_questions_cap,
        }

    @staticmethod
    def _normalize_questions(questions: List[str]) -> List[str]:
        if not isinstance(questions, list):
            raise ValueError("questions must be a list[str]")
        normalized = [str(q).strip() for q in questions if isinstance(q, str) and q.strip()]
        if not normalized:
            raise ValueError("questions must contain at least one non-empty string")
        return normalized

    def ask(self, *, session_id: str, questions: List[str], round: int) -> Dict[str, Any]:
        state = self._sessions.get(session_id)
        if state is None:
            raise KeyError(f"Unknown session_id: {session_id}")

        if state.done:
            return {
                "session_id": state.session_id,
                "case_id": state.case_id,
                "run_id": state.run_id,
                "round": round,
                "answers": [],
                "budget": {
                    "max_rounds": state.max_rounds,
                    "used_rounds": state.used_rounds,
                    "max_questions": state.max_questions,
                    "used_questions": state.used_questions,
                    "remaining_questions": max(state.max_questions - state.used_questions, 0),
                },
                "done": True,
                "parse_error": None,
            }

        if round != state.used_rounds + 1:
            raise ValueError(f"Round mismatch: expected {state.used_rounds + 1}, got {round}")

        normalized_questions = self._normalize_questions(questions)
        if len(normalized_questions) > state.max_questions_per_ask:
            normalized_questions = normalized_questions[: state.max_questions_per_ask]

        remaining_questions = state.max_questions - state.used_questions
        if remaining_questions <= 0:
            state.done = True
            return {
                "session_id": state.session_id,
                "case_id": state.case_id,
                "run_id": state.run_id,
                "round": round,
                "answers": [],
                "budget": {
                    "max_rounds": state.max_rounds,
                    "used_rounds": state.used_rounds,
                    "max_questions": state.max_questions,
                    "used_questions": state.used_questions,
                    "remaining_questions": 0,
                },
                "done": True,
                "parse_error": None,
            }

        normalized_questions = normalized_questions[:remaining_questions]
        question_payload = "\n".join([f"q{i + 1}: {q}" for i, q in enumerate(normalized_questions)])

        result = self.user_simulator.answer(
            query_full_text=state.case_view.query_full_text,
            amb_kb_json=state.case_view.amb_kb_json,
            solution_text=state.case_view.reference_solution_text,
            question=question_payload,
            expected_sub_questions=normalized_questions,
            runtime_feedback="",
        )

        state.used_rounds += 1
        state.used_questions += len(normalized_questions)
        state.done = state.used_rounds >= state.max_rounds or state.used_questions >= state.max_questions

        answers = [
            {
                "sub_question": a.sub_question,
                "classification": a.classification,
                "source": a.source,
                "answer": a.answer,
                "ref": a.ref,
                "canonical_value": a.canonical_value,
                "details": a.details,
            }
            for a in result.answers
        ]

        return {
            "session_id": state.session_id,
            "case_id": state.case_id,
            "run_id": state.run_id,
            "round": round,
            "answers": answers,
            "budget": {
                "max_rounds": state.max_rounds,
                "used_rounds": state.used_rounds,
                "max_questions": state.max_questions,
                "used_questions": state.used_questions,
                "remaining_questions": max(state.max_questions - state.used_questions, 0),
            },
            "done": state.done,
            "parse_error": result.parse_error,
        }
