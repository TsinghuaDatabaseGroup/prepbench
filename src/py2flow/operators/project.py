from __future__ import annotations

import re
from datetime import datetime
from typing import Any, Mapping, List, Optional, Tuple

import pandas as pd

from py2flow.errors import FlowExecutionError
from py2flow.ir import StepKind
from .base import Operator, ExecutionContext
from .expr import eval_expr


class Project(Operator):
    def execute(self, node_id: str, inputs: List[pd.DataFrame], params: Mapping[str, Any], ctx: ExecutionContext) -> pd.DataFrame:
        if len(inputs) != 1:
            raise ValueError("project expects 1 input")

        original_input_df = inputs[0]
        df = original_input_df.copy()
        on_error = params.get("on_error", "error")
        if on_error not in {"keep", "null", "error", "tag"}:
            raise ValueError(
                "project params.on_error must be keep|null|error|tag")
        error_cols = params.get("error_cols") if on_error == "tag" else None
        if on_error == "tag":
            if not isinstance(error_cols, list) or not error_cols or not all(isinstance(c, str) and c for c in error_cols):
                raise ValueError(
                    "project on_error=tag requires params.error_cols list[str]")

        def append_error(mask: pd.Series, message: str) -> None:
            if on_error != "tag":
                return
            col = error_cols[0]
            if col not in df.columns:
                df[col] = pd.Series(
                    [""] * len(df), index=df.index, dtype="string")
            existing = df[col].astype("string")
            add = pd.Series([""] * len(df), index=df.index, dtype="string")
            add.loc[mask] = message
            combined = existing.where(existing != "", add)
            combined = combined.where(add == "", combined + ";" + add)
            df[col] = combined

        def handle_exception(exc: BaseException, message: str, target_col: Optional[str] = None) -> None:
            if on_error == "error":
                help_text = None
                if isinstance(exc, NameError):
                    help_text = "If you meant a column, use df['col'] or backticks: `My Col`. Identifier-like columns are also available as bare names."
                raise FlowExecutionError(
                    node_id,
                    StepKind.PROJECT,
                    params,
                    exc,
                    message=message,
                    error_code="project_error",
                    help=help_text,
                ) from exc
            if on_error == "keep":
                return
            if target_col is not None:
                df[target_col] = pd.NA
            if on_error == "tag":
                append_error(
                    pd.Series([True] * len(df), index=df.index), message)

        # promote row to header (handle fake header rows)
        promote_idx = params.get("promote_row_to_header")
        if promote_idx is not None:
            if not isinstance(promote_idx, int):
                raise ValueError(
                    "project params.promote_row_to_header must be int")
            if promote_idx < 0 or promote_idx >= len(df):
                raise ValueError(
                    "project params.promote_row_to_header out of range")
            header_series = df.iloc[promote_idx].astype("string")
            new_cols: List[str] = []
            for v in header_series.tolist():
                if v is None:
                    new_cols.append("")
                else:
                    try:
                        import pandas as _pd
                        if v is _pd.NA:
                            new_cols.append("")
                        else:
                            new_cols.append(str(v))
                    except Exception:
                        new_cols.append(str(v))
            if len(new_cols) != df.shape[1]:
                raise ValueError(
                    "project promote_row_to_header: header length mismatch")
            # Drop the header row and reset index
            df = df.drop(df.index[promote_idx]).reset_index(drop=True)
            df.columns = new_cols

        # select
        select = params.get("select")
        if select is not None:
            if not isinstance(select, list):
                raise ValueError("project params.select must be list")
            cols: List[str] = []
            for item in select:
                if item == "*":
                    cols.extend([str(c) for c in df.columns])
                else:
                    cols.append(str(item))
            if len(set(cols)) != len(cols):
                raise ValueError(
                    "project params.select must not contain duplicate columns after expansion")
            missing = [c for c in cols if c not in df.columns]
            if missing:
                raise FlowExecutionError(
                    node_id,
                    StepKind.PROJECT,
                    params,
                    KeyError(missing),
                    message=f"project select missing columns: {missing}",
                    error_code="project_missing_columns",
                )
            df = df[cols].copy()

        # rename
        rename = params.get("rename")
        if rename is not None:
            if not isinstance(rename, Mapping):
                raise ValueError("project params.rename must be object")
            # Convert string keys to int if column names are integers
            rename_dict = {}
            for k, v in rename.items():
                try:
                    # Try to convert key to int if it's a numeric string and column exists
                    if isinstance(k, str) and k.isdigit() and int(k) in df.columns:
                        rename_dict[int(k)] = v
                    else:
                        rename_dict[k] = v
                except (ValueError, TypeError):
                    rename_dict[k] = v
            df = df.rename(columns=rename_dict)

        # compute
        compute = params.get("compute") or []
        if compute:
            if not isinstance(compute, list):
                raise ValueError("project params.compute must be list")
            for item in compute:
                if not isinstance(item, Mapping):
                    raise ValueError("project compute item must be object")
                as_col = item.get("as")
                expr = item.get("expr")
                if not isinstance(as_col, str) or not as_col or not isinstance(expr, str) or not expr:
                    raise ValueError("project compute requires {as, expr}")
                try:
                    val = eval_expr(expr, df)
                    if isinstance(val, pd.Series):
                        if len(val) != len(df):
                            raise ValueError(
                                f"compute expr length mismatch for {as_col}")
                        df[as_col] = val.values
                    else:
                        df[as_col] = val
                except Exception as exc:
                    handle_exception(
                        exc, f"project compute failed for {as_col}: {exc}", target_col=as_col)

        # cast
        cast = params.get("cast") or []
        if cast:
            if not isinstance(cast, list):
                raise ValueError("project params.cast must be list")
            for item in cast:
                if not isinstance(item, Mapping):
                    raise ValueError("project cast item must be object")
                col = item.get("col")
                dtype = item.get("dtype")
                errors = item.get("errors", "raise")
                if not isinstance(col, str) or not isinstance(dtype, str):
                    raise ValueError("project cast requires {col, dtype}")
                if col not in df.columns:
                    raise FlowExecutionError(
                        node_id,
                        StepKind.PROJECT,
                        params,
                        KeyError(col),
                        message=f"project cast missing column: {col}",
                        error_code="project_missing_columns",
                    )
                try:
                    converted, invalid_mask = _cast_series(
                        df[col], dtype, errors=str(errors))
                    df[col] = converted
                    if on_error == "tag" and invalid_mask is not None and invalid_mask.any():
                        append_error(invalid_mask, f"cast:{col}->{dtype}")
                except Exception as exc:
                    handle_exception(
                        exc, f"project cast failed for {col}: {exc}", target_col=col)

        # map
        map_ops = params.get("map") or []
        if map_ops:
            if not isinstance(map_ops, list):
                raise ValueError("project params.map must be list")
            for op in map_ops:
                if not isinstance(op, Mapping):
                    raise ValueError("project map item must be object")
                col = op.get("col")
                op_name = op.get("op")
                args = op.get("args") or {}
                if not isinstance(col, str) or not col or not isinstance(op_name, str) or not op_name:
                    raise ValueError("project map requires {col, op, args}")
                if not isinstance(args, Mapping):
                    raise ValueError("project map args must be an object")
                if col not in df.columns:
                    raise FlowExecutionError(
                        node_id,
                        StepKind.PROJECT,
                        params,
                        KeyError(col),
                        message=f"project map missing column: {col}",
                        error_code="project_missing_columns",
                    )
                top_when = op.get("when")
                args_when = args.get("when")
                if top_when is not None and args_when is not None and top_when != args_when:
                    raise ValueError("map.when and map args.when conflict")
                when_expr = top_when if top_when is not None else args_when
                if when_expr is not None:
                    if not isinstance(when_expr, str) or not when_expr:
                        raise ValueError("map.when must be a non-empty string")
                    if op_name in {"explode", "regex_extract", "complete_calendar"}:
                        raise ValueError(
                            f"map.when is not supported for op {op_name}")
                    mask = eval_expr(when_expr, df)
                    if isinstance(mask, bool):
                        mask = pd.Series(
                            [mask] * len(df), index=df.index)
                    elif isinstance(mask, pd.Series):
                        if len(mask) != len(df):
                            raise ValueError(
                                f"map.when length mismatch for {col}")
                    else:
                        raise ValueError(
                            "map.when must evaluate to bool or boolean Series")
                    mask = mask.fillna(False).astype(bool)
                else:
                    mask = None

                args_clean = dict(args)
                args_clean.pop("when", None)
                try:
                    if op_name == "explode":
                        df = _apply_explode(df, col, args_clean)
                    elif op_name == "regex_extract":
                        invalid = _apply_regex_extract(
                            df, source_col=col, args=args_clean)
                        if on_error == "tag" and invalid is not None and invalid.any():
                            append_error(invalid, f"map:{col}:{op_name}")
                    elif op_name == "complete_calendar":
                        df = _apply_complete_calendar(df, col, args_clean)
                    else:
                        series, invalid = _apply_map(
                            df, df[col], op_name, args_clean)
                        dest = args_clean.get("as")
                        if dest is not None and (not isinstance(dest, str) or not dest):
                            raise ValueError(
                                "map args.as must be a non-empty string when provided")
                        target_col = dest or col
                        if mask is not None:
                            base = df[target_col] if target_col in df.columns else df[col]
                            series = base.where(~mask, series)
                            if invalid is not None:
                                invalid = invalid & mask
                        df[target_col] = series.values
                        if on_error == "tag" and invalid is not None and invalid.any():
                            append_error(invalid, f"map:{col}:{op_name}")
                except Exception as exc:
                    if op_name == "regex_extract":
                        dest = args_clean.get("as")
                        if isinstance(dest, str) and dest:
                            handle_exception(
                                exc, f"project map failed for {col}.{op_name}: {exc}", target_col=dest)
                        elif isinstance(dest, list) and dest:
                            if on_error == "error":
                                raise FlowExecutionError(
                                    node_id,
                                    StepKind.PROJECT,
                                    params,
                                    exc,
                                    message=f"project map failed for {col}.{op_name}: {exc}",
                                    error_code="project_error",
                                ) from exc
                            if on_error == "null":
                                for d in dest:
                                    if isinstance(d, str) and d:
                                        df[d] = pd.NA
                            if on_error == "tag":
                                append_error(
                                    pd.Series([True] * len(df), index=df.index), f"map:{col}:{op_name}")
                        else:
                            handle_exception(
                                exc, f"project map failed for {col}.{op_name}: {exc}", target_col=col)
                    else:
                        dest = args_clean.get("as")
                        target_col = dest if isinstance(
                            dest, str) and dest else col
                        handle_exception(
                            exc, f"project map failed for {col}.{op_name}: {exc}", target_col=target_col)

        # expand (for scaffold generation)
        expand_cfg = params.get("expand")
        if expand_cfg is not None:
            if not isinstance(expand_cfg, Mapping):
                raise ValueError("project params.expand must be an object")
            try:
                # Pass original input df for to_value_expr evaluation (to access columns from upstream)
                df = _apply_expand(
                    df, expand_cfg, original_df=original_input_df)
            except Exception as exc:
                handle_exception(
                    exc, f"project expand failed: {exc}", target_col=None)

        return df


def _cast_series(series: pd.Series, dtype: str, errors: str) -> tuple[pd.Series, Optional[pd.Series]]:
    if errors not in {"raise", "null"}:
        raise ValueError("cast errors must be raise|null")

    if dtype == "string":
        return series.astype("string"), None

    if dtype == "datetime64[ns]":
        out = pd.to_datetime(
            series, errors="coerce" if errors == "null" else "raise")
        invalid = (out.isna() & series.notna()) if errors == "null" else None
        return out, invalid

    if dtype == "float64":
        out = pd.to_numeric(series, errors="coerce" if errors ==
                            "null" else "raise").astype("float64")
        invalid = (out.isna() & series.notna()) if errors == "null" else None
        return out, invalid

    if dtype == "int64":
        numeric = pd.to_numeric(
            series, errors="coerce" if errors == "null" else "raise")
        if errors == "null":
            out = numeric.astype("Int64")
            invalid = out.isna() & series.notna()
            return out, invalid
        return numeric.astype("int64"), None

    if dtype == "bool":
        return _to_bool(series, errors=errors)

    raise ValueError(f"unsupported dtype: {dtype}")


def _to_bool(series: pd.Series, errors: str) -> tuple[pd.Series, Optional[pd.Series]]:
    s = series
    if errors == "raise":
        # Best-effort strict parsing: only accept bool-like strings and 0/1.
        out, invalid = _to_bool(series, errors="null")
        if invalid is not None and invalid.any():
            bad = series[invalid].head(5).tolist()
            raise ValueError(f"bool cast failed for values like {bad}")
        return out.astype("bool"), None

    # errors == "null"
    s_str = s.astype("string").str.strip().str.lower()
    mapping = {
        "true": True,
        "t": True,
        "1": True,
        "yes": True,
        "y": True,
        "false": False,
        "f": False,
        "0": False,
        "no": False,
        "n": False,
    }
    out = s_str.map(mapping)
    # preserve already-bool values
    out = out.where(~s.apply(lambda v: isinstance(v, bool)),
                    s.astype("boolean"))
    invalid = out.isna() & s.notna()
    return out.astype("boolean"), invalid


def _apply_map(df: pd.DataFrame, series: pd.Series, op_name: str, args: Mapping[str, Any]) -> tuple[pd.Series, Optional[pd.Series]]:
    if op_name == "trim":
        return series.astype("string").str.strip(), None
    if op_name == "lower":
        return series.astype("string").str.lower(), None
    if op_name == "upper":
        return series.astype("string").str.upper(), None
    if op_name == "regex_replace":
        pattern = args.get("pattern")
        repl = args.get("repl", "")
        if not isinstance(pattern, str) or not isinstance(repl, str):
            raise ValueError("regex_replace args require {pattern, repl}")
        return series.astype("string").str.replace(pattern, repl, regex=True), None
    if op_name == "html_strip":
        return series.astype("string").str.replace(r"<[^>]+>", "", regex=True), None
    if op_name == "squeeze_whitespace":
        out = series.astype("string").str.replace(
            r"\s+", " ", regex=True).str.strip()
        return out, None
    if op_name == "fillna":
        if "value" not in args:
            raise ValueError("fillna args require {value}")
        return series.fillna(args.get("value")), None
    if op_name == "map_values":
        mapping = args.get("mapping")
        default = args.get("default", None)
        if not isinstance(mapping, Mapping):
            raise ValueError("map_values args require {mapping}")
        mapped = series.map(dict(mapping))
        missing = mapped.isna() & series.notna()
        if default is not None:
            mapped = mapped.fillna(default)
            missing = None
        return mapped, missing
    if op_name == "split":
        pattern = args.get("pattern")
        regex = args.get("regex", True)
        keep_empty = args.get("keep_empty", False)
        if not isinstance(pattern, str) or not pattern:
            raise ValueError("split args require non-empty {pattern}")
        if not isinstance(regex, bool):
            raise ValueError("split args.regex must be boolean")
        if not isinstance(keep_empty, bool):
            raise ValueError("split args.keep_empty must be boolean")
        out = series.astype("string").str.split(pattern, regex=regex)
        if not keep_empty:
            out = out.apply(
                lambda xs: [x for x in xs if x] if isinstance(xs, list) else xs)
        return out, None
    if op_name == "tokenize":
        pattern = args.get("pattern")
        to_lower = args.get("to_lower", True)
        min_len = args.get("min_len", 1)
        keep_alnum = args.get("keep_alnum", True)
        if not isinstance(pattern, str) or not pattern:
            raise ValueError("tokenize args require non-empty {pattern}")
        if not isinstance(to_lower, bool):
            raise ValueError("tokenize args.to_lower must be boolean")
        if not isinstance(min_len, int) or min_len < 1:
            raise ValueError("tokenize args.min_len must be int >= 1")
        if not isinstance(keep_alnum, bool):
            raise ValueError("tokenize args.keep_alnum must be boolean")

        token_re = re.compile(pattern)

        def tokenize_one(v: Any) -> Any:
            if v is None or v is pd.NA:
                return []
            if isinstance(v, float) and pd.isna(v):
                return []
            s = str(v)
            if to_lower:
                s = s.lower()
            toks = token_re.findall(s)
            out: list[str] = []
            for t in toks:
                tok = t
                if isinstance(tok, tuple):
                    tok = next((x for x in tok if x), "")
                tok = str(tok)
                if keep_alnum:
                    tok = "".join(ch for ch in tok if ch.isalnum())
                if len(tok) >= min_len:
                    out.append(tok)
            return out

        return series.apply(tokenize_one), None
    if op_name == "date_range_to_start":
        range_re = re.compile(
            r"^(?P<d1>\d{1,2})\s*-\s*(?P<d2>\d{1,2})\s+(?P<mon>[A-Za-z]+)\s*,\s*(?P<y>\d{4})$"
        )

        def normalize_one(v: Any) -> Any:
            if v is None or v is pd.NA:
                return pd.NA
            if isinstance(v, float) and pd.isna(v):
                return pd.NA
            text = str(v).strip()
            m = range_re.match(text)
            if not m:
                return text
            return f"{int(m.group('d1'))} {m.group('mon')}, {int(m.group('y')):04d}"

        return series.apply(normalize_one), None
    if op_name == "date_year_only":
        year_re = re.compile(r"^(?P<y>\d{4})$")
        year_ad_re = re.compile(r"^(?P<y>\d{1,4})\s*AD$", flags=re.IGNORECASE)

        def normalize_one(v: Any) -> Any:
            if v is None or v is pd.NA:
                return pd.NA
            if isinstance(v, float) and pd.isna(v):
                return pd.NA
            text = str(v).strip()
            m = year_re.fullmatch(text)
            if m:
                return f"01/01/{int(m.group('y')):04d}"
            m = year_ad_re.fullmatch(text)
            if m:
                return f"01/01/{int(m.group('y')):04d}"
            return text

        return series.apply(normalize_one), None
    if op_name == "group_cumcount":
        by = args.get("by")
        start = args.get("start", 1)
        sort = args.get("sort", False)
        if isinstance(by, str):
            by_cols = [by]
        elif isinstance(by, list) and by and all(isinstance(x, str) and x for x in by):
            by_cols = list(by)
        else:
            raise ValueError("group_cumcount args.by must be a non-empty string or list[str]")
        if not isinstance(start, int):
            raise ValueError("group_cumcount args.start must be int")
        if not isinstance(sort, bool):
            raise ValueError("group_cumcount args.sort must be bool")
        missing = [c for c in by_cols if c not in df.columns]
        if missing:
            raise ValueError(f"group_cumcount args.by missing columns: {missing}")
        out = df.groupby(by_cols, sort=sort).cumcount() + start
        return out.astype("Int64"), None
    if op_name == "parse_date_multi":
        formats = args.get("formats")
        out_fmt = args.get("out_fmt", "%d/%m/%Y")
        errors = args.get("errors", "null")
        if formats is not None and (not isinstance(formats, list) or not all(isinstance(x, str) and x for x in formats)):
            raise ValueError("parse_date_multi args.formats must be list[str] when provided")
        if not isinstance(out_fmt, str) or not out_fmt:
            raise ValueError("parse_date_multi args.out_fmt must be non-empty string")
        if errors not in {"null", "raise"}:
            raise ValueError("parse_date_multi args.errors must be null|raise")
        fmt_list = formats or ["%d %B, %Y", "%B %d, %Y", "%d %B %Y",
                               "%B %d %Y", "%d/%m/%Y", "%Y-%m-%d"]
        range_re = re.compile(
            r"^(?P<d1>\d{1,2})\s*-\s*(?P<d2>\d{1,2})\s+(?P<mon>[A-Za-z]+)\s*,\s*(?P<y>\d{4})$")
        year_re = re.compile(r"^(?P<y>\d{4})$")
        year_ad_re = re.compile(r"^(?P<y>\d{1,4})\s*AD$", flags=re.IGNORECASE)

        def normalize_one(v: Any) -> Any:
            if v is None or v is pd.NA:
                return pd.NA
            if isinstance(v, float) and pd.isna(v):
                return pd.NA
            text = str(v).strip()
            m = range_re.match(text)
            if m:
                text = f"{int(m.group('d1'))} {m.group('mon')}, {int(m.group('y')):04d}"
            m = year_re.fullmatch(text)
            if m:
                return f"01/01/{int(m.group('y')):04d}"
            m = year_ad_re.fullmatch(text)
            if m:
                return f"01/01/{int(m.group('y')):04d}"
            return text

        def parse_one(v: Any) -> Any:
            if v is None or v is pd.NA:
                return pd.NA
            if isinstance(v, float) and pd.isna(v):
                return pd.NA
            text = normalize_one(v)
            if text is pd.NA:
                return pd.NA
            for fmt in fmt_list:
                try:
                    dt = datetime.strptime(str(text), fmt)
                    return dt.strftime(out_fmt)
                except Exception:
                    continue
            dt = pd.to_datetime(text, errors="coerce")
            if pd.isna(dt):
                return pd.NA
            return pd.Timestamp(dt).strftime(out_fmt)

        out = series.apply(parse_one)
        invalid = (out.isna() & series.notna())
        if errors == "raise" and invalid.any():
            bad = series[invalid].head(5).tolist()
            raise ValueError(f"parse_date_multi failed for values like {bad}")
        if errors == "null":
            return out, invalid
        return out, None
    if op_name == "date_range":
        end_col = args.get("end_col")
        end_value = args.get("end")
        freq = args.get("freq", "D")
        if end_col is None and end_value is None:
            raise ValueError("date_range args require end_col or end")
        if end_col is not None:
            if not isinstance(end_col, str) or not end_col:
                raise ValueError("date_range args.end_col must be non-empty string when provided")
            if end_col not in df.columns:
                raise ValueError(f"date_range end_col not found: {end_col}")
            end_series = df[end_col]
        else:
            end_series = pd.Series(
                [end_value] * len(series), index=series.index)
        if not isinstance(freq, str) or not freq:
            raise ValueError("date_range args.freq must be non-empty string")

        def to_range(start_val: Any, end_val: Any) -> list[pd.Timestamp]:
            start_dt = pd.to_datetime(start_val, errors="coerce")
            end_dt = pd.to_datetime(end_val, errors="coerce")
            if pd.isna(start_dt) or pd.isna(end_dt):
                return []
            return list(pd.date_range(start_dt, end_dt, freq=freq))

        out = [to_range(s, e) for s, e in zip(series, end_series)]
        return pd.Series(out, index=series.index), None
    if op_name == "format_number":
        moving = args.get("moving", False)
        if not isinstance(moving, bool):
            raise ValueError("format_number args.moving must be boolean")

        def format_one(v: Any) -> Any:
            if v is None or v is pd.NA:
                return ""
            if isinstance(v, float) and pd.isna(v):
                return ""
            try:
                f = float(v)
            except Exception:
                return str(v) if v != "" else ""
            if abs(f) < 1e-10:
                return "0"
            if abs(f - round(f)) < 1e-10:
                return str(int(round(f)))
            if moving:
                return f"{f:.9f}".rstrip("0").rstrip(".")
            for prec in [6, 5, 4, 3, 2, 1]:
                s = f"{f:.{prec}f}".rstrip("0").rstrip(".")
                try:
                    if abs(float(s) - f) < 1e-6:
                        return s
                except Exception:
                    continue
            return f"{f:.6f}".rstrip("0").rstrip(".")

        return series.apply(format_one), None
    raise ValueError(f"unsupported map op: {op_name}")


def _apply_regex_extract(df: pd.DataFrame, source_col: str, args: Mapping[str, Any]) -> Optional[pd.Series]:
    pattern = args.get("pattern")
    group = args.get("group", None)
    dtype = args.get("dtype")
    errors = args.get("errors", "null")
    dest = args.get("as")
    flags = args.get("flags", 0)

    if not isinstance(pattern, str) or not pattern:
        raise ValueError("regex_extract args require non-empty {pattern}")
    if errors not in {"null", "raise"}:
        raise ValueError("regex_extract args.errors must be null|raise")
    if dtype is not None and not isinstance(dtype, str):
        raise ValueError(
            "regex_extract args.dtype must be a string when provided")

    re_flags = 0
    if isinstance(flags, int):
        re_flags = flags
    elif isinstance(flags, str):
        name_map = {
            "IGNORECASE": re.IGNORECASE,
            "I": re.IGNORECASE,
            "MULTILINE": re.MULTILINE,
            "M": re.MULTILINE,
            "DOTALL": re.DOTALL,
            "S": re.DOTALL,
        }
        parts = [p.strip() for p in flags.split("|") if p.strip()]
        for p in parts:
            if p not in name_map:
                raise ValueError(f"regex_extract flags has unknown flag: {p}")
            re_flags |= int(name_map[p])
    else:
        raise ValueError(
            "regex_extract args.flags must be int or string when provided")

    s = df[source_col].astype("string")
    extracted = s.str.extract(pattern, flags=re_flags, expand=True)
    if not isinstance(extracted, pd.DataFrame):
        raise ValueError(
            "regex_extract internal error: extract did not return DataFrame")

    group_keys: list[int | str] = []
    if group is None:
        if all(isinstance(c, str) and c for c in extracted.columns):
            group_keys = [str(c) for c in extracted.columns]
        else:
            raise ValueError(
                "regex_extract args.group is required for non-named capture groups")
    elif isinstance(group, (int, str)):
        group_keys = [group]
    elif isinstance(group, list) and group and all(isinstance(x, (int, str)) for x in group):
        group_keys = list(group)
    else:
        raise ValueError(
            "regex_extract args.group must be int|str|list[int|str]")

    if isinstance(dest, str):
        dest_cols = [dest]
    elif isinstance(dest, list):
        dest_cols = dest
    elif dest is None:
        dest_cols = []
    else:
        raise ValueError(
            "regex_extract args.as must be string|list[string] when provided")

    out_cols: list[str] = []
    if dest_cols:
        if len(dest_cols) != len(group_keys):
            raise ValueError(
                "regex_extract args.as length must match args.group length")
        if not all(isinstance(x, str) and x for x in dest_cols):
            raise ValueError(
                "regex_extract args.as must contain non-empty strings")
        out_cols = list(dest_cols)
    else:
        for g in group_keys:
            if isinstance(g, str):
                out_cols.append(g)
            else:
                out_cols.append(str(g))

    invalid_any: Optional[pd.Series] = None
    for g, out_col in zip(group_keys, out_cols):
        if isinstance(g, str):
            if g not in extracted.columns:
                raise ValueError(
                    f"regex_extract pattern has no named group {g!r}")
            raw = extracted[g]
        else:
            idx = int(g) - 1
            if idx < 0 or idx >= extracted.shape[1]:
                raise ValueError(
                    f"regex_extract group index out of range: {g}")
            raw = extracted.iloc[:, idx]

        series: pd.Series = raw.astype("string")
        invalid = (series.isna() & s.notna())

        if dtype is not None:
            casted, cast_invalid = _cast_series(
                series, dtype=dtype, errors=errors)
            df[out_col] = casted.values
            if cast_invalid is not None:
                invalid = invalid | cast_invalid
        else:
            df[out_col] = series.values

        if errors == "raise" and invalid.any():
            bad = df.loc[invalid, source_col].head(5).tolist()
            raise ValueError(f"regex_extract failed for values like {bad}")

        if errors == "null":
            invalid_any = invalid if invalid_any is None else (
                invalid_any | invalid)

    return invalid_any


def _apply_explode(df: pd.DataFrame, col: str, args: Mapping[str, Any]) -> pd.DataFrame:
    pos_col = args.get("pos_col")
    if pos_col is not None and (not isinstance(pos_col, str) or not pos_col):
        raise ValueError(
            "explode args.pos_col must be a non-empty string when provided")

    work = df.copy()

    if pos_col is not None:
        def to_positions(v: Any) -> Any:
            if v is None or v is pd.NA:
                return []
            if isinstance(v, float) and pd.isna(v):
                return []
            if isinstance(v, (list, tuple)):
                return list(range(len(v)))
            return pd.NA

        work[pos_col] = work[col].apply(to_positions)

        invalid = work[pos_col].isna() & work[col].notna()
        if invalid.any():
            bad = work.loc[invalid, col].head(5).tolist()
            raise ValueError(
                f"explode requires list-like values; got values like {bad}")
        work = work.explode([col, pos_col], ignore_index=True)
        return work

    def is_invalid_value(v: Any) -> bool:
        if v is None or v is pd.NA:
            return False
        if isinstance(v, float) and pd.isna(v):
            return False
        if isinstance(v, (list, tuple)):
            return False
        return True

    invalid = work[col].apply(is_invalid_value)
    if invalid.any():
        bad = work.loc[invalid, col].head(5).tolist()
        raise ValueError(
            f"explode requires list-like values; got values like {bad}")
    return work.explode(col, ignore_index=True)


def _apply_expand(df: pd.DataFrame, expand_cfg: Mapping[str, Any], original_df: Optional[pd.DataFrame] = None) -> pd.DataFrame:
    """Expand DataFrame by generating rows for each key group from start to end value.

    Args:
        df: Input DataFrame
        expand_cfg: Configuration dict with:
            - keys: list[str] - grouping keys
            - from_col: str - column name for start value
            - to_col: str (optional) - column name for end value, or
            - to_value: int/str (optional) - fixed end value, or
            - to_value_expr: str (optional) - expression to compute to_value from df
            - expand_col: str - name of the expanded column
            - keep_from_col: bool (default True) - whether to keep from_col in output

    Returns:
        Expanded DataFrame
    """
    keys = expand_cfg.get("keys")
    if not isinstance(keys, list) or not all(isinstance(k, str) and k for k in keys):
        raise ValueError("expand.keys must be a non-empty list of strings")

    from_col = expand_cfg.get("from_col")
    if not isinstance(from_col, str) or not from_col:
        raise ValueError("expand.from_col must be a non-empty string")

    to_col = expand_cfg.get("to_col")
    to_value = expand_cfg.get("to_value")
    to_value_expr = expand_cfg.get("to_value_expr")

    # Validate that exactly one of to_col, to_value, to_value_expr is specified
    specified = sum([to_col is not None, to_value is not None,
                    to_value_expr is not None])
    if specified != 1:
        raise ValueError(
            "expand must specify exactly one of to_col, to_value, or to_value_expr")

    expand_col = expand_cfg.get("expand_col")
    if not isinstance(expand_col, str) or not expand_col:
        raise ValueError("expand.expand_col must be a non-empty string")

    keep_from_col = expand_cfg.get("keep_from_col", True)
    if not isinstance(keep_from_col, bool):
        raise ValueError("expand.keep_from_col must be boolean")

    # Validate columns exist
    missing = [k for k in keys if k not in df.columns]
    if missing:
        raise ValueError(f"expand missing key columns: {missing}")
    if from_col not in df.columns:
        raise ValueError(f"expand missing from_col: {from_col}")
    if to_col is not None and to_col not in df.columns:
        raise ValueError(f"expand missing to_col: {to_col}")

    # Compute to_value if expression is provided
    if to_value_expr is not None:
        from .expr import eval_expr
        try:
            # Use original_df if provided (for accessing other columns), otherwise use current df
            eval_df = original_df if original_df is not None else df
            computed_value = eval_expr(to_value_expr, eval_df)
            if isinstance(computed_value, pd.Series):
                to_value = int(computed_value.iloc[0]) if len(
                    computed_value) > 0 else None
            else:
                to_value = int(computed_value)
        except Exception as exc:
            raise ValueError(f"expand to_value_expr evaluation failed: {exc}")

    # Get unique key combinations with their from/to values
    key_df = df[keys + [from_col] +
                ([to_col] if to_col else [])].drop_duplicates()

    # Generate scaffold rows
    scaffold_list = []
    for _, row in key_df.iterrows():
        key_values = {k: row[k] for k in keys}
        from_val = row[from_col]
        to_val = row[to_col] if to_col else to_value

        # Convert to appropriate numeric type
        try:
            from_int = int(from_val) if pd.notna(from_val) else None
            to_int = int(to_val) if pd.notna(to_val) else None
        except (ValueError, TypeError):
            raise ValueError(
                f"expand from_col and to_col/to_value must be numeric")

        if from_int is None or to_int is None:
            continue

        # Generate rows from from_val to to_val (inclusive)
        for val in range(from_int, to_int + 1):
            new_row = key_values.copy()
            new_row[expand_col] = val
            if keep_from_col:
                new_row[from_col] = from_int
            scaffold_list.append(new_row)

    return pd.DataFrame(scaffold_list)


def _apply_complete_calendar(df: pd.DataFrame, col: str, args: Mapping[str, Any]) -> pd.DataFrame:
    """Fill missing daily dates between min and max of a date column.

    Args:
        df: DataFrame to expand
        col: name of the date column
        args: optional settings {format: str|None, normalize: bool=True, freq: str='D'}
    Returns:
        DataFrame with filler rows for missing dates appended (other columns as NA)
    """
    if col not in df.columns:
        raise ValueError(f"complete_calendar missing column: {col}")

    fmt = args.get("format")
    normalize = args.get("normalize", True)
    freq = args.get("freq", "D")

    s = pd.to_datetime(df[col], format=fmt if isinstance(
        fmt, str) and fmt else None, errors="coerce")
    s = s.dropna()
    if s.empty:
        return df

    start = s.min()
    end = s.max()
    if normalize:
        start = start.normalize()
        end = end.normalize()

    full = pd.date_range(start, end, freq=freq)
    if normalize:
        existing = pd.Index(pd.to_datetime(
            df[col], errors="coerce").dropna().dt.normalize().unique())
    else:
        existing = pd.Index(pd.to_datetime(
            df[col], errors="coerce").dropna().unique())

    missing = full.difference(existing)
    if missing.empty:
        return df

    filler = pd.DataFrame({col: missing})
    return pd.concat([df, filler], ignore_index=True, sort=False)
