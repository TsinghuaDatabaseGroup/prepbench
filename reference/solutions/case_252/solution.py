from __future__ import annotations
import pandas as pd
from pathlib import Path


def solve(inputs_dir: Path) -> dict[str, pd.DataFrame]:
    
    input_csv = inputs_dir / "input_01.csv"
    df = pd.read_csv(input_csv)
    
    df["Max Monthly Deposit"] = df["Max Monthly Deposit"].str.replace("£", "", regex=False).astype(int)
    
    df["Provider"] = df.apply(
        lambda row: row["Provider"] + " (Conditions Apply)" 
        if pd.notna(row["Has Additional Conditions"]) and row["Has Additional Conditions"] == "Y"
        else row["Provider"],
        axis=1
    )
    
    df["Interest"] = df["Interest"].str.rstrip("%").astype(float) / 100
    
    df = df.drop(columns=["Has Additional Conditions"])
    
    months_list = []
    for _, row in df.iterrows():
        for month in range(1, 13):
            months_list.append({
                "Provider": row["Provider"],
                "Interest": row["Interest"],
                "Max Monthly Deposit": row["Max Monthly Deposit"],
                "Month": month
            })
    
    df_expanded = pd.DataFrame(months_list)
    
    df_expanded["Apply Interest"] = (
        df_expanded["Max Monthly Deposit"] * 
        (1 + df_expanded["Interest"] / 12) ** df_expanded["Month"]
    )
    
    
    def calculate_savings_each_month(group):
        group = group.sort_values("Month")
        savings = []
        for month in group["Month"]:
            total = 0
            for i in range(1, month + 1):
                months_interest = month - i + 1
                deposit_value = group.iloc[0]["Max Monthly Deposit"] * (1 + group.iloc[0]["Interest"] / 12) ** months_interest
                total += deposit_value
            savings.append(round(total, 2))
        group["Savings each month"] = savings
        return group
    
    df_expanded = df_expanded.groupby("Provider", group_keys=False).apply(calculate_savings_each_month)
    
    df_expanded["Max Possible Savings"] = df_expanded.groupby("Provider")["Savings each month"].transform("max")
    df_expanded["Max Possible Savings"] = df_expanded["Max Possible Savings"].round(2)
    
    df_expanded["Total Interest"] = (
        df_expanded["Max Possible Savings"] - 
        (df_expanded["Max Monthly Deposit"] * 12)
    )
    df_expanded["Total Interest"] = df_expanded["Total Interest"].round(2)
    
    df_expanded = df_expanded.drop(columns=["Apply Interest"])
    
    provider_summary = df_expanded.groupby("Provider").agg({
        "Max Possible Savings": "first",
        "Total Interest": "first"
    }).reset_index()
    
    provider_summary["Providers Ranked by Max Savings"] = (
        provider_summary["Max Possible Savings"]
        .rank(method="dense", ascending=False)
        .astype(int)
    )
    provider_summary["Providers Ranked by Total Interest"] = (
        provider_summary["Total Interest"]
        .rank(method="dense", ascending=False)
        .astype(int)
    )
    
    df_expanded = df_expanded.merge(
        provider_summary[["Provider", "Providers Ranked by Max Savings", "Providers Ranked by Total Interest"]],
        on="Provider",
        how="left"
    )
    
    df_expanded = df_expanded.sort_values(
        by=["Providers Ranked by Total Interest", "Month"],
        ascending=[True, True]
    )
    df_expanded["Sort"] = range(1, len(df_expanded) + 1)
    
    output_columns = [
        "Providers Ranked by Max Savings",
        "Providers Ranked by Total Interest",
        "Provider",
        "Interest",
        "Max Monthly Deposit",
        "Month",
        "Savings each month",
        "Max Possible Savings",
        "Total Interest",
        "Sort"
    ]
    
    result_df = df_expanded[output_columns].copy()
    
    return {
        "output_01.csv": result_df
    }


if __name__ == "__main__":
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    cand_dir = task_dir / "cand"
    cand_dir.mkdir(parents=True, exist_ok=True)
    
    results = solve(inputs_dir)
    for fname, df in results.items():
        df.to_csv(cand_dir / fname, index=False, encoding="utf-8")

