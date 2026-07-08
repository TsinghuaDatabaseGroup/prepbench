from pathlib import Path
import pandas as pd


def solve(inputs_dir: Path) -> dict[str, pd.DataFrame]:
    input_file = inputs_dir / "input_01.csv"
    df = pd.read_csv(input_file, dtype=str)
    
    id_cols = ["student_id", "first_name", "last_name", "Gender", "D.O.B"]
    
    df_2021 = df[id_cols + ["2021-attainment", "2021-effort", "2021-attendance", "2021-behaviour"]].copy()
    df_2021_long = pd.melt(
        df_2021,
        id_vars=id_cols,
        value_vars=["2021-attainment", "2021-effort", "2021-attendance", "2021-behaviour"],
        var_name="category",
        value_name="grade_2021"
    )
    df_2021_long["category"] = df_2021_long["category"].str.replace("2021-", "")
    df_2021_long["grade_2021"] = df_2021_long["grade_2021"].astype(float)
    
    df_2022 = df[id_cols + ["2022-attainment", "2022-effort", "2022-attendance", "2022-behaviour"]].copy()
    df_2022_long = pd.melt(
        df_2022,
        id_vars=id_cols,
        value_vars=["2022-attainment", "2022-effort", "2022-attendance", "2022-behaviour"],
        var_name="category",
        value_name="grade_2022"
    )
    df_2022_long["category"] = df_2022_long["category"].str.replace("2022-", "")
    df_2022_long["grade_2022"] = df_2022_long["grade_2022"].astype(float)
    
    df_merged = pd.merge(
        df_2021_long,
        df_2022_long,
        on=id_cols + ["category"],
        how="inner"
    )
    
    df_avg = df_merged.groupby(id_cols, as_index=False).agg({
        "grade_2021": "mean",
        "grade_2022": "mean"
    })
    
    df_avg = df_avg.rename(columns={
        "grade_2021": "2021",
        "grade_2022": "2022"
    })
    
    df_avg["Difference"] = df_avg["2022"] - df_avg["2021"]
    
    def categorize_progress(diff):
        if diff > 0:
            return "Improvement"
        elif diff == 0:
            return "No change"
        else:
            return "Cause for concern"
    
    df_avg["Progress"] = df_avg["Difference"].apply(categorize_progress)
    
    df_output = df_avg[df_avg["Progress"] == "Cause for concern"].copy()
    
    output_cols = ["student_id", "first_name", "last_name", "Gender", "D.O.B", "2021", "2022", "Difference", "Progress"]
    df_output = df_output[output_cols].copy()
    
    df_output["student_id"] = df_output["student_id"].astype(int)
    df_output["2021"] = df_output["2021"].astype(float)
    df_output["2022"] = df_output["2022"].astype(float)
    df_output["Difference"] = df_output["Difference"].astype(float)
    
    df_output = df_output.sort_values("student_id").reset_index(drop=True)
    
    return {"output_01.csv": df_output}


if __name__ == "__main__":
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    cand_dir = task_dir / "cand"
    cand_dir.mkdir(parents=True, exist_ok=True)
    
    outputs = solve(inputs_dir)
    for filename, df in outputs.items():
        df.to_csv(cand_dir / filename, index=False, encoding="utf-8")

