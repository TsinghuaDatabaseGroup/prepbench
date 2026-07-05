from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from graphlib import CycleError, TopologicalSorter
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Optional, Set, DefaultDict, Literal

import logging
import time

import pandas as pd

from .errors import FlowExecutionError, FlowValidationError
from .ir import DAG, Node, StepKind
from .operators import OperatorRegistry, get_global_operator_registry
from .operators.base import ExecutionContext, Operator


@dataclass(frozen=True)
class DebugConfig:
    dump_nodes: Set[str] | None = None
    trace: bool = False
    on_fail_dump: bool = False
    sample_rows: int = 3


class DAGExecutor:

    def __init__(
        self,
        dag: DAG,
        base_path: str | Path | None = None,
        logger: logging.Logger | None = None,
        operator_registry: OperatorRegistry | Mapping[StepKind, Operator] | None = None,
        debug: DebugConfig | None = None,
        input_tables: Mapping[str, pd.DataFrame] | None = None,
    ) -> None:
        self.dag = dag
        self.base_path = Path(base_path) if base_path is not None else None
        self._script_cache: Dict[str, Any] = {}
        if operator_registry is None:
            self._ops = dict(get_global_operator_registry().as_mapping())
        elif isinstance(operator_registry, OperatorRegistry):
            self._ops = dict(operator_registry.as_mapping())
        else:
            self._ops = dict(operator_registry)
        self._ctx = ExecutionContext(self.base_path, logger=logger, input_tables=input_tables)
        self._debug = debug or DebugConfig()
        self._ctx.executor = self

        self._deps: Dict[str, List[str]] = {nid: list(n.inputs) for nid, n in self.dag.nodes.items()}

        self._results: Dict[str, Any] = {}

    def run(
        self,
        targets: Optional[List[str]] = None,
        keep: Literal["outputs", "targets", "all", "none"] = "all",
    ) -> Dict[str, Any]:
        self.dag.validate()

        order = self._topological_order(self.dag.nodes)
        targets = targets or self._default_targets()
        target_set = set(targets)

        needed = self._backward_closure(target_set)
        refcnt = self._ref_counts(needed)
        self._results.clear()

        for node_id in order:
            if node_id not in needed:
                continue
            node = self.dag.nodes[node_id]
            upstream = [self._results[i] for i in node.inputs]
            t0 = time.time()
            try:
                res = self._execute_node(node, upstream)
            except BaseException as exc:
                if self._debug.on_fail_dump:
                    self._dump_failure(node, upstream, exc)
                if isinstance(exc, FlowValidationError):
                    raise
                if isinstance(exc, FlowExecutionError):
                    raise
                self._ctx.logger.error(f"node_failed id={node.id} kind={node.kind.value}: {exc}")
                raise FlowExecutionError(node.id, node.kind, node.params or {}, exc, error_code="operator_error") from exc
            self._ctx.logger.debug(
                f"node={node.id} kind={node.kind.value} took={time.time()-t0:.3f}s"
            )
            self._results[node_id] = res
            self._after_node(node, res)
            for i in node.inputs:
                if i in refcnt:
                    refcnt[i] -= 1
                    if refcnt[i] <= 0 and keep not in ("all",) and not (keep in ("outputs", "targets") and i in target_set):
                        self._results.pop(i, None)

        if keep == "outputs":
            outs = [nid for nid, n in self.dag.nodes.items() if n.kind is StepKind.OUTPUT]
            return {nid: self._results[nid] for nid in outs if nid in self._results}
        if keep == "targets":
            return {nid: self._results[nid] for nid in targets if nid in self._results}
        if keep == "none":
            return {}
        return dict(self._results)

    def _execute_node(self, node: Node, upstream: List[Any]) -> Any:
        op: Optional[Operator] = self._ops.get(node.kind)
        if op is None:
            raise ValueError(f"Unsupported StepKind: {node.kind}")
        res = op.execute(node.id, upstream, node.params or {}, self._ctx)
        if isinstance(res, pd.DataFrame) and node.kind is not StepKind.SORT:
            for up in upstream:
                if isinstance(up, pd.DataFrame) and res is up:
                    res = res.copy(deep=False)
                    break
        if isinstance(res, pd.DataFrame):
            if node.kind is StepKind.SORT:
                res.attrs["__py2flow_order__"] = True
            else:
                res.attrs.pop("__py2flow_order__", None)
        return res

    def _default_targets(self) -> List[str]:
        outs = [nid for nid, n in self.dag.nodes.items() if n.kind is StepKind.OUTPUT]
        return outs or list(self.dag.nodes.keys())

    def _backward_closure(self, targets: Set[str]) -> Set[str]:
        needed: Set[str] = set()
        stack: List[str] = list(targets)
        while stack:
            nid = stack.pop()
            if nid in needed:
                continue
            needed.add(nid)
            stack.extend(self._deps.get(nid, []))
        return needed

    def _ref_counts(self, needed: Set[str]) -> Dict[str, int]:
        cnt: DefaultDict[str, int] = defaultdict(int)
        for nid in needed:
            for i in self._deps.get(nid, []):
                if i in needed:
                    cnt[i] += 1
        return cnt

    @staticmethod
    def _topological_order(nodes: Mapping[str, Node]) -> List[str]:
        graph: Dict[str, Iterable[str]] = {node_id: node.inputs for node_id, node in nodes.items()}
        sorter = TopologicalSorter(graph)
        try:
            return list(sorter.static_order())
        except CycleError as exc:
            raise FlowValidationError(f"DAG has a cycle: {exc}", error_code="cycle") from exc

    def _prepare_script_nodes(self) -> None:  # pragma: no cover
        # Script syntax validation is handled in ir.DAG.validate(); compilation is cached by the operator.
        return

    def _after_node(self, node: Node, res: Any) -> None:
        if self._debug.trace and isinstance(res, pd.DataFrame):
            cols = list(res.columns)
            n = max(0, int(self._debug.sample_rows))
            sample = res.head(n).to_dict(orient="records") if n else []
            self._ctx.logger.info(
                f"trace node={node.id} kind={node.kind.value} rows={len(res)} cols={len(cols)} columns={cols}"
            )
            self._ctx.logger.info(f"trace node={node.id} sample={sample}")

        if self.base_path is None:
            return
        if self._debug.dump_nodes and node.id in self._debug.dump_nodes and isinstance(res, pd.DataFrame):
            debug_dir = self.base_path / "flow_cand" / "@debug"
            path = debug_dir / f"{node.id}.csv"
            self._ctx.io.write_df(res, path, "csv", {"index": False})

    def _dump_failure(self, node: Node, upstream: List[Any], exc: BaseException) -> None:
        if self.base_path is None:
            return
        debug_dir = self.base_path / "flow_cand" / "@debug" / "@fail" / node.id
        debug_dir.mkdir(parents=True, exist_ok=True)

        (debug_dir / "error.txt").write_text(f"{type(exc).__name__}: {exc}\n", encoding="utf-8")
        (debug_dir / "node_kind.txt").write_text(node.kind.value, encoding="utf-8")

        import json

        (debug_dir / "params.json").write_text(json.dumps(dict(node.params or {}), ensure_ascii=False, indent=2), encoding="utf-8")
        for idx, up in enumerate(upstream):
            if isinstance(up, pd.DataFrame):
                self._ctx.io.write_df(up, debug_dir / f"upstream_{idx}.csv", "csv", {"index": False})
