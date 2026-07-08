from __future__ import annotations
from pathlib import Path
import pandas as pd
from typing import Dict


def solve(inputs_dir: Path) -> Dict[str, pd.DataFrame]:
    file_dates = [
        ("input_01.csv", pd.to_datetime("2021-01-01")),
        ("input_02.csv", pd.to_datetime("2021-01-08")),
        ("input_03.csv", pd.to_datetime("2021-01-15")),
        ("input_04.csv", pd.to_datetime("2021-01-22")),
        ("input_05.csv", pd.to_datetime("2021-01-29")),
    ]

    frames = []
    for fname, rdate in file_dates:
        fpath = inputs_dir / fname
        if not fpath.exists():
            continue
        df = pd.read_csv(fpath, dtype={"Orders": str})
        df["Sale Date"] = pd.to_datetime(df["Sale Date"], format="%Y-%m-%d", errors="coerce")
        df["Reporting Date"] = rdate
        frames.append(df)

    if not frames:
        out = pd.DataFrame(columns=["Order Status", "Orders", "Sale Date", "Reporting Date"])
        return {"output_01.csv": out}

    full = pd.concat(frames, ignore_index=True)

    grp = full.groupby("Orders", as_index=False)
    first_seen = grp["Reporting Date"].min().rename(columns={"Reporting Date": "first_report"})
    last_seen = grp["Reporting Date"].max().rename(columns={"Reporting Date": "last_report"})

    base = full.copy()
    base = base.merge(first_seen, on="Orders", how="left")
    base["Order Status"] = (base["Reporting Date"] == base["first_report"]).map({True: "New Order", False: "Unfulfilled Order"})
    base = base.drop(columns=["first_report"])

    known_weeks = sorted(full["Reporting Date"].dropna().unique())
    last_available_week = known_weeks[-1]

    fulfill = last_seen.copy()
    fulfill["Reporting Date"] = fulfill["last_report"] + pd.to_timedelta(7, unit="D")
    fulfill = fulfill[fulfill["Reporting Date"] <= last_available_week].copy()
    fulfill["Order Status"] = "Fulfilled"
    fulfill = fulfill.drop(columns=["last_report"])

    sale_per_order = full.groupby("Orders", as_index=False)["Sale Date"].min()
    fulfill = fulfill.merge(sale_per_order, on="Orders", how="left")

    non_fulfilled = base[["Order Status", "Orders", "Sale Date", "Reporting Date"]].copy()
    fulfilled = fulfill[["Order Status", "Orders", "Sale Date", "Reporting Date"]].copy()
    output = pd.concat([non_fulfilled, fulfilled], ignore_index=True)

    def fmt_date(s: pd.Series) -> pd.Series:
        s = pd.to_datetime(s)
        return s.dt.strftime("%d/%m/%Y")

    output["Sale Date"] = fmt_date(output["Sale Date"])
    output["Reporting Date"] = fmt_date(output["Reporting Date"])

    output = output[["Order Status", "Orders", "Sale Date", "Reporting Date"]]

    return {"output_01.csv": output}


if __name__ == "__main__":
    import sys
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    cand_dir = task_dir / "cand"
    cand_dir.mkdir(parents=True, exist_ok=True)

    result = solve(inputs_dir)
    for fname, df in result.items():
        (cand_dir / fname).parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(cand_dir / fname, index=False, encoding="utf-8")

