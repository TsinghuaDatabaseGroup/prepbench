import pandas as pd
from pathlib import Path
from decimal import Decimal, ROUND_HALF_UP


def solve(inputs_dir: Path) -> dict[str, pd.DataFrame]:
    delayed_raw = pd.read_csv(inputs_dir / "input_01.csv")
    on_time_raw = pd.read_csv(inputs_dir / "input_02.csv")

    delayed_raw = delayed_raw.sort_values("RecordID").reset_index(drop=True)
    group_id = (delayed_raw["RecordID"] - 1) // 3

    def first_non_null(series: pd.Series) -> str:
        non_null = series.dropna()
        return non_null.iloc[0] if not non_null.empty else None

    delayed = (
        delayed_raw
        .assign(group_id=group_id)
        .groupby("group_id")
        .agg({
            "Airport": first_non_null,
            "Type": first_non_null,
            "Delay": first_non_null,
        })
        .reset_index(drop=True)
    )

    delayed["Airport"] = delayed["Airport"].astype(str).str.strip()
    delayed["Type"] = delayed["Type"].astype(str).str.strip()
    delayed["Delay"] = delayed["Delay"].astype(float)

    on_time_raw.columns = [col.strip() for col in on_time_raw.columns]
    on_time_raw["Airport"] = on_time_raw["Airport"].str.strip()
    on_time_raw["Type"] = on_time_raw["Type"].str.strip()
    on_time_raw["Number of flights"] = on_time_raw["Number of flights"].astype(int)

    valid_airports = set(on_time_raw["Airport"].unique())

    def clean_airport(code: str) -> str:
        code_str = str(code).strip().upper()
        if code_str in valid_airports:
            return code_str
        sorted_code = ''.join(sorted(code_str))
        matches = [apt for apt in valid_airports if ''.join(sorted(apt)) == sorted_code]
        if len(matches) == 1:
            return matches[0]
        return "Invalid"

    delayed["Airport"] = delayed["Airport"].apply(clean_airport)

    delayed_summary = (
        delayed.groupby(["Airport", "Type"], dropna=False)
        .agg(delayed_flights=("Delay", "size"), total_delay=("Delay", "sum"))
        .reset_index()
    )

    combined = on_time_raw.merge(delayed_summary, on=["Airport", "Type"], how="left")
    combined["delayed_flights"] = combined["delayed_flights"].fillna(0).astype(int)
    combined["total_delay"] = combined["total_delay"].fillna(0.0)

    combined["Total Flights"] = combined["Number of flights"] + combined["delayed_flights"]

    def calc_avg_delay(row):
        if row["Total Flights"] == 0:
            return 0.0
        return row["total_delay"] / row["Total Flights"]

    def calc_pct_delayed(row):
        if row["Total Flights"] == 0:
            return 0.0
        return (row["delayed_flights"] / row["Total Flights"]) * 100

    combined["Avg Delay (mins)"] = combined.apply(calc_avg_delay, axis=1)
    combined["% Flights Delayed"] = combined.apply(calc_pct_delayed, axis=1)

    def round_half_up(series: pd.Series) -> pd.Series:
        return series.apply(lambda value: float(Decimal(str(value)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)))

    output = (
        combined[combined["Airport"] != "Invalid"]
        [["Airport", "Type", "% Flights Delayed", "Avg Delay (mins)"]]
        .copy()
    )

    output["% Flights Delayed"] = round_half_up(output["% Flights Delayed"])
    output["Avg Delay (mins)"] = round_half_up(output["Avg Delay (mins)"])

    output = output.sort_values(["Airport", "Type"]).reset_index(drop=True)

    return {"output_01.csv": output}


if __name__ == "__main__":
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    cand_dir = task_dir / "cand"
    cand_dir.mkdir(parents=True, exist_ok=True)

    outputs = solve(inputs_dir)
    for filename, df in outputs.items():
        df.to_csv(cand_dir / filename, index=False)
