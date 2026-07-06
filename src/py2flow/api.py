from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping

from .ir import DAG
from .executor import DAGExecutor
from .exec_flow import exec_flow


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
