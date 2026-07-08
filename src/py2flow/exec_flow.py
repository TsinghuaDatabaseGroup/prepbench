from __future__ import annotations

import json
import logging
import os
from pathlib import Path
from typing import Any

from py2flow.executor import DAGExecutor
from py2flow.executor import DebugConfig
from py2flow.ir import DAG


def _resolve_under_root(root: Path, relative: Path, *, field: str) -> Path:
    root_resolved = root.resolve()
    candidate = Path(os.path.abspath(os.path.normpath(str(root_resolved / relative))))
    try:
        candidate.relative_to(root_resolved)
    except ValueError as exc:
        raise ValueError(f"{field} path escapes configured root: {relative}") from exc
    return candidate


def _map_input_paths_to_input_root(flow_dict: dict[str, Any], input_root: Path) -> None:
    nodes = flow_dict.get("nodes")
    if not isinstance(nodes, dict):
        return

    for node in nodes.values():
        if not isinstance(node, dict) or node.get("kind") != "input":
            continue
        params = node.get("params")
        if not isinstance(params, dict):
            continue
        raw_path = params.get("path")
        if not isinstance(raw_path, str) or not raw_path:
            continue

        path_obj = Path(raw_path)
        if path_obj.is_absolute():
            raise ValueError(f"input path must be relative to input_root: {raw_path}")

        # Generated flows normally use "inputs/<file>". The caller already
        # points input_root at the concrete input directory for one case.
        if path_obj.parts and path_obj.parts[0] == "inputs":
            relative = Path(*path_obj.parts[1:]) if len(path_obj.parts) > 1 else Path(".")
        else:
            relative = path_obj
        params["path"] = str(_resolve_under_root(input_root, relative, field="input"))


def _map_output_paths_to_output_root(flow_dict: dict[str, Any], output_root: Path) -> None:
    nodes = flow_dict.get("nodes")
    if not isinstance(nodes, dict):
        return

    for node in nodes.values():
        if not isinstance(node, dict) or node.get("kind") != "output":
            continue
        params = node.get("params")
        if not isinstance(params, dict):
            continue
        raw_path = params.get("path")
        if not isinstance(raw_path, str) or not raw_path:
            continue

        path_obj = Path(raw_path)
        if path_obj.is_absolute():
            raise ValueError(f"output path must be relative to output_root: {raw_path}")
        elif path_obj.parts and path_obj.parts[0] == "flow_cand":
            relative = Path(*path_obj.parts[1:]) if len(path_obj.parts) > 1 else Path(path_obj.name)
        else:
            relative = path_obj
        params["path"] = str(_resolve_under_root(output_root, relative, field="output"))


def exec_flow(
    flow_path: str | Path,
    input_root: str | Path,
    output_root: str | Path,
    *,
    dump_nodes: set[str] | None = None,
    trace: bool = False,
    on_fail_dump: bool = False,
    validate_only: bool = False,
    explain: bool = False,
    debug_sample: int = 3,
) -> dict[str, object]:
    """
    Load flow.json, validate as a py2flow DAG, and execute with pandas.
    Input paths are resolved under input_root; output paths are resolved under
    output_root. Other relative paths are resolved relative to the flow file.

    Note: flow.json only supports 11 kinds (input/project/filter/join/union/aggregate/dedup/sort/pivot/output/script)
    and CSV-only I/O.
    """
    flow_path = Path(flow_path).expanduser().resolve()
    input_root = Path(input_root).expanduser().resolve()
    output_root = Path(output_root).expanduser().resolve()
    if not flow_path.exists() or not flow_path.is_file():
        raise ValueError(f"Error: --flow-path is invalid or does not exist: {flow_path}")
    if not input_root.exists() or not input_root.is_dir():
        raise ValueError(f"Error: --input-root is invalid or does not exist: {input_root}")
    flow_dir = flow_path.parent

    with flow_path.open("r", encoding="utf-8") as f:
        try:
            flow_dict = json.load(f)
        except json.JSONDecodeError as exc:
            hint = (
                "Your flow.json may embed a large Script.inline_code and contain invalid JSON escaping. "
                "Please keep inline_code short and properly escaped, or refactor logic into standard operators (project/filter/aggregate/...) to reduce script size."
            )
            raise json.JSONDecodeError(f"{exc.msg}. {hint}", exc.doc, exc.pos) from exc
    _map_input_paths_to_input_root(flow_dict, input_root)
    _map_output_paths_to_output_root(flow_dict, output_root)
    dag = DAG.from_dict(flow_dict)
    if validate_only:
        return {}
    if trace:
        logging.basicConfig(level=logging.INFO)
    if explain:
        dag.validate()
        order = DAGExecutor._topological_order(dag.nodes)
        for nid in order:
            node = dag.nodes[nid]
            print(f"node={nid} kind={node.kind.value} inputs={node.inputs} params={sorted((node.params or {}).keys())}")
        return {}
    executor = DAGExecutor(
        dag,
        base_path=flow_dir,
        debug=DebugConfig(dump_nodes=dump_nodes, trace=trace, on_fail_dump=on_fail_dump, sample_rows=debug_sample),
    )
    return executor.run()
