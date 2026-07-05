from __future__ import annotations

from typing import Any, Mapping, List

import pandas as pd

from .base import Operator, ExecutionContext


class Union(Operator):
    def execute(self, node_id: str, inputs: List[pd.DataFrame], params: Mapping[str, Any], ctx: ExecutionContext) -> pd.DataFrame:
        if len(inputs) < 2:
            raise ValueError("union expects 2 or more inputs")

        if "distinct" not in params:
            raise ValueError("union requires params.distinct")
        distinct = params.get("distinct")
        if not isinstance(distinct, bool):
            raise ValueError("union params.distinct must be boolean")

        align = params.get("align", "by_name")
        if align != "by_name":
            raise ValueError("union align=by_position is not supported")
        fill_missing = params.get("fill_missing", "null")
        if fill_missing not in {"null", "error"}:
            raise ValueError("union fill_missing must be null|error")
        type_coerce = params.get("type_coerce", "error")
        if type_coerce != "error":
            raise ValueError("union type_coerce=safe_cast is not supported")

        frames = [df.copy() for df in inputs]
        all_cols: List[str] = []
        for df in frames:
            for c in df.columns:
                if c not in all_cols:
                    all_cols.append(str(c))

        if fill_missing == "error":
            expected = set(all_cols)
            for df in frames:
                if set(df.columns) != expected:
                    raise ValueError("union fill_missing=error requires all inputs to have the same columns")
        else:
            frames = [df.reindex(columns=all_cols) for df in frames]

        out = pd.concat(frames, ignore_index=True, sort=False)
        if distinct:
            out = out.drop_duplicates(ignore_index=True)
        return out
