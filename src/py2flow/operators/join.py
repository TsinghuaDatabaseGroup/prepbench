from __future__ import annotations

from typing import Any, Mapping, List, Dict, Optional, Tuple, Set
from uuid import uuid4

import pandas as pd

from py2flow.errors import FlowExecutionError, FlowValidationError
from py2flow.ir import StepKind
from .base import Operator, ExecutionContext


class Join(Operator):
    def execute(self, node_id: str, inputs: List[pd.DataFrame], params: Mapping[str, Any], ctx: ExecutionContext) -> pd.DataFrame:
        if len(inputs) != 2:
            raise ValueError("join expects exactly 2 inputs")
        left_df, right_df = inputs

        how = params.get("how", "inner")
        if how not in {"inner", "left", "right", "full", "semi", "anti"}:
            raise ValueError("join how must be inner|left|right|full|semi|anti")

        on = _normalize_keys(params.get("on"))
        left_on = _normalize_keys(params.get("left_on"))
        right_on = _normalize_keys(params.get("right_on"))
        if on is not None and (left_on is not None or right_on is not None):
            raise ValueError("join cannot specify both on and left_on/right_on")
        if on is None:
            if left_on is None or right_on is None or len(left_on) != len(right_on):
                raise ValueError("join requires on or left_on/right_on with same length")

        null_equal = bool(params.get("null_equal", False))
        suffixes = params.get("suffixes", ["_x", "_y"])
        if not isinstance(suffixes, list) or len(suffixes) != 2:
            raise ValueError("join suffixes must be [left_suffix, right_suffix]")
        suffixes_t = (str(suffixes[0]), str(suffixes[1]))

        select_left = params.get("select_left")
        select_right = params.get("select_right")

        left_keys = on if on is not None else left_on
        right_keys = on if on is not None else right_on
        if left_keys is None or right_keys is None:
            raise ValueError("join missing keys")

        fuzzy_match = params.get("fuzzy_match", False)
        if not isinstance(fuzzy_match, bool):
            raise ValueError("join params.fuzzy_match must be boolean")
        if fuzzy_match:
            if len(left_keys) != 1 or len(right_keys) != 1:
                raise ValueError("join fuzzy_match requires single key on each side")
            if how not in {"left", "inner"}:
                raise ValueError("join fuzzy_match only supports left or inner join")
            # Perform fuzzy substring matching
            left_key = left_keys[0]
            right_key = right_keys[0]
            left2 = left_df.copy()
            right2 = right_df.copy()
            # Prefer the most specific containing string; ties keep right-row order.
            matched = []
            for idx, left_row in left2.iterrows():
                left_val = str(left_row[left_key]).strip().lower() if pd.notna(left_row[left_key]) else ""
                if not left_val:
                    matched.append(None)
                    continue
                best_match = None
                best_score: tuple[int, int] | None = None
                for pos, (right_idx, right_row) in enumerate(right2.iterrows()):
                    right_val = str(right_row[right_key]).strip().lower() if pd.notna(right_row[right_key]) else ""
                    if left_val not in right_val:
                        continue
                    score = (len(right_val), pos)
                    if best_score is None or score < best_score:
                        # Store the positional offset (not the index label) so the
                        # later .iloc lookup is correct even when right2 carries a
                        # non-default index (e.g. after an upstream filter/join/sort).
                        best_match = pos
                        best_score = score
                matched.append(best_match)
            # Create result by joining matched rows
            result_rows = []
            for left_idx, right_idx in enumerate(matched):
                left_row = left2.iloc[left_idx].to_dict()
                if right_idx is not None:
                    right_row = right2.iloc[right_idx].to_dict()
                    # Merge: right values override left values for same keys
                    merged_row = {**left_row, **right_row}
                else:
                    if how == "inner":
                        continue
                    merged_row = left_row.copy()
                    for col in right2.columns:
                        if col not in merged_row:
                            merged_row[col] = pd.NA
                result_rows.append(merged_row)
            if result_rows:
                result_df = pd.DataFrame(result_rows)
            else:
                result_cols = list(left2.columns) + [c for c in right2.columns if c not in left2.columns]
                result_df = pd.DataFrame(columns=result_cols)
            if select_left is not None or select_right is not None:
                left_sel = _expand_select(select_left, left_df.columns)
                right_sel = _expand_select(select_right, right_df.columns)
                # Remove duplicates: if a column appears in both, keep it only once (right takes precedence in merge)
                all_cols = []
                seen = set()
                for c in left_sel:
                    if c not in seen:
                        all_cols.append(c)
                        seen.add(c)
                for c in right_sel:
                    if c not in seen:
                        all_cols.append(c)
                        seen.add(c)
                result_df = result_df[[c for c in all_cols if c in result_df.columns]]
            return result_df

        validate_cfg = params.get("validate")
        validate_tag: Optional[Tuple[str, str, Set[Tuple[Any, ...]], Set[Tuple[Any, ...]]]] = None
        if isinstance(validate_cfg, Mapping):
            mode = validate_cfg.get("mode")
            on_fail = validate_cfg.get("on_fail", "error")
            error_col = str(validate_cfg.get("error_col", "_join_error"))
            left_viol, right_viol, violates = _check_join_validate(left_df, right_df, left_keys, right_keys, mode)
            if violates and on_fail == "error":
                raise FlowValidationError(
                    f"join.validate failed mode={mode} (left_dup={bool(left_viol)} right_dup={bool(right_viol)})",
                    node_id=node_id,
                    step_kind=StepKind.JOIN,
                    error_code="join_validate_failed",
                )
            if on_fail == "tag":
                validate_tag = (error_col, f"join_validate_failed:{mode}", left_viol, right_viol)

        if how in {"semi", "anti"}:
            return _semi_anti(
                left_df,
                right_df,
                left_keys=left_keys,
                right_keys=right_keys,
                null_equal=null_equal,
                how=how,
            )

        left2, right2, sentinels = _apply_null_inequality(left_df, right_df, left_keys, right_keys, null_equal, node_id)

        merge_kwargs: Dict[str, Any] = {"how": "outer" if how == "full" else how, "suffixes": suffixes_t}
        if on is not None:
            merge_kwargs["on"] = left_keys
        else:
            merge_kwargs["left_on"] = left_keys
            merge_kwargs["right_on"] = right_keys
        merged = left2.merge(right2, **merge_kwargs)
        merged = _restore_nulls(merged, left_keys, right_keys, sentinels)
        if validate_tag is not None:
            error_col, marker, left_viol, right_viol = validate_tag
            merged[error_col] = pd.NA
            mask = pd.Series([False] * len(merged), index=merged.index)
            if left_viol and all(k in merged.columns for k in left_keys):
                mask = mask | pd.MultiIndex.from_frame(merged[left_keys]).isin(left_viol)
            if right_viol and all(k in merged.columns for k in right_keys):
                mask = mask | pd.MultiIndex.from_frame(merged[right_keys]).isin(right_viol)
            merged.loc[mask.values, error_col] = marker

        out_cols = _select_merge_columns(
            merged,
            left_df=left_df,
            right_df=right_df,
            left_keys=left_keys,
            right_keys=right_keys,
            on_keys=on,
            select_left=select_left,
            select_right=select_right,
            suffixes=suffixes_t,
        )
        if validate_tag is not None:
            error_col = validate_tag[0]
            if error_col not in out_cols:
                out_cols.append(error_col)
        return merged[out_cols].copy()


def _normalize_keys(value: Any) -> Optional[List[str]]:
    if value is None:
        return None
    if isinstance(value, str):
        return [value]
    if isinstance(value, list) and all(isinstance(x, str) and x for x in value):
        return list(value)
    raise ValueError("join key must be string or list[str]")


def _apply_null_inequality(
    left: pd.DataFrame,
    right: pd.DataFrame,
    left_keys: List[str],
    right_keys: List[str],
    null_equal: bool,
    node_id: str,
) -> tuple[pd.DataFrame, pd.DataFrame, List[Tuple[str, str]]]:
    if null_equal:
        return left.copy(), right.copy(), []
    left2 = left.copy()
    right2 = right.copy()
    sentinels: List[Tuple[str, str]] = []
    token = uuid4().hex
    for idx, (lk, rk) in enumerate(zip(left_keys, right_keys)):
        s_l = _make_null_sentinel("L", token, node_id, idx)
        s_r = _make_null_sentinel("R", token, node_id, idx)
        left2[lk] = left2[lk].where(left2[lk].notna(), s_l)
        right2[rk] = right2[rk].where(right2[rk].notna(), s_r)
        sentinels.append((s_l, s_r))
    return left2, right2, sentinels


def _make_null_sentinel(side: str, token: str, node_id: str, idx: int) -> str:
    if side not in {"L", "R"}:
        raise ValueError("side must be L or R")
    # Long, per-call random token; left/right are different by design.
    return f"__PY2FLOW_NULL_{side}__{token}__{node_id}__{idx}__"


def _restore_nulls(
    merged: pd.DataFrame,
    left_keys: List[str],
    right_keys: List[str],
    sentinels: List[Tuple[str, str]],
) -> pd.DataFrame:
    if not sentinels:
        return merged
    for (s_l, s_r), lk, rk in zip(sentinels, left_keys, right_keys):
        if lk in merged.columns:
            merged[lk] = merged[lk].replace({s_l: pd.NA, s_r: pd.NA})
        if rk in merged.columns and rk != lk:
            merged[rk] = merged[rk].replace({s_l: pd.NA, s_r: pd.NA})
    return merged


def _expand_select(select: Any, columns: pd.Index) -> List[str]:
    if select is None:
        return [str(c) for c in columns]
    if not isinstance(select, list) or not all(isinstance(x, str) and x for x in select):
        raise ValueError("select must be list[str]")
    out: List[str] = []
    for item in select:
        if item == "*":
            out.extend([str(c) for c in columns])
        else:
            out.append(item)
    return out


def _select_merge_columns(
    merged: pd.DataFrame,
    left_df: pd.DataFrame,
    right_df: pd.DataFrame,
    left_keys: List[str],
    right_keys: List[str],
    on_keys: Optional[List[str]],
    select_left: Any,
    select_right: Any,
    suffixes: Tuple[str, str],
) -> List[str]:
    left_sel = _expand_select(select_left, left_df.columns)
    right_sel = _expand_select(select_right, right_df.columns)

    # "Shared" join keys should not be suffixed and should appear only once in the merged output.
    # When `on` is used, pandas produces a single key column with that name.
    # When `left_on`/`right_on` is used, and a key pair has the same name (lk == rk),
    # pandas still produces a single key column (unsuffixed). Treat these as shared too.
    shared_on = set(on_keys or [])
    if on_keys is None:
        for lk, rk in zip(left_keys, right_keys):
            if lk == rk:
                shared_on.add(lk)
    cols: List[str] = []
    for col in left_sel:
        if col not in left_df.columns:
            raise ValueError(f"select_left references missing column: {col}")
        out_name = col + suffixes[0] if (col in right_df.columns and col not in shared_on) else col
        cols.append(out_name)
    for col in right_sel:
        if col not in right_df.columns:
            raise ValueError(f"select_right references missing column: {col}")
        if col in shared_on:
            out_name = col
        else:
            out_name = col + suffixes[1] if (col in left_df.columns and col not in shared_on) else col
        cols.append(out_name)

    deduped: List[str] = []
    for c in cols:
        if c not in deduped:
            deduped.append(c)
    missing = [c for c in deduped if c not in merged.columns]
    if missing:
        raise ValueError(f"join produced no column(s): {missing}")
    return deduped


def _semi_anti(
    left: pd.DataFrame,
    right: pd.DataFrame,
    left_keys: List[str],
    right_keys: List[str],
    null_equal: bool,
    how: str,
) -> pd.DataFrame:
    left2, right2, _ = _apply_null_inequality(left, right, left_keys, right_keys, null_equal, node_id="semi_anti")
    right_keys_df = right2[right_keys].drop_duplicates()
    if left_keys != right_keys:
        right_keys_df = right_keys_df.rename(columns={rk: lk for lk, rk in zip(left_keys, right_keys)})
    marker = left2.merge(right_keys_df, how="left", on=left_keys, indicator=True)["_merge"]
    if how == "semi":
        mask = marker == "both"
    else:
        mask = marker == "left_only"
    return left.loc[mask.values].copy()



def _duplicated_key_tuples(df: pd.DataFrame, keys: List[str]) -> Set[Tuple[Any, ...]]:
    key_df = df[keys]
    non_null = key_df.notna().all(axis=1)
    if not bool(non_null.any()):
        return set()
    tmp = key_df[non_null]
    dup_mask = tmp.duplicated(subset=keys, keep=False)
    if not bool(dup_mask.any()):
        return set()
    return set(pd.MultiIndex.from_frame(tmp[dup_mask]).tolist())


def _check_join_validate(
    left: pd.DataFrame,
    right: pd.DataFrame,
    left_keys: List[str],
    right_keys: List[str],
    mode: Any,
) -> Tuple[Set[Tuple[Any, ...]], Set[Tuple[Any, ...]], bool]:
    if mode not in {"1:1", "1:m", "m:1", "m:m"}:
        raise ValueError("join.validate.mode must be 1:1|1:m|m:1|m:m")

    left_viol = _duplicated_key_tuples(left, left_keys)
    right_viol = _duplicated_key_tuples(right, right_keys)

    violates = False
    if mode == "1:1":
        violates = bool(left_viol) or bool(right_viol)
    elif mode == "1:m":
        violates = bool(left_viol)
    elif mode == "m:1":
        violates = bool(right_viol)

    return left_viol, right_viol, violates
