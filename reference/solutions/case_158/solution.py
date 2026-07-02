import pandas as pd
from pathlib import Path
from decimal import Decimal, ROUND_HALF_UP


def solve(inputs_dir: Path) -> dict[str, pd.DataFrame]:
    
    people = pd.read_csv(inputs_dir / "input_13.csv")
    leaders = pd.read_csv(inputs_dir / "input_14.csv")
    locations = pd.read_csv(inputs_dir / "input_15.csv")
    goals = pd.read_csv(inputs_dir / "input_16.csv")
    dates = pd.read_csv(inputs_dir / "input_17.csv")
    
    people_joined = people.merge(
        locations, on="Location ID", how="left"
    ).merge(
        leaders, left_on="Leader 1", right_on="id", how="left", suffixes=("", "_leader")
    )
    
    people_joined["Agent Name"] = (
        people_joined["last_name"] + ", " + people_joined["first_name"]
    )
    people_joined["Leader Name"] = (
        people_joined["last_name_leader"] + ", " + people_joined["first_name_leader"]
    )
    
    people_final = people_joined[[
        "id", "Agent Name", "Leader 1", "Leader Name", "Location"
    ]].copy()
    
    dates["Month Start Date"] = pd.to_datetime(dates["Month Start Date"])
    dates_2021 = dates[dates["Month Start Date"].dt.year == 2021].copy()
    dates_2021["Month Start Date"] = dates_2021["Month Start Date"].dt.strftime("%d/%m/%Y")
    
    people_dates = people_final.assign(key=1).merge(
        dates_2021.assign(key=1), on="key"
    ).drop("key", axis=1)
    
    monthly_data_list = []
    
    for month_idx in range(1, 13):
        file_path = inputs_dir / f"input_{month_idx:02d}.csv"
        df = pd.read_csv(file_path)
        
        if "Calls Offered" in df.columns:
            df = df.rename(columns={
                "Calls Offered": "Offered",
                "Calls Not Answered": "Not Answered",
                "Calls Answered": "Answered"
            })
            df["Transfers"] = pd.NA
        
        month_date = pd.Timestamp(f"2021-{month_idx:02d}-01").strftime("%d/%m/%Y")
        df["Month Start Date"] = month_date
        
        df = df.rename(columns={"AgentID": "id"})
        
        monthly_data_list.append(df)
    
    monthly_data = pd.concat(monthly_data_list, ignore_index=True)
    
    result = people_dates.merge(
        monthly_data,
        on=["id", "Month Start Date"],
        how="left"
    )
    
    metric_cols = ["Answered", "Not Answered", "Offered", "Total Duration", "Sentiment"]
    
    all_metrics_na = result[metric_cols].isna().all(axis=1)
    
    for col in metric_cols:
        if col in result.columns:
            result.loc[~all_metrics_na, col] = result.loc[~all_metrics_na, col].fillna(0)
            result[col] = result[col].astype("Int64")
    
    if "Transfers" in result.columns:
        result.loc[all_metrics_na, "Transfers"] = pd.NA
    
    result = result.rename(columns={
        "Answered": "Calls Answered",
        "Not Answered": "Calls Not Answered",
        "Offered": "Calls Offered"
    })
    
    result["Not Answered Percent < 5"] = 5
    result["Sentiment Score >= 0"] = 0
    
    def round_to_3_decimals(val):
        if pd.isna(val):
            return pd.NA
        return float(Decimal(str(val)).quantize(Decimal('0.001'), rounding=ROUND_HALF_UP))
    
    result["Not Answered Rate"] = (
        result["Calls Not Answered"] / result["Calls Offered"]
    ).apply(round_to_3_decimals)
    
    def round_to_int(val):
        if pd.isna(val):
            return pd.NA
        return int(Decimal(str(val)).quantize(Decimal('1'), rounding=ROUND_HALF_UP))
    
    result["Agent Avg Duration"] = pd.NA
    mask = result["Calls Answered"].notna() & (result["Calls Answered"] > 0)
    if mask.any():
        result.loc[mask, "Agent Avg Duration"] = (
            result.loc[mask, "Total Duration"] / result.loc[mask, "Calls Answered"]
        ).apply(round_to_int).astype("Int64")
    mask_zero = result["Calls Answered"].notna() & (result["Calls Answered"] == 0)
    if mask_zero.any():
        result.loc[mask_zero, "Agent Avg Duration"] = 0
    
    result["Met Not Answered Rate"] = pd.NA
    mask = result["Not Answered Rate"].notna()
    result.loc[mask, "Met Not Answered Rate"] = result.loc[mask, "Not Answered Rate"] < (5 / 100)
    
    result["Met Sentiment Goal"] = pd.NA
    mask = result["Sentiment"].notna()
    result.loc[mask, "Met Sentiment Goal"] = result.loc[mask, "Sentiment"] >= 0
    
    output_cols = [
        "id",
        "Agent Name",
        "Leader 1",
        "Leader Name",
        "Month Start Date",
        "Location",
        "Calls Answered",
        "Calls Not Answered",
        "Not Answered Rate",
        "Met Not Answered Rate",
        "Not Answered Percent < 5",
        "Calls Offered",
        "Total Duration",
        "Agent Avg Duration",
        "Transfers",
        "Sentiment",
        "Sentiment Score >= 0",
        "Met Sentiment Goal"
    ]
    
    result = result[output_cols].copy()
    
    result["Met Not Answered Rate"] = result["Met Not Answered Rate"].astype("boolean")
    result["Met Sentiment Goal"] = result["Met Sentiment Goal"].astype("boolean")
    
    result["_sort_date"] = pd.to_datetime(result["Month Start Date"], format="%d/%m/%Y")
    result = result.sort_values(["id", "_sort_date"], ascending=[True, False]).reset_index(drop=True)
    result = result.drop("_sort_date", axis=1)
    
    return {"output_01.csv": result}


if __name__ == "__main__":
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    cand_dir = task_dir / "cand"
    cand_dir.mkdir(parents=True, exist_ok=True)
    
    outputs = solve(inputs_dir)
    for filename, df in outputs.items():
        if "Month Start Date" in df.columns:
            df["Month Start Date"] = df["Month Start Date"].astype(str)
        df.to_csv(cand_dir / filename, index=False, encoding="utf-8", na_rep="")

