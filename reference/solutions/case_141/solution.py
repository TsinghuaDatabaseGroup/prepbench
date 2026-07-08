from pathlib import Path
import pandas as pd
from datetime import datetime, timedelta


def solve(inputs_dir: Path) -> dict[str, pd.DataFrame]:
    inp_file = inputs_dir / "input_01.csv"
    df = pd.read_csv(inp_file)

    df["Date"] = pd.to_datetime(df["Date"], format="%d/%m/%Y")
    df = df.sort_values("Date").reset_index(drop=True)

    start_date = df["Date"].min()
    end_date = df["Date"].max()
    all_dates = pd.DataFrame(
        {"Date": pd.date_range(start_date, end_date, freq="D")})

    totals = df.set_index("Date")["Total Raised to date"].sort_index()

    totals_full = totals.reindex(all_dates["Date"]).ffill().fillna(0)

    all_dates["Days into fund raising"] = (
        all_dates["Date"] - start_date).dt.days

    all_dates["Total Raised to date"] = totals_full.values

    all_dates["Date_name"] = all_dates["Date"].dt.day_name()

    with pd.option_context('mode.use_inf_as_na', True):
        all_dates["Value raised per day"] = all_dates.apply(
            lambda r: (r["Total Raised to date"] / r["Days into fund raising"]
                       ) if r["Days into fund raising"] != 0 else float("nan"),
            axis=1
        )

    avg_per_weekday = (
        all_dates.groupby("Date_name")["Value raised per day"].mean().to_dict()
    )

    rows = []

    weekday_order = [
        "Wednesday",
        "Tuesday",
        "Sunday",
        "Saturday",
        "Monday",
        "Thursday",
        "Friday",
    ]

    for wd in weekday_order:
        sub = all_dates[all_dates["Date_name"] == wd].copy()
        sub = sub.sort_values("Days into fund raising", ascending=False)
        if wd in avg_per_weekday:
            avg_val = avg_per_weekday[wd]
        else:
            avg_val = float("nan")
        sub["Avg raised per weekday"] = avg_val
        sub_out = sub[[
            "Avg raised per weekday",
            "Value raised per day",
            "Days into fund raising",
            "Date_name",
            "Total Raised to date",
        ]].rename(columns={"Date_name": "Date"})
        rows.append(sub_out)

    out_df = pd.concat(rows, ignore_index=True)

    out_df = out_df[[
        "Avg raised per weekday",
        "Value raised per day",
        "Days into fund raising",
        "Date",
        "Total Raised to date",
    ]]

    out_df["Avg raised per weekday"] = out_df["Avg raised per weekday"].round(
        9)
    out_df["Value raised per day"] = out_df["Value raised per day"].round(9)
    out_df["Days into fund raising"] = out_df["Days into fund raising"].astype(
        int)
    out_df["Total Raised to date"] = out_df["Total Raised to date"].astype(int)

    return {"output_01.csv": out_df}


if __name__ == "__main__":
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"

    cand_dir = task_dir / "cand"
    cand_dir.mkdir(parents=True, exist_ok=True)

    outputs = solve(inputs_dir)
    for fname, df in outputs.items():
        (cand_dir / fname).parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(cand_dir / fname, index=False, encoding="utf-8")
