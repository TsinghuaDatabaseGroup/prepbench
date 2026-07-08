from __future__ import annotations

from pathlib import Path
from typing import Dict

import math
import pandas as pd


def solve(inputs_dir: Path) -> Dict[str, pd.DataFrame]:
    def _parse_number(text: str) -> float:
        if text is None:
            return math.nan
        s = str(text).strip()
        if s == "" or s.lower() in {"nan", "none"}:
            return math.nan
        s = s.replace(",", "").strip()
        if s.lower().endswith("k"):
            base = s[:-1]
            if base == "":
                return math.nan
            return float(base) * 1000.0
        return float(s)

    def _normalize_category(cat: str) -> str:
        if isinstance(cat, float) and math.isnan(cat):
            c = ""
        else:
            c = str(cat or "").strip()
        if c.replace(" ", "").lower() == "transactionfees":
            return "Transportation Fees"
        if c.lower() == "transaction fees":
            return "Transportation Fees"
        return c
    actual_path = inputs_dir / "input_01.csv"
    df_act_raw = pd.read_csv(actual_path, header=None, names=["Category", "Actual"], dtype=str)
    df_act_raw = df_act_raw[df_act_raw["Category"].astype(str).str.strip() != "2022"]
    df_act_raw["Category"] = df_act_raw["Category"].map(_normalize_category)
    df_act_raw["Actual Spending"] = df_act_raw["Actual"].map(_parse_number)
    df_act = df_act_raw[["Category", "Actual Spending"]].dropna(subset=["Category"]).reset_index(drop=True)

    budget_path = inputs_dir / "input_02.csv"
    df_bud_raw = pd.read_csv(budget_path, dtype=str)
    df_bud_raw = df_bud_raw.rename(columns={df_bud_raw.columns[0]: "Category", df_bud_raw.columns[1]: "Budget", df_bud_raw.columns[2]: "Notes"})
    df_bud_raw = df_bud_raw[df_bud_raw["Category"].astype(str).str.strip() != ""]
    df_bud_raw = df_bud_raw[df_bud_raw["Category"].astype(str).str.strip() != "2022"]
    df_bud_raw["Category"] = df_bud_raw["Category"].map(_normalize_category)
    df_bud_raw["Forecasted Spending"] = df_bud_raw["Budget"].map(_parse_number)
    df_bud = df_bud_raw[["Category", "Forecasted Spending"]].reset_index(drop=True)

    df = pd.merge(df_bud, df_act, on="Category", how="inner")

    diff = (df["Actual Spending"] - df["Forecasted Spending"]).round(0)
    df["Difference"] = diff.astype(float)

    df_out = df[["Category", "Forecasted Spending", "Actual Spending", "Difference"]].copy()

    return {"output_01.csv": df_out}


if __name__ == "__main__":
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    cand_dir = task_dir / "cand"
    cand_dir.mkdir(parents=True, exist_ok=True)

    outputs = solve(inputs_dir)
    for filename, data in outputs.items():
        out_path = cand_dir / filename
        data.to_csv(out_path, index=False, encoding="utf-8")


