from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = REPO_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from simulator import LocalUserSimulatorAPI


DEFAULT_QUESTION = "Should the monthly date be represented as the first day of each month?"
EXPECTED_CLI_ERRORS = (FileNotFoundError, RuntimeError, ValueError)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Check whether the local user simulator backend is usable.")
    parser.add_argument("--case", default="case_001", help="Case id to use for the check.")
    parser.add_argument("--run-id", default="simulator_check", help="Run id used in the simulator session.")
    parser.add_argument("--question", default=DEFAULT_QUESTION, help="Clarification question to ask.")
    return parser.parse_args()


def _backend_payload(api: LocalUserSimulatorAPI) -> dict[str, Any]:
    simulator = api.user_simulator
    return {
        "model": simulator.model_name,
        "base_url": simulator.base_url,
        "thinking": simulator.thinking_type,
        "temperature": simulator.temperature,
    }


def main() -> int:
    args = parse_args()
    payload: dict[str, Any] = {"ok": False, "case_id": args.case}
    try:
        api = LocalUserSimulatorAPI(max_rounds=1, max_questions=1, max_questions_per_ask=1)
        payload["backend"] = _backend_payload(api)
        session = api.start_session(case_id=args.case, run_id=args.run_id)
        response = api.ask(session_id=session["session_id"], questions=[args.question])
        answer = (response.get("answers") or [{}])[0]
        payload.update(
            {
                "ok": True,
                "case_id": response.get("case_id"),
                "session_started": True,
                "ask_ok": True,
                "parse_ok": response.get("parse_error") is None,
                "classification": answer.get("classification"),
                "answer": answer.get("answer"),
                "ref": answer.get("ref"),
                "parse_error": response.get("parse_error"),
            }
        )
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 0 if payload["parse_ok"] else 1
    except EXPECTED_CLI_ERRORS as exc:
        payload["error"] = str(exc)
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
