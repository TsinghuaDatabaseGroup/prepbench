from __future__ import annotations
from pathlib import Path
import pandas as pd
from typing import Dict


def solve(inputs_dir: Path) -> Dict[str, pd.DataFrame]:
    absences_path = inputs_dir / "input_01.csv"
    scaffold_path = inputs_dir / "input_02.csv"

    df_abs = pd.read_csv(absences_path)
    df_abs.columns = [c.strip() for c in df_abs.columns]

    df_abs["Start Date"] = pd.to_datetime(df_abs["Start Date"], format="%Y-%m-%d", errors="coerce")

    exploded_rows = []
    for _, row in df_abs.iterrows():
        start = row["Start Date"]
        days = int(row["Days Off"]) if pd.notna(row["Days Off"]) else 0
        if pd.isna(start) or days <= 0:
            continue
        dates = pd.date_range(start=start, periods=days, freq="D")
        exploded_rows.append(pd.DataFrame({
            "Date": dates,
            "Name": row["Name"],
        }))
    if exploded_rows:
        df_daily = pd.concat(exploded_rows, ignore_index=True)
    else:
        df_daily = pd.DataFrame({"Date": pd.Series(dtype="datetime64[ns]"), "Name": pd.Series(dtype="object")})

    df_scaffold = pd.read_csv(scaffold_path)
    start_date = pd.Timestamp("2021-04-01")
    df_scaffold["Date"] = start_date + pd.to_timedelta(df_scaffold.iloc[:, 0], unit="D")

    end_date = pd.Timestamp("2021-05-31")
    df_scaffold = df_scaffold.loc[(df_scaffold["Date"] >= start_date) & (df_scaffold["Date"] <= end_date), ["Date"]]

    counts = (
        df_daily.groupby("Date", as_index=False)["Name"].nunique()
        .rename(columns={"Name": "Number of people off each day"})
    )

    out = df_scaffold.merge(counts, on="Date", how="left").fillna({"Number of people off each day": 0})

    out["Number of people off each day"] = out["Number of people off each day"].astype(int)

    out["Date"] = out["Date"].dt.strftime("%d/%m/%Y 00:00:00")

    out = out[["Date", "Number of people off each day"]]

    return {"output_01.csv": out}


if __name__ == "__main__":
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    cand_dir = task_dir / "cand"
    cand_dir.mkdir(parents=True, exist_ok=True)

    outputs = solve(inputs_dir)
    for filename, df in outputs.items():
        (cand_dir / filename).write_text("", encoding="utf-8")
        df.to_csv(cand_dir / filename, index=False, encoding="utf-8")

