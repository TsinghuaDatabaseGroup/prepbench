import pandas as pd
from pathlib import Path

def solve(inputs_dir: Path) -> dict[str, pd.DataFrame]:
    opp_df = pd.read_csv(inputs_dir / "input_02.csv")
    
    opp_df = opp_df[["Id", "CreatedDate", "CloseDate", "StageName"]].copy()
    
    opp_df.rename(columns={"Id": "OppID"}, inplace=True)
    
    opened_df = opp_df[["OppID", "CreatedDate", "StageName"]].copy()
    opened_df["Date"] = opened_df["CreatedDate"]
    opened_df["Stage"] = "Opened"
    opened_df["SortOrder"] = 0
    opened_df = opened_df[["OppID", "Date", "Stage", "SortOrder"]]
    
    not_closed_df = opp_df[~opp_df["StageName"].isin(["Closed Won", "Closed Lost"])].copy()
    close_df = not_closed_df[["OppID", "CloseDate", "StageName"]].copy()
    close_df["Date"] = close_df["CloseDate"]
    close_df["Stage"] = "ExpectedCloseDate"
    close_df["SortOrder"] = 11
    close_df = close_df[["OppID", "Date", "Stage", "SortOrder"]]
    
    opp_result = pd.concat([opened_df, close_df], ignore_index=True)
    
    history_df = pd.read_csv(inputs_dir / "input_01.csv")
    
    history_df.rename(columns={"CreatedDate": "Date", "StageName": "Stage"}, inplace=True)
    
    history_df = history_df[["OppID", "Date", "Stage", "SortOrder"]]
    
    combined_df = pd.concat([opp_result, history_df], ignore_index=True)
    
    combined_df = combined_df.drop_duplicates(subset=["OppID", "Date", "Stage", "SortOrder"], keep="first")
    
    combined_df = combined_df.reset_index(drop=True)
    
    return {
        "output_01.csv": combined_df
    }

if __name__ == "__main__":
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    cand_dir = task_dir / "cand"
    cand_dir.mkdir(parents=True, exist_ok=True)
    
    outputs = solve(inputs_dir)
    for filename, df in outputs.items():
        df.to_csv(cand_dir / filename, index=False, encoding="utf-8")

