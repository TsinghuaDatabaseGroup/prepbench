import pandas as pd
from pathlib import Path


def solve(inputs_dir: Path) -> dict[str, pd.DataFrame]:
    input_file = inputs_dir / "input_01.csv"
    df = pd.read_csv(input_file)
    
    product_parts = df["Product Name"].str.split(" - ", n=1, expand=True)
    df["Product Type"] = product_parts[0]
    df["Size"] = product_parts[1]
    
    df = df[df["Product Type"] == "Liquid"].copy()
    
    aggregated = df.groupby(["Store Name", "Size", "Scent Name"], as_index=False)["Sale Value"].sum()
    
    aggregated["Rank of Product & Scent by Store"] = aggregated.groupby("Store Name")["Sale Value"].rank(
        method="dense", ascending=False
    ).astype(int)
    
    top10 = aggregated[aggregated["Rank of Product & Scent by Store"] <= 10].copy()
    
    top10["Sale Value"] = (top10["Sale Value"] / 10).round() * 10
    
    output_cols = ["Store Name", "Rank of Product & Scent by Store", "Scent Name", "Size", "Sale Value"]
    top10 = top10[output_cols].copy()
    
    top10 = top10.sort_values(["Store Name", "Rank of Product & Scent by Store"])
    
    store_order = ["Chelsea", "Dulwich", "Lewisham", "Notting Hill", "Shoreditch", "Wimbledon"]
    
    result = {}
    for idx, store_name in enumerate(store_order, start=1):
        store_data = top10[top10["Store Name"] == store_name].copy()
        store_data["Rank of Product & Scent by Store"] = store_data["Rank of Product & Scent by Store"].astype(int)
        store_data["Sale Value"] = store_data["Sale Value"].astype(int)
        store_data = store_data.sort_values("Rank of Product & Scent by Store").reset_index(drop=True)
        result[f"output_{idx:02d}.csv"] = store_data
    
    return result


if __name__ == "__main__":
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    cand_dir = task_dir / "cand"
    cand_dir.mkdir(parents=True, exist_ok=True)
    
    outputs = solve(inputs_dir)
    for filename, df in outputs.items():
        df.to_csv(cand_dir / filename, index=False, encoding="utf-8")

