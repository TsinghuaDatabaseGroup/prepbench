from datetime import datetime
from pathlib import Path

import numpy as np
import pandas as pd

def solve(inputs_dir: Path) -> dict[str, pd.DataFrame]:
    df = pd.read_csv(inputs_dir / "input_01.csv")
    
    df = df[df["Units"] == "min"].copy()
    
    df["Value"] = pd.to_numeric(df["Value"], errors="coerce")
    
    last_col = df.columns[-1]
    split_cols = df[last_col].str.split(" - ", n=2, expand=True)
    df["Coach"] = split_cols[0].str.strip()
    df["Calories"] = split_cols[1].str.strip().astype(int)
    df["Music Type"] = split_cols[2].str.strip()

    df["Minutes"] = df["Value"].astype(float)

    def parse_date(date_str):
        try:
            date_str = str(date_str).strip()
            for fmt in ["%d/%m/%Y", "%d/%m/%y", "%d/%m/%Y", "%d/%m/%y"]:
                try:
                    dt = datetime.strptime(date_str, fmt)
                    return dt.year
                except:
                    continue
            parts = date_str.split("/")
            if len(parts) == 3:
                day, month, year = parts
                if len(year) == 2:
                    year = "20" + year
                return int(year)
            return None
        except:
            return None
    
    df["Year"] = df["Date"].apply(parse_date)
    
    df = df[df["Year"].isin([2021, 2022])].copy()
    
    def format_decimal(value: float, decimals: int = 1) -> str:
        rounded = round(float(value), decimals)
        formatted = f"{rounded:.{decimals}f}"
        formatted = formatted.rstrip("0").rstrip(".")
        return formatted

    speed_kph = 30

    results_dict: dict[int, dict[str, str]] = {}
    
    for year in [2022, 2021]:
        year_data = df[df["Year"] == year].copy()
        
        if len(year_data) == 0:
            continue
        year_data = year_data.copy()
        year_data = year_data[year_data["Minutes"] > 0]
        year_data["Calories per Minute"] = year_data["Calories"] / year_data["Minutes"]

        total_mins = float(year_data["Minutes"].sum())

        total_rides = len(year_data)

        avg_calories_per_ride = year_data["Calories"].mean()

        total_distance = (total_mins / 60.0) * speed_kph

        avg_calories_per_minute = year_data["Calories per Minute"].mean()

        mins_per_coach = (
            year_data.groupby("Coach")["Minutes"].sum().sort_values(ascending=False)
        )
        max_mins_value = mins_per_coach.iloc[0]
        max_coaches = mins_per_coach[mins_per_coach == max_mins_value].sort_index()
        max_coach_mins = max_coaches.index[0]
        total_mins_per_coach_str = f"{max_coach_mins} ({int(max_mins_value)})"

        coach_cpm = (
            year_data.groupby("Coach")["Calories per Minute"].mean().sort_values(ascending=False)
        )
        max_cpm_value = coach_cpm.iloc[0]
        max_cpm_coaches = coach_cpm[coach_cpm == max_cpm_value].sort_index()
        max_coach_cpm = max_cpm_coaches.index[0]
        calories_per_min_per_coach_str = (
            f"{max_coach_cpm} ({format_decimal(max_cpm_value, 1)})"
        )

        results_dict[year] = {
            "Total Mins": str(int(total_mins)),
            "Avg. Calories per Ride": format_decimal(avg_calories_per_ride, 1),
            "Total Distance": format_decimal(total_distance, 1),
            "Avg. Calories per Minute": format_decimal(avg_calories_per_minute, 1),
            "Total Rides": str(total_rides),
            "Calories per Minute per Coach": calories_per_min_per_coach_str,
            "Total Mins per Coach": total_mins_per_coach_str,
        }
    
    measures = [
        "Total Mins",
        "Avg. Calories per Ride",
        "Total Distance",
        "Avg. Calories per Minute",
        "Total Rides",
        "Calories per Minute per Coach",
        "Total Mins per Coach"
    ]
    
    rows = []
    for measure in measures:
        row = {
            "Measure": measure,
            "2022": results_dict.get(2022, {}).get(measure, ""),
            "2021": results_dict.get(2021, {}).get(measure, ""),
        }
        rows.append(row)

    output_df = pd.DataFrame(rows, columns=["Measure", "2022", "2021"])
    
    return {"output_01.csv": output_df}


if __name__ == "__main__":
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    cand_dir = task_dir / "cand"
    cand_dir.mkdir(parents=True, exist_ok=True)
    
    outputs = solve(inputs_dir)
    for filename, df in outputs.items():
        df.to_csv(cand_dir / filename, index=False, encoding="utf-8")

