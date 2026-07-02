from __future__ import annotations

from pathlib import Path
from typing import Dict, List

import math
import pandas as pd


def solve(inputs_dir: Path) -> Dict[str, pd.DataFrame]:
    def parse_budget_table(path: Path) -> pd.DataFrame:
        raw = pd.read_csv(path, header=None)
        rows: List[dict] = []
        for i in range(1, len(raw)):
            cat = str(raw.iloc[i, 0]).strip()
            if not cat or cat == 'nan':
                continue
            amount_cell = str(raw.iloc[i, 1]).strip() if raw.shape[1] > 1 else ''
            num_str = ''.join(ch for ch in amount_cell if (ch.isdigit()))
            if not num_str:
                continue
            annual = float(num_str)
            rows.append({"Category": cat, "AnnualBudget": annual})
        return pd.DataFrame(rows)

    def month_name_with_typo(dt: pd.Timestamp) -> str:
        m = dt.month
        names = {
            1: "January",
            2: "February",
            3: "March",
            4: "April",
            5: "May",
            6: "June",
            7: "July",
            8: "August",
            9: "Sepetember",
            10: "October",
            11: "November",
            12: "December",
        }
        return names[m]

    def load_monthly_actuals(indir: Path) -> pd.DataFrame:
        frames: List[pd.DataFrame] = []
        for csv_path in sorted(indir.glob("input_*.csv")):
            if csv_path.name == "input_01.csv":
                continue
            df = pd.read_csv(csv_path)
            if df.columns[0].startswith("Unnamed"):
                df = df.drop(columns=[df.columns[0]])
            date_col = df.columns[0]
            row = df.iloc[0].to_dict()
            row["__date"] = pd.to_datetime(date_col)
            rename_map = {"TransactionFees": "Transaction Fees"}
            normalized = {rename_map.get(k, k): v for k, v in row.items() if k != date_col}
            normalized["__date"] = pd.to_datetime(date_col)
            frames.append(pd.DataFrame([normalized]))
        monthly = pd.concat(frames, ignore_index=True)
        return monthly

    df_budget = parse_budget_table(inputs_dir / "input_01.csv")
    df_budget["MonthlyBudget"] = (df_budget["AnnualBudget"] / 12.0).round().astype(int)

    df_monthly = load_monthly_actuals(inputs_dir)
    keep_cols = [c for c in df_monthly.columns if c in set(df_budget["Category"]) or c == "__date"]
    df_monthly = df_monthly[keep_cols]

    long_actual = df_monthly.melt(id_vars=["__date"], var_name="Category", value_name="Actual Spending")
    annual_actual = long_actual.groupby("Category", as_index=False)["Actual Spending"].sum().rename(columns={"Actual Spending": "AnnualActual"})

    df_above = annual_actual.merge(df_budget, on="Category", how="inner")
    df_above = df_above[df_above["AnnualActual"] > df_above["AnnualBudget"]]
    above_categories = set(df_above["Category"].unique())

    long_actual = long_actual[long_actual["Category"].isin(above_categories)].copy()
    monthly_budget_map = dict(zip(df_budget["Category"], df_budget["MonthlyBudget"]))
    long_actual["Budget"] = long_actual["Category"].map(monthly_budget_map)
    long_actual["Actual Spending"] = long_actual["Actual Spending"].round().astype(int)
    long_actual["Difference"] = long_actual["Actual Spending"] - long_actual["Budget"]
    long_actual["Month"] = long_actual["__date"].apply(month_name_with_typo)

    idx = long_actual.groupby("Month")["Difference"].idxmax()
    result = long_actual.loc[idx, ["Month", "Category", "Actual Spending", "Budget", "Difference"]].copy()

    result = result.astype({
        "Month": str,
        "Category": str,
        "Actual Spending": int,
        "Budget": int,
        "Difference": int,
    })

    return {"output_01.csv": result}


if __name__ == "__main__":
    task_dir = Path(__file__).parent
    inputs = task_dir / "inputs"
    cand_dir = task_dir / "cand"
    cand_dir.mkdir(parents=True, exist_ok=True)

    outputs = solve(inputs)
    for fname, df in outputs.items():
        (cand_dir / fname).parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(cand_dir / fname, index=False)


