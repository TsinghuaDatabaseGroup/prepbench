from __future__ import annotations
from pathlib import Path
import pandas as pd


def solve(inputs_dir: Path) -> dict[str, pd.DataFrame]:
    df_contracts = pd.read_csv(inputs_dir / "input_01.csv")
    seq_path = inputs_dir / "input_02.csv"
    if seq_path.exists():
        df_seq = pd.read_csv(seq_path)
        if "Length" in df_seq.columns:
            df_seq = df_seq[["Length"]].dropna()
            df_seq["Length"] = df_seq["Length"].astype(int)
        else:
            max_len = int(df_contracts["Contract Length (months)"].max(
            )) if not df_contracts.empty else 0
            df_seq = pd.DataFrame({"Length": list(range(1, max_len + 1))})
    else:
        max_len = int(df_contracts["Contract Length (months)"].max(
        )) if not df_contracts.empty else 0
        df_seq = pd.DataFrame({"Length": list(range(1, max_len + 1))})

    df_contracts["Start Date"] = pd.to_datetime(
        df_contracts["Start Date"], format="%Y-%m-%d", errors="raise")

    df_contracts = df_contracts.rename(columns={
        "Contract Length (months)": "Contract Length"
    })

    df_contracts["__key"] = 1
    df_seq["__key"] = 1

    df_expanded = df_contracts.merge(df_seq, on="__key", how="left")
    df_expanded = df_expanded[df_expanded["Length"]
                              <= df_expanded["Contract Length"]].copy()

    df_expanded["Payment Date"] = df_expanded.apply(
        lambda r: r["Start Date"] + pd.DateOffset(months=int(r["Length"]) - 1), axis=1
    )

    df_expanded.sort_values(["Name", "Payment Date"], inplace=True)
    df_expanded["Cumulative Monthly Cost"] = df_expanded.groupby("Name")[
        "Monthly Cost"].cumsum()

    out = df_expanded[["Name", "Payment Date",
                       "Monthly Cost", "Cumulative Monthly Cost"]].copy()

    person_order = (
        df_contracts[["Name", "Contract Length", "Start Date"]]
        .drop_duplicates()
        .sort_values(["Contract Length", "Start Date", "Name"], ascending=[True, False, True])
    )
    person_order["__order"] = range(len(person_order))
    out = out.merge(person_order[["Name", "__order"]], on="Name", how="left")
    out.sort_values(["__order", "Payment Date"], inplace=True)
    out.drop(columns=["__order"], inplace=True)

    out["Payment Date"] = out["Payment Date"].dt.strftime("%d/%m/%Y")

    return {
        "output_01.csv": out
    }


if __name__ == "__main__":
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    cand_dir = task_dir / "cand"
    cand_dir.mkdir(parents=True, exist_ok=True)

    result = solve(inputs_dir)
    for filename, df in result.items():
        (cand_dir / filename).parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(cand_dir / filename, index=False, encoding="utf-8")
