
import math
import numpy as np
import pandas as pd
from pathlib import Path


PLACEHOLDER_LEAVE_DATE = pd.Timestamp("2023-06-30")


def _round_half_up(series: pd.Series, decimals: int) -> pd.Series:
    factor = 10 ** decimals

    def _round(value: float) -> float:
        if pd.isna(value):
            return value
        return math.copysign(
            math.floor(abs(value) * factor + 0.5) / factor,
            value,
        )

    return series.apply(_round)


def _enumerate_months(row: pd.Series) -> list[pd.Timestamp]:
    start = row["hire_date"]
    end = row["range_end"]

    if pd.isna(start) or pd.isna(end) or start > end:
        return []

    periods = pd.period_range(start=start, end=end, freq="M")
    return periods.to_timestamp(how="end").normalize().to_list()


def solve(inputs_dir: Path) -> dict[str, pd.DataFrame]:
    df = pd.read_csv(
        inputs_dir / "input_01.csv",
        parse_dates=["hire_date", "leave_date"],
        dayfirst=True,
    )

    df = df.loc[:, ["dc_nbr", "employee_id", "hire_date", "leave_date"]].copy()
    df["hire_month_start"] = df["hire_date"].dt.to_period(
        "M").dt.to_timestamp()
    df = (
        df.groupby(["dc_nbr", "employee_id",
                   "hire_month_start"], as_index=False)
        .agg(leave_date=("leave_date", "max"))
        .rename(columns={"hire_month_start": "hire_date"})
    )

    df["range_end"] = df["leave_date"].fillna(PLACEHOLDER_LEAVE_DATE)
    df["month_end_list"] = df.apply(_enumerate_months, axis=1)
    df = df.loc[df["month_end_list"].map(len) > 0].copy()

    df_monthly = df.loc[:, ["dc_nbr", "leave_date", "month_end_list"]].explode(
        "month_end_list"
    )
    df_monthly = df_monthly.rename(
        columns={"month_end_list": "month_end_date"})
    df_monthly["month_end_date"] = pd.to_datetime(
        df_monthly["month_end_date"]
    ).dt.normalize()

    df_monthly["is_active_at_month_end"] = (
        df_monthly["leave_date"].isna()
        | (df_monthly["leave_date"] >= df_monthly["month_end_date"])
    )
    df_monthly["left_in_month"] = (
        df_monthly["leave_date"].notna()
        & (
            df_monthly["leave_date"].dt.to_period("M")
            == df_monthly["month_end_date"].dt.to_period("M")
        )
    )

    monthly_stats = (
        df_monthly.groupby(["dc_nbr", "month_end_date"])
        .agg(
            ee_count=("is_active_at_month_end", "sum"),
            ee_leaving=("left_in_month", "sum"),
        )
        .reset_index()
    )

    coverage = monthly_stats.groupby(
        "dc_nbr")["month_end_date"].agg(["min", "max"])
    timeline_frames: list[pd.DataFrame] = []
    for dc, bounds in coverage.iterrows():
        months = (
            pd.period_range(start=bounds["min"], end=bounds["max"], freq="M")
            .to_timestamp(how="end")
            .normalize()
        )
        timeline_frames.append(
            pd.DataFrame({"dc_nbr": dc, "month_end_date": months})
        )
    timeline = pd.concat(timeline_frames, ignore_index=True)

    full_stats = timeline.merge(
        monthly_stats, on=["dc_nbr", "month_end_date"], how="left"
    )
    full_stats[["ee_count", "ee_leaving"]] = (
        full_stats[["ee_count", "ee_leaving"]].fillna(0).astype(int)
    )
    full_stats = full_stats.sort_values(["dc_nbr", "month_end_date"]).reset_index(
        drop=True
    )

    full_stats["ee_count_pm"] = full_stats.groupby("dc_nbr")[
        "ee_count"].shift(1)
    full_stats["ee_count_p12"] = full_stats.groupby("dc_nbr")[
        "ee_count"].shift(12)

    full_stats["avg_ee_month"] = (
        (full_stats["ee_count_pm"] + full_stats["ee_count"]) / 2
    )
    full_stats["avg_ee_p12"] = (
        (full_stats["ee_count_p12"] + full_stats["ee_count"]) / 2
    )
    full_stats["avg_ee_month"] = _round_half_up(full_stats["avg_ee_month"], 6)
    full_stats["avg_ee_p12"] = _round_half_up(full_stats["avg_ee_p12"], 6)

    full_stats["ee_leaving_p12"] = full_stats.groupby("dc_nbr")["ee_leaving"].transform(
        lambda s: s.rolling(window=12, min_periods=12).sum()
    )
    full_stats["ee_leaving_p12"] = (
        full_stats["ee_leaving_p12"].round().astype("Int64")
    )

    full_stats["turnover_month"] = (
        full_stats["ee_leaving"] / full_stats["avg_ee_month"] * 100
    )
    full_stats.loc[
        full_stats["avg_ee_month"].isna() | (full_stats["avg_ee_month"] == 0),
        "turnover_month",
    ] = np.nan
    full_stats["turnover_month"] = _round_half_up(
        full_stats["turnover_month"], 2)

    ee_leaving_p12_float = full_stats["ee_leaving_p12"].astype(float)
    full_stats["turnover_p12"] = (
        ee_leaving_p12_float / full_stats["avg_ee_p12"] * 100
    )
    full_stats.loc[
        full_stats["avg_ee_p12"].isna()
        | (full_stats["avg_ee_p12"] == 0)
        | ee_leaving_p12_float.isna(),
        "turnover_p12",
    ] = np.nan
    full_stats["turnover_p12"] = _round_half_up(full_stats["turnover_p12"], 2)

    output_cols = [
        "dc_nbr",
        "month_end_date",
        "ee_count",
        "ee_leaving",
        "ee_leaving_p12",
        "avg_ee_month",
        "avg_ee_p12",
        "turnover_month",
        "turnover_p12",
    ]
    output_df = full_stats[output_cols].copy()
    output_df["month_end_date"] = output_df["month_end_date"].dt.strftime(
        "%d/%m/%Y")
    output_df["dc_nbr"] = output_df["dc_nbr"].astype(int)
    output_df["ee_count"] = output_df["ee_count"].astype(int)
    output_df["ee_leaving"] = output_df["ee_leaving"].astype(int)
    output_df["ee_leaving_p12"] = output_df["ee_leaving_p12"].astype("Int64")

    return {"output_01.csv": output_df}


if __name__ == "__main__":
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    cand_dir = task_dir / "cand"

    cand_dir.mkdir(parents=True, exist_ok=True)

    solutions = solve(inputs_dir)

    for filename, df in solutions.items():
        df.to_csv(cand_dir / filename, index=False, encoding="utf-8")
