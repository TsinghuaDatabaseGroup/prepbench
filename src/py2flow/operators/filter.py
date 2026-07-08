from __future__ import annotations

from typing import Any, Mapping, List

import pandas as pd

from py2flow.errors import FlowExecutionError
from py2flow.ir import StepKind
from .base import Operator, ExecutionContext
from .expr import eval_expr


class Filter(Operator):
    def execute(self, node_id: str, inputs: List[pd.DataFrame], params: Mapping[str, Any], ctx: ExecutionContext) -> pd.DataFrame:
        if len(inputs) != 1:
            raise ValueError("filter expects exactly 1 input")
        df = inputs[0]
        predicate = params.get("predicate")
        if not isinstance(predicate, str) or not predicate:
            raise ValueError("filter requires params.predicate")

        null_as_false = params.get("null_as_false", True)
        if not isinstance(null_as_false, bool):
            raise ValueError("filter params.null_as_false must be boolean")

        try:
            result = eval_expr(predicate, df)
        except Exception as exc:
            help_text = None
            if isinstance(exc, NameError):
                help_text = "If you meant a column, use df['col'] or backticks: `My Col`. Identifier-like columns are also available as bare names."
            raise FlowExecutionError(
                node_id,
                StepKind.FILTER,
                params,
                exc,
                message=f"filter predicate eval failed: {exc}",
                error_code="predicate_eval",
                help=help_text,
            ) from exc

        if isinstance(result, (bool, int)):
            mask = pd.Series([bool(result)] * len(df), index=df.index)
        elif isinstance(result, pd.Series):
            if len(result) != len(df):
                raise FlowExecutionError(
                    node_id,
                    StepKind.FILTER,
                    params,
                    ValueError("mask length mismatch"),
                    message=f"filter predicate produced mask of length {len(result)} for df length {len(df)}",
                    error_code="predicate_eval",
                )
            mask = result
        else:
            raise FlowExecutionError(
                node_id,
                StepKind.FILTER,
                params,
                TypeError(f"predicate returned {type(result)}"),
                message="filter predicate must return a boolean scalar or a boolean Series",
                error_code="predicate_eval",
            )

        if null_as_false:
            mask = mask.fillna(False)
        return df[mask.astype(bool)].copy()
