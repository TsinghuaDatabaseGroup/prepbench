from __future__ import annotations
import pandas as pd
from pathlib import Path
import math


def solve(inputs_dir: Path) -> dict[str, pd.DataFrame]:
    attendance_df = pd.read_csv(inputs_dir / "input_01.csv")

    test_scores_df = pd.read_csv(inputs_dir / "input_02.csv", skiprows=1)

    merged_df = pd.merge(
        attendance_df,
        test_scores_df,
        on="student_name",
        how="inner"
    )

    merged_df["subject"] = merged_df["subject"].replace({
        "Sciece": "Science",
        "Engish": "English"
    })

    name_parts = merged_df["student_name"].str.split("_", n=1, expand=True)
    merged_df["First Name"] = name_parts[0].str.strip()
    merged_df["Surname"] = name_parts[1].str.strip()

    def standard_round(x):
        return int(math.floor(x + 0.5))

    merged_df["TestScoreInteger"] = merged_df["test_score"].apply(
        standard_round)

    def get_attendance_flag(percentage):
        if percentage >= 0.90:
            return "High Attendance"
        elif percentage >= 0.70:
            return "Medium Attendance"
        else:
            return "Low Attendance"

    merged_df["Attendance Flag"] = merged_df["attendance_percentage"].apply(
        get_attendance_flag)

    result_df = pd.DataFrame({
        "Attendance Flag": merged_df["Attendance Flag"],
        "First Name": merged_df["First Name"],
        "Surname": merged_df["Surname"],
        "Attendance_Percentage": merged_df["attendance_percentage"],
        "Student_ID": merged_df["student_id"],
        "Subject": merged_df["subject"],
        "Test_score": merged_df["test_score"],
        "TestScoreInteger": merged_df["TestScoreInteger"]
    })

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
        (cand_dir / fname).parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(cand_dir / fname, index=False, encoding="utf-8")
