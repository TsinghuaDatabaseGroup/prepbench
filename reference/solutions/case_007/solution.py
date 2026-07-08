from __future__ import annotations
from pathlib import Path
import pandas as pd


def solve(inputs_dir: Path) -> dict[str, pd.DataFrame]:
    dep_path = inputs_dir / "input_01.csv"
    alloc_path = inputs_dir / "input_02.csv"

    df_dep = pd.read_csv(dep_path)
    df_alloc = pd.read_csv(alloc_path)

    dep_id = df_alloc["Departure ID"].astype(str)
    date_part = dep_id.str[-10:]
    df_alloc["Ship ID"] = dep_id.str[:-11]
    df_alloc["Departure Date"] = (
        date_part.str[6:10] + "-" +
        date_part.str[3:5] + "-" + date_part.str[0:2]
    )

    agg = (
        df_alloc.groupby(["Ship ID", "Departure Date"], as_index=False)[
            ["Weight Allocated", "Volume Allocated"]
        ].sum()
    )

    df_dep["__order__"] = range(len(df_dep))
    df = df_dep.merge(agg, on=["Ship ID", "Departure Date"], how="left")

    df["Weight Allocated"] = df["Weight Allocated"].fillna(0).astype(int)
    df["Volume Allocated"] = df["Volume Allocated"].fillna(0).astype(int)

    df["Max Weight Exceeded?"] = df["Weight Allocated"] > df["Max Weight"]
    df["Max Volume Exceeded?"] = df["Volume Allocated"] > df["Max Volume"]

    df["Departure Date"] = (
        df["Departure Date"].str[8:10]
        + "/"
        + df["Departure Date"].str[5:7]
        + "/"
        + df["Departure Date"].str[0:4]
    )

    cols = [
        "Ship ID",
        "Departure Date",
        "Max Weight",
        "Max Volume",
        "Weight Allocated",
        "Volume Allocated",
        "Max Weight Exceeded?",
        "Max Volume Exceeded?",
    ]

    df = df.sort_values("__order__").loc[:, cols]

    return {"output_01.csv": df}


if __name__ == "__main__":
    from pathlib import Path

    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"

    cand_dir = task_dir / "cand"
    cand_dir.mkdir(parents=True, exist_ok=True)

    outputs = solve(inputs_dir)
    for filename, df in outputs.items():
        (cand_dir / filename).parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(cand_dir / filename, index=False, encoding="utf-8")
