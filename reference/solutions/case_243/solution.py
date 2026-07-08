from __future__ import annotations

from difflib import SequenceMatcher
from pathlib import Path
from typing import Dict

import pandas as pd


SUBJECTS = [
    "French",
    "English",
    "Science",
    "History",
    "Math",
    "Physical Education",
    "Geography",
]


def _normalize_subject(value: object) -> object:
    if pd.isna(value):
        return pd.NA
    subject = str(value).strip()
    if not subject or subject.lower() == "null":
        return pd.NA

    for canonical in SUBJECTS:
        if subject.lower() == canonical.lower():
            return canonical

    best_match = subject
    best_ratio = -1.0
    for candidate in SUBJECTS:
        ratio = SequenceMatcher(None, subject.lower(),
                                candidate.lower()).ratio()
        if ratio > best_ratio:
            best_ratio = ratio
            best_match = candidate
    return best_match


def solve(inputs_dir: Path) -> Dict[str, pd.DataFrame]:
    input_path = inputs_dir / "input_01.csv"
    df = pd.read_csv(input_path)

    class_columns = [col for col in df.columns if "Class" in col]
    melted = df.melt(
        id_vars=["Name"],
        value_vars=class_columns,
        var_name="class_flag",
        value_name="Subject",
    )

    melted["Subject"] = (
        melted["Subject"]
        .replace(r"^\s*$", pd.NA, regex=True)
        .replace("Null", pd.NA)
        .pipe(lambda s: s.map(_normalize_subject))
    )

    melted = melted.dropna(subset=["Subject"])

    status_map = {
        "Class": "Active",
        "Dropped Class": "Drop Outs",
    }

    melted["Active Flag"] = (
        melted["class_flag"].str.replace(r"\d", "", regex=True).str.strip()
    )
    melted["Active Flag"] = melted["Active Flag"].map(status_map)
    melted = melted.dropna(subset=["Active Flag"])

    summary = (
        melted.groupby(["Subject", "Active Flag"], sort=False)["Name"]
        .size()
        .reset_index(name="Count")
    )

    pivot = (
        summary.pivot(index="Subject", columns="Active Flag", values="Count")
        .fillna(0)
        .astype(int)
        .rename_axis(None, axis=1)
    )

    for col in ["Active", "Drop Outs"]:
        if col not in pivot:
            pivot[col] = 0

    pivot = pivot[["Drop Outs", "Active"]].reset_index()

    pivot["Total Enrolled"] = pivot["Drop Outs"] + pivot["Active"]
    pivot["Drop Out Rate"] = (
        pivot["Drop Outs"] / pivot["Total Enrolled"]
    ).round(9)

    order = pd.Categorical(pivot["Subject"], SUBJECTS, ordered=True)
    pivot = (
        pivot.assign(_order=order)
        .sort_values(["_order", "Subject"])
        .drop(columns="_order")
        .reset_index(drop=True)
    )

    final_df = pivot[
        ["Subject", "Drop Outs", "Active", "Total Enrolled", "Drop Out Rate"]
    ]

    return {"output_01.csv": final_df}


if __name__ == "__main__":
    task_dir = Path(__file__).parent
    inputs_directory = task_dir / "inputs"
    cand_dir = task_dir / "cand"
    cand_dir.mkdir(exist_ok=True)

    outputs = solve(inputs_directory)
    for filename, dataframe in outputs.items():
        dataframe.to_csv(cand_dir / filename, index=False)
