from __future__ import annotations

from typing import Any, Mapping, List, Dict, Callable
from uuid import uuid4

import pandas as pd

from py2flow.errors import FlowExecutionError
from py2flow.ir import StepKind
from .base import Operator, ExecutionContext
from .expr import eval_expr


class Aggregate(Operator):
    def execute(self, node_id: str, inputs: List[pd.DataFrame], params: Mapping[str, Any], ctx: ExecutionContext) -> pd.DataFrame:
        if len(inputs) != 1:
            raise ValueError("aggregate expects exactly 1 input")
        df = inputs[0]

        group_keys = params.get("group_keys", [])
        if not isinstance(group_keys, list) or not all(isinstance(x, str) and x for x in group_keys):
            raise ValueError("aggregate params.group_keys must be list[str]")

        aggs = params.get("aggs")
        if not isinstance(aggs, list) or not aggs:
            raise ValueError("aggregate params.aggs must be a non-empty list")

        having = params.get("having")
        if having is not None and (not isinstance(having, str) or not having):
            raise ValueError("aggregate params.having must be a non-empty string when provided")

        null_group = bool(params.get("null_group", True))

        work = df.copy()
        sentinels: Dict[str, str] = {}
        if group_keys and null_group:
            sentinel_token = uuid4().hex
            for col in group_keys:
                sentinel = f"__PY2FLOW_NULL_GROUP__{sentinel_token}_{col}__"
                sentinels[col] = sentinel
                work[col] = work[col].where(work[col].notna(), sentinel)

        grouped = _groupby(work, group_keys, null_group) if group_keys else None

        out_series: Dict[str, Any] = {}
        for idx, agg in enumerate(aggs):
            if not isinstance(agg, Mapping):
                raise ValueError("aggregate aggs item must be an object")
            out_name = agg.get("as")
            func = agg.get("func")
            expr = agg.get("expr")
            distinct = bool(agg.get("distinct", False))
            if not isinstance(out_name, str) or not out_name:
                raise ValueError("aggregate aggs item requires string 'as'")
            if func not in {"sum", "count", "min", "max", "avg", "count_distinct", "prod"}:
                raise ValueError("aggregate aggs item has unsupported func")
            if expr is not None and (not isinstance(expr, str) or not expr):
                raise ValueError("aggregate aggs item expr must be a non-empty string when provided")

            if expr is None and func == "count":
                if group_keys:
                    out_series[out_name] = grouped.size()  # type: ignore[union-attr]
                else:
                    out_series[out_name] = pd.Series([len(work)], index=[0])
                continue

            if expr is None:
                raise ValueError(f"aggregate func={func} requires expr")

            try:
                value = eval_expr(expr, work)
            except Exception as exc:
                raise FlowExecutionError(
                    node_id,
                    StepKind.AGGREGATE,
                    params,
                    exc,
                    message=f"aggregate expr eval failed for {out_name}: {exc}",
                    error_code="aggregate_expr_eval",
                ) from exc

            if isinstance(value, pd.Series):
                series = value
            else:
                series = pd.Series([value] * len(work), index=work.index)

            col = f"__py2flow_agg_{idx}__"
            work[col] = series
            if group_keys:
                g = _groupby(work, group_keys, null_group)[col]
                out_series[out_name] = _apply_group_agg(g, func, distinct)
            else:
                out_series[out_name] = _apply_scalar_agg(work[col], func, distinct)

        if group_keys:
            result = pd.concat(out_series, axis=1).reset_index()
            for col, sentinel in sentinels.items():
                if col in result.columns:
                    result[col] = result[col].replace({sentinel: pd.NA})
        else:
            row: Dict[str, Any] = {k: (v.iloc[0] if isinstance(v, pd.Series) else v) for k, v in out_series.items()}
            result = pd.DataFrame([row])

        if having is not None:
            try:
                pred = eval_expr(having, result)
            except Exception as exc:
                raise FlowExecutionError(
                    node_id,
                    StepKind.AGGREGATE,
                    params,
                    exc,
                    message=f"aggregate having eval failed: {exc}",
                    error_code="aggregate_having_eval",
                ) from exc
            if isinstance(pred, bool):
                mask = pd.Series([pred] * len(result), index=result.index)
            elif isinstance(pred, pd.Series):
                mask = pred
            else:
                raise FlowExecutionError(
                    node_id,
                    StepKind.AGGREGATE,
                    params,
                    TypeError(type(pred)),
                    message="aggregate having must return bool or boolean Series",
                    error_code="aggregate_having_eval",
                )
            result = result[mask.fillna(False).astype(bool)].copy()

        return result


def _groupby(df: pd.DataFrame, keys: List[str], null_group: bool) -> pd.core.groupby.generic.DataFrameGroupBy:
    if not keys:
        raise ValueError("groupby keys must be non-empty")
    try:
        return df.groupby(keys, dropna=not null_group, sort=False)
    except TypeError:
        return df.groupby(keys, sort=False)


def _apply_group_agg(g: pd.core.groupby.generic.SeriesGroupBy, func: str, distinct: bool) -> pd.Series:
    if func == "count_distinct":
        return g.nunique(dropna=True)

    if not distinct:
        if func == "sum":
            return g.sum()
        if func == "count":
            return g.count()
        if func == "min":
            return g.min()
        if func == "max":
            return g.max()
        if func == "avg":
            return g.mean()
        if func == "prod":
            return g.prod()
        raise ValueError(f"unsupported func: {func}")

    def reduce_fn(series: pd.Series) -> Any:
        series = series.drop_duplicates()
        if func == "sum":
            return series.sum()
        if func == "count":
            return series.count()
        if func == "min":
            return series.min()
        if func == "max":
            return series.max()
        if func == "avg":
            return series.mean()
        if func == "prod":
            return series.prod()
        raise ValueError(f"unsupported func: {func}")

    return g.apply(reduce_fn)


def _apply_scalar_agg(series: pd.Series, func: str, distinct: bool) -> Any:
    if distinct:
        series = series.drop_duplicates()
    if func == "sum":
        return series.sum()
    if func == "count":
        return series.count()
    if func == "min":
        return series.min()
    if func == "max":
        return series.max()
    if func == "avg":
        return series.mean()
    if func == "prod":
        return series.prod()
    if func == "count_distinct":
        return series.nunique(dropna=True)
    raise ValueError(f"unsupported func: {func}")
