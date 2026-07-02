import pandas as pd
from pathlib import Path


def solve(inputs_dir: Path) -> dict[str, pd.DataFrame]:
    f_jul = inputs_dir / "input_02.csv"
    f_aug = inputs_dir / "input_01.csv"

    df_jul = pd.read_csv(f_jul)
    df_aug = pd.read_csv(f_aug)

    df_jul["Date"] = "01/07/2023"
    df_aug["Date"] = "01/08/2023"

    combined = pd.concat([df_jul, df_aug], ignore_index=True)

    combined["Sequence ID"] = range(1, len(combined) + 1)

    combined["Quantity"] = combined["Quantity"].astype(int)

    combined_sorted = combined.sort_values(["Customer", "Book", "Date", "Sequence ID"]).copy()
    combined_sorted["Prev Qty"] = (
        combined_sorted.groupby(["Customer", "Book"])
        ["Quantity"].shift(1)
    )
    combined_sorted["Bigger Order?"] = combined_sorted["Quantity"] - combined_sorted["Prev Qty"]

    out = combined_sorted.sort_values("Sequence ID").copy()

    out = out[[
        "Customer",
        "Book",
        "Date",
        "Sequence ID",
        "Quantity",
        "Bigger Order?",
    ]]

    out["Date"] = out["Date"].astype(str)

    return {
        "output_01.csv": out.reset_index(drop=True)
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
