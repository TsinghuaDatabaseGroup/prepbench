from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Callable, Optional

from evaluate.core import evaluate


CandidateDirResolver = Callable[[str], Optional[Path]]


FIELDNAMES = [
    "case_name",
    "execution",
    "evaluation",
    "candidate_dir",
    "gt_dir",
    "error_type",
    "error_message",
]


def _case_sort_key(value: str | Path) -> int:
    name = Path(value).name
    try:
        return int(name.split("_", 1)[1])
    except Exception:
        return 10**9


def _row_template(case_name: str, gt_case_dir: Path, cand_dir: Path | None) -> dict[str, str]:
    return {
        "case_name": case_name,
        "execution": "fail",
        "evaluation": "false",
        "candidate_dir": str(cand_dir.resolve()) if cand_dir else "",
        "gt_dir": str(gt_case_dir.resolve()),
        "error_type": "",
        "error_message": "",
    }


def _aggregate(rows: list[dict[str, str]]) -> dict[str, object]:
    total = len(rows)
    success_count = sum(1 for row in rows if row["execution"] == "success")
    correct_count = sum(1 for row in rows if row["evaluation"] == "correct")
    missing_count = sum(1 for row in rows if row["error_type"] == "NOT_FOUND")
    failed_count = total - correct_count
    return {
        "total": total,
        "success": success_count,
        "correct": correct_count,
        "missing": missing_count,
        "failed": failed_count,
        "accuracy": (correct_count / total) if total else 0.0,
        "passed": total > 0 and correct_count == total,
    }


def evaluate_case_outputs(
    *,
    gt_root: Path,
    case_names: list[str],
    candidate_dir_for_case: CandidateDirResolver,
    output_dir: Path,
    summary_csv_name: str = "summary.csv",
    summary_json_name: str = "summary.json",
) -> dict[str, object]:
    if not gt_root.is_dir():
        raise FileNotFoundError(f"GT root not found: {gt_root}")
    if not case_names:
        raise ValueError("No case ids to evaluate")

    output_dir.mkdir(parents=True, exist_ok=True)
    rows: list[dict[str, str]] = []

    for case_name in sorted(case_names, key=_case_sort_key):
        gt_case_dir = gt_root / case_name
        cand_dir = candidate_dir_for_case(case_name)
        row = _row_template(case_name, gt_case_dir, cand_dir)

        if not gt_case_dir.is_dir():
            row["error_type"] = "GT_NOT_FOUND"
            row["error_message"] = f"GT case directory not found: {gt_case_dir}"
            rows.append(row)
            continue

        if cand_dir is None or not cand_dir.is_dir() or not any(cand_dir.glob("output_*.csv")):
            row["error_type"] = "NOT_FOUND"
            expected = cand_dir if cand_dir is not None else Path(case_name)
            row["error_message"] = f"No candidate output_*.csv files found under {expected}."
            rows.append(row)
            continue

        passed, first_error = evaluate(str(gt_case_dir), str(cand_dir))
        row["execution"] = "success"
        row["evaluation"] = "correct" if bool(passed) else "false"
        if not passed and isinstance(first_error, dict):
            row["error_type"] = str(first_error.get("error_type") or "UNKNOWN")
            row["error_message"] = str(first_error.get("message") or "")
        rows.append(row)

    summary_csv = output_dir / summary_csv_name
    with summary_csv.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)

    aggregate = _aggregate(rows)
    summary_json = output_dir / summary_json_name
    summary = {
        "aggregate": aggregate,
        "cases": rows,
        "summary_csv": str(summary_csv),
    }
    summary_json.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    summary["summary_json"] = str(summary_json)
    return summary
