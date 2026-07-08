from __future__ import annotations
from pathlib import Path
import pandas as pd
import statistics as stats


def solve(inputs_dir: Path) -> dict[str, pd.DataFrame]:
    input_file = inputs_dir / "input_01.csv"
    df = pd.read_csv(input_file)

    df["_order"] = range(len(df))
    df["Date"] = pd.to_datetime(df["Date"], format="%d/%m/%Y", errors="raise")

    weeks_order: list[int] = []
    for wk in df["Week"].tolist():
        if wk not in weeks_order:
            weeks_order.append(wk)

    records = []
    for wk in weeks_order:
        vals = df.loc[df["Week"] == wk, "Complaints"].astype(float).tolist()
        mean = stats.mean(vals)
        sd = stats.stdev(vals) if len(vals) > 1 else float("nan")
        records.append({"Week": wk, "Mean": mean, "Standard Deviation": sd})
    agg = pd.DataFrame(records)

    df = df.merge(agg, on="Week", how="left")

    df["Lower Control Limit 1"] = df["Mean"] - df["Standard Deviation"]
    df["Upper Control Limit 1"] = df["Mean"] + df["Standard Deviation"]
    df["Lower Control Limit 2"] = df["Mean"] - 2 * df["Standard Deviation"]
    df["Upper Control Limit 2"] = df["Mean"] + 2 * df["Standard Deviation"]
    df["Lower Control Limit 3"] = df["Mean"] - 3 * df["Standard Deviation"]
    df["Upper Control Limit 3"] = df["Mean"] + 3 * df["Standard Deviation"]

    def fmt_date(series: pd.Series) -> pd.Series:
        return series.dt.strftime("%Y-%m-%d")

    out1_mask = (df["Complaints"] < df["Lower Control Limit 1"]) | (
        df["Complaints"] > df["Upper Control Limit 1"])
    out1 = df.loc[out1_mask].copy()
    out1["Variation (1SD)"] = 2 * out1["Standard Deviation"]
    out1["Outlier? (1SD)"] = "Outside"
    out1["Lower Control Limit"] = out1["Lower Control Limit 1"]
    out1["Upper Control Limit"] = out1["Upper Control Limit 1"]
    out1["Date_str"] = fmt_date(out1["Date"])
    out1 = out1.sort_values(["_order"])
    out1 = out1[[
        "Variation (1SD)",
        "Outlier? (1SD)",
        "Lower Control Limit",
        "Upper Control Limit",
        "Standard Deviation",
        "Mean",
        "Date_str",
        "Week",
        "Complaints",
        "Department",
    ]].rename(columns={"Date_str": "Date"})

    out2_mask = (df["Complaints"] < df["Lower Control Limit 2"]) | (df["Complaints"] > df["Upper Control Limit 2"]) \


    out2 = df.loc[out2_mask].copy()
    out2["Outlier (2SD)"] = "Outlier"
    out2["Variation (2SD)"] = 4 * out2["Standard Deviation"]
    out2["Lower Control Limit (2SD)"] = out2["Lower Control Limit 2"]
    out2["Upper Control Limit (2SD)"] = out2["Upper Control Limit 2"]
    out2["Date_str"] = fmt_date(out2["Date"])
    out2 = out2.sort_values(["_order"])
    out2 = out2[[
        "Outlier (2SD)",
        "Variation (2SD)",
        "Lower Control Limit (2SD)",
        "Upper Control Limit (2SD)",
        "Standard Deviation",
        "Mean",
        "Date_str",
        "Week",
        "Complaints",
        "Department",
    ]].rename(columns={"Date_str": "Date"})

    out3_mask = (df["Complaints"] < df["Lower Control Limit 3"]) | (
        df["Complaints"] > df["Upper Control Limit 3"])
    out3 = df.loc[out3_mask].copy()
    out3["Outlier (3SD)"] = "Outlier"
    out3["Variation (3SD)"] = 6 * out3["Standard Deviation"]
    out3["Lower Control Limit (3SD)"] = out3["Lower Control Limit 3"]
    out3["Upper Control Limit (3SD)"] = out3["Upper Control Limit 3"]
    out3["Date_str"] = fmt_date(out3["Date"])
    out3 = out3.sort_values(["_order"])
    out3 = out3[[
        "Outlier (3SD)",
        "Variation (3SD)",
        "Lower Control Limit (3SD)",
        "Upper Control Limit (3SD)",
        "Standard Deviation",
        "Mean",
        "Date_str",
        "Week",
        "Complaints",
        "Department",
    ]].rename(columns={"Date_str": "Date"})

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

    results = solve(inputs_dir)
    for filename, df in results.items():
        (cand_dir / filename).parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(cand_dir / filename, index=False, encoding="utf-8")
