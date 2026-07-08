import pandas as pd
from pathlib import Path
import re
from typing import Dict, List, Optional


def _clean_show_name(s: str) -> str:
    return re.sub(r"\s*\(.*\)$", "", str(s)).strip().upper()


def solve(inputs_dir: Path) -> Dict[str, pd.DataFrame]:
    survey = pd.read_csv(inputs_dir / "input_01.csv")
    content_raw = pd.read_csv(inputs_dir / "input_02.csv", encoding="latin1")
    devices = pd.read_csv(inputs_dir / "input_03.csv")

    cols_for_dedup = [c for c in survey.columns if c != "Timestamp"]
    survey_deduped = survey.drop_duplicates(subset=cols_for_dedup).copy()

    first_col = content_raw.columns[0]
    content = (
        content_raw[[first_col]]
        .rename(columns={first_col: "Show_Raw"})
        .dropna()
        .copy()
    )
    content["Show"] = content["Show_Raw"].apply(_clean_show_name)
    valid_shows = content[["Show"]].drop_duplicates().copy()

    device_col = "How have you been watching Netflix? (Phone, TV, etc.)"
    df_devices = survey_deduped[[device_col]].copy().dropna(subset=[device_col])

    accepted_map = {d.lower(): d for d in devices["Device"].tolist()}

    def extract_devices(text: str) -> Optional[List[str]]:
        s = str(text)
        s_norm = s.replace("&", ",").replace("/", ",")
        parts = [p.strip() for p in re.split(r"[,\n]", s_norm) if p.strip()]
        found: List[str] = []
        for p in parts:
            key = p.lower()
            if key in accepted_map:
                found.append(accepted_map[key])
            elif key in {"etc", "etc."}:
                continue
        if not found:
            only_etc = all(p.lower() in {"etc", "etc."} for p in parts) if parts else True
            return None if only_etc else ["Other"]
        seen = set()
        unique = []
        for d in found:
            if d not in seen:
                seen.add(d)
                unique.append(d)
        return unique

    df_devices["Device"] = df_devices[device_col].apply(extract_devices)
    df_devices = df_devices.dropna(subset=["Device"]).explode("Device")

    output_01 = (
        df_devices.groupby("Device").size().reset_index(name="Count")
    )

    name_col = "What is your name?"
    binge_col = "What have you been binging during lockdown?"

    def split_shows(text: str) -> List[str]:
        tokens = [t.strip() for t in re.split(r",|;", str(text)) if t.strip()]
        cleaned = [_clean_show_name(t) for t in tokens if t.strip()]
        return [t for t in cleaned if t]

    watched = survey_deduped[[name_col, binge_col]].dropna(subset=[binge_col]).copy()
    watched["Show"] = watched[binge_col].apply(split_shows)
    watched = watched.explode("Show").dropna(subset=["Show"]).copy()
    watched = watched[[name_col, "Show"]].drop_duplicates()
    watched = watched.merge(valid_shows, on="Show", how="inner")

    rating_cols = [
        c
        for c in survey.columns
        if c.startswith("How would you rate ") and 'Other' not in c
    ]

    ratings_predef = (
        survey_deduped.melt(
            id_vars=[name_col], value_vars=rating_cols, var_name="ShowCol", value_name="Rating"
        )
        .dropna(subset=["Rating"])
        .copy()
    )
    ratings_predef["Show"] = (
        ratings_predef["ShowCol"]
        .str.replace("How would you rate ", "", regex=False)
        .str.replace("?", "", regex=False)
        .str.replace('"', "", regex=False)
        .str.strip()
        .apply(_clean_show_name)
    )
    ratings_predef = ratings_predef[[name_col, "Show", "Rating"]]

    ratings_predef = ratings_predef.merge(watched, on=[name_col, "Show"], how="inner")

    other_col = 'How would you rate "Other"?'
    others = survey_deduped[[name_col, binge_col, other_col]].dropna(subset=[other_col]).copy()
    others = others.rename(columns={other_col: "Rating"})

    predef_show_names = set(
        _clean_show_name(
            c.replace("How would you rate ", "").replace("?", "").replace('"', "").strip()
        )
        for c in rating_cols
    )
    valid_set = set(valid_shows["Show"].tolist())

    def pick_unique_other(show_text: str):
        shows = split_shows(show_text)
        candidates = [s for s in shows if s not in predef_show_names and s in valid_set]
        return candidates[0] if len(candidates) == 1 else None

    others["Show"] = others[binge_col].apply(pick_unique_other)
    ratings_other = others.dropna(subset=["Show"])[["Show", "Rating"]]

    all_ratings = pd.concat([ratings_predef[["Show", "Rating"]], ratings_other[["Show", "Rating"]]], ignore_index=True)
    all_ratings["Rating"] = pd.to_numeric(all_ratings["Rating"], errors="coerce")
    all_ratings = all_ratings.dropna(subset=["Rating"])

    avg = all_ratings.groupby("Show", as_index=False)["Rating"].mean()
    avg["Rank"] = avg["Rating"].rank(method="dense", ascending=False).astype(int)

    output_02 = avg[["Rank", "Show", "Rating"]].sort_values(by=["Rank", "Show"])

    try:
        print("DEBUG_OTHER_SHOWS:", sorted(ratings_other["Show"].unique().tolist()))
    except Exception:
        pass

    return {
        "output_01.csv": output_01,
        "output_02.csv": output_02,
    }


if __name__ == "__main__":
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    cand_dir = task_dir / "cand"

    if not cand_dir.exists():
        cand_dir.mkdir(parents=True)

    results = solve(inputs_dir)

    for filename, df in results.items():
        df.to_csv(cand_dir / filename, index=False, encoding="utf-8")
