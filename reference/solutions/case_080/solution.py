from __future__ import annotations
from pathlib import Path
from typing import Dict
import pandas as pd
import numpy as np
from datetime import timedelta


def solve(inputs_dir: Path) -> Dict[str, pd.DataFrame]:
    daily_sales = pd.read_csv(inputs_dir / "input_01.csv")
    scent_info = pd.read_csv(inputs_dir / "input_02.csv")
    units_ordered = pd.read_csv(inputs_dir / "input_03.csv")
    
    daily_sales["Date"] = pd.to_datetime(daily_sales["Date"])
    units_ordered["Date"] = pd.to_datetime(units_ordered["Date"])
    
    daily_sales = daily_sales.merge(scent_info[["Scent Code", "Scent", "Price", "Cost"]], on="Scent Code", how="left")
    
    daily_sales["Units Sold"] = daily_sales["Daily Sales"] / daily_sales["Price"]
    
    def get_week_start(date):
        weekday = date.weekday()
        if weekday == 2:
            return date
        elif weekday < 2:
            days_back = weekday + 5
            return date - timedelta(days=days_back)
        else:
            days_back = weekday - 2
            return date - timedelta(days=days_back)
    
    daily_sales["Week Start"] = daily_sales["Date"].apply(get_week_start)
    
    weekly_summary = daily_sales.groupby(["Week Start", "Scent Code", "Scent", "Price", "Cost"]).agg({
        "Units Sold": "sum",
        "Daily Sales": "sum"
    }).reset_index()
    weekly_summary.columns = ["Week Start", "Scent Code", "Scent", "Price", "Cost", "Weekly Units Sold", "Weekly Sales"]
    
    units_ordered["Week Start"] = units_ordered["Date"]
    weekly_summary = weekly_summary.merge(units_ordered[["Week Start", "Units Ordered"]], on="Week Start", how="left")
    
    weekly_summary["Waste"] = weekly_summary["Units Ordered"] - weekly_summary["Weekly Units Sold"]
    weekly_summary["Waste Cost"] = weekly_summary["Cost"] * weekly_summary["Waste"]
    weekly_summary["Original Profit"] = weekly_summary["Weekly Sales"] - weekly_summary["Waste Cost"]
    
    avg_units_per_day = daily_sales.groupby("Scent Code")["Units Sold"].mean().reset_index()
    avg_units_per_day.columns = ["Scent Code", "Avg Units Per Day"]
    
    avg_units_per_day["Rounded Up"] = np.ceil(avg_units_per_day["Avg Units Per Day"])
    
    avg_units_per_day["Rounded to 10"] = (np.round(avg_units_per_day["Rounded Up"] / 10) * 10).astype(int)
    
    avg_units_per_day["New Units Per Week"] = avg_units_per_day["Rounded to 10"] * 7
    
    avg_units_per_day = avg_units_per_day.merge(scent_info[["Scent Code", "Scent", "Price", "Cost"]], on="Scent Code", how="left")
    
    results = []
    for _, row in avg_units_per_day.iterrows():
        scent_code = row["Scent Code"]
        scent = row["Scent"]
        price = row["Price"]
        cost = row["Cost"]
        new_units_per_week = row["New Units Per Week"]
        
        scent_weekly = weekly_summary[weekly_summary["Scent Code"] == scent_code].copy()
        
        scent_weekly["New Units Ordered"] = new_units_per_week
        scent_weekly["New Waste"] = scent_weekly["New Units Ordered"] - scent_weekly["Weekly Units Sold"]
        
        scent_weekly["New Waste Cost"] = scent_weekly.apply(
            lambda row: 0 if row["New Waste"] < 0 else row["New Waste"] * cost,
            axis=1
        )
        
        scent_weekly["Adjusted Weekly Sales"] = scent_weekly.apply(
            lambda row: row["New Units Ordered"] * price if row["New Waste"] < 0 else row["Weekly Sales"],
            axis=1
        )
        
        scent_weekly["New Profit"] = scent_weekly["Adjusted Weekly Sales"] - scent_weekly["New Waste Cost"]
        
        original_profit = scent_weekly["Original Profit"].sum()
        
        new_profit = scent_weekly["New Profit"].sum()
        
        difference = new_profit - original_profit
        
        results.append({
            "Scent": scent,
            "Total Profit": original_profit,
            "New Profit": new_profit,
            "Difference": difference
        })
    
    output = pd.DataFrame(results)
    
    output["Total Profit"] = output["Total Profit"].round(2)
    output["New Profit"] = output["New Profit"].round(2)
    output["Difference"] = output["Difference"].round(2)
    
    output = output.sort_values("Scent").reset_index(drop=True)
    
    return {"output_01.csv": output}


if __name__ == "__main__":
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    cand_dir = task_dir / "cand"
    cand_dir.mkdir(parents=True, exist_ok=True)

    outputs = solve(inputs_dir)
    for fname, df in outputs.items():
        df.to_csv(cand_dir / fname, index=False, encoding="utf-8")
