from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = REPO_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from prepbench.case_ids import normalize_case_id
from prepbench.submission_eval import evaluate_submission


EXPECTED_CLI_ERRORS = (FileNotFoundError, RuntimeError, ValueError)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Create a known-correct single-case candidate from GT and verify "
            "that the PrepBench evaluator accepts it."
        )
    )
    parser.add_argument("--case", default="case_001", help="Case id to demo, such as case_001 or 1.")
    parser.add_argument(
        "--output-root",
        default="@runs/evaluate_demo/clarified",
        help="Demo run root to write under.",
    )
    parser.add_argument("--mode", default="clarified", choices=["clarified", "interactive", "workflow"])
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    case_id = normalize_case_id(args.case)
    gt_dir = REPO_ROOT / "src" / "evaluate" / "gt" / case_id
    if not gt_dir.is_dir():
        raise FileNotFoundError(f"GT directory not found: {gt_dir}")

    run_root = REPO_ROOT / args.output_root
    if run_root.name != args.mode:
        raise ValueError(f"--mode {args.mode!r} does not match output root segment {run_root.name!r}")

    cand_dir = run_root / case_id / "result"
    if cand_dir.exists():
        shutil.rmtree(cand_dir)
    cand_dir.mkdir(parents=True, exist_ok=True)

    copied = []
    for gt_csv in sorted(gt_dir.glob("output_*.csv")):
        shutil.copy2(gt_csv, cand_dir / gt_csv.name)
        copied.append(gt_csv.name)
    if not copied:
        raise FileNotFoundError(f"No output_*.csv files found under: {gt_dir}")

    summary = evaluate_submission(run_root=run_root, mode=args.mode, case_id=case_id)
    aggregate = summary["aggregate"]
    result = {
        "case_id": case_id,
        "candidate_dir": str(cand_dir.relative_to(REPO_ROOT)),
        "copied_outputs": copied,
        "passed": bool(aggregate["passed"]),
        "summary_path": str((run_root / "evaluation" / "summary.json").relative_to(REPO_ROOT)),
    }
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if aggregate["passed"] else 1


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except EXPECTED_CLI_ERRORS as exc:
        print(f"error: {exc}", file=sys.stderr)
        raise SystemExit(2)
