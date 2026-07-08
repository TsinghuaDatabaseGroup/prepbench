import pandas as pd
from pathlib import Path
from datetime import datetime

def solve(inputs_dir: Path) -> dict[str, pd.DataFrame]:
    transactions_file = inputs_dir / "input_01.csv"
    df_trans = pd.read_csv(transactions_file)
    
    targets_file = inputs_dir / "input_02.csv"
    df_targets = pd.read_csv(targets_file)
    
    df_trans = df_trans[df_trans["Transaction Code"].str.contains("DSB", case=False, na=False)]
    
    df_trans["Online or In-Person"] = df_trans["Online or In-Person"].map({1: "Online", 2: "In-Person"})
    
    df_trans["Transaction Date"] = pd.to_datetime(df_trans["Transaction Date"], format="%d/%m/%Y %H:%M:%S")
    df_trans["Quarter"] = df_trans["Transaction Date"].dt.quarter
    
    df_trans_summary = df_trans.groupby(["Online or In-Person", "Quarter"])["Value"].sum().reset_index()
    df_trans_summary.rename(columns={"Value": "Value"}, inplace=True)
    
    df_targets_pivoted = df_targets.melt(
        id_vars=["Online or In-Person"],
        value_vars=["Q1", "Q2", "Q3", "Q4"],
        var_name="Quarter_str",
        value_name="Quarterly Targets"
    )
    
    df_targets_pivoted["Quarter"] = df_targets_pivoted["Quarter_str"].str.replace("Q", "").astype(int)
    
    df_targets_pivoted = df_targets_pivoted[["Online or In-Person", "Quarter", "Quarterly Targets"]]
    
    df_result = pd.merge(
        df_trans_summary,
        df_targets_pivoted,
        on=["Online or In-Person", "Quarter"],
        how="inner"
    )
    
    df_result["Variance to Target"] = df_result["Value"] - df_result["Quarterly Targets"]
    
    df_result = df_result[[
        "Online or In-Person",
        "Quarter",
        "Value",
        "Quarterly Targets",
        "Variance to Target"
    ]]
    
    df_result["Quarter"] = df_result["Quarter"].astype(int)
    df_result["Value"] = df_result["Value"].astype(int)
    df_result["Quarterly Targets"] = df_result["Quarterly Targets"].astype(int)
    df_result["Variance to Target"] = df_result["Variance to Target"].astype(int)
    
    df_result = df_result.sort_values(["Online or In-Person", "Quarter"], ascending=[False, True])
    
    return {
        "output_01.csv": df_result.reset_index(drop=True)
    }

if __name__ == "__main__":
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    cand_dir = task_dir / "cand"
    cand_dir.mkdir(parents=True, exist_ok=True)
    
    outputs = solve(inputs_dir)
    for filename, df in outputs.items():
        output_path = cand_dir / filename
        df.to_csv(output_path, index=False, encoding="utf-8")

