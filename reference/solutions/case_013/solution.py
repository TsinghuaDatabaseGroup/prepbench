from __future__ import annotations
from pathlib import Path
import pandas as pd
import numpy as np


def solve(inputs_dir: Path) -> dict[str, pd.DataFrame]:
    tx_path = inputs_dir / "input_01.csv"
    acct_path = inputs_dir / "input_02.csv"

    df = pd.read_csv(tx_path)
    acct = pd.read_csv(acct_path)

    df["Date"] = pd.to_datetime(df["Date"], format="%Y-%m-%d")

    acct_cols = ["Account", "Name", "Max Credit"]
    acct = acct[acct_cols]
    df = df.merge(acct, on="Account", how="left")

    df["BelowZero"] = (df["Balance"] < 0).astype(int)
    df["BeyondMax"] = (df["Balance"] < -df["Max Credit"]).astype(int)

    def fmt_date(d: pd.Timestamp) -> str:
        return d.strftime("%d/%m/%Y")

    df["Month"] = df["Date"].dt.month
    df["MonthStart"] = df["Date"].values.astype("datetime64[M]")
    df["MonthStart"] = pd.to_datetime(df["MonthStart"])

    g_month = (
        df
        .groupby(["Account", "Name", "Month", "MonthStart"], as_index=False)
        .agg(
            **{
                "Days Below Zero balance?": ("BelowZero", "sum"),
                "Days Beyond Max Credit": ("BeyondMax", "sum"),
                "Monthly Avg Transactions": ("Transaction", "mean"),
                "Monthly Avg Balances": ("Balance", "mean"),
            }
        )
    )

    g_month["Monthly Avg Transactions"] = g_month["Monthly Avg Transactions"].round(0).astype(int)
    g_month["Monthly Avg Balances"] = g_month["Monthly Avg Balances"].round(2)

    out1 = g_month.copy()
    out1["Date"] = out1["MonthStart"].apply(lambda x: fmt_date(pd.Timestamp(year=x.year, month=x.month, day=1)))
    out1 = out1[[
        "Days Beyond Max Credit",
        "Days Below Zero balance?",
        "Monthly Avg Transactions",
        "Monthly Avg Balances",
        "Month",
        "Account",
        "Name",
        "Date",
    ]]

    def month_to_quarter(m: int) -> int:
        return (int(m) - 1) // 3 + 1

    df["Quarter"] = df["Month"].apply(month_to_quarter)

    def quarter_start_date(ts: pd.Timestamp) -> pd.Timestamp:
        q = month_to_quarter(ts.month)
        q_start_month = 3 * (q - 1) + 1
        return pd.Timestamp(year=ts.year, month=q_start_month, day=1)

    df["QuarterStart"] = df["Date"].apply(quarter_start_date)

    g_quarter = (
        df
        .groupby(["Account", "Name", "Quarter", "QuarterStart"], as_index=False)
        .agg(
            **{
                "Below Zero balance?": ("BelowZero", "sum"),
                "Beyond Max Credit": ("BeyondMax", "sum"),
                "Quartlery Avg Transaction": ("Transaction", "mean"),
                "Quarterly Avg Balance": ("Balance", "mean"),
            }
        )
    )

    g_quarter["Quartlery Avg Transaction"] = g_quarter["Quartlery Avg Transaction"].round(0).astype(int)
    g_quarter["Quarterly Avg Balance"] = g_quarter["Quarterly Avg Balance"].round(2)

    out2 = g_quarter.copy()
    out2["Date"] = out2["QuarterStart"].apply(fmt_date)
    out2 = out2[[
        "Beyond Max Credit",
        "Below Zero balance?",
        "Quarter",
        "Account",
        "Name",
        "Quartlery Avg Transaction",
        "Quarterly Avg Balance",
        "Date",
    ]]

    def first_sunday(year: int) -> pd.Timestamp:
        d = pd.Timestamp(year=year, month=1, day=1)
        offset = (6 - d.weekday()) % 7
        return d + pd.Timedelta(days=offset)

    def week_number_and_anchor(d: pd.Timestamp) -> tuple[int, pd.Timestamp]:
        fs = first_sunday(d.year)
        if d < fs:
            return 1, pd.Timestamp(year=d.year, month=1, day=1)
        delta_days = (d - fs).days
        delta_weeks = delta_days // 7
        week_no = 2 + delta_weeks
        anchor = fs + pd.Timedelta(days=7 * delta_weeks)
        return week_no, anchor

    week_info = df["Date"].apply(week_number_and_anchor)
    df["Week"] = week_info.apply(lambda x: x[0])
    df["WeekAnchor"] = week_info.apply(lambda x: x[1])

    g_week = (
        df
        .groupby(["Account", "Name", "Week", "WeekAnchor"], as_index=False)
        .agg(
            **{
                "Days Below Zero balance?": ("BelowZero", "sum"),
                "Days Beyond Max Credit": ("BeyondMax", "sum"),
                "Weekly Avg Transactions": ("Transaction", "mean"),
                "Weekly Avg Balances": ("Balance", "mean"),
            }
        )
    )

    g_week["Weekly Avg Transactions"] = g_week["Weekly Avg Transactions"].round(0).astype(int)
    g_week["Weekly Avg Balances"] = g_week["Weekly Avg Balances"].round(2)

    out3 = g_week.copy()
    out3["Date"] = out3.apply(
        lambda r: fmt_date(pd.Timestamp(year=int(r["WeekAnchor"].year), month=int(r["WeekAnchor"].month), day=int(r["WeekAnchor"].day)))
        if r["Week"] != 1 else fmt_date(pd.Timestamp(year=int(r["WeekAnchor"].year), month=1, day=1)),
        axis=1,
    )

    out3 = out3[[
        "Weekly Avg Transactions",
        "Weekly Avg Balances",
        "Days Below Zero balance?",
        "Days Beyond Max Credit",
        "Week",
        "Account",
        "Name",
        "Date",
    ]]

    return {
        "output_01.csv": out1,
        "output_02.csv": out2,
        "output_03.csv": out3,
    }


if __name__ == "__main__":
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    cand_dir = task_dir / "cand"
    cand_dir.mkdir(parents=True, exist_ok=True)

    dfs = solve(inputs_dir)

    for fname, df in dfs.items():
        (cand_dir / fname).parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(cand_dir / fname, index=False, encoding="utf-8")

