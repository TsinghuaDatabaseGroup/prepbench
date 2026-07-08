from __future__ import annotations

import math
from pathlib import Path

import pandas as pd


REPORT_LABELS: dict[str, str] = {
    "input_01.csv": "2017 to 2018",
    "input_02.csv": "2018 to 2019",
    "input_03.csv": "2019 to 2020",
    "input_04.csv": "2020 to 2021",
    "input_05.csv": "2021 to 2022",
}


def _format_gap_value(value: float) -> str:
    abs_val = abs(value)
    rounded = round(abs_val, 1)
    ceil_val = math.ceil(rounded * 100) / 100
    raw_str = format(ceil_val, ".17g")

    if abs_val < 10:
        trimmed = raw_str[:4]
    elif abs_val < 100:
        trimmed = raw_str[:5]
    else:
        trimmed = raw_str[:6]

    if trimmed.endswith("0") and len(trimmed) > 1:
        trimmed = trimmed[:-1]
    if trimmed.endswith("."):
        trimmed = trimmed[:-1]
    return trimmed


def _build_pay_gap_statement(value: float) -> str:
    if pd.isna(value) or value == 0:
        return "In this organisation, men's and women's median hourly pay is equal."

    direction = "lower" if value > 0 else "higher"
    formatted_value = _format_gap_value(value)
    return (
        "In this organisation, women's median hourly pay is "
        f"{formatted_value}% {direction} than men's."
    )


def _load_inputs(inputs_dir: Path) -> pd.DataFrame:
    frames: list[pd.DataFrame] = []
    for filename, report in REPORT_LABELS.items():
        csv_path = inputs_dir / filename
        if not csv_path.exists():
            continue
        df = pd.read_csv(csv_path)
        df["Report"] = report
        frames.append(df)

    if not frames:
        raise FileNotFoundError("未找到任何输入文件，无法生成输出。")

    return pd.concat(frames, ignore_index=True)


def solve(inputs_dir: Path) -> dict[str, pd.DataFrame]:
    df = _load_inputs(inputs_dir)

    df["EmployerId"] = pd.to_numeric(
        df["EmployerId"], errors="coerce").astype("Int64")
    df = df[df["EmployerId"].notna()].copy()
    df["DiffMedianHourlyPercent"] = pd.to_numeric(
        df["DiffMedianHourlyPercent"], errors="coerce"
    )
    df["Year"] = df["Report"].str.extract(r"^(\d{4})").astype(int)
    df["DateSubmitted"] = pd.to_datetime(df["DateSubmitted"], errors="coerce")

    df["__row_id"] = range(len(df))
    max_year = df.groupby("EmployerId")["Year"].transform("max")
    latest_name_rows = df.loc[df["Year"] == max_year,
                              ["EmployerId", "EmployerName"]].copy()
    latest_name_rows = latest_name_rows.drop_duplicates(
        subset=["EmployerId", "EmployerName"])
    latest_name_rows["__name_ord"] = latest_name_rows.groupby(
        "EmployerId").cumcount()

    df_no_name = df.drop(columns=["EmployerName"])
    df = df_no_name.merge(
        latest_name_rows,
        on="EmployerId",
        how="inner",
    )
    df.sort_values(by=["__row_id", "__name_ord"], inplace=True)
    df.drop(columns=["__row_id", "__name_ord"], inplace=True)

    df["Pay Gap"] = df["DiffMedianHourlyPercent"].apply(
        _build_pay_gap_statement)

    output_cols = [
        "Year",
        "Report",
        "EmployerName",
        "EmployerId",
        "EmployerSize",
        "DiffMedianHourlyPercent",
        "Pay Gap",
    ]
    output = df[output_cols].drop_duplicates().copy()
    output["EmployerId"] = output["EmployerId"].astype(int)
    output.sort_values(by=["Year", "Report", "EmployerId"], inplace=True)
    output.reset_index(drop=True, inplace=True)

    return {"output_01.csv": output}


if __name__ == "__main__":
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    cand_dir = task_dir / "cand"
    cand_dir.mkdir(parents=True, exist_ok=True)

    outputs = solve(inputs_dir)
    for filename, df in outputs.items():
        df.to_csv(cand_dir / filename, index=False, encoding="utf-8")
