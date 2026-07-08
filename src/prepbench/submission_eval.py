from __future__ import annotations

import csv
import json
from pathlib import Path

from evaluate.batch import FIELDNAMES, evaluate_case_outputs

from .case_ids import normalize_case_id
from .workspaces import MODES, discover_case_ids, repo_root, validate_run_root_mode


def evaluate_submission(
    *,
    run_root: str | Path,
    mode: str,
    case_id: str | None = None,
    gt_root: str | Path | None = None,
) -> dict[str, object]:
    resolved_run_root = Path(run_root).expanduser()
    if not resolved_run_root.is_absolute():
        resolved_run_root = repo_root() / resolved_run_root
    resolved_run_root = resolved_run_root.resolve()
    if not resolved_run_root.is_dir():
        raise FileNotFoundError(f"run root not found: {resolved_run_root}")

    validate_run_root_mode(resolved_run_root, mode)
    resolved_gt_root = Path(gt_root).expanduser() if gt_root is not None else repo_root() / "src" / "evaluate" / "gt"
    if not resolved_gt_root.is_absolute():
        resolved_gt_root = repo_root() / resolved_gt_root
    resolved_gt_root = resolved_gt_root.resolve()
    if not resolved_gt_root.is_dir():
        raise FileNotFoundError(f"GT root not found: {resolved_gt_root}")

    if case_id:
        case_names = [normalize_case_id(case_id)]
    else:
        case_names = discover_case_ids(resolved_gt_root)
    if not case_names:
        raise ValueError(f"No GT case_* directories found under {resolved_gt_root}")

    summary = evaluate_case_outputs(
        gt_root=resolved_gt_root,
        case_names=case_names,
        candidate_dir_for_case=lambda name: resolved_run_root / name / "result",
        output_dir=resolved_run_root / "evaluation",
    )
    if case_id:
        case_name = case_names[0]
        case_csv = resolved_run_root / "evaluation" / f"{case_name}.summary.csv"
        with case_csv.open("w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
            writer.writeheader()
            writer.writerows(summary["cases"])
        case_json = resolved_run_root / "evaluation" / f"{case_name}.summary.json"
        case_summary = dict(summary)
        case_summary["summary_csv"] = str(case_csv)
        case_summary["summary_json"] = str(case_json)
        case_json.write_text(json.dumps(case_summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        summary["case_summary_csv"] = str(case_csv)
        summary["case_summary_json"] = str(case_json)
    return summary


def valid_modes() -> tuple[str, ...]:
    return MODES
