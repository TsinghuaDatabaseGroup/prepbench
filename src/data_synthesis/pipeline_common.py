from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, Optional

from core.case_assets import solution_assets_root
from core.data_head import DataHead
from core.executor import CodeExecutor
from core.utils.code import extract_single_solution_from_raw
from evaluate.core import evaluate


@dataclass(frozen=True)
class RepoPaths:
    repo_root: Path
    data_root: Path
    gt_root: Path
    solutions_root: Path
    output_root: Path


def build_repo_paths() -> RepoPaths:
    repo_root = Path(__file__).resolve().parents[2]
    return RepoPaths(
        repo_root=repo_root,
        data_root=repo_root / "data",
        gt_root=repo_root / "src" / "evaluate" / "gt",
        solutions_root=solution_assets_root(),
        output_root=repo_root / "src" / "data_synthesis" / "output",
    )


def normalize_model_dir(model: str) -> str:
    if not isinstance(model, str) or not model.strip():
        raise ValueError("model must be a non-empty string")
    return model.strip().replace("/", "__")


def parse_case_selector(selector: str) -> list[str]:
    if not selector:
        return []

    out: list[str] = []
    for part in selector.split(","):
        token = part.strip()
        if not token:
            continue
        if "-" in token:
            left, right = token.split("-", 1)
            if left.isdigit() and right.isdigit():
                start, end = int(left), int(right)
                if start > end:
                    start, end = end, start
                out.extend(f"case_{i:03d}" for i in range(start, end + 1))
                continue
        if token.isdigit():
            out.append(f"case_{int(token):03d}")
            continue
        out.append(token)

    # stable dedupe
    seen: set[str] = set()
    deduped: list[str] = []
    for case_name in out:
        if case_name in seen:
            continue
        seen.add(case_name)
        deduped.append(case_name)
    return deduped


def list_cases(data_root: Path, selector: str) -> list[str]:
    requested = parse_case_selector(selector)
    if requested:
        return [name for name in requested if (data_root / name).is_dir()]
    return sorted(p.name for p in data_root.glob("case_*") if p.is_dir())


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def profile_inputs(input_dir: Path) -> dict[str, Any]:
    preview = DataHead().get_preview(input_dir)
    return preview if isinstance(preview, dict) else {}


def profile_summary_text(input_dir: Path) -> str:
    summary = profile_inputs(input_dir)
    return json.dumps(summary, ensure_ascii=False, indent=2)


def summarize_eval_error(error: Optional[dict[str, Any]]) -> str:
    if not isinstance(error, dict):
        return "unknown evaluation mismatch"
    error_type = str(error.get("error_type") or "UNKNOWN")
    message = str(error.get("message") or "")
    detail = error.get("detail")
    detail_text = ""
    if isinstance(detail, dict) and detail:
        detail_text = json.dumps(detail, ensure_ascii=False)
    parts = [f"type={error_type}"]
    if message:
        parts.append(f"message={message}")
    if detail_text:
        parts.append(f"detail={detail_text}")
    return " | ".join(parts)


def evaluate_candidate(case_name: str, cand_dir: Path, gt_root: Path) -> tuple[bool, Optional[dict[str, Any]]]:
    gt_dir = gt_root / case_name
    if not gt_dir.is_dir():
        return False, {"error_type": "GT_NOT_FOUND", "message": f"GT dir not found: {gt_dir}"}
    return evaluate(str(gt_dir), str(cand_dir))


def extract_solve_code(raw_text: str) -> str:
    code, _ = extract_single_solution_from_raw(raw_text)
    return code.strip()


def execute_solve_code(
    solve_code: str,
    input_dir: Path,
    work_dir: Path,
    *,
    timeout: int,
) -> dict[str, Any]:
    work_dir.mkdir(parents=True, exist_ok=True)
    solution_dir = work_dir / "solution"
    solution_dir.mkdir(parents=True, exist_ok=True)

    if not solve_code.strip():
        return {
            "ok": False,
            "rc": 1,
            "stderr": "empty solve code",
            "stdout": "",
            "cand_dir": str((solution_dir / "cand").resolve()),
            "code_path": str((solution_dir / "code.py").resolve()),
            "main_path": str((solution_dir / "main.py").resolve()),
        }

    try:
        tmpl_path = Path(__file__).resolve().parents[1] / "core" / "templates" / "solve_template.py.j2"
        if not tmpl_path.exists():
            raise FileNotFoundError(f"Template not found: {tmpl_path}")
        tmpl = tmpl_path.read_text(encoding="utf-8")
        main_code = tmpl.replace("{{ solve_source }}", solve_code)
    except Exception as exc:
        return {
            "ok": False,
            "rc": 1,
            "stderr": f"render_main_failed: {exc}",
            "stdout": "",
            "cand_dir": str((solution_dir / "cand").resolve()),
            "code_path": str((solution_dir / "code.py").resolve()),
            "main_path": str((solution_dir / "main.py").resolve()),
        }

    code_path = solution_dir / "code.py"
    main_path = solution_dir / "main.py"
    code_path.write_text(solve_code, encoding="utf-8")
    main_path.write_text(main_code, encoding="utf-8")

    input_files = {p.name: p for p in sorted(input_dir.glob("*.csv"))}
    executor = CodeExecutor()
    ok, stderr, stdout, _ = executor.execute_code(main_code, input_files, timeout=timeout, work_dir=solution_dir)
    return {
        "ok": bool(ok),
        "rc": 0 if ok else 1,
        "stderr": stderr,
        "stdout": stdout,
        "cand_dir": str((solution_dir / "cand").resolve()),
        "code_path": str(code_path.resolve()),
        "main_path": str(main_path.resolve()),
    }


def ensure_parent(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def save_lines(path: Path, lines: Iterable[str]) -> None:
    ensure_parent(path)
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
