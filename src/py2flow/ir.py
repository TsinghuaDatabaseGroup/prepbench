from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from graphlib import CycleError, TopologicalSorter
from typing import Any, Dict, Iterable, List, Mapping, Optional, Set

from .errors import FlowValidationError


class StepKind(str, Enum):
    INPUT = "input"
    PROJECT = "project"
    FILTER = "filter"
    JOIN = "join"
    UNION = "union"
    AGGREGATE = "aggregate"
    DEDUP = "dedup"
    SORT = "sort"
    PIVOT = "pivot"
    OUTPUT = "output"
    SCRIPT = "script"


_ALLOWED_KINDS: Set[str] = {k.value for k in StepKind}


@dataclass
class Node:
    id: str
    kind: StepKind
    inputs: List[str] = field(default_factory=list)
    params: Dict[str, Any] = field(default_factory=dict)
    label: str | None = None
    description: str | None = None


@dataclass
class DAG:
    id: str
    name: str
    # v2 spec removed version; we keep it as metadata and ignore it when parsing.
    version: str = ""
    nodes: Dict[str, Node] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "DAG":
        dag_id = data.get("id")
        name = data.get("name")
        version = str(data.get("version") or "")

        if not isinstance(dag_id, str) or not dag_id:
            raise FlowValidationError(
                "DAG.id must be a non-empty string", error_code="node_validation")
        if not isinstance(name, str) or not name:
            raise FlowValidationError(
                "DAG.name must be a non-empty string", error_code="node_validation")

        nodes_raw = data.get("nodes")
        if not isinstance(nodes_raw, Mapping):
            raise FlowValidationError(
                "DAG.nodes must be a mapping of node_id -> node dict", error_code="node_validation")

        nodes: Dict[str, Node] = {}
        for node_id, node_data in nodes_raw.items():
            if not isinstance(node_id, str) or not node_id:
                raise FlowValidationError(
                    "node_id must be a non-empty string", error_code="node_validation")
            if not isinstance(node_data, Mapping):
                raise FlowValidationError(
                    f"Node definition for {node_id} must be an object",
                    node_id=node_id,
                    error_code="node_validation",
                )
            kind_value = node_data.get("kind")
            if not isinstance(kind_value, str) or not kind_value:
                raise FlowValidationError(
                    f"Node {node_id} missing string kind",
                    node_id=node_id,
                    error_code="node_validation",
                )
            if kind_value not in _ALLOWED_KINDS:
                raise FlowValidationError(
                    f"Node {node_id} has unsupported kind: {kind_value}",
                    node_id=node_id,
                    error_code="node_validation",
                    help=f"Use a lower-case kind from: {sorted(_ALLOWED_KINDS)}",
                )
            kind = StepKind(kind_value)

            raw_inputs = node_data.get("inputs", {})
            if raw_inputs is None:
                raw_inputs = {}
            if not isinstance(raw_inputs, Mapping):
                raise FlowValidationError(
                    f"Node {node_id} inputs must be an object (mapping)",
                    node_id=node_id,
                    step_kind=kind,
                    error_code="node_validation",
                    help="Use inputs as an object. Unary nodes: {\"in\":\"<node>\"}. Join: {\"left\":\"<node>\",\"right\":\"<node>\"}. Union: {\"items\":[\"a\",\"b\"]}.",
                )
            inputs = _parse_inputs(node_id, kind, raw_inputs)

            raw_params = node_data.get("params", {})
            if raw_params is None:
                raw_params = {}
            if not isinstance(raw_params, Mapping):
                raise FlowValidationError(
                    f"Node {node_id} params must be an object (mapping)",
                    node_id=node_id,
                    step_kind=kind,
                    error_code="node_validation",
                )
            params = dict(raw_params)
            nodes[node_id] = Node(
                id=node_id,
                kind=kind,
                inputs=inputs,
                params=params,
                label=node_data.get("label"),
                description=node_data.get("description"),
            )

        dag = cls(id=dag_id, name=name, version=version, nodes=nodes)
        dag.validate()
        return dag

    def validate(self) -> None:
        _validate_references(self.nodes)
        for node in self.nodes.values():
            _validate_node(node)
        _validate_acyclic(self.nodes)
        _validate_reachable_from_outputs(self.nodes)


def _validate_references(nodes: Mapping[str, Node]) -> None:
    node_ids = set(nodes.keys())
    for node in nodes.values():
        missing = [nid for nid in node.inputs if nid not in node_ids]
        if missing:
            raise FlowValidationError(
                f"Node {node.id} has inputs that do not exist: {missing}",
                node_id=node.id,
                step_kind=node.kind,
                error_code="node_validation",
            )


def _validate_acyclic(nodes: Mapping[str, Node]) -> None:
    graph: Dict[str, Iterable[str]] = {
        nid: node.inputs for nid, node in nodes.items()}
    sorter = TopologicalSorter(graph)
    try:
        list(sorter.static_order())
    except CycleError as exc:
        raise FlowValidationError(
            f"DAG has a cycle: {exc}", error_code="cycle") from exc


def _validate_reachable_from_outputs(nodes: Mapping[str, Node]) -> None:
    output_nodes = [nid for nid,
                    n in nodes.items() if n.kind is StepKind.OUTPUT]
    if not output_nodes:
        return
    reachable: Set[str] = set()
    stack: List[str] = list(output_nodes)
    while stack:
        nid = stack.pop()
        if nid in reachable:
            continue
        reachable.add(nid)
        stack.extend(nodes[nid].inputs)
    unreachable = [nid for nid in nodes.keys() if nid not in reachable]
    if unreachable:
        raise FlowValidationError(
            f"Unreachable node(s) not contributing to any Output: {sorted(unreachable)}",
            error_code="unreachable_nodes",
        )


def raise_validation(
    node_id: str,
    kind: StepKind,
    error_code: str,
    message: str,
    field: str | None = None,
    help: str | None = None,
) -> None:
    raise FlowValidationError(message, node_id=node_id, step_kind=kind,
                              error_code=error_code, field=field, help=help)

def _parse_inputs(node_id: str, kind: StepKind, inputs: Mapping[str, Any]) -> List[str]:
    def unknown_keys(allowed: Set[str]) -> List[str]:
        return [k for k in inputs.keys() if k not in allowed]

    if kind is StepKind.INPUT:
        if inputs:
            raise_validation(
                node_id,
                kind,
                "invalid_inputs_shape",
                "input must not have inputs",
                field="inputs",
                help="Remove inputs for input nodes (inputs must be {}).",
            )
        return []

    if kind is StepKind.JOIN:
        bad = unknown_keys({"left", "right"})
        if bad:
            raise_validation(
                node_id,
                kind,
                "invalid_inputs_shape",
                f"join.inputs has unknown key(s): {bad}",
                field="inputs",
                help="Use join.inputs = {\"left\": \"<node>\", \"right\": \"<node>\"}.",
            )
        left = inputs.get("left")
        right = inputs.get("right")
        if not isinstance(left, str) or not isinstance(right, str) or not left or not right:
            raise_validation(
                node_id,
                kind,
                "invalid_inputs_shape",
                "join.inputs must have non-empty string left/right",
                field="inputs",
                help="Use join.inputs = {\"left\": \"<node>\", \"right\": \"<node>\"}.",
            )
        return [left, right]

    if kind is StepKind.UNION:
        bad = unknown_keys({"items"})
        if bad:
            raise_validation(
                node_id,
                kind,
                "invalid_inputs_shape",
                f"union.inputs has unknown key(s): {bad}",
                field="inputs",
                help="Use union.inputs = {\"items\": [\"<node_a>\", \"<node_b>\", ...]}.",
            )
        items = inputs.get("items")
        if not isinstance(items, list) or len(items) < 2 or not all(isinstance(x, str) and x for x in items):
            raise_validation(
                node_id,
                kind,
                "invalid_inputs_shape",
                "union.inputs.items must be a list[str] of length >= 2",
                field="inputs",
                help="Use union.inputs = {\"items\": [\"<node_a>\", \"<node_b>\"]} (length >= 2).",
            )
        return list(items)

    bad = unknown_keys({"in"})
    if bad:
        raise_validation(
            node_id,
            kind,
            "invalid_inputs_shape",
            f"unary inputs has unknown key(s): {bad} (expected only 'in')",
            field="inputs",
            help="Use unary inputs = {\"in\": \"<upstream_node>\"}.",
        )
    upstream = inputs.get("in")
    if not isinstance(upstream, str) or not upstream:
        raise_validation(
            node_id,
            kind,
            "invalid_inputs_shape",
            "unary inputs must have non-empty string 'in'",
            field="inputs",
            help="Use unary inputs = {\"in\": \"<upstream_node>\"}.",
        )
    return [upstream]


def _validate_node(node: Node) -> None:
    validators = {
        StepKind.INPUT: _validate_input,
        StepKind.PROJECT: _validate_project,
        StepKind.FILTER: _validate_filter,
        StepKind.JOIN: _validate_join,
        StepKind.UNION: _validate_union,
        StepKind.AGGREGATE: _validate_aggregate,
        StepKind.DEDUP: _validate_dedup,
        StepKind.SORT: _validate_sort,
        StepKind.PIVOT: _validate_pivot,
        StepKind.OUTPUT: _validate_output,
        StepKind.SCRIPT: _validate_script,
    }
    validator = validators.get(node.kind)
    if validator is None:
        raise FlowValidationError(
            f"Unsupported kind: {node.kind.value}",
            node_id=node.id,
            step_kind=node.kind,
            error_code="node_validation",
        )
    validator(node)


def _reject_unknown_params(node: Node, allowed: Set[str]) -> None:
    # Allow metadata fields starting with _ (for rendering hints, descriptions, etc.)
    # These fields are ignored during execution but can be used by renderers
    unknown = [k for k in node.params.keys() if k not in allowed and not k.startswith("_")]
    if unknown:
        raise_validation(
            node.id,
            node.kind,
            "node_validation",
            f"unknown params key(s): {sorted(unknown)}",
        )


def _require_str(node: Node, key: str) -> str:
    val = node.params.get(key)
    if not isinstance(val, str) or not val:
        raise_validation(
            node.id,
            node.kind,
            "node_validation",
            f"missing non-empty string params.{key}",
        )
    return val


def _require_bool(node: Node, key: str) -> bool:
    val = node.params.get(key)
    if not isinstance(val, bool):
        raise_validation(node.id, node.kind, "node_validation",
                         f"params.{key} must be boolean")
    return val


def _optional_bool(node: Node, key: str, default: bool) -> bool:
    val = node.params.get(key, default)
    if not isinstance(val, bool):
        raise_validation(node.id, node.kind, "node_validation",
                         f"params.{key} must be boolean")
    return val


def _optional_str_list(node: Node, key: str) -> Optional[List[str]]:
    if key not in node.params:
        return None
    val = node.params.get(key)
    if val is None:
        return None
    if not isinstance(val, list) or not all(isinstance(x, str) and x for x in val):
        raise_validation(node.id, node.kind, "node_validation",
                         f"params.{key} must be a list of strings")
    return list(val)


def _validate_input(node: Node) -> None:
    _reject_unknown_params(
        node,
        {
            "path",
            "mode",
            "delimiter",
            "encoding",
            "na_values",
            "keep_default_na",
            "parse_dates",
            "dtype",
            "skiprows",
            "header",
            "on_bad_lines",
            "quotechar",
            "escapechar",
            "data",
            "source_type",
        },
    )
    data = node.params.get("data")
    source_type = node.params.get("source_type")
    if data is not None or source_type == "inline":
        if source_type not in (None, "inline"):
            raise FlowValidationError(
                f"Node {node.id} params.source_type must be inline when provided",
                node_id=node.id,
                step_kind=node.kind,
                error_code="node_validation",
            )
        if data is None:
            raise FlowValidationError(
                f"Node {node.id} params.data is required for inline inputs",
                node_id=node.id,
                step_kind=node.kind,
                error_code="node_validation",
            )
        if not isinstance(data, (list, Mapping)):
            raise FlowValidationError(
                f"Node {node.id} params.data must be list[dict] or dict[str,list]",
                node_id=node.id,
                step_kind=node.kind,
                error_code="node_validation",
            )
        return

    _require_str(node, "path")
    if "mode" in node.params and node.params["mode"] is not None:
        mode = node.params["mode"]
        if not isinstance(mode, str) or mode not in {"csv", "line"}:
            raise FlowValidationError(
                f"Node {node.id} params.mode must be csv|line when provided",
                node_id=node.id,
                step_kind=node.kind,
                error_code="node_validation",
            )
    if "delimiter" in node.params and not isinstance(node.params["delimiter"], str):
        raise FlowValidationError(
            f"Node {node.id} params.delimiter must be a string",
            node_id=node.id,
            step_kind=node.kind,
            error_code="node_validation",
        )
    if "encoding" in node.params:
        enc = node.params["encoding"]
        if not (
            isinstance(enc, str)
            or (isinstance(enc, list) and enc and all(isinstance(x, str) and x for x in enc))
        ):
            raise FlowValidationError(
                f"Node {node.id} params.encoding must be string or non-empty list[string]",
                node_id=node.id,
                step_kind=node.kind,
                error_code="node_validation",
            )
    if "na_values" in node.params:
        na = node.params["na_values"]
        if not isinstance(na, list) or not all(isinstance(x, str) for x in na):
            raise FlowValidationError(
                f"Node {node.id} params.na_values must be a list of strings",
                node_id=node.id,
                step_kind=node.kind,
                error_code="node_validation",
            )
    if "keep_default_na" in node.params:
        _require_bool(node, "keep_default_na")
    if "parse_dates" in node.params:
        pdv = node.params["parse_dates"]
        if not isinstance(pdv, list) or not all(isinstance(x, str) and x for x in pdv):
            raise FlowValidationError(
                f"Node {node.id} params.parse_dates must be a list of strings",
                node_id=node.id,
                step_kind=node.kind,
                error_code="node_validation",
            )
    if "dtype" in node.params:
        dt = node.params["dtype"]
        if not isinstance(dt, Mapping) or not all(isinstance(k, str) and isinstance(v, str) for k, v in dt.items()):
            raise FlowValidationError(
                f"Node {node.id} params.dtype must be a mapping of string->string",
                node_id=node.id,
                step_kind=node.kind,
                error_code="node_validation",
            )
    if "skiprows" in node.params and node.params["skiprows"] is not None:
        sr = node.params["skiprows"]
        if not isinstance(sr, int) or sr < 0:
            raise FlowValidationError(
                f"Node {node.id} params.skiprows must be a non-negative integer when provided",
                node_id=node.id,
                step_kind=node.kind,
                error_code="node_validation",
            )
    if "header" in node.params and node.params["header"] is not None:
        hd = node.params["header"]
        if not (hd is None or isinstance(hd, int) or (isinstance(hd, list) and all(isinstance(x, int) for x in hd))):
            raise FlowValidationError(
                f"Node {node.id} params.header must be int|list[int]|null when provided",
                node_id=node.id,
                step_kind=node.kind,
                error_code="node_validation",
            )
    if "on_bad_lines" in node.params and node.params["on_bad_lines"] is not None:
        obl = node.params["on_bad_lines"]
        if obl not in {"error", "warn", "skip"}:
            raise FlowValidationError(
                f"Node {node.id} params.on_bad_lines must be error|warn|skip when provided",
                node_id=node.id,
                step_kind=node.kind,
                error_code="node_validation",
            )
    for key in ("quotechar", "escapechar"):
        if key in node.params and node.params[key] is not None:
            v = node.params[key]
            if not isinstance(v, str) or len(v) != 1:
                raise FlowValidationError(
                    f"Node {node.id} params.{key} must be a single-character string when provided",
                    node_id=node.id,
                    step_kind=node.kind,
                    error_code="node_validation",
                )


def _validate_project(node: Node) -> None:
    forbidden = sorted(set(node.params.keys()) & {
                       "sort_by", "ascending", "na_position", "order_by", "stable", "limit"})
    if forbidden:
        raise_validation(
            node.id,
            node.kind,
            "project_forbid_sort_fields",
            f"project forbids sort-related params: {forbidden} (use sort operator)",
            field="params",
            help="Use a separate sort node. Example: {\"kind\":\"sort\",\"params\":{\"order_by\":[{\"expr\":\"df['col']\",\"asc\":true,\"nulls\":\"last\"}]}}",
        )
    _reject_unknown_params(
        node,
        {
            "select",
            "rename",
            "compute",
            "cast",
            "map",
            "expand",
            "on_error",
            "error_cols",
            "promote_row_to_header",
        },
    )
    on_error = node.params.get("on_error", "error")
    if on_error not in {"keep", "null", "error", "tag"}:
        raise FlowValidationError(
            f"Node {node.id} params.on_error must be one of keep|null|error|tag",
            node_id=node.id,
            step_kind=node.kind,
            error_code="node_validation",
        )
    if on_error == "tag":
        error_cols = _optional_str_list(node, "error_cols")
        if not error_cols:
            raise FlowValidationError(
                f"Node {node.id} project.on_error=tag requires params.error_cols",
                node_id=node.id,
                step_kind=node.kind,
                error_code="node_validation",
            )
    if "select" in node.params:
        sel = node.params["select"]
        if not isinstance(sel, list) or not all(isinstance(x, str) and x for x in sel):
            raise FlowValidationError(
                f"Node {node.id} params.select must be a list of strings",
                node_id=node.id,
                step_kind=node.kind,
                error_code="node_validation",
            )
    if "rename" in node.params:
        ren = node.params["rename"]
        if not isinstance(ren, Mapping) or not all(isinstance(k, str) and isinstance(v, str) for k, v in ren.items()):
            raise FlowValidationError(
                f"Node {node.id} params.rename must be a mapping of string->string",
                node_id=node.id,
                step_kind=node.kind,
                error_code="node_validation",
            )
    if "compute" in node.params:
        compute = node.params["compute"]
        if not isinstance(compute, list):
            raise FlowValidationError(
                f"Node {node.id} params.compute must be a list",
                node_id=node.id,
                step_kind=node.kind,
                error_code="node_validation",
            )
        for item in compute:
            if not isinstance(item, Mapping):
                raise FlowValidationError(
                    f"Node {node.id} compute item must be an object",
                    node_id=node.id,
                    step_kind=node.kind,
                    error_code="node_validation",
                )
            unknown = [k for k in item.keys() if k not in {"as", "expr"} and not k.startswith("_")]
            if unknown:
                raise FlowValidationError(
                    f"Node {node.id} compute item has unknown key(s): {sorted(unknown)}",
                    node_id=node.id,
                    step_kind=node.kind,
                    error_code="node_validation",
                )
            if not isinstance(item.get("as"), str) or not item.get("as"):
                raise FlowValidationError(
                    f"Node {node.id} compute item missing string 'as'",
                    node_id=node.id,
                    step_kind=node.kind,
                    error_code="node_validation",
                )
            if not isinstance(item.get("expr"), str) or not item.get("expr"):
                raise FlowValidationError(
                    f"Node {node.id} compute item missing string 'expr'",
                    node_id=node.id,
                    step_kind=node.kind,
                    error_code="node_validation",
                )
    if "cast" in node.params:
        cast = node.params["cast"]
        if not isinstance(cast, list):
            raise FlowValidationError(
                f"Node {node.id} params.cast must be a list",
                node_id=node.id,
                step_kind=node.kind,
                error_code="node_validation",
            )
        allowed_dtype = {"string", "int64",
                         "float64", "bool", "datetime64[ns]"}
        for item in cast:
            if not isinstance(item, Mapping):
                raise FlowValidationError(
                    f"Node {node.id} cast item must be an object",
                    node_id=node.id,
                    step_kind=node.kind,
                    error_code="node_validation",
                )
            unknown = [k for k in item.keys() if k not in {
                "col", "dtype", "errors"}]
            if unknown:
                raise FlowValidationError(
                    f"Node {node.id} cast item has unknown key(s): {sorted(unknown)}",
                    node_id=node.id,
                    step_kind=node.kind,
                    error_code="node_validation",
                )
            if not isinstance(item.get("col"), str) or not item.get("col"):
                raise FlowValidationError(
                    f"Node {node.id} cast item missing string 'col'",
                    node_id=node.id,
                    step_kind=node.kind,
                    error_code="node_validation",
                )
            dt = item.get("dtype")
            if not isinstance(dt, str) or dt not in allowed_dtype:
                raise FlowValidationError(
                    f"Node {node.id} cast item dtype must be one of {sorted(allowed_dtype)}",
                    node_id=node.id,
                    step_kind=node.kind,
                    error_code="node_validation",
                )
            err = item.get("errors", "raise")
            if err not in {"raise", "null"}:
                raise FlowValidationError(
                    f"Node {node.id} cast item errors must be raise|null",
                    node_id=node.id,
                    step_kind=node.kind,
                    error_code="node_validation",
                )
    if "map" in node.params:
        ops = node.params["map"]
        if not isinstance(ops, list):
            raise FlowValidationError(
                f"Node {node.id} params.map must be a list",
                node_id=node.id,
                step_kind=node.kind,
                error_code="node_validation",
            )
        allowed = {
            "trim",
            "lower",
            "upper",
            "regex_replace",
            "regex_extract",
            "html_strip",
            "squeeze_whitespace",
            "split",
            "tokenize",
            "explode",
            "fillna",
            "map_values",
            "complete_calendar",
            "parse_date_multi",
            "date_range",
            "date_range_to_start",
            "date_year_only",
            "group_cumcount",
            "format_number",
        }
        for op in ops:
            if not isinstance(op, Mapping):
                raise FlowValidationError(
                    f"Node {node.id} map item must be an object",
                    node_id=node.id,
                    step_kind=node.kind,
                    error_code="node_validation",
                )
            unknown = [k for k in op.keys() if k not in {"col", "op", "args", "when"}]
            if unknown:
                raise FlowValidationError(
                    f"Node {node.id} map item has unknown key(s): {sorted(unknown)}",
                    node_id=node.id,
                    step_kind=node.kind,
                    error_code="node_validation",
                )
            if not isinstance(op.get("col"), str) or not op.get("col"):
                raise FlowValidationError(
                    f"Node {node.id} map item missing string 'col'",
                    node_id=node.id,
                    step_kind=node.kind,
                    error_code="node_validation",
                )
            op_name = op.get("op")
            if not isinstance(op_name, str) or op_name not in allowed:
                raise FlowValidationError(
                    f"Node {node.id} map item op must be one of {sorted(allowed)}",
                    node_id=node.id,
                    step_kind=node.kind,
                    error_code="node_validation",
                )
            args = op.get("args")
            if args is not None:
                if not isinstance(args, Mapping):
                    raise FlowValidationError(
                        f"Node {node.id} map item args must be an object when provided",
                        node_id=node.id,
                        step_kind=node.kind,
                        error_code="node_validation",
                    )
            top_when = op.get("when")
            args_when = args.get("when") if isinstance(args, Mapping) else None
            for label, when_expr in (("map.when", top_when), ("map args.when", args_when)):
                if when_expr is not None and (not isinstance(when_expr, str) or not when_expr):
                    raise FlowValidationError(
                        f"Node {node.id} {label} must be a non-empty string when provided",
                        node_id=node.id,
                        step_kind=node.kind,
                        error_code="node_validation",
                    )
            if top_when is not None and args_when is not None and top_when != args_when:
                raise FlowValidationError(
                    f"Node {node.id} map.when conflicts with map args.when",
                    node_id=node.id,
                    step_kind=node.kind,
                    error_code="node_validation",
                )
    if "expand" in node.params:
        expand = node.params.get("expand")
        if not isinstance(expand, Mapping):
            raise FlowValidationError(
                f"Node {node.id} params.expand must be an object",
                node_id=node.id,
                step_kind=node.kind,
                error_code="node_validation",
            )
        unknown = [k for k in expand.keys() if k not in {
            "keys", "from_col", "to_col", "to_value", "to_value_expr", "expand_col", "keep_from_col"}]
        if unknown:
            raise FlowValidationError(
                f"Node {node.id} expand has unknown key(s): {sorted(unknown)}",
                node_id=node.id,
                step_kind=node.kind,
                error_code="node_validation",
            )
        keys = expand.get("keys")
        if not isinstance(keys, list) or not keys or not all(isinstance(x, str) and x for x in keys):
            raise FlowValidationError(
                f"Node {node.id} expand.keys must be a non-empty list of strings",
                node_id=node.id,
                step_kind=node.kind,
                error_code="node_validation",
            )
        from_col = expand.get("from_col")
        if not isinstance(from_col, str) or not from_col:
            raise FlowValidationError(
                f"Node {node.id} expand.from_col must be a non-empty string",
                node_id=node.id,
                step_kind=node.kind,
                error_code="node_validation",
            )
        to_col = expand.get("to_col")
        to_value = expand.get("to_value")
        to_value_expr = expand.get("to_value_expr")
        specified = sum(
            [to_col is not None, to_value is not None, to_value_expr is not None])
        if specified != 1:
            raise FlowValidationError(
                f"Node {node.id} expand must specify exactly one of to_col, to_value, or to_value_expr",
                node_id=node.id,
                step_kind=node.kind,
                error_code="node_validation",
            )
        if to_col is not None and (not isinstance(to_col, str) or not to_col):
            raise FlowValidationError(
                f"Node {node.id} expand.to_col must be a non-empty string when provided",
                node_id=node.id,
                step_kind=node.kind,
                error_code="node_validation",
            )
        expand_col = expand.get("expand_col")
        if not isinstance(expand_col, str) or not expand_col:
            raise FlowValidationError(
                f"Node {node.id} expand.expand_col must be a non-empty string",
                node_id=node.id,
                step_kind=node.kind,
                error_code="node_validation",
            )
        if to_value_expr is not None:
            if not isinstance(to_value_expr, str) or not to_value_expr:
                raise FlowValidationError(
                    f"Node {node.id} expand.to_value_expr must be a non-empty string when provided",
                    node_id=node.id,
                    step_kind=node.kind,
                    error_code="node_validation",
                )
        if "keep_from_col" in expand:
            keep_from_col = expand.get("keep_from_col")
            if not isinstance(keep_from_col, bool):
                raise FlowValidationError(
                    f"Node {node.id} expand.keep_from_col must be boolean",
                    node_id=node.id,
                    step_kind=node.kind,
                    error_code="node_validation",
                )
def _validate_filter(node: Node) -> None:
    _reject_unknown_params(node, {"predicate", "null_as_false"})
    predicate = _require_str(node, "predicate")
    _optional_bool(node, "null_as_false", True)


def _normalize_join_keys(value: Any) -> Optional[List[str]]:
    if value is None:
        return None
    if isinstance(value, str):
        return [value]
    if isinstance(value, list) and all(isinstance(x, str) and x for x in value):
        return list(value)
    return None


def _validate_join(node: Node) -> None:
    # Allow fuzzy_match parameter
    fuzzy_match = node.params.get("fuzzy_match")
    if fuzzy_match is not None and not isinstance(fuzzy_match, bool):
        raise FlowValidationError(
            f"Node {node.id} join.params.fuzzy_match must be boolean",
            node_id=node.id,
            step_kind=StepKind.JOIN,
            error_code="node_validation",
        )
    _reject_unknown_params(
        node,
        {
            "how",
            "on",
            "left_on",
            "right_on",
            "null_equal",
            "suffixes",
            "select_left",
            "select_right",
            "validate",
            "fuzzy_match",
        },
    )
    how = node.params.get("how", "inner")
    if how not in {"inner", "left", "right", "full", "semi", "anti"}:
        raise FlowValidationError(
            f"Node {node.id} join.how must be one of inner|left|right|full|semi|anti",
            node_id=node.id,
            step_kind=node.kind,
            error_code="node_validation",
        )

    on = _normalize_join_keys(node.params.get("on"))
    left_on = _normalize_join_keys(node.params.get("left_on"))
    right_on = _normalize_join_keys(node.params.get("right_on"))
    if on is not None and (left_on is not None or right_on is not None):
        raise FlowValidationError(
            f"Node {node.id} join cannot specify both on and left_on/right_on",
            node_id=node.id,
            step_kind=node.kind,
            error_code="node_validation",
        )
    if on is None:
        if left_on is None or right_on is None or len(left_on) != len(right_on):
            raise FlowValidationError(
                f"Node {node.id} join requires on or left_on/right_on with same length",
                node_id=node.id,
                step_kind=node.kind,
                error_code="node_validation",
            )
    if fuzzy_match:
        left_keys = on if on is not None else left_on
        right_keys = on if on is not None else right_on
        if how not in {"left", "inner"}:
            raise FlowValidationError(
                f"Node {node.id} join.fuzzy_match only supports how=left|inner",
                node_id=node.id,
                step_kind=node.kind,
                error_code="node_validation",
            )
        if left_keys is None or right_keys is None or len(left_keys) != 1 or len(right_keys) != 1:
            raise FlowValidationError(
                f"Node {node.id} join.fuzzy_match requires one left key and one right key",
                node_id=node.id,
                step_kind=node.kind,
                error_code="node_validation",
            )

    if "null_equal" in node.params:
        _require_bool(node, "null_equal")
    if "suffixes" in node.params:
        suf = node.params["suffixes"]
        if not isinstance(suf, list) or len(suf) != 2 or not all(isinstance(x, str) for x in suf):
            raise FlowValidationError(
                f"Node {node.id} join.suffixes must be [str,str]",
                node_id=node.id,
                step_kind=node.kind,
                error_code="node_validation",
            )
    if "select_left" in node.params:
        _optional_str_list(node, "select_left")
    if "select_right" in node.params:
        _optional_str_list(node, "select_right")
    if "validate" in node.params:
        val = node.params["validate"]
        if not isinstance(val, Mapping):
            raise FlowValidationError(
                f"Node {node.id} join.validate must be an object",
                node_id=node.id,
                step_kind=node.kind,
                error_code="node_validation",
            )
        unknown = [k for k in val.keys() if k not in {
            "mode", "on_fail", "error_col"}]
        if unknown:
            raise FlowValidationError(
                f"Node {node.id} join.validate has unknown key(s): {sorted(unknown)}",
                node_id=node.id,
                step_kind=node.kind,
                error_code="node_validation",
            )
        mode = val.get("mode")
        if mode not in {"1:1", "1:m", "m:1", "m:m"}:
            raise FlowValidationError(
                f"Node {node.id} join.validate.mode must be one of 1:1|1:m|m:1|m:m",
                node_id=node.id,
                step_kind=node.kind,
                error_code="node_validation",
            )
        on_fail = val.get("on_fail", "error")
        if on_fail not in {"error", "tag"}:
            raise FlowValidationError(
                f"Node {node.id} join.validate.on_fail must be error|tag",
                node_id=node.id,
                step_kind=node.kind,
                error_code="node_validation",
            )
        if "error_col" in val:
            err_col = val.get("error_col")
            if not isinstance(err_col, str) or not err_col:
                raise FlowValidationError(
                    f"Node {node.id} join.validate.error_col must be a non-empty string when provided",
                    node_id=node.id,
                    step_kind=node.kind,
                    error_code="node_validation",
                )


def _validate_union(node: Node) -> None:
    if "join" in node.params:
        raise_validation(
            node.id,
            node.kind,
            "union_join_forbidden",
            "union.params.join is forbidden; use align/fill_missing/distinct only",
            field="join",
            help="Remove params.join. Use params.align/fill_missing/type_coerce and always set params.distinct (true/false).",
        )
    _reject_unknown_params(
        node, {"distinct", "align", "fill_missing", "type_coerce"})
    if "distinct" not in node.params:
        raise FlowValidationError(
            f"Node {node.id} union requires params.distinct",
            node_id=node.id,
            step_kind=node.kind,
            error_code="union_distinct_required",
            field="distinct",
            help="Add params.distinct: false (or true) to union nodes.",
        )
    _require_bool(node, "distinct")
    align = node.params.get("align", "by_name")
    if align != "by_name":
        raise FlowValidationError(
            f"Node {node.id} union.align only supports by_name in this implementation",
            node_id=node.id,
            step_kind=node.kind,
            error_code="node_validation",
        )
    fill_missing = node.params.get("fill_missing", "null")
    if fill_missing not in {"null", "error"}:
        raise FlowValidationError(
            f"Node {node.id} union.fill_missing must be null|error",
            node_id=node.id,
            step_kind=node.kind,
            error_code="node_validation",
        )
    type_coerce = node.params.get("type_coerce", "error")
    if type_coerce != "error":
        raise FlowValidationError(
            f"Node {node.id} union.type_coerce only supports error in this implementation",
            node_id=node.id,
            step_kind=node.kind,
            error_code="node_validation",
        )


def _validate_aggregate(node: Node) -> None:
    _reject_unknown_params(
        node, {"group_keys", "aggs", "having", "null_group"})
    group_keys = node.params.get("group_keys", [])
    if not isinstance(group_keys, list) or not all(isinstance(x, str) and x for x in group_keys):
        raise FlowValidationError(
            f"Node {node.id} aggregate.group_keys must be a list of strings",
            node_id=node.id,
            step_kind=node.kind,
            error_code="node_validation",
        )
    aggs = node.params.get("aggs")
    if not isinstance(aggs, list) or not aggs:
        raise FlowValidationError(
            f"Node {node.id} aggregate.aggs must be a non-empty list",
            node_id=node.id,
            step_kind=node.kind,
            error_code="node_validation",
        )
    allowed = {"sum", "count", "min", "max", "avg", "count_distinct", "prod"}
    for agg in aggs:
        if not isinstance(agg, Mapping):
            raise FlowValidationError(
                f"Node {node.id} aggregate.aggs item must be an object",
                node_id=node.id,
                step_kind=node.kind,
                error_code="node_validation",
            )
        unknown = [k for k in agg.keys() if k not in {
            "as", "func", "expr", "distinct"}]
        if unknown:
            raise FlowValidationError(
                f"Node {node.id} aggregate aggs item has unknown key(s): {sorted(unknown)}",
                node_id=node.id,
                step_kind=node.kind,
                error_code="node_validation",
            )
        if not isinstance(agg.get("as"), str) or not agg.get("as"):
            raise FlowValidationError(
                f"Node {node.id} aggregate.aggs item requires string 'as'",
                node_id=node.id,
                step_kind=node.kind,
                error_code="node_validation",
            )
        func = agg.get("func")
        if func not in allowed:
            raise FlowValidationError(
                f"Node {node.id} aggregate.aggs item func must be one of {sorted(allowed)}",
                node_id=node.id,
                step_kind=node.kind,
                error_code="node_validation",
            )
        expr = agg.get("expr")
        if expr is not None and (not isinstance(expr, str) or not expr):
            raise FlowValidationError(
                f"Node {node.id} aggregate.aggs item expr must be a non-empty string when provided",
                node_id=node.id,
                step_kind=node.kind,
                error_code="node_validation",
            )
    if "having" in node.params and node.params["having"] is not None:
        _require_str(node, "having")
    _optional_bool(node, "null_group", True)


def _validate_dedup(node: Node) -> None:
    _reject_unknown_params(
        node, {"keys", "output", "keep", "order_by", "on_missing_tiebreaker"})
    keys = node.params.get("keys", None)
    if "on_missing_tiebreaker" in node.params:
        omt = node.params.get("on_missing_tiebreaker")
        if omt != "error":
            raise FlowValidationError(
                f"Node {node.id} dedup.on_missing_tiebreaker only supports 'error' in this implementation",
                node_id=node.id,
                step_kind=node.kind,
                error_code="node_validation",
            )
    if keys is not None:
        if not isinstance(keys, list) or not all(isinstance(x, str) and x for x in keys):
            raise FlowValidationError(
                f"Node {node.id} dedup.keys must be null or a list of strings",
                node_id=node.id,
                step_kind=node.kind,
                error_code="node_validation",
            )
    output = node.params.get("output", "all_cols")
    if output not in {"all_cols", "keys_only"}:
        raise FlowValidationError(
            f"Node {node.id} dedup.output must be all_cols|keys_only",
            node_id=node.id,
            step_kind=node.kind,
            error_code="node_validation",
        )
    keep = node.params.get("keep", "first")
    if keep not in {"first", "last", "none"}:
        raise FlowValidationError(
            f"Node {node.id} dedup.keep must be first|last|none",
            node_id=node.id,
            step_kind=node.kind,
            error_code="node_validation",
        )

    order_by = node.params.get("order_by")
    if order_by is not None:
        if not isinstance(order_by, list) or not order_by:
            raise FlowValidationError(
                f"Node {node.id} dedup.order_by must be a non-empty list when provided",
                node_id=node.id,
                step_kind=node.kind,
                error_code="node_validation",
            )
        for item in order_by:
            if not isinstance(item, Mapping) or not isinstance(item.get("expr"), str) or not item.get("expr"):
                raise FlowValidationError(
                    f"Node {node.id} dedup.order_by item requires string expr",
                    node_id=node.id,
                    step_kind=node.kind,
                    error_code="node_validation",
                )
            unknown = [k for k in item.keys() if k not in {
                "expr", "asc", "nulls"}]
            if unknown:
                raise FlowValidationError(
                    f"Node {node.id} dedup.order_by item has unknown key(s): {sorted(unknown)}",
                    node_id=node.id,
                    step_kind=node.kind,
                    error_code="node_validation",
                )

    if keys is not None and output == "all_cols" and keep in {"first", "last"}:
        if not isinstance(order_by, list) or not order_by:
            raise FlowValidationError(
                f"Node {node.id} dedup missing deterministic tiebreaker order_by",
                node_id=node.id,
                step_kind=node.kind,
                error_code="dedup_missing_tiebreaker",
            )


def _validate_sort(node: Node) -> None:
    _reject_unknown_params(
        node, {"order_by", "stable", "limit", "partition_by", "limit_per_group"})
    order_by = node.params.get("order_by")
    if not isinstance(order_by, list) or not order_by:
        raise FlowValidationError(
            f"Node {node.id} sort requires non-empty params.order_by",
            node_id=node.id,
            step_kind=node.kind,
            error_code="node_validation",
        )
    for item in order_by:
        if not isinstance(item, Mapping):
            raise FlowValidationError(
                f"Node {node.id} sort.order_by item must be an object",
                node_id=node.id,
                step_kind=node.kind,
                error_code="node_validation",
            )
        expr = item.get("expr")
        if not isinstance(expr, str) or not expr:
            raise FlowValidationError(
                f"Node {node.id} sort.order_by item requires string expr",
                node_id=node.id,
                step_kind=node.kind,
                error_code="node_validation",
            )
        asc = item.get("asc", True)
        if not isinstance(asc, bool):
            raise FlowValidationError(
                f"Node {node.id} sort.order_by item asc must be boolean",
                node_id=node.id,
                step_kind=node.kind,
                error_code="node_validation",
            )
        nulls = item.get("nulls", "last")
        if nulls not in {"first", "last"}:
            raise FlowValidationError(
                f"Node {node.id} sort.order_by item nulls must be first|last",
                node_id=node.id,
                step_kind=node.kind,
                error_code="node_validation",
            )
        unknown = [k for k in item.keys() if k not in {"expr", "asc", "nulls"}]
        if unknown:
            raise FlowValidationError(
                f"Node {node.id} sort.order_by item has unknown key(s): {sorted(unknown)}",
                node_id=node.id,
                step_kind=node.kind,
                error_code="node_validation",
            )
    _optional_bool(node, "stable", True)
    if "limit" in node.params and node.params["limit"] is not None:
        lim = node.params["limit"]
        if not isinstance(lim, int) or lim < 0:
            raise FlowValidationError(
                f"Node {node.id} sort.limit must be a non-negative integer",
                node_id=node.id,
                step_kind=node.kind,
                error_code="node_validation",
            )
    if "partition_by" in node.params and node.params["partition_by"] is not None:
        pb = node.params["partition_by"]
        if not isinstance(pb, list) or not pb or not all(isinstance(x, str) and x for x in pb):
            raise FlowValidationError(
                f"Node {node.id} sort.partition_by must be a non-empty list of strings when provided",
                node_id=node.id,
                step_kind=node.kind,
                error_code="node_validation",
            )
    if "limit_per_group" in node.params and node.params["limit_per_group"] is not None:
        lpg = node.params["limit_per_group"]
        if not isinstance(lpg, int) or lpg < 0:
            raise FlowValidationError(
                f"Node {node.id} sort.limit_per_group must be a non-negative integer when provided",
                node_id=node.id,
                step_kind=node.kind,
                error_code="node_validation",
            )


def _validate_pivot(node: Node) -> None:
    _reject_unknown_params(
        node,
        {
            "mode",
            "index",
            "columns",
            "values",
            "agg",
            "fill_value",
            "id_cols",
            "value_vars",
            "names_to",
            "values_to",
            "row_key_pattern",
            "column_pattern",
            "data_offset",
            "drop_contains",
            "numeric_fields",
            "key_row",
            "pair_size",
            "key_col_offset",
            "value_cols",
            "key_col",
            "skip_empty_keys",
            "skip_cols",
        },
    )
    mode = node.params.get("mode")
    if mode not in {"pivot_wider", "pivot_longer", "pivot_longer_from_rows", "pivot_longer_paired"}:
        raise FlowValidationError(
            f"Node {node.id} pivot.mode must be pivot_wider|pivot_longer|pivot_longer_from_rows|pivot_longer_paired",
            node_id=node.id,
            step_kind=node.kind,
            error_code="node_validation",
        )
    if mode == "pivot_longer":
        for key in ("id_cols", "value_vars"):
            lst = node.params.get(key)
            if not isinstance(lst, list) or not lst or not all(isinstance(x, str) and x for x in lst):
                raise FlowValidationError(
                    f"Node {node.id} pivot_longer requires non-empty {key}",
                    node_id=node.id,
                    step_kind=node.kind,
                    error_code="node_validation",
                )
        _require_str(node, "names_to")
        _require_str(node, "values_to")
        return
    if mode == "pivot_longer_from_rows":
        for key in ("row_key_pattern", "column_pattern"):
            lst = node.params.get(key)
            if not isinstance(lst, list) or not lst or not all(isinstance(x, str) and x for x in lst):
                raise FlowValidationError(
                    f"Node {node.id} pivot_longer_from_rows requires non-empty {key}",
                    node_id=node.id,
                    step_kind=node.kind,
                    error_code="node_validation",
                )
        _require_str(node, "names_to")
        data_offset = node.params.get("data_offset", 2)
        if not isinstance(data_offset, int) or data_offset < 0:
            raise FlowValidationError(
                f"Node {node.id} pivot_longer_from_rows data_offset must be non-negative int",
                node_id=node.id,
                step_kind=node.kind,
                error_code="node_validation",
            )
        if "drop_contains" in node.params:
            dc = node.params.get("drop_contains")
            if not isinstance(dc, list) or not all(isinstance(x, str) for x in dc):
                raise FlowValidationError(
                    f"Node {node.id} pivot_longer_from_rows drop_contains must be list[str]",
                    node_id=node.id,
                    step_kind=node.kind,
                    error_code="node_validation",
                )
        if "numeric_fields" in node.params:
            nf = node.params.get("numeric_fields")
            if not isinstance(nf, list) or not all(isinstance(x, str) and x for x in nf):
                raise FlowValidationError(
                    f"Node {node.id} pivot_longer_from_rows numeric_fields must be list[str]",
                    node_id=node.id,
                    step_kind=node.kind,
                    error_code="node_validation",
                )
        return
    if mode == "pivot_longer_paired":
        key_row = node.params.get("key_row")
        if not isinstance(key_row, int) or key_row < 0:
            raise FlowValidationError(
                f"Node {node.id} pivot_longer_paired requires non-negative int key_row",
                node_id=node.id,
                step_kind=node.kind,
                error_code="node_validation",
            )
        pair_size = node.params.get("pair_size")
        if not isinstance(pair_size, int) or pair_size < 1:
            raise FlowValidationError(
                f"Node {node.id} pivot_longer_paired requires positive int pair_size",
                node_id=node.id,
                step_kind=node.kind,
                error_code="node_validation",
            )
        key_col_offset = node.params.get("key_col_offset", 0)
        if not isinstance(key_col_offset, int) or key_col_offset < 0 or key_col_offset >= pair_size:
            raise FlowValidationError(
                f"Node {node.id} pivot_longer_paired key_col_offset must be in [0, pair_size)",
                node_id=node.id,
                step_kind=node.kind,
                error_code="node_validation",
            )
        value_cols = node.params.get("value_cols")
        if not isinstance(value_cols, list) or not value_cols or not all(isinstance(x, str) and x for x in value_cols):
            raise FlowValidationError(
                f"Node {node.id} pivot_longer_paired requires non-empty list value_cols[str]",
                node_id=node.id,
                step_kind=node.kind,
                error_code="node_validation",
            )
        _require_str(node, "key_col")
        _optional_bool(node, "skip_empty_keys", True)
        skip_cols = node.params.get("skip_cols", 0)
        if not isinstance(skip_cols, int) or skip_cols < 0:
            raise FlowValidationError(
                f"Node {node.id} pivot_longer_paired skip_cols must be a non-negative int",
                node_id=node.id,
                step_kind=node.kind,
                error_code="node_validation",
            )
        if "id_cols" in node.params:
            id_cols = node.params.get("id_cols")
            if not isinstance(id_cols, list) or not all(isinstance(x, str) and x for x in id_cols):
                raise FlowValidationError(
                    f"Node {node.id} pivot_longer_paired id_cols must be a list of non-empty strings",
                    node_id=node.id,
                    step_kind=node.kind,
                    error_code="node_validation",
                )
        return

    for key in ("index", "columns", "values"):
        lst = node.params.get(key)
        if not isinstance(lst, list) or not lst or not all(isinstance(x, str) and x for x in lst):
            raise FlowValidationError(
                f"Node {node.id} pivot_wider requires non-empty {key}",
                node_id=node.id,
                step_kind=node.kind,
                error_code="node_validation",
            )
    if "agg" in node.params and node.params["agg"] is not None:
        agg = node.params["agg"]
        if agg not in {"sum", "count", "min", "max", "avg"}:
            raise FlowValidationError(
                f"Node {node.id} pivot_wider.agg must be sum|count|min|max|avg",
                node_id=node.id,
                step_kind=node.kind,
                error_code="node_validation",
            )


def _validate_output(node: Node) -> None:
    _reject_unknown_params(node, {"path", "schema_enforce", "schema",
                           "write_order", "datetime_format", "encoding", "lineterminator"})
    _require_str(node, "path")
    schema_enforce = _optional_bool(node, "schema_enforce", False)
    if schema_enforce and node.params.get("schema") is None:
        raise_validation(
            node.id,
            node.kind,
            "output_schema_required",
            "output.schema_enforce=true requires params.schema",
            field="schema",
        )
    _optional_bool(node, "write_order", True)
    schema = node.params.get("schema")
    if schema is not None:
        if not isinstance(schema, Mapping):
            raise FlowValidationError(
                f"Node {node.id} output.schema must be an object when provided",
                node_id=node.id,
                step_kind=node.kind,
                error_code="node_validation",
            )
        unknown = [k for k in schema.keys() if k not in {
            "columns", "order", "dtype"}]
        if unknown:
            raise FlowValidationError(
                f"Node {node.id} output.schema has unknown key(s): {sorted(unknown)}",
                node_id=node.id,
                step_kind=node.kind,
                error_code="node_validation",
            )
    if "datetime_format" in node.params and node.params["datetime_format"] is not None:
        dtf = node.params["datetime_format"]
        if not isinstance(dtf, Mapping) or not all(isinstance(k, str) and isinstance(v, str) and k and v for k, v in dtf.items()):
            raise FlowValidationError(
                f"Node {node.id} output.datetime_format must be a mapping of non-empty string->string when provided",
                node_id=node.id,
                step_kind=node.kind,
                error_code="node_validation",
            )
    for key in ("encoding", "lineterminator"):
        if key in node.params and node.params[key] is not None:
            v = node.params[key]
            if not isinstance(v, str) or not v:
                raise FlowValidationError(
                    f"Node {node.id} output.{key} must be a non-empty string when provided",
                    node_id=node.id,
                    step_kind=node.kind,
                    error_code="node_validation",
                )


def _validate_script(node: Node) -> None:
    _reject_unknown_params(
        node, {"deterministic", "side_effects", "inline_code"})
    _optional_bool(node, "deterministic", True)
    _optional_bool(node, "side_effects", False)
    code = node.params.get("inline_code")
    if not isinstance(code, str) or not code.strip():
        raise FlowValidationError(
            f"Node {node.id} script.inline_code must be a non-empty string",
            node_id=node.id,
            step_kind=node.kind,
            error_code="node_validation",
            help="Use params.inline_code with a transform(df, pd, np) function. params.code/handler are not supported in this spec.",
        )
    try:
        compile(code, f"<py2flow:script:{node.id}>", "exec")
    except SyntaxError as exc:
        raise FlowValidationError(
            f"Node {node.id} script.inline_code has syntax error: {exc}",
            node_id=node.id,
            step_kind=node.kind,
            error_code="node_validation",
        ) from exc
