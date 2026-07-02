import pandas as pd
from pathlib import Path


def solve(inputs_dir: Path) -> dict[str, pd.DataFrame]:
    dates_df = pd.read_csv(inputs_dir / "input_06.csv")
    date_strings = dates_df["Dates"].tolist()
    if len(date_strings) == 5:
        date_strings = [date_strings[4], date_strings[0], date_strings[3], date_strings[1], date_strings[2]]

    clapham_files = [f"input_{i:02d}.csv" for i in range(1, 6)]
    wimbledon_files = [f"input_{i:02d}.csv" for i in range(7, 12)]

    all_dfs: list[pd.DataFrame] = []

    for file, date_str in zip(clapham_files, date_strings):
        df = pd.read_csv(inputs_dir / file)
        df["Store"] = "Clapham"
        df["Dates"] = date_str
        all_dfs.append(df)

    for file, date_str in zip(wimbledon_files, date_strings):
        df = pd.read_csv(inputs_dir / file)
        df["Store"] = "Wimbledon"
        df["Dates"] = date_str
        all_dfs.append(df)

    full_data = pd.concat(all_dfs, ignore_index=True)
    full_data = full_data.drop_duplicates()

    store_totals = full_data.groupby("Store").agg(
        Total_Volume=("Sales Volume", "sum"),
        Total_Value=("Sales Value", "sum"),
    ).reset_index()

    scent_sales = (
        full_data.groupby(["Store", "Scent"]).agg(
            Scent_Volume=("Sales Volume", "sum"),
            Scent_Value=("Sales Value", "sum"),
        ).reset_index()
    )
    scent_sales = scent_sales.merge(store_totals, on="Store", how="left")
    scent_sales["Scent % of Store Sales Volumes"] = (scent_sales["Scent_Volume"] / scent_sales["Total_Volume"]).round(2)
    scent_sales["Scent % of Store Sales Values"] = (scent_sales["Scent_Value"] / scent_sales["Total_Value"]).round(2)

    output_01 = scent_sales[[
        "Store",
        "Scent",
        "Scent % of Store Sales Volumes",
        "Scent % of Store Sales Values",
    ]]

    daily_sales = (
        full_data.groupby(["Store", "Dates"]).agg(
            Daily_Volume=("Sales Volume", "sum"),
            Daily_Value=("Sales Value", "sum"),
        ).reset_index()
    )
    daily_sales = daily_sales.merge(store_totals, on="Store", how="left")
    daily_sales["Weekday % of Store Sales Volumes"] = (daily_sales["Daily_Volume"] / daily_sales["Total_Volume"]).round(2)
    daily_sales["Weekday % of Store Sales Value"] = (daily_sales["Daily_Value"] / daily_sales["Total_Value"]).round(2)

    output_02 = daily_sales[[
        "Store",
        "Dates",
        "Weekday % of Store Sales Volumes",
        "Weekday % of Store Sales Value",
    ]]

    return {
        "output_01.csv": output_01,
        "output_02.csv": output_02,
    }


if __name__ == "__main__":
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    cand_dir = task_dir / "cand"

    cand_dir.mkdir(exist_ok=True)

    results = solve(inputs_dir)
    for filename, df in results.items():
        (cand_dir / filename).parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(cand_dir / filename, index=False, encoding="utf-8")
