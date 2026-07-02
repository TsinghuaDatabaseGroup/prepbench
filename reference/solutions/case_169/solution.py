import pandas as pd
from pathlib import Path
import re
from datetime import datetime


def solve(inputs_dir: Path) -> dict[str, pd.DataFrame]:
    input_file = inputs_dir / "input_01.csv"
    df = pd.read_csv(input_file)

    region_col = "Region"
    value_cols = [col for col in df.columns if col != region_col]

    df_melted = df.melt(
        id_vars=[region_col],
        value_vars=value_cols,
        var_name="column_name",
        value_name="value"
    )

    def parse_column_name(col_name):
        parts = col_name.split("___")
        if len(parts) == 3:
            bike_type = parts[0]
            month_str = parts[1]
            measure = parts[2]
            return bike_type, month_str, measure
        return None, None, None

    parsed = df_melted["column_name"].apply(parse_column_name)
    df_melted["Bike Type"] = [p[0] for p in parsed]
    df_melted["Month_str"] = [p[1] for p in parsed]
    df_melted["Measure"] = [p[2] for p in parsed]

    month_map = {
        "Jan": "01", "Feb": "02", "Mar": "03", "Apr": "04",
        "May": "05", "Jun": "06", "Jul": "07", "Aug": "08",
        "Sep": "09", "Oct": "10", "Nov": "11", "Dec": "12"
    }

    def convert_month(month_str):
        if pd.isna(month_str):
            return None
        match = re.match(r"([A-Za-z]+)_(\d+)", month_str)
        if match:
            month_abbr = match.group(1)
            year_suffix = match.group(2)
            month_num = month_map.get(month_abbr, "01")
            year = f"20{year_suffix}"
            return f"01/{month_num}/{year}"
        return None

    df_melted["Month"] = df_melted["Month_str"].apply(convert_month)

    df_sales = df_melted[df_melted["Measure"] == "Sales"].copy()
    df_profit = df_melted[df_melted["Measure"] == "Profit"].copy()

    df_sales = df_sales.rename(columns={"value": "Sales"})
    df_profit = df_profit.rename(columns={"value": "Profit"})

    df_merged = pd.merge(
        df_sales[["Bike Type", "Region", "Month", "Sales"]],
        df_profit[["Bike Type", "Region", "Month", "Profit"]],
        on=["Bike Type", "Region", "Month"],
        how="inner"
    )

    result = df_merged[["Bike Type", "Region",
                        "Month", "Sales", "Profit"]].copy()

    result["Sales"] = pd.to_numeric(result["Sales"], errors="coerce").round(9)
    result["Profit"] = pd.to_numeric(
        result["Profit"], errors="coerce").round(9)

    result = result.sort_values(
        by=["Bike Type", "Region", "Month"]).reset_index(drop=True)

    return {
        "output_01.csv": result
    }


if __name__ == "__main__":
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    cand_dir = task_dir / "cand"
    cand_dir.mkdir(parents=True, exist_ok=True)

    outputs = solve(inputs_dir)
    for filename, df in outputs.items():
        df.to_csv(cand_dir / filename, index=False, encoding="utf-8")
