from __future__ import annotations

import json
import os
import shutil
from pathlib import Path
from typing import Literal

from .case_ids import normalize_case_id


Mode = Literal["clarified", "interactive", "workflow"]
MODES: tuple[str, ...] = ("clarified", "interactive", "workflow")


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def normalize_mode(mode: str) -> Mode:
    value = str(mode or "").strip().lower()
    if value not in MODES:
        raise ValueError(f"mode must be one of {', '.join(MODES)}")
    return value  # type: ignore[return-value]


def _case_sort_key(value: str | Path) -> int:
    name = Path(value).name
    try:
        return int(name.split("_", 1)[1])
    except Exception:
        return 10**9


def resolve_repo_path(path: str | Path) -> Path:
    path_obj = Path(path).expanduser()
    if not path_obj.is_absolute():
        path_obj = repo_root() / path_obj
    return path_obj.resolve()


def discover_case_ids(case_root: str | Path) -> list[str]:
    root = resolve_repo_path(case_root)
    if not root.is_dir():
        raise FileNotFoundError(f"case root not found: {root}")
    return sorted([path.name for path in root.glob("case_*") if path.is_dir()], key=_case_sort_key)


def validate_run_root_mode(run_root: Path, mode: str) -> str:
    normalized_mode = normalize_mode(mode)
    if run_root.name != normalized_mode:
        raise ValueError(f"--mode {normalized_mode!r} does not match run-root mode segment {run_root.name!r}")
    return normalized_mode


def _relative_symlink(target: Path, link_path: Path) -> None:
    link_path.parent.mkdir(parents=True, exist_ok=True)
    relative_target = os.path.relpath(target.resolve(), start=link_path.parent.resolve())
    link_path.symlink_to(relative_target)


def _reset_workspace(path: Path, *, force: bool) -> None:
    if not path.exists() and not path.is_symlink():
        return
    if not force:
        raise FileExistsError(f"workspace already exists: {path}")
    if path.is_dir() and not path.is_symlink():
        shutil.rmtree(path)
    else:
        path.unlink()


def _symlink_input_files(source_dir: Path, workspace_inputs: Path) -> None:
    workspace_inputs.mkdir(parents=True, exist_ok=True)
    for source_path in sorted(source_dir.rglob("*")):
        relative = source_path.relative_to(source_dir)
        target_path = workspace_inputs / relative
        if source_path.is_dir():
            target_path.mkdir(parents=True, exist_ok=True)
            continue
        if source_path.is_file():
            _relative_symlink(source_path, target_path)


def _write_simulator_doc(path: Path, *, case_id: str) -> None:
    path.write_text(
        f"""# User Simulator

Use the Python API when the agent needs clarification:

```python
from simulator import LocalUserSimulatorAPI

api = LocalUserSimulatorAPI()
session = api.start_session(case_id="{case_id}", run_id="run")
reply = api.ask(session_id=session["session_id"], questions=["<clarification question>"])
```

Honor-system boundary: do not read `query_full.md`, `amb_kb.json`, or ground-truth outputs when running interactive/workflow mode.
""",
        encoding="utf-8",
    )


def prepare_case_workspace(
    *,
    case_id: str,
    mode: str,
    run_root: str | Path,
    data_root: str | Path | None = None,
    workflow_prompt: str | Path | None = None,
    force: bool = False,
) -> Path:
    normalized_case_id = normalize_case_id(case_id)
    normalized_mode = normalize_mode(mode)
    root = repo_root()
    resolved_data_root = Path(data_root).expanduser() if data_root is not None else root / "data"
    if not resolved_data_root.is_absolute():
        resolved_data_root = root / resolved_data_root
    case_dir = (resolved_data_root / normalized_case_id).resolve()
    if not case_dir.is_dir():
        raise FileNotFoundError(f"case directory not found: {case_dir}")
    source_inputs = case_dir / "inputs"
    if not source_inputs.is_dir():
        raise FileNotFoundError(f"inputs directory not found: {source_inputs}")

    query_name = "query_full.md" if normalized_mode == "clarified" else "query.md"
    query_path = case_dir / query_name
    if not query_path.is_file():
        raise FileNotFoundError(f"query file not found: {query_path}")

    resolved_run_root = Path(run_root).expanduser()
    if not resolved_run_root.is_absolute():
        resolved_run_root = root / resolved_run_root
    validate_run_root_mode(resolved_run_root, normalized_mode)
    workspace = (resolved_run_root / normalized_case_id).resolve()
    _reset_workspace(workspace, force=force)

    workspace.mkdir(parents=True, exist_ok=True)
    _relative_symlink(query_path, workspace / "query.md")
    _symlink_input_files(source_inputs, workspace / "inputs")
    (workspace / "result").mkdir(parents=True, exist_ok=True)

    if normalized_mode in {"interactive", "workflow"}:
        _write_simulator_doc(workspace / "simulator.md", case_id=normalized_case_id)

    if normalized_mode == "workflow":
        prompt_path = Path(workflow_prompt).expanduser() if workflow_prompt is not None else root / "src" / "agents" / "prompts" / "flow_agent.yaml"
        if not prompt_path.is_absolute():
            prompt_path = root / prompt_path
        if not prompt_path.is_file():
            raise FileNotFoundError(f"workflow prompt not found: {prompt_path}")
        _relative_symlink(prompt_path, workspace / "workflow_prompt.yaml")

    return workspace


def workspace_summary(workspace: Path, *, case_id: str, mode: str) -> dict[str, object]:
    return {
        "case_id": normalize_case_id(case_id),
        "mode": normalize_mode(mode),
        "workspace": str(workspace),
        "result_dir": str(workspace / "result"),
        "files": sorted(path.name for path in workspace.iterdir()),
    }


def workspace_summary_json(workspace: Path, *, case_id: str, mode: str) -> str:
    return json.dumps(workspace_summary(workspace, case_id=case_id, mode=mode), ensure_ascii=False, indent=2)
