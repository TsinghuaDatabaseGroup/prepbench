from __future__ import annotations

from typing import Any, Mapping, List, Tuple, Optional

import pandas as pd

from py2flow.errors import FlowExecutionError
from py2flow.ir import StepKind
from .base import Operator, ExecutionContext
from .expr import eval_expr


class Sort(Operator):
    def execute(self, node_id: str, inputs: List[pd.DataFrame], params: Mapping[str, Any], ctx: ExecutionContext) -> pd.DataFrame:
        if len(inputs) != 1:
            raise ValueError("sort expects exactly 1 input")
        df = inputs[0]

        order_by = params.get("order_by")
        if not isinstance(order_by, list) or not order_by:
            raise ValueError("sort requires params.order_by list")

        stable = params.get("stable", True)
        if not isinstance(stable, bool):
            raise ValueError("sort stable must be boolean")
        limit = params.get("limit")
        if limit is not None and (not isinstance(limit, int) or limit < 0):
            raise ValueError("sort limit must be non-negative int")

        partition_by = params.get("partition_by")
        if partition_by is not None:
            if not isinstance(partition_by, list) or not partition_by or not all(isinstance(x, str) and x for x in partition_by):
                raise ValueError("sort partition_by must be a non-empty list[str] when provided")
        limit_per_group = params.get("limit_per_group")
        if limit_per_group is not None and (not isinstance(limit_per_group, int) or limit_per_group < 0):
            raise ValueError("sort limit_per_group must be a non-negative int")

        work, sort_cols, ascending, temp_cols = _build_order_by(df, order_by)
        try:
            work = work.sort_values(by=sort_cols, ascending=ascending, kind="mergesort" if stable else "quicksort")
        except Exception as exc:
            raise FlowExecutionError(
                node_id,
                StepKind.SORT,
                params,
                exc,
                message=f"sort failed: {exc}",
                error_code="sort_error",
            ) from exc
        if temp_cols:
            work = work.drop(columns=temp_cols)
        if partition_by is not None and limit_per_group is not None:
            rank = work.groupby(partition_by, sort=False).cumcount()
            work = work.loc[rank < limit_per_group]
        if limit is not None:
            work = work.head(limit)
        return work.copy()


def _build_order_by(df: pd.DataFrame, order_by: List[Mapping[str, Any]]) -> Tuple[pd.DataFrame, List[str], List[bool], List[str]]:
    work = df.copy()
    sort_cols: List[str] = []
    ascending: List[bool] = []
    temp_cols: List[str] = []

    for idx, item in enumerate(order_by):
        if not isinstance(item, Mapping):
            raise ValueError("order_by item must be an object")
        expr = item.get("expr")
        if not isinstance(expr, str) or not expr:
            raise ValueError("order_by item requires expr")
        asc = item.get("asc", True)
        nulls = item.get("nulls", "last")
        if not isinstance(asc, bool) or nulls not in {"first", "last"}:
            raise ValueError("order_by item invalid asc/nulls")

        value = eval_expr(expr, work)
        if isinstance(value, pd.Series):
            series = value
        else:
            series = pd.Series([value] * len(work), index=work.index)

        key_col = f"__py2flow_sort_key_{idx}__"
        null_col = f"__py2flow_sort_null_{idx}__"
        work[key_col] = series
        work[null_col] = series.isna()
        temp_cols.extend([key_col, null_col])

        if nulls == "last":
            sort_cols.extend([null_col, key_col])
            ascending.extend([True, asc])
        else:
            sort_cols.extend([null_col, key_col])
            ascending.extend([False, asc])

    return work, sort_cols, ascending, temp_cols
