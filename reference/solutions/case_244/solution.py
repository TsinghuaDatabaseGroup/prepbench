import pandas as pd
from pathlib import Path


def solve(inputs_dir: Path) -> dict[str, pd.DataFrame]:
    df_nat = pd.read_csv(inputs_dir / "input_01.csv")
    df_name = pd.read_csv(inputs_dir / "input_02.csv")


    replacements = {
        "Meksiko": "Mexico",
        "Frans": "France",
        "Egipt": "Egypt",
    }
    df_nat["Nationality"] = df_nat["Nationality"].replace(replacements)

    grp = (
        df_nat.groupby(["Classroom", "Nationality"], as_index=False)
        .agg(Name=("Student ID", "nunique"))
    )

    grp = grp.sort_values(["Classroom", "Name", "Nationality"], ascending=[True, False, True])

    top = grp.groupby("Classroom", as_index=False).head(1)

    out = top[["Nationality", "Classroom", "Name"]].reset_index(drop=True)

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
