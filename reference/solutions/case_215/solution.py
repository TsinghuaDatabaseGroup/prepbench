from __future__ import annotations
import pandas as pd
from pathlib import Path


def solve(inputs_dir: Path) -> dict[str, pd.DataFrame]:
    uk_customers = pd.read_csv(inputs_dir / "input_01.csv")
    roi_customers = pd.read_csv(inputs_dir / "input_02.csv")
    uk_holidays = pd.read_csv(inputs_dir / "input_03.csv")
    
    uk_holidays = uk_holidays.copy()
    uk_holidays["Year"] = uk_holidays["Year"].ffill()
    uk_holidays = uk_holidays[uk_holidays["Date"].notna()].copy()
    uk_holidays["Date"] = pd.to_datetime(uk_holidays["Date"])
    uk_holidays["UK Bank Holiday"] = pd.to_datetime(
        uk_holidays["Year"].astype(int).astype(str) + "-" + 
        uk_holidays["Date"].dt.strftime("%m-%d")
    )
    uk_holidays = uk_holidays[["UK Bank Holiday"]].drop_duplicates()
    
    uk_customers["Date"] = pd.to_datetime(uk_customers["Date"])
    
    uk_customers = uk_customers.merge(
        uk_holidays, 
        left_on="Date", 
        right_on="UK Bank Holiday", 
        how="left"
    )
    
    uk_customers["Day"] = uk_customers["Date"].dt.day_name()
    
    uk_customers["Reporting Day"] = uk_customers.apply(
        lambda row: "N" if str(row["Day"]).startswith("S") 
        else ("Y" if pd.isna(row["UK Bank Holiday"]) else "N"),
        axis=1
    )
    
    min_date = uk_customers["Date"].min()
    max_date = uk_customers["Date"].max()
    all_dates = pd.date_range(start=min_date, end=max_date, freq="D")
    all_dates_df = pd.DataFrame({"Date": all_dates})
    all_dates_df["Day"] = all_dates_df["Date"].dt.day_name()
    all_dates_df = all_dates_df.merge(uk_holidays, left_on="Date", right_on="UK Bank Holiday", how="left")
    all_dates_df["Reporting Day"] = all_dates_df.apply(
        lambda row: "N" if str(row["Day"]).startswith("S")
        else ("Y" if pd.isna(row["UK Bank Holiday"]) else "N"),
        axis=1
    )
    
    reporting_dates = all_dates_df[all_dates_df["Reporting Day"] == "Y"]["Date"].sort_values()
    
    def find_next_reporting_date(date):
        next_dates = reporting_dates[reporting_dates >= date]
        if len(next_dates) > 0:
            return next_dates.iloc[0]
        return date
    
    uk_customers["Reporting Date"] = uk_customers["Date"].apply(find_next_reporting_date)
    
    uk_agg = uk_customers.groupby("Reporting Date", as_index=False)["New Customers"].sum()
    
    uk_agg["Month"] = uk_agg["Reporting Date"].dt.to_period("M").dt.to_timestamp()
    last_day_per_month = uk_agg.groupby("Month")["Reporting Date"].max().reset_index()
    last_day_per_month.columns = ["Month", "Last Day"]
    uk_agg = uk_agg.merge(last_day_per_month, on="Month", how="left")
    
    def get_reporting_month(row):
        if row["Reporting Date"] < row["Last Day"]:
            month_name = row["Reporting Date"].strftime("%B")
            year = row["Reporting Date"].year
            return f"{month_name}-{year}"
        else:
            next_month = row["Reporting Date"] + pd.DateOffset(months=1)
            month_name = next_month.strftime("%B")
            year = next_month.year
            return f"{month_name}-{year}"
    
    uk_agg["Reporting Month"] = uk_agg.apply(get_reporting_month, axis=1)
    
    uk_agg = uk_agg[uk_agg["Reporting Month"] != "January-2024"].copy()
    
    uk_agg = uk_agg.sort_values(["Reporting Month", "Reporting Date"])
    uk_agg["Reporting Day"] = uk_agg.groupby("Reporting Month").cumcount() + 1
    
    roi_customers["Reporting Date"] = pd.to_datetime(roi_customers["Reporting Date"])
    roi_customers["Reporting Month"] = pd.to_datetime(roi_customers["Reporting Month"])
    def format_roi_month_from_date(date_val):
        if pd.isna(date_val):
            return ""
        month_map = {
            1: "Jan", 2: "Feb", 3: "Mar", 4: "Apr", 5: "May", 6: "Jun",
            7: "Jul", 8: "Aug", 9: "Sept", 10: "Oct", 11: "Nov", 12: "Dec"
        }
        month_abbr = month_map[date_val.month]
        year_short = str(date_val.year)[-2:]
        return f"{month_abbr}-{year_short}"
    
    roi_customers["Reporting Month"] = roi_customers["Reporting Month"].apply(format_roi_month_from_date)
    
    roi_renamed = roi_customers.rename(columns={
        "Reporting Month": "ROI Reporting Month",
        "Reporting Day": "ROI Reporting Day",
        "New Customers": "ROI New Customers"
    })
    
    roi_renamed["ROI Reporting Date"] = roi_renamed["Reporting Date"]
    roi_renamed["Reporting Date"] = roi_renamed["ROI Reporting Date"].apply(find_next_reporting_date)
    
    roi_agg = roi_renamed.groupby("Reporting Date", as_index=False).agg({
        "ROI New Customers": "sum",
        "ROI Reporting Month": "first"
    })
    
    result = roi_agg.merge(
        uk_agg,
        on="Reporting Date",
        how="right"
    )
    
    
    result["New Customers"] = result["New Customers"].fillna(0).astype(int)
    result["ROI New Customers"] = result["ROI New Customers"].fillna(0).astype(int)
    
    result = result[~result["Reporting Date"].isin([pd.Timestamp("2023-12-29"), pd.Timestamp("2023-12-30")])].copy()
    
    def get_misalignment_flag(row):
        if pd.isna(row["ROI Reporting Month"]) or str(row["ROI Reporting Month"]) == "nan":
            return "X"
        uk_month_prefix = str(row["Reporting Month"])[:3] if pd.notna(row["Reporting Month"]) else ""
        roi_month_prefix = str(row["ROI Reporting Month"])[:3] if pd.notna(row["ROI Reporting Month"]) else ""
        if uk_month_prefix != roi_month_prefix:
            return "X"
        return ""
    
    result["Misalignment Flag"] = result.apply(get_misalignment_flag, axis=1)
    
    result["Reporting Date_temp"] = result["Reporting Date"]
    result["Reporting Date"] = result["Reporting Date"].dt.strftime("%d/%m/%Y")
    
    result["ROI Reporting Month"] = result["ROI Reporting Month"].fillna("")
    
    result = result.sort_values("Reporting Date_temp")
    
    output = result[[
        "Misalignment Flag",
        "Reporting Month",
        "Reporting Day",
        "Reporting Date",
        "New Customers",
        "ROI New Customers",
        "ROI Reporting Month"
    ]].copy()
    
    output["Reporting Day"] = output["Reporting Day"].astype(int)
    output["New Customers"] = output["New Customers"].astype(int)
    output["ROI New Customers"] = output["ROI New Customers"].astype(int)
    
    return {
        "output_01.csv": output.reset_index(drop=True)
    }


if __name__ == "__main__":
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    cand_dir = task_dir / "cand"
    cand_dir.mkdir(parents=True, exist_ok=True)

    results = solve(inputs_dir)
    for fname, df in results.items():
        (cand_dir / fname).parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(cand_dir / fname, index=False, encoding="utf-8")
