from __future__ import annotations

from pathlib import Path
from typing import Dict

import pandas as pd


def solve(inputs_dir: Path) -> Dict[str, pd.DataFrame]:
    def _strip_series(s: pd.Series) -> pd.Series:
        if pd.api.types.is_string_dtype(s):
            return s.astype(str).str.strip()
        return s

    def _normalize_text_columns(df: pd.DataFrame, cols: list[str]) -> pd.DataFrame:
        for c in cols:
            if c in df.columns:
                df[c] = _strip_series(df[c])
        return df

    recall_path = inputs_dir / "input_01.csv"
    store_path = inputs_dir / "input_02.csv"

    recall = pd.read_csv(recall_path)
    store = pd.read_csv(store_path)

    recall = _normalize_text_columns(recall, ["Category", "Product ID"])
    store = _normalize_text_columns(store, ["City", "Store", "Category", "Product ID"])

    recall["Unit Price"] = pd.to_numeric(recall["Unit Price"], errors="coerce")
    store["Unit Price"] = pd.to_numeric(store["Unit Price"], errors="coerce")
    store["Quantity"] = pd.to_numeric(store["Quantity"], errors="coerce")

    recalled = store.merge(
        recall[["Category", "Product ID", "Unit Price"]].rename(columns={"Unit Price": "Unit Price Recall"}),
        on=["Category", "Product ID"],
        how="inner",
    )

    recalled["Lost Amount"] = recalled["Unit Price"] * recalled["Quantity"]

    out1 = (
        recalled.groupby("Category", as_index=False)["Lost Amount"].sum()
        .rename(columns={"Lost Amount": "Total Price Rounded"})
    )
    out1["Total Price Rounded"] = out1["Total Price Rounded"].round(2)

    out2 = (
        recalled.groupby("Store", as_index=False)["Lost Amount"].sum()
        .rename(columns={"Lost Amount": "Total Price Rounded"})
    )
    out2["Total Price Rounded"] = out2["Total Price Rounded"].round(2)
    out2["Issue Level"] = out2["Total Price Rounded"].apply(lambda v: "High Priority" if v >= 5000 else "Low Priority")

    return {
        "output_01.csv": out1[["Category", "Total Price Rounded"]],
        "output_02.csv": out2[["Store", "Total Price Rounded", "Issue Level"]],
    }


if __name__ == "__main__":
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    cand_dir = task_dir / "cand"
    cand_dir.mkdir(parents=True, exist_ok=True)

    outputs = solve(inputs_dir)
    for filename, df in outputs.items():
        df.to_csv(cand_dir / filename, index=False, encoding="utf-8")


