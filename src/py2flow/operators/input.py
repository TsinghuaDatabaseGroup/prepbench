from __future__ import annotations

from typing import Any, Mapping, List

import pandas as pd

from .base import Operator, ExecutionContext


class Input(Operator):
    def execute(self, node_id: str, inputs: List[pd.DataFrame], params: Mapping[str, Any], ctx: ExecutionContext) -> pd.DataFrame:
        if inputs:
            raise ValueError("input expects no inputs")
        if ctx.input_tables is not None:
            table = ctx.input_tables.get(node_id)
            if table is not None:
                if not isinstance(table, pd.DataFrame):
                    raise ValueError("input_tables must map node_id to pandas DataFrame")
                return table.copy(deep=False)
        data = params.get("data")
        source_type = params.get("source_type")
        if data is not None or source_type == "inline":
            if source_type not in (None, "inline"):
                raise ValueError("input params.source_type must be inline when provided")
            if data is None:
                raise ValueError("input params.data is required for inline inputs")
            if not isinstance(data, (list, dict)):
                raise ValueError("input params.data must be list[dict] or dict[str,list]")
            return pd.DataFrame(data)

        path = params.get("path")
        if not isinstance(path, str) or not path:
            raise ValueError("input requires params.path")
        resolved = ctx.resolve_path(path)
        mode = params.get("mode", "csv")
        if mode not in {"csv", "line"}:
            raise ValueError("input params.mode must be csv|line")

        encoding = params.get("encoding", "utf-8")
        encodings: list[str]
        if isinstance(encoding, str):
            encodings = [encoding]
        elif isinstance(encoding, list) and encoding and all(isinstance(x, str) and x for x in encoding):
            encodings = list(encoding)
        else:
            raise ValueError("input params.encoding must be string or list[string]")

        skiprows = params.get("skiprows", 0)
        if not isinstance(skiprows, int) or skiprows < 0:
            raise ValueError("input params.skiprows must be a non-negative int")

        if mode == "line":
            last_exc: BaseException | None = None
            for enc in encodings:
                try:
                    lines = resolved.read_text(encoding=enc).splitlines()
                    break
                except Exception as exc:
                    last_exc = exc
                    ctx.logger.warning(
                        "input read attempt failed node=%s mode=line encoding=%s path=%s error=%s",
                        node_id,
                        enc,
                        resolved,
                        exc,
                    )
                    lines = []
            else:
                raise ValueError(f"input line read failed for encodings={encodings}: {last_exc}")
            if skiprows:
                lines = lines[skiprows:]
            return pd.DataFrame({"raw": pd.Series(lines, dtype="string")})

        options_base: dict[str, Any] = {}
        options_base["sep"] = params.get("delimiter", ",")
        if "na_values" in params:
            options_base["na_values"] = params.get("na_values")
        if "keep_default_na" in params:
            options_base["keep_default_na"] = params.get("keep_default_na")
        if "parse_dates" in params:
            options_base["parse_dates"] = params.get("parse_dates")
        if "dtype" in params:
            options_base["dtype"] = params.get("dtype")
        if "skiprows" in params:
            options_base["skiprows"] = skiprows
        if "header" in params:
            options_base["header"] = params.get("header")
        if "on_bad_lines" in params:
            options_base["on_bad_lines"] = params.get("on_bad_lines")
        if "quotechar" in params:
            options_base["quotechar"] = params.get("quotechar")
        if "escapechar" in params:
            options_base["escapechar"] = params.get("escapechar")

        last_exc: BaseException | None = None
        for enc in encodings:
            options = dict(options_base)
            options["encoding"] = enc
            try:
                return ctx.io.read_df(resolved, "csv", options)
            except Exception as exc:
                last_exc = exc
                ctx.logger.warning(
                    "input read attempt failed node=%s mode=csv encoding=%s path=%s error=%s",
                    node_id,
                    enc,
                    resolved,
                    exc,
                )
        raise ValueError(f"input csv read failed for encodings={encodings}: {last_exc}")
