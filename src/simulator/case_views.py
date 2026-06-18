from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from simulator.case_assets import read_reference_solution_text


@dataclass(frozen=True)
class PublicCaseView:
    case_dir: Path
    case_id: str
    query_path: Path
    query_text: str
    input_dir: Path
    input_files: tuple[Path, ...]


@dataclass(frozen=True)
class InternalCaseView(PublicCaseView):
    query_full_path: Path
    query_full_text: str
    amb_kb_path: Path
    amb_kb_json: dict[str, Any]
    reference_solution_text: str


def _require_case_dir(case_dir: Path) -> Path:
    resolved = case_dir.resolve()
    if not resolved.is_dir():
        raise FileNotFoundError(f"Case directory not found: {resolved}")
    return resolved


def _read_required_text(path: Path) -> str:
    if not path.exists():
        raise FileNotFoundError(f"Required file not found: {path}")
    return path.read_text(encoding="utf-8")


def _read_required_json_object(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(f"Required file not found: {path}")
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"Expected JSON object in {path}")
    return data


def load_public_case_view(case_dir: Path) -> PublicCaseView:
    resolved_case = _require_case_dir(case_dir)
    query_path = resolved_case / "query.md"
    query_text = _read_required_text(query_path)

    input_dir = resolved_case / "inputs"
    if not input_dir.is_dir():
        raise FileNotFoundError(f"Required directory not found: {input_dir}")
    input_files = tuple(sorted(input_dir.glob("*.csv")))

    return PublicCaseView(
        case_dir=resolved_case,
        case_id=resolved_case.name,
        query_path=query_path,
        query_text=query_text,
        input_dir=input_dir,
        input_files=input_files,
    )


def load_internal_case_view(
    case_dir: Path,
    *,
    require_reference_solution: bool = False,
) -> InternalCaseView:
    public = load_public_case_view(case_dir)
    query_full_path = public.case_dir / "query_full.md"
    amb_kb_path = public.case_dir / "amb_kb.json"

    query_full_text = _read_required_text(query_full_path)
    amb_kb_json = _read_required_json_object(amb_kb_path)
    reference_solution_text = read_reference_solution_text(public.case_dir)
    if require_reference_solution and not reference_solution_text.strip():
        raise FileNotFoundError(
            "Reference solution is required for "
            f"{public.case_id}. Set PREPBENCH_SOLUTIONS_ROOT to your private "
            "solutions directory if not using the default local mount point."
        )

    return InternalCaseView(
        case_dir=public.case_dir,
        case_id=public.case_id,
        query_path=public.query_path,
        query_text=public.query_text,
        input_dir=public.input_dir,
        input_files=public.input_files,
        query_full_path=query_full_path,
        query_full_text=query_full_text,
        amb_kb_path=amb_kb_path,
        amb_kb_json=amb_kb_json,
        reference_solution_text=reference_solution_text,
    )
