from typing import Any, Dict, Optional, Tuple
from pathlib import Path

from .evaluator import Evaluator


def _resolve_config_path(gt_dir: str, config_path: Optional[str]) -> Optional[str]:
    """If config_path is not provided, auto-discover config.json under gt_dir."""
    if config_path:
        return config_path
    cfg = Path(gt_dir) / "config.json"
    if cfg.exists() and cfg.is_file():
        return str(cfg)
    return None


def evaluate(
    gt_dir: str,
    cand_dir: str,
    config_path: Optional[str] = None,
) -> Tuple[bool, Optional[Dict[str, Any]]]:
    """
    Runs the evaluation and returns (passed, first_error).
    - passed: True if all files match
    - first_error: first mismatch entry or None on success
    """
    resolved_cfg = _resolve_config_path(gt_dir, config_path)
    evaluator = Evaluator(gt_dir, cand_dir, resolved_cfg)
    report = evaluator.run()
    passed = bool(report.get("passed", False))
    if passed:
        return True, None
    errors = report.get("errors") or []
    if errors:
        return False, errors[0]
    return False, {"error_type": "UNKNOWN", "message": "Evaluation failed without error details"}

