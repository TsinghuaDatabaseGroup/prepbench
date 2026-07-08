from __future__ import annotations

from typing import Any, Mapping, Tuple


MAX_SCRIPT_NODES = 3
MAX_SCRIPT_INLINE_CODE_CHARS = 1500


def _error(
    message: str,
    *,
    node_id: str | None = None,
    step_kind: str | None = None,
    field: str | None = None,
    error_code: str = "node_validation",
) -> tuple[bool, str, dict]:
    details = {
        "error_code": error_code,
        "node_id": node_id,
        "step_kind": step_kind,
        "field": field,
    }
    return False, message, details


def _validate_project_rename(node_id: str, params: Mapping[str, Any]) -> tuple[bool, str, dict]:
    rename = params.get("rename")
    if rename is None:
        return True, "", {}
    if not isinstance(rename, Mapping):
        return _error(
            f"Node {node_id} params.rename must be a mapping of string->string",
            node_id=node_id,
            step_kind="StepKind.PROJECT",
            field="rename",
        )
    for src, dst in rename.items():
        if not isinstance(src, str) or not isinstance(dst, str):
            return _error(
                f"Node {node_id} params.rename must be a mapping of string->string",
                node_id=node_id,
                step_kind="StepKind.PROJECT",
                field="rename",
            )
    return True, "", {}


def validate_script_constraints(flow_dict: Mapping[str, Any]) -> Tuple[bool, str, dict]:
    """
    Validate additional script-level constraints before execution.

    Return format is compatible with existing flow_phase handling:
      (is_valid, error_message, error_details)
    """
    nodes = flow_dict.get("nodes")
    if not isinstance(nodes, Mapping):
        return _error("DAG.nodes must be a mapping of node_id -> node dict", field="nodes")

    script_count = 0
    for node_id, node_data in nodes.items():
        if not isinstance(node_id, str) or not node_id:
            return _error("node_id must be a non-empty string", field="nodes")
        if not isinstance(node_data, Mapping):
            return _error(
                f"Node definition for {node_id} must be an object",
                node_id=node_id,
                field="node",
            )
        kind = node_data.get("kind")
        params = node_data.get("params", {})
        if params is None:
            params = {}
        if not isinstance(params, Mapping):
            return _error(
                f"Node {node_id} params must be an object (mapping)",
                node_id=node_id,
                step_kind=str(kind) if kind is not None else None,
                field="params",
            )

        if kind == "project":
            ok, message, details = _validate_project_rename(node_id, params)
            if not ok:
                return ok, message, details
        elif kind == "script":
            script_count += 1
            if script_count > MAX_SCRIPT_NODES:
                return _error(
                    f"Workflow uses too many script nodes: {script_count} > {MAX_SCRIPT_NODES}",
                    node_id=node_id,
                    step_kind="script",
                    field="inline_code",
                    error_code="script_limit",
                )
            code = params.get("inline_code")
            if isinstance(code, str) and len(code) > MAX_SCRIPT_INLINE_CODE_CHARS:
                return _error(
                    f"Node {node_id} script.inline_code is too long: {len(code)} > {MAX_SCRIPT_INLINE_CODE_CHARS} chars",
                    node_id=node_id,
                    step_kind="script",
                    field="inline_code",
                    error_code="script_limit",
                )

    return True, "", {}
