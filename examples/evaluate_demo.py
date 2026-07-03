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

from evaluate.core import evaluate
from prepbench.case_ids import normalize_case_id


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
        default="@output/evaluate_demo/oracle",
        help="Demo results root to write under.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    case_id = normalize_case_id(args.case)
    gt_dir = REPO_ROOT / "src" / "evaluate" / "gt" / case_id
    if not gt_dir.is_dir():
        raise FileNotFoundError(f"GT directory not found: {gt_dir}")

    cand_dir = REPO_ROOT / args.output_root / case_id / "solution" / "cand"
    if cand_dir.exists():
        shutil.rmtree(cand_dir)
    cand_dir.mkdir(parents=True, exist_ok=True)

    copied = []
    for gt_csv in sorted(gt_dir.glob("output_*.csv")):
        shutil.copy2(gt_csv, cand_dir / gt_csv.name)
        copied.append(gt_csv.name)
    if not copied:
        raise FileNotFoundError(f"No output_*.csv files found under: {gt_dir}")

    passed, first_error = evaluate(str(gt_dir), str(cand_dir))
    result = {
        "case_id": case_id,
        "candidate_dir": str(cand_dir.relative_to(REPO_ROOT)),
        "copied_outputs": copied,
        "passed": passed,
        "first_error": first_error,
    }
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
