from __future__ import annotations

from pathlib import Path
from typing import Dict

import pandas as pd


def solve(inputs_dir: Path) -> Dict[str, pd.DataFrame]:
    engagements = pd.read_csv(inputs_dir / "input_01.csv")
    grades = pd.read_csv(inputs_dir / "input_02.csv")
    initials_map = pd.read_csv(inputs_dir / "input_03.csv")

    id_to_initial = dict(zip(initials_map["Initial ID"], initials_map["Initial"]))

    engagements["Initials"] = engagements["Consultant Forename"].map(id_to_initial).astype(str) + \
                               engagements["Consultant Surname"].map(id_to_initial).astype(str)

    def to_date(day_col: str, month_col: str) -> pd.Series:
        s = pd.to_datetime(
            {
                "year": 2024,
                "month": engagements[month_col].astype(int),
                "day": engagements[day_col].astype(int),
            },
            errors="coerce",
        )
        return s

    engagements["Engagement Start Date"] = to_date("Engagement Start Day", "Engagement Start Month")
    engagements["Engagement End Date"] = to_date("Engagement End Day", "Engagement End Month")

    engagements["Corrected Grade ID"] = engagements.groupby("Initials")["Grade"].transform("min")

    def drop_invalid_same_day(g: pd.DataFrame) -> pd.DataFrame:
        g = g.copy()
        dup_start = g.duplicated(subset=["Engagement Start Date"], keep=False)
        mask_invalid = (g["Engagement End Date"] < g["Engagement Start Date"]) & dup_start
        return g.loc[~mask_invalid]

    engagements = engagements.groupby("Initials", group_keys=False).apply(drop_invalid_same_day)

    df = engagements.merge(
        grades.rename(columns={"Grade ID": "Corrected Grade ID"}),
        on="Corrected Grade ID",
        how="left",
        validate="many_to_one",
    )

    df = df.sort_values(["Initials", "Engagement Start Date", "Engagement End Date"], ascending=[True, True, True]).reset_index(drop=True)

    df["Engagement Order"] = df.groupby("Initials").cumcount() + 1

    df["prev_end"] = df.groupby("Initials")["Engagement End Date"].shift(1)
    mask_valid = df["prev_end"].isna() | (df["Engagement Start Date"] >= df["prev_end"])
    df = df.loc[mask_valid].copy()

    out = df[[
        "Engagement Start Date",
        "Engagement End Date",
        "Initials",
        "Engagement Order",
        "Grade Name",
        "Day Rate",
    ]].copy()

    for col in ["Engagement Start Date", "Engagement End Date"]:
        out[col] = pd.to_datetime(out[col]).dt.strftime("%d/%m/%Y")

    out["Engagement Order"] = pd.to_numeric(out["Engagement Order"], downcast="integer")
    out["Day Rate"] = pd.to_numeric(out["Day Rate"], downcast="integer")

    return {"output_01.csv": out}


if __name__ == "__main__":
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    cand_dir = task_dir / "cand"
    cand_dir.mkdir(parents=True, exist_ok=True)

    outputs = solve(inputs_dir)
    for filename, df in outputs.items():
        (cand_dir / filename).parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(cand_dir / filename, index=False, encoding="utf-8")
