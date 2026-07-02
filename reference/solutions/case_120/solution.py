from __future__ import annotations
from pathlib import Path
from typing import Dict
import pandas as pd
import re


def solve(inputs_dir: Path) -> Dict[str, pd.DataFrame]:
    files = sorted(inputs_dir.glob('input_*.csv'))
    dfs = []
    for f in files:
        m = re.search(r"input_(\d+)\.csv$", f.name)
        if not m:
            continue
        month = int(m.group(1))
        df = pd.read_csv(f)
        df["__month"] = month
        dfs.append(df)

    if not dfs:
        return {"output_01.csv": pd.DataFrame(columns=[
            "New Trolley Inventory?",
            "Variance Rank by Destination",
            "Variance",
            "Avg Price per Product",
            "Date",
            "Product",
            "first_name",
            "last_name",
            "email",
            "Price",
            "Destination",
        ])}

    df_all = pd.concat(dfs, ignore_index=True)

    for col in df_all.select_dtypes(include=['object']).columns:
        df_all[col] = df_all[col].astype(str).str.strip()

    df_all["Day of Month"] = pd.to_numeric(
        df_all["Day of Month"], errors="coerce").astype("Int64")
    df_all["Date"] = pd.to_datetime({
        'year': 2021,
        'month': df_all["__month"],
        'day': df_all["Day of Month"].astype('int')
    }, errors='coerce')

    cutoff = pd.Timestamp('2021-06-01')
    df_all["New Trolley Inventory?"] = df_all["Date"] >= cutoff

    def clean_product(x: str) -> str:
        if not isinstance(x, str):
            x = str(x)
        parts = x.split('-', 1)
        return parts[0].strip() if len(parts) > 1 else x.strip()

    df_all["Product_clean"] = df_all["Product"].apply(clean_product)

    def parse_price(x):
        if pd.isna(x):
            return pd.NA
        s = str(x).strip().replace(',', '')
        if s.startswith('$'):
            s = s[1:]
        try:
            return float(s)
        except Exception:
            return pd.NA

    df_all["Price_num"] = df_all["Price"].apply(parse_price).astype(float)

    avg_price = df_all.groupby("Product_clean", dropna=False)[
        "Price_num"].mean().rename("Avg Price per Product")
    avg_price = avg_price.round(9)
    df_all = df_all.join(avg_price, on="Product_clean")

    df_all["Variance"] = (df_all["Price_num"] -
                          df_all["Avg Price per Product"]).round(9)

    df_all["Variance Rank by Destination"] = (
        df_all.groupby(["Destination", "New Trolley Inventory?"])["Variance"]
        .rank(method="first", ascending=False)
        .astype(int)
    )

    df_top = df_all[df_all["Variance Rank by Destination"] <= 5].copy()

    out_cols = [
        "New Trolley Inventory?",
        "Variance Rank by Destination",
        "Variance",
        "Avg Price per Product",
        "Date",
        "Product",
        "first_name",
        "last_name",
        "email",
        "Price",
        "Destination",
    ]

    out_df = pd.DataFrame()
    out_df["New Trolley Inventory?"] = df_top["New Trolley Inventory?"].astype(
        bool)
    out_df["Variance Rank by Destination"] = df_top["Variance Rank by Destination"].astype(
        int)
    out_df["Variance"] = df_top["Variance"].astype(float)
    out_df["Avg Price per Product"] = df_top["Avg Price per Product"].astype(
        float)
    out_df["Date"] = df_top["Date"].dt.strftime("%d/%m/%Y")
    out_df["Product"] = df_top["Product_clean"]
    out_df["first_name"] = df_top["first_name"]
    out_df["last_name"] = df_top["last_name"]
    out_df["email"] = df_top["email"]
    out_df["Price"] = df_top["Price_num"].astype(float)
    out_df["Destination"] = df_top["Destination"]

    out_df = out_df.sort_values(by=["Destination", "New Trolley Inventory?",
                                "Variance Rank by Destination", "Date", "Product"], ascending=[True, True, True, True, True])

    return {"output_01.csv": out_df[out_cols]}


if __name__ == "__main__":
    import sys
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    cand_dir = task_dir / "cand"
    cand_dir.mkdir(parents=True, exist_ok=True)

    outputs = solve(inputs_dir)
    for fname, df in outputs.items():
        (cand_dir / fname).parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(cand_dir / fname, index=False, encoding="utf-8")
    for fname in outputs.keys():
        print(str(cand_dir / fname))
