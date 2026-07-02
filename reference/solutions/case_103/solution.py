from __future__ import annotations
import pandas as pd
from pathlib import Path


def solve(inputs_dir: Path) -> dict[str, pd.DataFrame]:
    store_files = [
        inputs_dir / "input_01.csv",
        inputs_dir / "input_02.csv",
        inputs_dir / "input_03.csv",
        inputs_dir / "input_04.csv",
        inputs_dir / "input_05.csv",
    ]
    
    store_names = ["Manchester", "London", "Leeds", "York", "Birmingham"]
    
    dfs = []
    for i, file_path in enumerate(store_files):
        df = pd.read_csv(file_path)
        df["Store"] = store_names[i]
        dfs.append(df)
    
    union_df = pd.concat(dfs, ignore_index=True)
    
    id_vars = ["Date", "Store"]
    value_vars = [col for col in union_df.columns if col not in id_vars]
    
    pivoted_df = union_df.melt(
        id_vars=id_vars,
        value_vars=value_vars,
        var_name="Customer Type - Product",
        value_name="Products Sold"
    )
    
    split_cols = pivoted_df["Customer Type - Product"].str.split(" - ", n=1, expand=True)
    pivoted_df["Customer Type"] = split_cols[0]
    pivoted_df["Product"] = split_cols[1]
    
    pivoted_df = pivoted_df.drop(columns=["Customer Type - Product", "Customer Type"])
    
    pivoted_df["Date"] = pd.to_datetime(pivoted_df["Date"])
    pivoted_df["Quarter"] = pivoted_df["Date"].dt.quarter
    
    aggregated_df = pivoted_df.groupby(["Store", "Quarter"], as_index=False)["Products Sold"].sum()
    
    targets_df = pd.read_csv(inputs_dir / "input_06.csv")
    
    result_df = aggregated_df.merge(
        targets_df,
        on=["Store", "Quarter"],
        how="inner"
    )
    
    result_df["Variance to Target"] = result_df["Products Sold"] - result_df["Target"]
    
    result_df["Rank"] = result_df.groupby("Quarter")["Variance to Target"].rank(
        method="dense",
        ascending=False
    ).astype(int)
    
    output_df = result_df[[
        "Quarter",
        "Rank",
        "Store",
        "Products Sold",
        "Target",
        "Variance to Target"
    ]].copy()
    
    output_df["Quarter"] = output_df["Quarter"].astype(int)
    output_df["Rank"] = output_df["Rank"].astype(int)
    output_df["Products Sold"] = output_df["Products Sold"].astype(int)
    output_df["Target"] = output_df["Target"].astype(int)
    output_df["Variance to Target"] = output_df["Variance to Target"].astype(int)
    
    output_df = output_df.sort_values(["Quarter", "Rank"]).reset_index(drop=True)
    
    return {
        "output_01.csv": output_df,
    }


if __name__ == "__main__":
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    cand_dir = task_dir / "cand"
    cand_dir.mkdir(parents=True, exist_ok=True)
    
    results = solve(inputs_dir)
    for fname, df in results.items():
        df.to_csv(cand_dir / fname, index=False, encoding="utf-8")

