from __future__ import annotations
from pathlib import Path
import pandas as pd
import numpy as np
import re


def solve(inputs_dir: Path) -> dict[str, pd.DataFrame]:
    all_rows = []
    pattern = re.compile(r"input_(\d{2})\.csv$")

    if inputs_dir.exists():
        for fp in sorted(inputs_dir.glob("input_*.csv")):
            m = pattern.search(fp.name)
            if not m:
                continue
            month_num = int(m.group(1))
            df = pd.read_csv(fp, dtype=str)
            needed = ["Scent", "Product Type", "Return"]
            for col in needed:
                if col not in df.columns:
                    df[col] = pd.Series([None] * len(df))
            df = df[needed].copy()
            df["Month"] = month_num
            all_rows.append(df)

    data = pd.concat(all_rows, ignore_index=True) if all_rows else pd.DataFrame(columns=["Scent", "Product Type", "Return", "Month"]) 

    for c in ["Scent", "Product Type", "Return"]:
        if c in data.columns:
            data[c] = data[c].astype(str).str.strip()
    ret_map = {"true": True, "false": False, "True": True, "False": False}
    data["is_return"] = data["Return"].map(ret_map)
    data["is_return"] = data["is_return"].fillna(False)

    fruit_scents = set(["Apricot", "Raspberry", "Pineapple", "Lemon", "Lime"])
    data["FruitFlag"] = np.where(data["Scent"].isin(fruit_scents), "Fruit", "Non-Fruit")

    def agg_counts(df: pd.DataFrame, type_values: pd.Series) -> pd.DataFrame:
        temp = pd.DataFrame({
            "Type": type_values,
            "Returned Orders": df["is_return"].astype(bool).astype(int),
            "Total Orders": 1,
        })
        grouped = temp.groupby("Type", as_index=False).agg({
            "Returned Orders": "sum",
            "Total Orders": "sum",
        })
        grouped["% Returned"] = (grouped["Returned Orders"] / grouped["Total Orders"] * 100).round(1)
        grouped = grouped[["Returned Orders", "Total Orders", "% Returned", "Type"]]
        return grouped

    by_prod = agg_counts(data, data["Product Type"])

    all_row = agg_counts(data, pd.Series(["All"] * len(data), index=data.index))
    all_row = all_row.groupby("Type", as_index=False).sum(numeric_only=True)
    all_row["% Returned"] = (all_row["Returned Orders"] / all_row["Total Orders"] * 100).round(1)
    all_row = all_row[["Returned Orders", "Total Orders", "% Returned", "Type"]]

    by_fruit = agg_counts(data, data["FruitFlag"])

    by_month = agg_counts(data, data["Month"].map(lambda m: f"2019-{int(m):02d}-01"))

    order_types = ["Bar", "Massage Bar", "Bath Bomb", "Liquid"]
    by_prod = by_prod.set_index("Type").loc[order_types].reset_index()

    order_mid = ["All", "Non-Fruit", "Fruit"]
    mid = pd.concat([
        all_row,
        by_fruit.set_index("Type").loc[["Non-Fruit", "Fruit"]].reset_index(),
    ], ignore_index=True)

    month_order = [
        "2019-05-01",
        "2019-04-01",
        "2019-03-01",
        "2019-02-01",
        "2019-01-01",
        "2019-06-01",
    ]
    by_month = by_month.set_index("Type").loc[month_order].reset_index()

    out = pd.concat([by_prod, mid, by_month], ignore_index=True)

    for c in ["Returned Orders", "Total Orders"]:
        out[c] = pd.to_numeric(out[c], downcast="integer")
    out["% Returned"] = pd.to_numeric(out["% Returned"])
    out["Type"] = out["Type"].astype(str)

    return {"output_01.csv": out}


if __name__ == "__main__":
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    cand_dir = task_dir / "cand"
    cand_dir.mkdir(parents=True, exist_ok=True)
    outputs = solve(inputs_dir)
    for fname, df in outputs.items():
        (cand_dir / fname).parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(cand_dir / fname, index=False, encoding="utf-8")

