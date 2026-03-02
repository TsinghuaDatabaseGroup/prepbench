from __future__ import annotations

import os
import re
from pathlib import Path


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def solution_assets_root(root: Path | None = None) -> Path:
    if root is not None:
        return root.resolve()
    env_root = os.getenv("PREPBENCH_SOLUTIONS_ROOT", "").strip()
    if env_root:
        return Path(env_root).expanduser().resolve()
    return repo_root() / "simulator" / "assets" / "solutions"


def _extract_case_index(case_name: str) -> str | None:
    token = str(case_name or "").strip().lower()
    if not token:
        return None
    match = re.fullmatch(r"case[_-]?(\d+)", token)
    if match:
        return f"{int(match.group(1)):03d}"
    if token.isdigit():
        return f"{int(token):03d}"
    return None


def _candidate_relative_paths(case_name: str) -> list[Path]:
    raw = str(case_name or "").strip()
    if not raw:
        return []

    candidates: list[str] = []

    def _push(value: str) -> None:
        val = value.strip()
        if val and val not in candidates:
            candidates.append(val)

    _push(raw)
    idx = _extract_case_index(raw)
    if idx is not None:
        _push(f"case_{idx}")
        _push(f"case{idx}")

    rel_paths: list[Path] = []
    seen: set[Path] = set()
    for token in candidates:
        for rel in (Path(f"{token}.py"), Path(token) / "solution.py"):
            if rel in seen:
                continue
            seen.add(rel)
            rel_paths.append(rel)
    return rel_paths


def _candidate_solution_paths(case_name: str, root: Path | None = None) -> list[Path]:
    base = solution_assets_root(root)
    return [base / rel for rel in _candidate_relative_paths(case_name)]


def external_solution_path(case_name: str, root: Path | None = None) -> Path:
    candidates = _candidate_solution_paths(case_name, root)
    if candidates:
        return candidates[0]
    return solution_assets_root(root) / f"{case_name}.py"


def preferred_reference_solution_write_path(case_name: str, root: Path | None = None) -> Path:
    base = solution_assets_root(root)
    for path in _candidate_solution_paths(case_name, root):
        if path.exists():
            return path
    idx = _extract_case_index(case_name)
    if idx is not None:
        return base / f"case{idx}" / "solution.py"
    token = str(case_name or "").strip()
    return base / f"{token}.py"


def resolve_reference_solution_path(case_dir: Path, root: Path | None = None) -> Path | None:
    """Resolve the reference solution path for a case."""
    case_name = case_dir.name
    for path in _candidate_solution_paths(case_name, root):
        if path.exists():
            return path
    return None


def require_reference_solution_path(case_dir: Path, root: Path | None = None) -> Path:
    path = resolve_reference_solution_path(case_dir, root)
    if path is not None:
        return path

    base = solution_assets_root(root)
    checked = _candidate_relative_paths(case_dir.name)
    checked_text = ", ".join(str(p) for p in checked) if checked else f"{case_dir.name}.py"
    raise FileNotFoundError(
        "Reference solution not found for "
        f"{case_dir.name}. Checked under {base}: {checked_text}. "
        "Set PREPBENCH_SOLUTIONS_ROOT to your private solutions directory if needed."
    )


def read_reference_solution_text(case_dir: Path, root: Path | None = None) -> str:
    path = resolve_reference_solution_path(case_dir, root)
    if path is None:
        return ""
    try:
        return path.read_text(encoding="utf-8")
    except Exception:
        return ""
