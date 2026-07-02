import pandas as pd
from pathlib import Path
from datetime import datetime

def solve(inputs_dir: Path) -> dict[str, pd.DataFrame]:
    df = pd.read_csv(inputs_dir / "input_01.csv")
    
    df = df[df["Poll"] != "RCP Average"].copy()
    
    def parse_end_date(date_str):
        if pd.isna(date_str):
            return None
        end_date_str = date_str.split(" - ")[-1].strip()
        try:
            parts = end_date_str.split("/")
            month = int(parts[0])
            day = int(parts[1])
            year = 2019 if month == 12 else 2020
            dt = datetime(year, month, day)
            return dt.strftime("%d/%m/%Y")
        except:
            return None
    
    df["End Date"] = df["Date"].apply(parse_end_date)
    
    def parse_sample_type(sample_str):
        if pd.isna(sample_str) or sample_str == "--":
            return "Unknown"
        sample_str = str(sample_str).strip()
        if "LV" in sample_str.upper():
            return "Likely Voter"
        elif "RV" in sample_str.upper():
            return "Registered Voter"
        else:
            return "Unknown"
    
    df["Sample Type"] = df["Sample"].apply(parse_sample_type)
    
    candidate_cols = ["Sanders", "Biden", "Bloomberg", "Warren", "Buttigieg", "Klobuchar", "Steyer", "Gabbard"]
    
    id_vars = ["Poll", "End Date", "Sample Type"]
    df_melted = df.melt(
        id_vars=id_vars,
        value_vars=candidate_cols,
        var_name="Candidate",
        value_name="Poll Results"
    )
    
    df_melted = df_melted[df_melted["Poll Results"].notna()].copy()
    df_melted = df_melted[df_melted["Poll Results"] != "--"].copy()
    
    df_melted["Poll Results"] = pd.to_numeric(df_melted["Poll Results"], errors="coerce")
    df_melted = df_melted[df_melted["Poll Results"].notna()].copy()
    
    df_melted["Rank"] = df_melted.groupby(["Poll", "End Date"])["Poll Results"].rank(method="max", ascending=False).astype(int)
    
    def calculate_spread(group):
        poll_results = group["Poll Results"].sort_values(ascending=False).values
        if len(poll_results) >= 2:
            spread = poll_results[0] - poll_results[1]
        else:
            spread = 0
        group = group.copy()
        group["Spread from 1st to 2nd Place"] = spread
        return group
    
    df_melted = df_melted.groupby(["Poll", "End Date"], group_keys=False).apply(calculate_spread).reset_index(drop=True)
    
    result = df_melted[[
        "Candidate",
        "Poll Results",
        "Spread from 1st to 2nd Place",
        "Rank",
        "End Date",
        "Sample Type",
        "Poll"
    ]].copy()
    
    result["Poll Results"] = result["Poll Results"].astype(float)
    result["Spread from 1st to 2nd Place"] = result["Spread from 1st to 2nd Place"].astype(float)
    result["Rank"] = result["Rank"].astype(int)
    
    result["_sort_date"] = pd.to_datetime(result["End Date"], format="%d/%m/%Y")
    result = result.sort_values(
        by=["_sort_date", "Poll", "Rank", "Candidate"],
        ascending=[True, True, True, True]
    ).reset_index(drop=True)
    result = result.drop(columns=["_sort_date"])
    
    return {"output_01.csv": result}

if __name__ == "__main__":
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    cand_dir = task_dir / "cand"
    cand_dir.mkdir(parents=True, exist_ok=True)
    
    outputs = solve(inputs_dir)
    for filename, df in outputs.items():
        df.to_csv(cand_dir / filename, index=False, encoding="utf-8")

