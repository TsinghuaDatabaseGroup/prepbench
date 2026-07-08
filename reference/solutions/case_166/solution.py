from __future__ import annotations
from pathlib import Path
import pandas as pd
import numpy as np
from typing import Dict


TODAY = pd.Timestamp("2022-04-13")


def month_floor(ts: pd.Timestamp) -> pd.Timestamp:
    return pd.Timestamp(year=ts.year, month=ts.month, day=1)


def months_diff_from_apr_2022(end_dt: pd.Timestamp) -> int:
    return (end_dt.year - 2022) * 12 + (end_dt.month - 4)


def months_between_inclusive(start_dt: pd.Timestamp, end_dt: pd.Timestamp) -> int:
    return (end_dt.year - start_dt.year) * 12 + (end_dt.month - start_dt.month)


def generate_month_series(start_dt: pd.Timestamp, n_months: int) -> pd.Series:
    start_month = month_floor(start_dt)
    return pd.date_range(start=start_month, periods=n_months, freq="MS")


def solve(inputs_dir: Path) -> dict[str, pd.DataFrame]:
    prices = pd.read_csv(inputs_dir / "input_01.csv")
    contracts = pd.read_csv(inputs_dir / "input_02.csv")

    contracts["Contract Start"] = pd.to_datetime(contracts["Contract Start"])
    contracts["Contract End"] = pd.to_datetime(contracts["Contract End"])

    contracts = contracts.merge(
        prices,
        on=["City", "Office Size"],
        how="left",
        validate="m:1",
        suffixes=("", "_price"),
    )

    contracts["Contract Length"] = contracts.apply(
        lambda r: months_between_inclusive(r["Contract Start"], r["Contract End"]), axis=1
    )
    contracts["Months Until Expiry"] = contracts["Contract End"].apply(months_diff_from_apr_2022)

    rows = []
    for _, r in contracts.iterrows():
        n_months = int(r["Contract Length"])
        month_series = generate_month_series(r["Contract Start"], n_months)
        rent = float(r["Rent per Month"])
        cum = 0.0
        for dt in month_series:
            cum += rent
            rows.append({
                "Cumulative Monthly Cost": cum,
                "ID": str(r["ID"]),
                "Country": r["Country"],
                "City": r["City"],
                "Address": r["Address"],
                "Company": r["Company"],
                "Office Size": r["Office Size"],
                "Contract Start": r["Contract Start"],
                "Contract End": r["Contract End"],
                "Contract Length": int(r["Contract Length"]),
                "Months Until Expiry": int(r["Months Until Expiry"]),
                "People": int(r["People"]),
                "Per Person": float(r["Per Person"]),
                "Rent per Month": float(r["Rent per Month"]),
                "Month Divider": dt,
            })

    out1 = pd.DataFrame(rows, columns=[
        "Cumulative Monthly Cost",
        "ID","Country","City","Address","Company","Office Size",
        "Contract Start","Contract End","Contract Length","Months Until Expiry",
        "People","Per Person","Rent per Month","Month Divider"
    ])

    def fmt_dmy(series: pd.Series) -> pd.Series:
        return pd.to_datetime(series).dt.strftime("%d/%m/%Y")

    out1["Contract Start"] = fmt_dmy(out1["Contract Start"])
    out1["Contract End"] = fmt_dmy(out1["Contract End"])
    out1["Month Divider"] = fmt_dmy(out1["Month Divider"])

    def to_int_text(series: pd.Series) -> pd.Series:
        nums = pd.to_numeric(series, errors="coerce")
        nums = nums.replace([np.inf, -np.inf], np.nan)
        nums = pd.to_numeric(nums, errors="coerce")
        ints = nums.round(0).astype("Int64")
        return ints.astype("string").fillna("")

    out1["ID"] = to_int_text(out1["ID"])
    for col in [
        "Cumulative Monthly Cost",
        "Contract Length",
        "Months Until Expiry",
        "People",
        "Per Person",
        "Rent per Month",
    ]:
        out1[col] = to_int_text(out1[col])

    out1_month_dt = pd.to_datetime(out1["Month Divider"], format="%d/%m/%Y")
    out1_with_dt = out1.copy()
    out1_with_dt["Month_dt"] = out1_month_dt

    years = list(range(2021, 2027))
    data = {"Year": years, "EoY and Current": [pd.NA] * len(years)}

    y2021_sum = pd.to_numeric(
        out1_with_dt.loc[out1_with_dt["Month_dt"].dt.year == 2021, "Rent per Month"],
        errors="coerce",
    ).sum()
    if pd.notna(y2021_sum) and y2021_sum != 0:
        data["EoY and Current"][years.index(2021)] = float(y2021_sum)

    y2022_mask = (out1_with_dt["Month_dt"].dt.year == 2022) & (out1_with_dt["Month_dt"].dt.month <= 4)
    y2022_sum = pd.to_numeric(
        out1_with_dt.loc[y2022_mask, "Rent per Month"],
        errors="coerce",
    ).sum()
    if pd.notna(y2022_sum) and y2022_sum != 0:
        data["EoY and Current"][years.index(2022)] = float(y2022_sum)

    out2 = pd.DataFrame(data, columns=["Year", "EoY and Current"])
    out2["Year"] = to_int_text(out2["Year"])
    out2["EoY and Current"] = to_int_text(out2["EoY and Current"])

    return {
        "output_01.csv": out1,
        "output_02.csv": out2,
    }


if __name__ == "__main__":
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    cand_dir = task_dir / "cand"
    cand_dir.mkdir(exist_ok=True)

    outputs = solve(inputs_dir)

    for fname, df in outputs.items():
        (cand_dir / fname).parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(cand_dir / fname, index=False, encoding="utf-8")
