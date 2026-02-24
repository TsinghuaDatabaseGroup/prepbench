from __future__ import annotations

import shutil
from pathlib import Path

from core.orchestration.mode_spec import get_mode_spec


def summarize_eval(eval_report: dict) -> dict:
    return {
        "passed": bool(eval_report.get("passed", False)),
        "errors": (eval_report.get("errors") or [])[:20],
        "diff_summary": eval_report.get("diff_summary", {}),
    }


def resolve_query_path(
    tdir: Path,
    *,
    run_mode: str,
) -> Path:
    """Resolve query file path based on run_mode.

    - disamb/disamb_only: uses query_full.md
    - orig/interact/e2e: uses query.md
    - flow: solution-only mode; query file is not used by flow execution
    """
    spec = get_mode_spec(run_mode)
    if spec.query_source == "query_full":
        return tdir / "query_full.md"
    if spec.query_source == "solution_only":
        # Kept for compatibility with callers expecting a Path.
        # Flow execution itself reads reference solution code directly.
        return tdir / "query.md"
    return tdir / "query.md"


def copy_solution_artifacts(final_solution_src: Path, final_solution_dst: Path) -> None:
    final_solution_dst.mkdir(parents=True, exist_ok=True)

    code_src = final_solution_src / "code.py"
    if code_src.exists():
        shutil.copy2(code_src, final_solution_dst / "solution.py")

    main_src = final_solution_src / "main.py"
    if main_src.exists():
        shutil.copy2(main_src, final_solution_dst / "main.py")

    exec_src = final_solution_src / "execution.json"
    if exec_src.exists():
        shutil.copy2(exec_src, final_solution_dst / "execution.json")

    eval_src = final_solution_src / "evaluation.json"
    if eval_src.exists():
        shutil.copy2(eval_src, final_solution_dst / "evaluation.json")

    cand_src = final_solution_src / "cand"
    if cand_src.exists():
        cand_dst = final_solution_dst / "cand"
        if cand_dst.exists():
            shutil.rmtree(cand_dst)
        shutil.copytree(cand_src, cand_dst)

    # Flow mode artifacts
    flow_json_src = final_solution_src / "flow.json"
    if flow_json_src.exists():
        shutil.copy2(flow_json_src, final_solution_dst / "flow.json")

    flow_cand_src = final_solution_src / "flow_cand"
    if flow_cand_src.exists():
        flow_cand_dst = final_solution_dst / "flow_cand"
        if flow_cand_dst.exists():
            shutil.rmtree(flow_cand_dst)
        shutil.copytree(flow_cand_src, flow_cand_dst)
