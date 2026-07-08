import pandas as pd
from pathlib import Path


def solve(inputs_dir: Path) -> dict[str, pd.DataFrame]:
    df = pd.read_csv(inputs_dir / "input_01.csv")
    
    damage_cols = ["Name", "Category", "Phy", "Mag", "Fire", "Ligh", "Holy"]
    level_cols = ["Name", "Str", "Dex", "Int", "Fai", "Arc"]
    
    damage_stats = df[damage_cols].copy()
    level_reqs = df[level_cols].copy()
    
    damage_pivot = damage_stats.melt(
        id_vars=["Name", "Category"],
        value_vars=["Phy", "Mag", "Fire", "Ligh", "Holy"],
        var_name="Damage Type",
        value_name="Values"
    )
    
    def split_damage(value):
        if pd.isna(value) or value == "-":
            return 0, 0
        parts = str(value).strip().split()
        if len(parts) == 2:
            attack = 0 if parts[0] == "-" else int(parts[0])
            resistance = 0 if parts[1] == "-" else int(parts[1])
            return attack, resistance
        elif len(parts) == 1:
            if parts[0] == "-":
                return 0, 0
            else:
                return int(parts[0]), 0
        return 0, 0
    
    damage_split = damage_pivot["Values"].apply(
        lambda x: pd.Series(split_damage(x), index=["Attack Damage", "Damage Resistance"])
    )
    damage_pivot = pd.concat([damage_pivot, damage_split], axis=1)
    
    damage_pivot["Attack Damage"] = damage_pivot["Attack Damage"].fillna(0).astype(int)
    damage_pivot["Damage Resistance"] = damage_pivot["Damage Resistance"].fillna(0).astype(int)
    
    level_pivot = level_reqs.melt(
        id_vars=["Name"],
        value_vars=["Str", "Dex", "Int", "Fai", "Arc"],
        var_name="Attribute",
        value_name="Values"
    )
    
    def split_level(value):
        if pd.isna(value) or value == "-":
            return 0, 0
        parts = str(value).strip().split()
        if len(parts) == 2:
            level = 0 if parts[0] == "-" else int(parts[0])
            scaling = 0 if parts[1] == "-" else (0 if parts[1] == "-" else 1)
            return level, scaling
        elif len(parts) == 1:
            if parts[0] == "-":
                return 0, 0
            else:
                try:
                    return int(parts[0]), 0
                except:
                    return 0, 0
        return 0, 0
    
    level_split = level_pivot["Values"].apply(
        lambda x: pd.Series(split_level(x), index=["Required Level", "Attribute Scaling"])
    )
    level_pivot = pd.concat([level_pivot, level_split], axis=1)
    
    level_pivot["Required Level"] = level_pivot["Required Level"].fillna(0).astype(int)
    level_pivot["Attribute Scaling"] = level_pivot["Attribute Scaling"].fillna(0).astype(int)
    
    total_damage = damage_pivot.groupby("Name")["Attack Damage"].sum().reset_index()
    total_damage.columns = ["Name", "Total Attack Damage"]
    
    total_level = level_pivot.groupby("Name")["Required Level"].sum().reset_index()
    total_level.columns = ["Name", "Total Required Level"]
    
    merged = total_damage.merge(total_level, on="Name", how="inner")
    merged = merged.merge(
        df[["Name", "Category"]].drop_duplicates(),
        on="Name",
        how="left"
    )
    
    merged["Rank"] = merged.groupby("Total Required Level")["Total Attack Damage"].rank(
        method="dense", ascending=False
    )
    
    result = merged[merged["Rank"] == 1].copy()
    result = result[["Name", "Category", "Total Required Level", "Total Attack Damage"]].copy()
    result.columns = ["Name", "Category", "Required Level", "Attack Damage"]
    
    result = result.sort_values("Required Level").reset_index(drop=True)
    
    return {"output_01.csv": result}


if __name__ == "__main__":
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    cand_dir = task_dir / "cand"
    cand_dir.mkdir(parents=True, exist_ok=True)
    
    outputs = solve(inputs_dir)
    for filename, df in outputs.items():
        df.to_csv(cand_dir / filename, index=False, encoding="utf-8")

