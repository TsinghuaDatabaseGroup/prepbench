from __future__ import annotations

import argparse
import json
import logging
from pathlib import Path

from py2flow.errors import FlowError
from py2flow.executor import DAGExecutor
from py2flow.executor import DebugConfig
from py2flow.ir import DAG


def _map_input_paths_to_input_root(flow_dict: dict, input_root: Path) -> None:
    nodes = flow_dict.get("nodes")
    if not isinstance(nodes, dict):
        return

    for node in nodes.values():
        if not isinstance(node, dict):
            continue
        if node.get("kind") != "input":
            continue
        params = node.get("params")
        if not isinstance(params, dict):
            continue
        raw_path = params.get("path")
        if not isinstance(raw_path, str) or not raw_path:
            continue

        path_obj = Path(raw_path)
        if path_obj.is_absolute():
            continue

        # Common pattern in generated flows is "inputs/<file>".
        # input_root already points to the real inputs directory.
        if path_obj.parts and path_obj.parts[0] == "inputs":
            relative = Path(*path_obj.parts[1:]) if len(path_obj.parts) > 1 else Path(".")
        else:
            relative = path_obj

        params["path"] = str((input_root / relative).resolve())


def exec_flow(
    flow_path: str | Path,
    input_root: str | Path,
    *,
    dump_nodes: set[str] | None = None,
    trace: bool = False,
    on_fail_dump: bool = False,
    validate_only: bool = False,
    explain: bool = False,
    debug_sample: int = 3,
) -> dict[str, object]:
    """
    Load flow.json from flow_path, validate as a py2flow DAG, and execute with pandas.
    Input node paths are resolved from input_root.
    Other relative paths (such as outputs) are resolved relative to the flow directory.

    Note: flow.json only supports 11 kinds (input/project/filter/join/union/aggregate/dedup/sort/pivot/output/script)
    and CSV-only I/O.
    """
    flow_path = Path(flow_path)
    input_root = Path(input_root)
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

    _map_input_paths_to_input_root(flow_dict, input_root=input_root)
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


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Execute py2flow flow.json with explicit flow and input paths (11 kinds, CSV-only I/O)."
    )
    parser.add_argument(
        "--flow-path",
        required=True,
        help="Path to flow.json",
    )
    parser.add_argument(
        "--input-root",
        required=True,
        help="Directory path containing input CSV files",
    )
    parser.add_argument(
        "--dump-nodes",
        default="",
        help="Comma-separated node ids to dump to <flow_dir>/flow_cand/@debug/<node>.csv",
    )
    parser.add_argument(
        "--trace",
        action="store_true",
        help="Log per-node rows/columns and a small sample",
    )
    parser.add_argument(
        "--on-fail-dump",
        action="store_true",
        help="On failure, dump upstream inputs and params to <flow_dir>/flow_cand/@debug/@fail/<node>/",
    )
    parser.add_argument(
        "--validate-only",
        action="store_true",
        help="Only parse and validate flow.json; do not execute",
    )
    parser.add_argument(
        "--explain",
        action="store_true",
        help="Print node summary (kind/inputs/params keys) after validation; do not execute",
    )
    parser.add_argument(
        "--debug-sample",
        type=int,
        default=3,
        help="When --trace is set, number of rows to include in the sample (default: 3)",
    )

    args = parser.parse_args()
    dump_nodes = {x.strip() for x in str(args.dump_nodes).split(",") if x.strip()} or None
    try:
        exec_flow(
            Path(args.flow_path),
            Path(args.input_root),
            dump_nodes=dump_nodes,
            trace=bool(args.trace),
            on_fail_dump=bool(args.on_fail_dump),
            validate_only=bool(args.validate_only),
            explain=bool(args.explain),
            debug_sample=int(args.debug_sample),
        )
    except FlowError as exc:
        print(str(exc))
        help_text = getattr(exc, "help", None)
        if help_text:
            print(f"Help: {help_text}")
        raise SystemExit(1) from exc
