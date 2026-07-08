import pandas as pd
from pathlib import Path


def solve(inputs_dir: Path) -> dict[str, pd.DataFrame]:
    
    info = pd.read_csv(inputs_dir / "input_01.csv", skiprows=1)
    info = info[~info["Surf Site"].str.contains("*", na=False, regex=False)]
    info = info[info["Surf Site"].notna()].copy()
    info["Surf Site"] = info["Surf Site"].str.strip()
    
    location = pd.read_csv(inputs_dir / "input_02.csv")
    location["Surf Site"] = location["Site"].str.replace(" - South Devon", "", regex=False)
    
    preppers = pd.read_csv(inputs_dir / "input_03.csv")
    preppers["Skill"] = preppers["Skill"].str.strip()
    
    info_location = info.merge(
        location[["Surf Site", "Surf Season"]],
        on="Surf Site",
        how="left"
    )
    
    matches = []
    
    for _, person in preppers.iterrows():
        person_name = person["Name"]
        person_skill = person["Skill"]
        person_season = person["Season"]
        person_board = person["Board Type"]
        
        for _, site in info_location.iterrows():
            skill_levels = str(site["Skill Level"]).split(", ")
            skill_match = person_skill in skill_levels
            
            person_seasons = set(s.strip() for s in str(person_season).split(","))
            surf_seasons = set(s.strip() for s in str(site["Surf Season"]).split(","))
            season_match = len(person_seasons & surf_seasons) > 0
            
            person_boards = set(s.strip() for s in str(person_board).split(","))
            site_boards = set(s.strip() for s in str(site["Boards"]).split(","))
            board_match = len(person_boards & site_boards) > 0
            
            if skill_match and season_match and board_match:
                matches.append({
                    "Name": person_name,
                    "Surf Site": site["Surf Site"],
                    "Swell Direction": site["Swell Direction"],
                    "Reliability": site["Reliability"],
                    "Wind Direction": site["Wind Direction"],
                    "Type": site["Type"],
                    "Boards": site["Boards"],
                    "Skill Level": site["Skill Level"],
                    "Surf Season": site["Surf Season"],
                    "Rating": site["Rating"]
                })
    
    result_df = pd.DataFrame(matches)
    
    result_df = result_df.drop_duplicates(subset=["Name", "Surf Site"])
    
    reliability_order = {
        "Rarely Breaks": 1,
        "Inconsistent": 2,
        "Fairly Inconsistent": 3,
        "Fairly Consistent": 4,
        "Very Consistent": 5
    }
    
    result_df["Reliability_Order"] = result_df["Reliability"].map(reliability_order)
    
    result_df = result_df.sort_values(
        ["Name", "Rating", "Reliability_Order"],
        ascending=[True, False, False]
    )
    
    top_sites = result_df.groupby("Name").first().reset_index()
    
    output_cols = [
        "Name",
        "Surf Site",
        "Swell Direction",
        "Reliability",
        "Wind Direction",
        "Type",
        "Boards",
        "Skill Level",
        "Surf Season",
        "Rating"
    ]
    
    result = top_sites[output_cols].copy()
    
    result = result.sort_values("Name").reset_index(drop=True)
    
    return {"output_01.csv": result}


if __name__ == "__main__":
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    cand_dir = task_dir / "cand"
    cand_dir.mkdir(parents=True, exist_ok=True)
    
    outputs = solve(inputs_dir)
    for filename, df in outputs.items():
        df.to_csv(cand_dir / filename, index=False, encoding="utf-8")
