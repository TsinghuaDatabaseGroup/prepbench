from __future__ import annotations

from pathlib import Path

import pandas as pd


def solve(inputs_dir: Path) -> dict[str, pd.DataFrame]:
    input_path = inputs_dir / "input_01.csv"
    df = pd.read_csv(input_path)

    df["Engagement Start Date"] = pd.to_datetime(df["Engagement Start Date"], format="%Y-%m-%d")
    df["Engagement End Date"] = pd.to_datetime(df["Engagement End Date"], format="%Y-%m-%d")
    df["Calendar Days"] = (df["Engagement End Date"] - df["Engagement Start Date"]).dt.days

    expanded_rows: list[dict[str, object]] = []
    for _, row in df.iterrows():
        start = row["Engagement Start Date"]
        end = row["Engagement End Date"]

        if pd.isna(start) or pd.isna(end):
            dates = pd.DatetimeIndex([])
        elif start <= end:
            dates = pd.date_range(start, end, freq="D")
        else:
            dates = pd.DatetimeIndex([start, end])

        weekday_dates = [d for d in dates if d.weekday() < 5]
        for work_day in weekday_dates:
            expanded_rows.append(
                {
                    "Initials": row["Initials"],
                    "Engagement Order": row["Engagement Order"],
                    "Grade Name": row["Grade Name"],
                    "Day Rate": row["Day Rate"],
                    "Work Day": work_day,
                }
            )

    if expanded_rows:
        expanded_df = pd.DataFrame(expanded_rows)
    else:
        expanded_df = pd.DataFrame(
            columns=["Initials", "Engagement Order", "Grade Name", "Day Rate", "Work Day"]
        )

    keys = ["Initials", "Engagement Order", "Grade Name"]
    if not expanded_df.empty:
        day_rate_summary = expanded_df.groupby(
            keys, as_index=False, dropna=False
        )["Day Rate"].sum()
    else:
        day_rate_summary = pd.DataFrame(columns=keys + ["Day Rate"])
    base_info = df[keys + ["Calendar Days"]].drop_duplicates(subset=keys, keep="first")
    result = day_rate_summary.merge(base_info, on=keys, how="left")

    result["Overall Rank"] = result["Day Rate"].rank(method="min", ascending=False)
    result["Grade Rank"] = result.groupby("Grade Name")["Day Rate"].rank(
        method="min", ascending=False
    )

    output = pd.DataFrame(
        {
            "Calendar Days": result["Calendar Days"].astype(int),
            "Initials": result["Initials"],
            "Engagement Order": result["Engagement Order"].astype(int),
            "Grade Name": result["Grade Name"],
            "Day Rate": result["Day Rate"].astype(int),
            "Overall Rank": result["Overall Rank"].astype(int),
            "Grade Rank": result["Grade Rank"].astype(int),
        }
    )

    output = output.sort_values(
        ["Overall Rank", "Grade Rank", "Initials", "Engagement Order"]
    ).reset_index(drop=True)

    return {"output_01.csv": output}


if __name__ == "__main__":
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    cand_dir = task_dir / "cand"
    cand_dir.mkdir(parents=True, exist_ok=True)

    for filename, df in solve(inputs_dir).items():
        df.to_csv(cand_dir / filename, index=False, encoding="utf-8")

