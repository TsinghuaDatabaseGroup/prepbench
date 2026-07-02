from pathlib import Path
import pandas as pd
from typing import Dict


def solve(inputs_dir: Path) -> Dict[str, pd.DataFrame]:
    pkm_path = inputs_dir / "input_01.csv"
    evo_path = inputs_dir / "input_02.csv"
    df = pd.read_csv(pkm_path)
    evo = pd.read_csv(evo_path)

    def clean_num(x: str) -> str | None:
        if pd.isna(x):
            return None
        s = str(x).strip().replace("\xa0", "").replace("\u00a0", "")
        if "." in s:
            return None
        s_main = s.strip()
        return s_main

    df["#"] = df["#"].apply(clean_num)
    mask_num = df["#"].notna() & df["#"].astype(str).str.fullmatch(r"\d+")
    df = df[mask_num].copy()
    df["#"] = df["#"].astype(int)
    df = df[df["#"] <= 386]
    df = df[~df["Name"].str.match(r"^Mega\b", na=False)]

    cols_keep = [
        "#", "Name", "Total", "HP", "Attack", "Defense", "Special Attack", "Special Defense", "Speed",
    ]
    df = df[cols_keep].drop_duplicates(
        subset=["Name"], keep="first").reset_index(drop=True)

    evo = evo.copy()
    for c in ["Evolving from", "Evolving to", "Condition", "Evolution Type"]:
        if c in evo.columns:
            evo[c] = evo[c].astype(str).replace({"nan": ""})
    evo = evo[(evo["Evolving from"].notna()) & (evo["Evolving to"].notna())]
    evo = evo[(evo["Evolving from"].str.strip() != "")
              & (evo["Evolving to"].str.strip() != "")]

    valid_names = set(df["Name"].tolist())
    evo = evo[evo["Evolving to"].isin(valid_names)].copy()
    evo = evo.drop_duplicates(
        subset=["Evolving from", "Evolving to"], keep="first")

    def to_level_num(v):
        if pd.isna(v):
            return pd.NA
        s = str(v).strip()
        if s == "":
            return pd.NA
        try:
            f = float(s)
            return int(f)
        except Exception:
            return pd.NA

    evo["Level_num"] = evo["Level"].apply(to_level_num)

    parent_map = {}
    for _, r in evo.iterrows():
        child = r["Evolving to"]
        parent = r["Evolving from"]
        parent_map.setdefault(child, parent)

    children_map = {}
    for _, r in evo.iterrows():
        parent = r["Evolving from"]
        child = r["Evolving to"]
        children_map.setdefault(parent, []).append(child)

    def find_root(name: str) -> str:
        seen = set()
        cur = name
        while cur in parent_map and cur not in seen:
            seen.add(cur)
            cur = parent_map[cur]
        return cur

    def is_third_stage(name: str) -> bool:
        p = parent_map.get(name)
        if not p:
            return False
        gp = parent_map.get(p)
        return gp is not None

    out_rows = []
    df_stats = df.set_index("Name")

    for name in df_stats.index:
        stats = df_stats.loc[name]
        root = find_root(name)
        tos = children_map.get(name, [])
        if not tos:
            out_rows.append({
                "Evolution Group": root,
                "#": int(stats["#"]),
                "Name": name,
                "Total": int(stats["Total"]),
                "HP": int(stats["HP"]),
                "Attack": int(stats["Attack"]),
                "Defense": int(stats["Defense"]),
                "Special Attack": int(stats["Special Attack"]),
                "Special Defense": int(stats["Special Defense"]),
                "Speed": int(stats["Speed"]),
                "Evolving from": parent_map.get(name, ""),
                "Evolving to": "",
                "Level": pd.NA,
                "Condition": "",
                "Evolution Type": "",
                "First Evolution": root if is_third_stage(name) else "",
            })
        else:
            for to_name in tos:
                er = evo[(evo["Evolving from"] == name) & (
                    evo["Evolving to"] == to_name)].iloc[0]
                out_rows.append({
                    "Evolution Group": root,
                    "#": int(stats["#"]),
                    "Name": name,
                    "Total": int(stats["Total"]),
                    "HP": int(stats["HP"]),
                    "Attack": int(stats["Attack"]),
                    "Defense": int(stats["Defense"]),
                    "Special Attack": int(stats["Special Attack"]),
                    "Special Defense": int(stats["Special Defense"]),
                    "Speed": int(stats["Speed"]),
                    "Evolving from": parent_map.get(name, ""),
                    "Evolving to": to_name,
                    "Level": er["Level_num"],
                    "Condition": er.get("Condition", "") if pd.notna(er.get("Condition", "")) else "",
                    "Evolution Type": er.get("Evolution Type", "") if pd.notna(er.get("Evolution Type", "")) else "",
                    "First Evolution": root if is_third_stage(name) else "",
                })

    out = pd.DataFrame(out_rows)

    out = out[[
        "Evolution Group", "#", "Name", "Total", "HP", "Attack", "Defense",
        "Special Attack", "Special Defense", "Speed", "Evolving from", "Evolving to",
        "Level", "Condition", "Evolution Type", "First Evolution"
    ]]

    num_cols = ["#", "Total", "HP", "Attack", "Defense",
                "Special Attack", "Special Defense", "Speed", "Level"]
    for c in num_cols:
        if c == "Level":
            out[c] = pd.to_numeric(out[c], errors="coerce").astype("Int64")
        else:
            out[c] = pd.to_numeric(out[c], errors="coerce", downcast="integer")

    out = out.drop_duplicates().reset_index(drop=True)

    return {"output_01.csv": out}


if __name__ == "__main__":
    import sys
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    cand_dir = task_dir / "cand"
    cand_dir.mkdir(parents=True, exist_ok=True)
    result = solve(inputs_dir)
    for fname, df in result.items():
        df.to_csv(cand_dir / fname, index=False, encoding="utf-8")
