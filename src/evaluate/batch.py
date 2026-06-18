from __future__ import annotations

import argparse
import csv
from pathlib import Path
from typing import Optional

from evaluate.core import evaluate


def _resolve_repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def _discover_case_dirs(results_root: Path) -> list[Path]:
    direct = sorted(
        [p for p in results_root.glob("case_*") if p.is_dir()],
        key=lambda p: p.name,
    )
    if direct:
        return direct

    nested = sorted(
        [p for p in results_root.rglob("case_*") if p.is_dir() and (p / "solution").is_dir()],
        key=lambda p: str(p),
    )
    return nested


def _pick_candidate_dir(case_dir: Path) -> tuple[str, Optional[Path]]:
    solution_dir = case_dir / "solution"
    cand = solution_dir / "cand"
    if cand.is_dir() and any(cand.glob("*.csv")):
        return "cand", cand
    return "none", None


def run_batch(results_root: Path) -> Path:
    repo_root = _resolve_repo_root()
    gt_root = repo_root / "evaluate" / "gt"
    if not gt_root.is_dir():
        raise FileNotFoundError(f"GT root not found: {gt_root}")

    gt_case_dirs = sorted(
        [p for p in gt_root.glob("case_*") if p.is_dir()],
        key=lambda p: p.name,
    )
    if not gt_case_dirs:
        raise FileNotFoundError(f"No GT case_* directories found under: {gt_root}")

    discovered_case_dirs = _discover_case_dirs(results_root)
    case_dir_by_name: dict[str, Path] = {}
    for case_dir in discovered_case_dirs:
        case_dir_by_name.setdefault(case_dir.name, case_dir)

    output_csv = results_root / "evaluation_summary.csv"
    acc_txt = results_root / "acc.txt"
    rows: list[dict[str, str]] = []

    for gt_case_dir in gt_case_dirs:
        case_name = gt_case_dir.name
        case_dir = case_dir_by_name.get(case_name)
        cand_kind = "none"
        cand_dir: Optional[Path] = None
        if case_dir is not None:
            cand_kind, cand_dir = _pick_candidate_dir(case_dir)

        row = {
            "case_name": case_name,
            "execution": "fail",
            "evaluation": "false",
            "candidate_dir": str(cand_dir.resolve()) if cand_dir else "",
            "gt_dir": str(gt_case_dir.resolve()),
            "error_type": "",
            "error_message": "",
        }

        if case_dir is None:
            row["error_type"] = "NOT_FOUND"
            row["error_message"] = f"Result case directory not found: {results_root / case_name}"
            rows.append(row)
            continue

        if cand_dir is None:
            row["error_type"] = "NOT_FOUND"
            row["error_message"] = f"No candidate CSV outputs found under {case_dir / 'solution' / 'cand'}."
            rows.append(row)
            continue

        passed, first_error = evaluate(str(gt_case_dir), str(cand_dir))
        row["execution"] = "success"
        row["evaluation"] = "correct" if bool(passed) else "false"
        if not passed and isinstance(first_error, dict):
            row["error_type"] = str(first_error.get("error_type") or "UNKNOWN")
            row["error_message"] = str(first_error.get("message") or "")
        rows.append(row)

    fieldnames = [
        "case_name",
        "execution",
        "evaluation",
        "candidate_dir",
        "gt_dir",
        "error_type",
        "error_message",
    ]
    with output_csv.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    total = len(rows)
    success_count = sum(1 for r in rows if r["execution"] == "success")
    correct_count = sum(1 for r in rows if r["evaluation"] == "correct")
    accuracy = (correct_count / total) if total > 0 else 0.0
    acc_txt.write_text(f"{accuracy:.6f}\n", encoding="utf-8")
    print(
        f"[evaluate.batch] total={total} success={success_count} correct={correct_count} "
        f"accuracy={accuracy:.6f} candidate_dir=cand output={output_csv} acc={acc_txt}"
    )
    return output_csv


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Batch-evaluate PrepBench results under a single results root."
    )
    parser.add_argument(
        "--results-root",
        required=True,
        type=str,
        help="Path like @output/<method>/<track>, containing case_* directories.",
    )
    args = parser.parse_args()

    results_root = Path(args.results_root).resolve()
    if not results_root.is_dir():
        raise FileNotFoundError(f"results_root is not a directory: {results_root}")

    run_batch(results_root)


if __name__ == "__main__":
    main()
