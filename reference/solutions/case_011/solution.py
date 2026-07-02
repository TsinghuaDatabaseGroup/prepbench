from __future__ import annotations
from pathlib import Path
import pandas as pd
from typing import Dict


def solve(inputs_dir: Path) -> dict[str, pd.DataFrame]:
    in_file = inputs_dir / "input_01.csv"
    df = pd.read_csv(in_file, dtype=str)

    records: list[dict] = []

    for _, row in df.iterrows():
        name = str(row["JSON_Name"]) if pd.notna(row["JSON_Name"]) else ""
        val = row["JSON_ValueString"]
        if not name:
            continue
        parts = name.split(".")
        if "meta" in parts:
            continue
        try:
            idx = int(parts[-1])
        except Exception:
            continue

        dtype: str | None = None
        if "timestamp" in parts:
            dtype = "timestamp"
        elif "indicators" in parts:
            if "quote" in parts:
                for m in ["open", "high", "low", "close", "volume"]:
                    if m in parts:
                        dtype = m
                        break
            elif "adjclose" in parts:
                if "adjclose" in parts:
                    dtype = "adjclose"
        if dtype is None:
            continue

        records.append({"Row": idx, "DataType": dtype, "Value": val})

    if not records:
        out = pd.DataFrame(columns=["Date", "volume", "high", "low", "adjclose", "close", "open", "Row"])
        return {"output_01.csv": out}

    tidy = pd.DataFrame.from_records(records)

    def to_num(x):
        try:
            return pd.to_numeric(x)
        except Exception:
            return pd.NA

    tidy["Value"] = tidy.apply(lambda r: int(r["Value"]) if r["DataType"] == "timestamp" else to_num(r["Value"]), axis=1)

    wide = tidy.pivot_table(index="Row", columns="DataType", values="Value", aggfunc="first").reset_index()

    if "timestamp" in wide.columns:
        ts = pd.to_datetime(wide["timestamp"], unit="s")
        date_str = ts.dt.strftime("%d/%m/%Y %H:%M:%S")
    else:
        date_str = pd.Series([None] * len(wide))

    for col in ["volume", "high", "low", "adjclose", "close", "open"]:
        if col not in wide.columns:
            wide[col] = pd.NA

    wide["Date"] = date_str

    out_df = wide[["Date", "volume", "high", "low", "adjclose", "close", "open", "Row"]].copy()

    for c in ["high", "low", "adjclose", "close", "open"]:
        out_df[c] = pd.to_numeric(out_df[c], errors="coerce")
    
    out_df["volume"] = pd.to_numeric(out_df["volume"], errors="coerce").astype("Int64")
    out_df["Row"] = pd.to_numeric(out_df["Row"], errors="coerce").astype("Int64")

    return {"output_01.csv": out_df}


if __name__ == "__main__":
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    cand_dir = task_dir / "cand"
    cand_dir.mkdir(parents=True, exist_ok=True)

    outputs = solve(inputs_dir)
    for fname, df in outputs.items():
        (cand_dir / fname).parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(cand_dir / fname, index=False, encoding="utf-8", float_format='%.9f')

