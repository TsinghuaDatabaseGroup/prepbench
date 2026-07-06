from __future__ import annotations

from pathlib import Path

from evaluate.batch import evaluate_case_outputs

from .case_ids import normalize_case_id
from .workspaces import MODES, normalize_mode, repo_root


def discover_gt_cases(gt_root: Path) -> list[str]:
    return [path.name for path in gt_root.glob("case_*") if path.is_dir()]


def validate_run_root_mode(run_root: Path, mode: str) -> str:
    normalized_mode = normalize_mode(mode)
    if run_root.name != normalized_mode:
        raise ValueError(f"--mode {normalized_mode!r} does not match run-root mode segment {run_root.name!r}")
    return normalized_mode


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
        case_names = discover_gt_cases(resolved_gt_root)
    if not case_names:
        raise ValueError(f"No GT case_* directories found under {resolved_gt_root}")

    return evaluate_case_outputs(
        gt_root=resolved_gt_root,
        case_names=case_names,
        candidate_dir_for_case=lambda name: resolved_run_root / name / "result",
        output_dir=resolved_run_root / "evaluation",
    )


def valid_modes() -> tuple[str, ...]:
    return MODES
