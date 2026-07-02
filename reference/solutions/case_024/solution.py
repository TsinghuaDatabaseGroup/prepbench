from __future__ import annotations
from pathlib import Path
import pandas as pd
from typing import Dict



def solve(inputs_dir: Path) -> Dict[str, pd.DataFrame]:
    df_cal = pd.read_csv(inputs_dir / "input_01.csv")
    day_type_map = dict(zip(df_cal["Date"], df_cal["Holiday?"]))

    df_chat = pd.read_csv(inputs_dir / "input_02.csv")

    parsed = df_chat["Field_1"].str.extract(
        r"\[(\d{2})/(\d{2})/(\d{4}), (\d{2}):(\d{2}):(\d{2})\] (.*?): (.*)"
    )
    parsed.columns = ["day", "month", "year", "hour",
                      "minute", "second", "Name", "Message"]

    dt = pd.to_datetime(
        parsed[["year", "month", "day", "hour", "minute", "second"]].astype(int))
    cal_key = dt.dt.day.astype(str) + " " + dt.dt.month_name()
    day_type = cal_key.map(day_type_map)

    seconds = dt.dt.hour * 3600 + dt.dt.minute * 60 + dt.dt.second
    work_window = (
        (day_type == "Weekday") &
        (
            seconds.between(9 * 3600, 11 * 3600 + 59 * 60 + 59)
            | seconds.between(13 * 3600, 17 * 3600)
        )
    )

    df = pd.DataFrame({
        "Name": parsed["Name"],
        "Text": 1,
        "Number of Words": parsed["Message"].str.findall(r"[A-Za-z']+").str.len(),
        "Text while at work": work_window.astype(int),
    })

    agg = df.groupby("Name", as_index=False).agg(
        {"Text": "sum", "Number of Words": "sum", "Text while at work": "sum"}
    )

    from decimal import Decimal, ROUND_HALF_UP

    def _avg_row(row):
        num = Decimal(int(row["Number of Words"]))
        den = Decimal(int(row["Text"]))
        return float((num / den).quantize(Decimal("0.1"), rounding=ROUND_HALF_UP))

    def _pct_row(row):
        num = Decimal(int(row["Text while at work"])) * Decimal(100)
        den = Decimal(int(row["Text"]))
        return float((num / den).quantize(Decimal("0.1"), rounding=ROUND_HALF_UP))

    agg["Avg Words/Sentence"] = agg.apply(_avg_row, axis=1)
    agg["% sent from work"] = agg.apply(_pct_row, axis=1)

    agg = agg[[
        "Name", "Text", "Number of Words", "Avg Words/Sentence", "Text while at work", "% sent from work"
    ]]

    agg = agg.sort_values("Name")

    return {"output_01.csv": agg}


if __name__ == "__main__":
    import sys
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    cand_dir = task_dir / "cand"
    cand_dir.mkdir(parents=True, exist_ok=True)

    outputs = solve(inputs_dir)

    for fname, df in outputs.items():
        out_path = cand_dir / fname
        df.to_csv(out_path, index=False, encoding="utf-8")

    print("Wrote:", ", ".join(str((cand_dir / k).resolve())
          for k in outputs.keys()))
