from __future__ import annotations

from typing import Any, Mapping, List, Tuple

import pandas as pd

from py2flow.errors import FlowExecutionError
from py2flow.ir import StepKind
from .base import Operator, ExecutionContext
from .expr import eval_expr


class Dedup(Operator):
    def execute(self, node_id: str, inputs: List[pd.DataFrame], params: Mapping[str, Any], ctx: ExecutionContext) -> pd.DataFrame:
        if len(inputs) != 1:
            raise ValueError("dedup expects exactly 1 input")
        df = inputs[0]

        keys = params.get("keys", None)
        output = params.get("output", "all_cols")
        keep = params.get("keep", "first")

        if keys is None:
            return df.drop_duplicates().copy()
        if not isinstance(keys, list) or not all(isinstance(x, str) and x for x in keys):
            raise ValueError("dedup keys must be null or list[str]")

        if output == "keys_only":
            return df[keys].drop_duplicates().copy()
        if output != "all_cols":
            raise ValueError("dedup output must be all_cols|keys_only")

        if keep == "none":
            return df.drop_duplicates(subset=keys, keep=False).copy()
        if keep not in {"first", "last"}:
            raise ValueError("dedup keep must be first|last|none")

        order_by = params.get("order_by")
        if not isinstance(order_by, list) or not order_by:
            raise ValueError("dedup keep=first/last requires order_by")

        stable = True
        work, sort_cols, ascending, temp_cols = _build_order_by(df, order_by, stable=stable)
        try:
            work = work.sort_values(by=sort_cols, ascending=ascending, kind="mergesort")
        except Exception as exc:
            raise FlowExecutionError(
                node_id,
                StepKind.DEDUP,
                params,
                exc,
                message=f"dedup sort failed: {exc}",
                error_code="dedup_sort",
            ) from exc
        if temp_cols:
            work = work.drop(columns=temp_cols)
        return work.drop_duplicates(subset=keys, keep=keep).copy()


def _build_order_by(df: pd.DataFrame, order_by: List[Mapping[str, Any]], stable: bool) -> Tuple[pd.DataFrame, List[str], List[bool], List[str]]:
    work = df.copy()
    sort_cols: List[str] = []
    ascending: List[bool] = []
    temp_cols: List[str] = []

    for idx, item in enumerate(order_by):
        expr = item.get("expr")
        if not isinstance(expr, str) or not expr:
            raise ValueError("order_by item requires expr")
        asc = item.get("asc", True)
        nulls = item.get("nulls", "last")
        if not isinstance(asc, bool) or nulls not in {"first", "last"}:
            raise ValueError("order_by item invalid asc/nulls")

        try:
            value = eval_expr(expr, work)
        except Exception as exc:
            raise ValueError(f"order_by expr failed: {expr!r} ({exc})") from exc

        if isinstance(value, pd.Series):
            series = value
        else:
            series = pd.Series([value] * len(work), index=work.index)

        key_col = f"__py2flow_order_key_{idx}__"
        null_col = f"__py2flow_order_null_{idx}__"
        work[key_col] = series
        work[null_col] = series.isna()
        temp_cols.extend([key_col, null_col])

        # nulls ordering: sort by null-flag first, then actual key
        if nulls == "last":
            sort_cols.extend([null_col, key_col])
            ascending.extend([True, asc])
        else:
            sort_cols.extend([null_col, key_col])
            ascending.extend([False, asc])

    return work, sort_cols, ascending, temp_cols
