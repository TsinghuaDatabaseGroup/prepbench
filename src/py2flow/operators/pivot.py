from __future__ import annotations

from typing import Any, Mapping, List, Callable

import pandas as pd
import numpy as np

from .base import Operator, ExecutionContext


class Pivot(Operator):
    def execute(self, node_id: str, inputs: List[pd.DataFrame], params: Mapping[str, Any], ctx: ExecutionContext) -> pd.DataFrame:
        if len(inputs) != 1:
            raise ValueError("pivot expects exactly 1 input")
        df = inputs[0]
        mode = params.get("mode")
        if mode == "pivot_longer":
            id_cols = params.get("id_cols")
            value_vars = params.get("value_vars")
            names_to = params.get("names_to")
            values_to = params.get("values_to")
            if not isinstance(id_cols, list) or not isinstance(value_vars, list):
                raise ValueError(
                    "pivot_longer requires id_cols/value_vars lists")
            if not isinstance(names_to, str) or not isinstance(values_to, str):
                raise ValueError(
                    "pivot_longer requires names_to/values_to strings")
            return pd.melt(df, id_vars=id_cols, value_vars=value_vars, var_name=names_to, value_name=values_to)

        if mode == "pivot_wider":
            index = params.get("index")
            columns = params.get("columns")
            values = params.get("values")
            if not isinstance(index, list) or not isinstance(columns, list) or not isinstance(values, list):
                raise ValueError(
                    "pivot_wider requires index/columns/values lists")
            agg = params.get("agg")
            fill_value = params.get("fill_value", 0)
            if agg is None:
                aggfunc: Callable[..., Any] | str = "sum"
            else:
                agg_map: dict[str, Callable[..., Any] | str] = {
                    "sum": "sum",
                    "count": "count",
                    "min": "min",
                    "max": "max",
                    "avg": "mean",
                }
                if agg not in agg_map:
                    raise ValueError(
                        "pivot_wider agg must be sum|count|min|max|avg")
                aggfunc = agg_map[agg]
            table = df.pivot_table(
                index=index, columns=columns, values=values, aggfunc=aggfunc, fill_value=fill_value)
            table = table.reset_index()
            if isinstance(table.columns, pd.MultiIndex):
                table.columns = [
                    "_".join(str(p) for p in col if p != "") for col in table.columns]
            else:
                table.columns = [str(c) for c in table.columns]
            return table

        if mode == "pivot_longer_from_rows":
            row_key_pattern = params.get("row_key_pattern")
            column_pattern = params.get("column_pattern")
            names_to = params.get("names_to", "key")
            data_offset = params.get("data_offset", 2)
            drop_contains = params.get("drop_contains", [])
            numeric_fields = params.get("numeric_fields", [])

            if not isinstance(row_key_pattern, list) or not row_key_pattern or not all(isinstance(x, str) and x for x in row_key_pattern):
                raise ValueError(
                    "pivot_longer_from_rows requires non-empty list row_key_pattern")
            if not isinstance(column_pattern, list) or not column_pattern or not all(isinstance(x, str) and x for x in column_pattern):
                raise ValueError(
                    "pivot_longer_from_rows requires non-empty list column_pattern")
            if not isinstance(names_to, str) or not names_to:
                raise ValueError(
                    "pivot_longer_from_rows requires non-empty string names_to")
            if not isinstance(data_offset, int) or data_offset < 0:
                raise ValueError(
                    "pivot_longer_from_rows requires non-negative int data_offset")
            if not (isinstance(drop_contains, list) and all(isinstance(x, str) for x in drop_contains)):
                raise ValueError(
                    "pivot_longer_from_rows drop_contains must be list[str]")
            if not (isinstance(numeric_fields, list) and all(isinstance(x, str) and x for x in numeric_fields)):
                raise ValueError(
                    "pivot_longer_from_rows numeric_fields must be list[str]")

            table = df.fillna("").astype(str).apply(
                lambda col: col.str.strip())
            key_set = set(row_key_pattern)
            marker_rows = table.index[table.apply(
                lambda r: r.isin(key_set).any(), axis=1)]
            if marker_rows.empty:
                return pd.DataFrame(columns=[names_to, *column_pattern])

            blocks: list[pd.DataFrame] = []
            for idx, start in enumerate(marker_rows):
                end = marker_rows[idx + 1] if idx + \
                    1 < len(marker_rows) else len(table)
                marker_row = table.iloc[start]
                data = table.iloc[start + data_offset: end]
                if data.empty:
                    continue
                if drop_contains:
                    data = data[~data.apply(lambda r: any(
                        tok in " ".join(r) for tok in drop_contains), axis=1)]
                data = data[(data != "").any(axis=1)]
                if data.empty:
                    continue

                key_positions = np.where(marker_row.isin(key_set))[0]
                if key_positions.size == 0:
                    continue

                col_indices: list[int] = []
                col_keys: list[str] = []
                col_fields: list[str] = []
                for pos in key_positions:
                    key_val = marker_row.iloc[pos]
                    for offset, field in enumerate(column_pattern):
                        col_idx = pos + offset
                        if col_idx < table.shape[1]:
                            col_indices.append(col_idx)
                            col_keys.append(key_val)
                            col_fields.append(field)
                if not col_indices:
                    continue

                block = data.iloc[:, col_indices].copy()
                block.columns = pd.MultiIndex.from_arrays(
                    [col_keys, col_fields])
                stacked = block.stack(level=0, future_stack=True).reset_index()
                stacked = stacked.rename(
                    columns={"level_0": "row_id", "level_1": names_to})
                blocks.append(stacked[[names_to, *column_pattern]])

            result = pd.concat(blocks, ignore_index=True) if blocks else pd.DataFrame(
                columns=[names_to, *column_pattern])
            for col in numeric_fields:
                if col in result.columns:
                    result = result[result[col].str.isdigit()]
                    result[col] = result[col].astype(int)
            return result

        if mode == "pivot_longer_paired":
            key_row = params.get("key_row")
            pair_size = params.get("pair_size")
            key_col_offset = params.get("key_col_offset", 0)
            value_cols = params.get("value_cols")
            key_col = params.get("key_col", "key")
            skip_empty_keys = params.get("skip_empty_keys", True)
            id_cols = params.get("id_cols")
            skip_cols = params.get("skip_cols", 0)

            if not isinstance(key_row, int) or key_row < 0:
                raise ValueError(
                    "pivot_longer_paired requires non-negative int key_row")
            if not isinstance(pair_size, int) or pair_size < 1:
                raise ValueError(
                    "pivot_longer_paired requires positive int pair_size")
            if not isinstance(key_col_offset, int) or key_col_offset < 0 or key_col_offset >= pair_size:
                raise ValueError(
                    "pivot_longer_paired key_col_offset must be in [0, pair_size)")
            if not isinstance(value_cols, list) or not value_cols or not all(isinstance(x, str) and x for x in value_cols):
                raise ValueError(
                    "pivot_longer_paired requires non-empty list value_cols[str]")
            if len(value_cols) > pair_size - key_col_offset:
                raise ValueError(
                    "pivot_longer_paired value_cols length exceeds available columns in pair")
            if not isinstance(key_col, str) or not key_col:
                raise ValueError(
                    "pivot_longer_paired requires non-empty string key_col")
            if not isinstance(skip_empty_keys, bool):
                raise ValueError(
                    "pivot_longer_paired skip_empty_keys must be boolean")
            if not isinstance(skip_cols, int) or skip_cols < 0:
                raise ValueError(
                    "pivot_longer_paired skip_cols must be a non-negative int")
            if id_cols is not None:
                if not isinstance(id_cols, list) or not all(isinstance(x, str) and x for x in id_cols):
                    raise ValueError(
                        "pivot_longer_paired id_cols must be a list of non-empty strings")
                # Validate that id_cols exist in the dataframe
                missing_cols = [col for col in id_cols if col not in df.columns]
                if missing_cols:
                    raise ValueError(
                        f"pivot_longer_paired id_cols contains missing columns: {missing_cols}")

            if key_row >= len(df):
                raise ValueError(
                    f"pivot_longer_paired key_row {key_row} out of range")

            # Extract keys from key_row
            key_row_data = df.iloc[key_row]
            num_cols = len(df.columns)
            # Calculate number of pairs, accounting for skipped columns
            available_cols = num_cols - skip_cols
            num_pairs = (available_cols + pair_size - 1) // pair_size if available_cols > 0 else 0

            # Extract id columns if specified
            id_data = None
            if id_cols:
                id_data = df.iloc[key_row + 1:, [df.columns.get_loc(col) for col in id_cols]].reset_index(drop=True)

            records = []
            for pair_idx in range(num_pairs):
                # Calculate column index accounting for skipped columns
                key_col_idx = skip_cols + pair_idx * pair_size + key_col_offset
                if key_col_idx >= num_cols:
                    continue

                key_val = key_row_data.iloc[key_col_idx]
                if skip_empty_keys:
                    if pd.isna(key_val) or (isinstance(key_val, str) and not key_val.strip()):
                        continue
                    key_val = str(key_val).strip()
                else:
                    key_val = str(key_val) if not pd.isna(key_val) else ""

                # Extract value columns relative to this paired header key.
                pair_data = {}
                data_length = len(df) - key_row - 1
                for val_idx, val_col_name in enumerate(value_cols):
                    if val_idx == 0:
                        # First value column is in the same column as key
                        val_col_idx = skip_cols + pair_idx * pair_size + key_col_offset
                    else:
                        # Subsequent value columns are offset from key column
                        val_col_idx = skip_cols + pair_idx * pair_size + key_col_offset + val_idx
                    if val_col_idx >= num_cols:
                        pair_data[val_col_name] = pd.Series(
                            [pd.NA] * data_length, dtype=object)
                    else:
                        pair_data[val_col_name] = df.iloc[key_row +
                                                          1:, val_col_idx].reset_index(drop=True).values

                # Create DataFrame for this pair with consistent length
                if data_length <= 0:
                    continue
                pair_df = pd.DataFrame(pair_data)
                pair_df[key_col] = key_val

                # Add id columns if specified
                if id_cols and id_data is not None:
                    # Ensure id_data length matches pair_df length
                    if len(id_data) != len(pair_df):
                        raise ValueError(
                            f"pivot_longer_paired: id_data length ({len(id_data)}) does not match pair data length ({len(pair_df)})")
                    for col in id_cols:
                        pair_df[col] = id_data[col].values

                records.append(pair_df)

            if not records:
                result_cols = [key_col, *value_cols]
                if id_cols:
                    result_cols = [*id_cols, *result_cols]
                return pd.DataFrame(columns=result_cols)

            result = pd.concat(records, ignore_index=True)
            # Reorder columns: id_cols first (if any), then key_col, then value_cols
            result_cols = [key_col, *value_cols]
            if id_cols:
                result_cols = [*id_cols, *result_cols]
            result = result[result_cols]
            return result

        raise ValueError(
            "pivot requires mode pivot_wider|pivot_longer|pivot_longer_from_rows|pivot_longer_paired")
