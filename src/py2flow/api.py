from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping

from .ir import DAG
from .executor import DAGExecutor
from .errors import FlowError, error_to_dict
from .exec_flow import exec_flow


WORKFLOW_ERROR_TYPES = (FileNotFoundError, FlowError, RuntimeError, ValueError)


def missing_output_files_error(output_root: str | Path) -> dict[str, object]:
    return {
        "type": "workflow_contract_error",
        "message": "Workflow executed but did not write any output_*.csv files directly under output_root.",
        "node_id": None,
        "step_kind": None,
        "field": "output_root",
        "error_code": "missing_output_files",
        "help": "Use output params.path like 'output_01.csv', not 'result/output_01.csv' or another nested path.",
        "output_root": str(Path(output_root).expanduser().resolve()),
    }


def execute_flow_dict(
    flow_dict: Mapping[str, Any],
    base_path: str | Path | None = None,
    input_tables: Mapping[str, Any] | None = None,
    **run_kwargs: Any,
) -> dict[str, Any]:
    dag = DAG.from_dict(dict(flow_dict))
    executor = DAGExecutor(dag, base_path=base_path, input_tables=input_tables)
    return executor.run(**run_kwargs)


def execute_flow_file(
    flow_path: str | Path,
    input_root: str | Path | None = None,
    output_root: str | Path | None = None,
    **run_kwargs: Any,
) -> dict[str, object]:
    cwd = Path.cwd()
    resolved_input_root = Path(input_root) if input_root is not None else cwd / "inputs"
    resolved_output_root = Path(output_root) if output_root is not None else cwd / "result"
    resolved_output_root.mkdir(parents=True, exist_ok=True)
    return exec_flow(
        flow_path=flow_path,
        input_root=resolved_input_root,
        output_root=resolved_output_root,
        **run_kwargs,
    )


def run_flow_file(
    flow_path: str | Path,
    input_root: str | Path | None = None,
    output_root: str | Path | None = None,
    require_outputs: bool = False,
    **run_kwargs: Any,
) -> dict[str, object]:
    cwd = Path.cwd()
    resolved_output_root = Path(output_root) if output_root is not None else cwd / "result"
    resolved_output_root = resolved_output_root.expanduser().resolve()
    try:
        result = execute_flow_file(
            flow_path=flow_path,
            input_root=input_root,
            output_root=resolved_output_root,
            **run_kwargs,
        )
    except WORKFLOW_ERROR_TYPES as exc:
        return {"ok": False, "result": None, "error": error_to_dict(exc)}
    if require_outputs and not (run_kwargs.get("explain") or run_kwargs.get("validate_only")):
        output_files = sorted(path.name for path in resolved_output_root.glob("output_*.csv"))
        if not output_files:
            return {"ok": False, "result": None, "error": missing_output_files_error(resolved_output_root)}
    return {"ok": True, "result": result, "error": None}
