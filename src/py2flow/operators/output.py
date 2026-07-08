from __future__ import annotations

from typing import Any, Mapping, List

import pandas as pd

from .base import Operator, ExecutionContext


def _format_datetime_series(series: pd.Series, fmt: str) -> pd.Series:
    if pd.api.types.is_datetime64_any_dtype(series):
        dt = series
    else:
        dt = pd.to_datetime(series, errors="coerce")
    if getattr(dt.dt, "tz", None) is not None:
        dt = dt.dt.tz_convert(None)
    return dt.dt.strftime(fmt).astype("string")


class Output(Operator):
    def execute(self, node_id: str, inputs: List[pd.DataFrame], params: Mapping[str, Any], ctx: ExecutionContext) -> pd.DataFrame:
        if len(inputs) != 1:
            raise ValueError("output expects exactly 1 input")
        df = inputs[0]
        path = params.get("path")
        if not isinstance(path, str) or not path:
            raise ValueError("output requires params.path")

        schema_enforce = bool(params.get("schema_enforce", False))
        write_order = params.get("write_order", True)
        if not isinstance(write_order, bool):
            raise ValueError("output.write_order must be boolean")
        schema: Any = params.get("schema")
        out = df
        if schema_enforce:
            if not isinstance(schema, Mapping):
                raise ValueError("output.schema_enforce=true requires params.schema object")
            expected_columns = schema.get("columns")
            if isinstance(expected_columns, list):
                expected_columns = [str(c) for c in expected_columns]
                if set(out.columns) != set(expected_columns):
                    raise ValueError(f"output schema column set mismatch: expected={expected_columns} got={list(out.columns)}")
            order = schema.get("order") or schema.get("columns")
            if isinstance(order, list) and write_order:
                order = [str(c) for c in order]
                missing = [c for c in order if c not in out.columns]
                if missing:
                    raise ValueError(f"output schema order references missing columns: {missing}")
                out = out[order]
            dtype = schema.get("dtype")
            if isinstance(dtype, Mapping):
                out = out.astype(dict(dtype))
        elif isinstance(schema, Mapping) and write_order:
            order = schema.get("order") or schema.get("columns")
            if isinstance(order, list):
                order = [str(c) for c in order]
                missing = [c for c in order if c not in out.columns]
                if missing:
                    raise ValueError(f"output schema order references missing columns: {missing}")
                remaining = [c for c in out.columns if c not in order]
                out = out[order + remaining]

        datetime_format = params.get("datetime_format")
        if isinstance(datetime_format, Mapping) and datetime_format:
            out = out.copy()
            for col, fmt in datetime_format.items():
                if not isinstance(col, str) or not isinstance(fmt, str) or not col or not fmt:
                    raise ValueError("output.datetime_format must be a mapping of non-empty string->string")
                if col not in out.columns:
                    continue
                out[col] = _format_datetime_series(out[col], fmt)

        resolved = ctx.resolve_path(path)
        options: dict[str, Any] = {"index": False}
        encoding = params.get("encoding")
        if encoding is not None:
            if not isinstance(encoding, str) or not encoding:
                raise ValueError("output.encoding must be a non-empty string when provided")
            options["encoding"] = encoding
        lineterminator = params.get("lineterminator")
        if lineterminator is not None:
            if not isinstance(lineterminator, str) or not lineterminator:
                raise ValueError("output.lineterminator must be a non-empty string when provided")
            options["lineterminator"] = lineterminator
        ctx.io.write_df(out, resolved, "csv", options)
        return out
