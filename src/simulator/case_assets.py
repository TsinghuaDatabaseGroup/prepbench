from __future__ import annotations

import os
import re
from pathlib import Path


def package_root() -> Path:
    return Path(__file__).resolve().parents[1]


def solution_assets_root(root: Path | None = None) -> Path:
    if root is not None:
        return root.resolve()
    env_root = os.getenv("PREPBENCH_SOLUTIONS_ROOT", "").strip()
    if env_root:
        return Path(env_root).expanduser().resolve()
    return package_root() / "simulator" / "assets" / "solutions"


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

    def push(value: str) -> None:
        val = value.strip()
        if val and val not in candidates:
            candidates.append(val)

    push(raw)
    idx = _extract_case_index(raw)
    if idx is not None:
        push(f"case_{idx}")
        push(f"case{idx}")

    rel_paths: list[Path] = []
    seen: set[Path] = set()
    for token in candidates:
        for rel in (Path(f"{token}.py"), Path(token) / "solution.py"):
            if rel in seen:
                continue
            seen.add(rel)
            rel_paths.append(rel)
    return rel_paths


def resolve_reference_solution_path(case_dir: Path, root: Path | None = None) -> Path | None:
    base = solution_assets_root(root)
    for rel in _candidate_relative_paths(case_dir.name):
        path = base / rel
        if path.exists():
            return path
    return None


def read_reference_solution_text(case_dir: Path, root: Path | None = None) -> str:
    path = resolve_reference_solution_path(case_dir, root)
    if path is None:
        return ""
    try:
        return path.read_text(encoding="utf-8")
    except Exception:
        return ""
