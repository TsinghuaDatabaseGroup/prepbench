from __future__ import annotations
from pathlib import Path
import pandas as pd


def _read_weekly_sales(inputs_dir: Path) -> pd.DataFrame:
    sales_files = []
    for p in sorted((inputs_dir).glob("input_*.csv")):
        if p.name == "input_04.csv":
            continue
        try:
            df = pd.read_csv(p)
        except Exception:
            continue
        cols = set(df.columns.str.strip())
        if {"Date", "Type"}.issubset(cols) and (({"Sales Volume", "Sales Value"}.issubset(cols)) or ({"Volume", "Value"}.issubset(cols))):
            sales_files.append(p)

    if not sales_files:
        return pd.DataFrame(columns=["Type", "Week", "Sales Volume", "Sales Value"])

    frames = []
    for p in sales_files:
        df = pd.read_csv(p)
        if {"Sales Volume", "Sales Value"}.issubset(set(df.columns)):
            df = df[["Date", "Type", "Sales Volume", "Sales Value"]].copy()
        else:
            df = df[["Date", "Type", "Volume", "Value"]].copy()
            df = df.rename(
                columns={"Volume": "Sales Volume", "Value": "Sales Value"})
        df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
        df = df.dropna(subset=["Date"])
        df["Week"] = df["Date"].dt.isocalendar().week.astype(int)
        df["Type"] = df["Type"].str.strip().str.lower()
        frames.append(df)

    sales = pd.concat(frames, ignore_index=True)
    weekly = (
        sales.groupby(["Type", "Week"], as_index=False)
        .agg({"Sales Volume": "sum", "Sales Value": "sum"})
    )
    return weekly[["Type", "Week", "Sales Volume", "Sales Value"]]


def _read_profit_min(inputs_dir: Path) -> pd.DataFrame:
    path = inputs_dir / "input_04.csv"
    raw = pd.read_csv(path, header=None)
    header_idx = None
    for i in range(len(raw)):
        row = raw.iloc[i].astype(str).str.strip().tolist()
        if ("Week" in row) and ("Type" in row) and ("Profit Min Sales Volume" in row):
            header_idx = i
            break
    if header_idx is None:
        raise ValueError("Could not locate Profit Min header in input_04.csv")

    profit_df = pd.read_csv(path, skiprows=header_idx + 1, header=None)
    profit_df = profit_df.iloc[:, :6].copy()
    profit_df.columns = ["c0", "c1", "Week", "Type",
                         "Profit Min Sales Volume", "Profit Min Sales Value"]
    profit_df = profit_df.dropna(subset=["Type"])
    profit_df = profit_df[profit_df["Week"].astype(
        str).str.contains("2020_", na=False)]
    profit_df["Week"] = profit_df["Week"].astype(
        str).str.extract(r"2020_(\d+)").astype(int)
    profit_df["Type"] = profit_df["Type"].str.strip().str.lower()
    profit_df["Profit Min Sales Volume"] = pd.to_numeric(
        profit_df["Profit Min Sales Volume"], errors="coerce")
    profit_df["Profit Min Sales Value"] = pd.to_numeric(
        profit_df["Profit Min Sales Value"], errors="coerce")
    profit_df = profit_df.drop(columns=["c0", "c1"]).reset_index(drop=True)
    return profit_df[["Type", "Week", "Profit Min Sales Volume", "Profit Min Sales Value"]]


def _read_budgets(inputs_dir: Path) -> pd.DataFrame:
    path = inputs_dir / "input_04.csv"
    raw = pd.read_csv(path, header=None)
    header_idx = None
    for i in range(len(raw)):
        row = raw.iloc[i].astype(str).str.strip().tolist()
        if ("Type" in row) and ("Measure" in row) and any("00:00:00" in c for c in row):
            header_idx = i
            break
    if header_idx is None:
        raise ValueError("Could not locate Budget header in input_04.csv")

    budget = pd.read_csv(path, skiprows=header_idx, header=0)
    budget.columns = [str(c).strip() for c in budget.columns]
    date_cols = [c for c in budget.columns if "00:00:00" in c]
    if not date_cols:
        raise ValueError("No date columns found in budget table")
    date_cols_sorted = sorted(date_cols)
    mid_col = date_cols_sorted[1] if len(
        date_cols_sorted) >= 2 else date_cols_sorted[0]
    latest_col = date_cols_sorted[-1]

    budget_sel = budget[["Type", "Measure", mid_col, latest_col]].copy()
    budget_sel["Type"] = budget_sel["Type"].astype(str).str.strip()

    def norm_type(t: str) -> str:
        t = t.lower()
        if "bar" in t:
            return "bar"
        if "liquid" in t:
            return "liquid"
        return t

    budget_sel["Type_norm"] = budget_sel["Type"].map(norm_type)
    budget_sel[mid_col] = pd.to_numeric(budget_sel[mid_col], errors="coerce")
    budget_sel[latest_col] = pd.to_numeric(
        budget_sel[latest_col], errors="coerce")

    bud_mid = (
        budget_sel.pivot_table(
            index="Type_norm", columns="Measure", values=mid_col, aggfunc="first")
        .reset_index()
        .rename_axis(None, axis=1)
        .rename(columns={"Type_norm": "Type", "Budget Volume": "Budget Volume_mid", "Budget Value": "Budget Value_mid"})
    )
    bud_latest = (
        budget_sel.pivot_table(
            index="Type_norm", columns="Measure", values=latest_col, aggfunc="first")
        .reset_index()
        .rename_axis(None, axis=1)
        .rename(columns={"Type_norm": "Type", "Budget Volume": "Budget Volume_latest", "Budget Value": "Budget Value_latest"})
    )
    bud = bud_mid.merge(bud_latest, on="Type", how="inner")
    bud["Type"] = bud["Type"].str.strip().str.lower()
    return bud


def solve(inputs_dir: Path) -> dict[str, pd.DataFrame]:
    weekly = _read_weekly_sales(inputs_dir)
    profit_min = _read_profit_min(inputs_dir)
    budgets = _read_budgets(inputs_dir)

    df_profit = weekly.merge(profit_min, on=["Type", "Week"], how="inner")
    cond_profit = (df_profit["Sales Volume"] >= df_profit["Profit Min Sales Volume"]) & (
        df_profit["Sales Value"] >= df_profit["Profit Min Sales Value"]
    )
    out02 = df_profit.loc[cond_profit, [
        "Type", "Week", "Sales Volume", "Sales Value", "Profit Min Sales Volume", "Profit Min Sales Value"
    ]].copy()
    out02 = out02.sort_values(["Type", "Week"]).reset_index(drop=True)

    df_budget = weekly.merge(budgets, on="Type", how="left")

    df_budget["Budget Volume"] = df_budget.apply(lambda r: r.get(
        "Budget Volume_mid") if r["Week"] <= 5 else r.get("Budget Volume_latest"), axis=1)
    df_budget["Budget Value"] = df_budget.apply(lambda r: r.get(
        "Budget Value_mid") if r["Week"] <= 5 else r.get("Budget Value_latest"), axis=1)

    df_profit_flag = df_profit.assign(
        exceed=((df_profit["Sales Volume"] >= df_profit["Profit Min Sales Volume"]) & (
            df_profit["Sales Value"] >= df_profit["Profit Min Sales Value"]))
    )[["Type", "Week", "exceed"]]
    df_budget = df_budget.merge(
        df_profit_flag, on=["Type", "Week"], how="left")
    df_budget["exceed"] = df_budget["exceed"].fillna(False)

    cond_week = df_budget["Week"].between(5, 8)
    cond_not_reach = (df_budget["Sales Volume"] < df_budget["Budget Volume"]) | (
        df_budget["Sales Value"] < df_budget["Budget Value"])
    out01 = df_budget.loc[cond_week & (~df_budget["exceed"]) & cond_not_reach, [
        "Type", "Week", "Sales Volume", "Budget Volume", "Sales Value", "Budget Value"
    ]].copy()

    out01 = out01.sort_values(["Type", "Week"]).reset_index(drop=True)

    return {
        "output_01.csv": out01,
        "output_02.csv": out02,
    }


if __name__ == "__main__":
    import sys
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    cand_dir = task_dir / "cand"
    cand_dir.mkdir(exist_ok=True)

    dfs = solve(inputs_dir)
    for filename, df in dfs.items():
        (cand_dir / filename).parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(cand_dir / filename, index=False, encoding="utf-8")
