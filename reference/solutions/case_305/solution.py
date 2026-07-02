from __future__ import annotations

from pathlib import Path
from typing import Dict

import pandas as pd
import re


def solve(inputs_dir: Path) -> Dict[str, pd.DataFrame]:

    def parse_week_number(week_str: str) -> int | None:
        if pd.isna(week_str):
            return None
        m = re.search(r"Week\s*(\d+)", str(week_str))
        return int(m.group(1)) if m else None

    def is_final_week(week_str: str) -> bool:
        if pd.isna(week_str):
            return False
        s = str(week_str)
        if re.search(r"(?i)(semi\s*-?\s*final|quarter\s*-?\s*final)", s):
            return False
        return re.search(r"(?i)\bfinal\b", s) is not None

    def parse_scores_to_metrics(score_str: str) -> tuple[float | None, int | None, float | None]:
        if pd.isna(score_str):
            return None, None, None
        s = str(score_str).strip()
        if not s or s.lower().startswith("no scores"):
            return None, None, None
        m_total = re.match(r"^\s*(\d+(?:\.\d+)?)", s)
        if not m_total:
            return None, None, None
        try:
            total = float(m_total.group(1))
        except ValueError:
            return None, None, None
        m_judges = re.search(r"\(([^)]*)\)", s)
        if not m_judges:
            return None, None, None
        judges_part = m_judges.group(1)
        parts = [p.strip() for p in judges_part.split(",") if p.strip()]
        numeric_parts = []
        for p in parts:
            try:
                float(p)
                numeric_parts.append(p)
            except Exception:
                pass
        num_judges = len(numeric_parts)
        if num_judges == 0:
            return None, None, None
        avg = total / num_judges
        return total, num_judges, avg

    def normalize_final_position(result_str: str) -> str | None:
        if pd.isna(result_str):
            return None
        s = str(result_str).strip()
        sl = s.lower()
        if "winner" in sl:
            return "Winners"
        if "runner" in sl:
            return "Runners-up"
        if "third" in sl:
            return "Third place"
        return None

    input_path = inputs_dir / "input_01.csv"
    df = pd.read_csv(input_path, dtype=str)

    mask_header = (df.get("Couple").fillna("") == "Couple") | (df.get("Scores").fillna("") == "Scores")
    df = df.loc[~mask_header].copy()

    df["Week_num"] = df["Week"].apply(parse_week_number)
    df["is_final"] = df["Week"].apply(is_final_week)

    parsed = df["Scores"].apply(parse_scores_to_metrics)
    df["Total_Score"] = [t[0] for t in parsed]
    df["Num_Judges"] = [t[1] for t in parsed]
    df["Avg_Judge_Score"] = [t[2] for t in parsed]

    df_scored = df.loc[df["Avg_Judge_Score"].notna()].copy()

    group_keys = ["Series", "Couple"]

    tmp = df_scored.loc[df_scored["Week_num"].notna()].copy()
    tmp["Week_num"] = tmp["Week_num"].astype(int)
    first_week = tmp.groupby(group_keys, as_index=False)["Week_num"].min().rename(columns={"Week_num": "first_week"})
    tmp = tmp.merge(first_week, on=group_keys, how="left")
    first_scores = (
        tmp.loc[tmp["Week_num"] == tmp["first_week"]]
        .groupby(group_keys, as_index=False)
        .agg({"Avg_Judge_Score": "mean"})
        .rename(columns={"Avg_Judge_Score": "First_Avg"})
    )

    df_scored["Finalist Positions"] = df_scored["Result"].apply(normalize_final_position)
    finals = df_scored.loc[df_scored["is_final"]].copy()
    grp = finals.groupby(group_keys, as_index=False)
    final_scores = grp.agg({
        "Total_Score": "sum",
        "Num_Judges": "sum",
        "Finalist Positions": lambda s: s.dropna().iloc[0] if s.dropna().size > 0 else None,
    })
    final_scores["Final_Avg"] = final_scores["Total_Score"] / final_scores["Num_Judges"]
    final_scores = final_scores.drop(columns=["Total_Score", "Num_Judges"]) 
    final_scores = final_scores.loc[final_scores["Finalist Positions"].notna()].copy()

    merged = final_scores.merge(first_scores, on=group_keys, how="left")

    merged["% Change"] = (merged["Final_Avg"] - merged["First_Avg"]) / merged["First_Avg"]

    out = merged[["Series", "Couple", "Finalist Positions", "Final_Avg", "% Change"]].copy()
    out = out.rename(columns={"Final_Avg": "Avg Judge's Score"})

    with pd.option_context("mode.chained_assignment", None):
        out["Series"] = pd.to_numeric(out["Series"], errors="coerce")
    out = out.loc[out["Series"].between(1, 21, inclusive="both")]

    return {
        "output_01.csv": out,
    }


if __name__ == "__main__":
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    cand_dir = task_dir / "cand"
    cand_dir.mkdir(parents=True, exist_ok=True)

    outputs = solve(inputs_dir)
    for filename, df in outputs.items():
        (cand_dir / filename).parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(cand_dir / filename, index=False, encoding="utf-8")


