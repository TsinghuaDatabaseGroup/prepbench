from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = REPO_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from simulator import LocalUserSimulatorAPI


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run a local user-simulator demo.")
    parser.add_argument("--case", default="case_001")
    parser.add_argument("--run-id", default="demo")
    parser.add_argument(
        "--question",
        default="Should the monthly date be represented as the first day of each month?",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    api = LocalUserSimulatorAPI(max_rounds=3, question_ratio=2.5)
    session = api.start_session(case_id=args.case, run_id=args.run_id)
    response = api.ask(
        session_id=session["session_id"],
        questions=[args.question],
        round=1,
    )
    print(json.dumps({"session": session, "response": response}, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
