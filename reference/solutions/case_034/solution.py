from __future__ import annotations
from pathlib import Path
import pandas as pd
import re


def solve(inputs_dir: Path) -> dict[str, pd.DataFrame]:
    dates_path = inputs_dir / "input_01.csv"
    rules_path = inputs_dir / "input_02.csv"

    df_dates = pd.read_csv(dates_path, parse_dates=["Date"])
    df_rules = pd.read_csv(rules_path)

    df_dates = df_dates.sort_values("Date").copy()
    df_dates["Weekday"] = df_dates["Date"].dt.day_name()
    df_dates["Month Name"] = df_dates["Date"].dt.month_name()
    df_dates["Year"] = df_dates["Date"].dt.year
    df_dates["Month"] = df_dates["Date"].dt.month

    df_dates["n_in_month"] = (
        df_dates.sort_values(["Year", "Month", "Date"])\
            .groupby(["Year", "Month", "Weekday"])\
            .cumcount() + 1
    )

    def parse_schedule(text: str) -> tuple[int, str]:
        m = re.match(r"^(\d+)(?:st|nd|rd|th) (\w+) of the Month$", str(text).strip())
        if not m:
            raise ValueError(f"Unrecognized schedule format: {text}")
        n = int(m.group(1))
        weekday = m.group(2)
        return n, weekday

    df_rules = df_rules.reset_index().rename(columns={"index": "rule_order"})

    out_rows = []
    for _, r in df_rules.iterrows():
        n, wk = parse_schedule(r["Delivery Schedule"])
        matched = df_dates[(df_dates["Weekday"] == wk) & (df_dates["n_in_month"] == n)].copy()
        if matched.empty:
            continue
        matched["Product"] = r["Product"]
        matched["Scent"] = r["Scent"]
        matched["Supplier"] = r["Supplier"]
        matched["Quantity"] = r["Quantity"]
        matched["rule_order"] = r["rule_order"]
        out_rows.append(matched)

    if out_rows:
        df_out = pd.concat(out_rows, ignore_index=True)
    else:
        df_out = pd.DataFrame(columns=["Month Name", "Weekday", "Date", "Product", "Scent", "Supplier", "Quantity"])

    df_out = df_out.sort_values(["Date", "rule_order", "Product", "Scent"]).copy()
    df_out["Date"] = df_out["Date"].dt.strftime("%d/%m/%Y")

    df_out = df_out[[
        "Month Name",
        "Weekday",
        "Date",
        "Product",
        "Scent",
        "Supplier",
        "Quantity",
    ]]

    df_out["Quantity"] = pd.to_numeric(df_out["Quantity"], errors="raise")

    return {"output_01.csv": df_out}


if __name__ == "__main__":
    import sys
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    cand_dir = task_dir / "cand"
    cand_dir.mkdir(parents=True, exist_ok=True)

    outputs = solve(inputs_dir)
    for fname, df in outputs.items():
        (cand_dir / fname).write_text("")
        df.to_csv(cand_dir / fname, index=False, encoding="utf-8")

