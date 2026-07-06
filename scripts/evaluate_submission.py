from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = REPO_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from prepbench.submission_eval import evaluate_submission, valid_modes


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Evaluate PrepBench result tables under a run root.")
    parser.add_argument("--mode", required=True, choices=valid_modes(), help="Public mode to evaluate.")
    parser.add_argument("--run-root", required=True, help="Run root like @runs/<agent>/<mode>.")
    parser.add_argument("--case", default="", help="Optional single case id for debugging.")
    parser.add_argument("--gt-root", default="src/evaluate/gt", help="Ground-truth root.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    summary = evaluate_submission(
        run_root=args.run_root,
        mode=args.mode,
        case_id=args.case or None,
        gt_root=args.gt_root,
    )
    print(json.dumps(summary["aggregate"], ensure_ascii=False, indent=2))
    aggregate = summary.get("aggregate")
    passed = isinstance(aggregate, dict) and bool(aggregate.get("passed"))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
