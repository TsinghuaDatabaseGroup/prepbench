from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping, Optional

from .ir import DAG
from .executor import DAGExecutor


def execute_flow_dict(
    flow_dict: Mapping[str, Any],
    base_path: str | Path | None = None,
    input_tables: Mapping[str, Any] | None = None,
    **run_kwargs: Any,
) -> dict[str, Any]:
    dag = DAG.from_dict(dict(flow_dict))
    executor = DAGExecutor(dag, base_path=base_path, input_tables=input_tables)
    return executor.run(**run_kwargs)
