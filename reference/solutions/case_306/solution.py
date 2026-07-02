import pandas as pd
from pathlib import Path
from typing import Dict


def solve(inputs_dir: Path) -> Dict[str, pd.DataFrame]:
    input_csv = inputs_dir / "input_01.csv"

    df = pd.read_csv(input_csv, dtype=str)

    df = df.rename(columns={"first_name": "Name"})

    parts = df["File Paths"].str.split(" ", n=1, expand=True)
    parts.columns = ["ListKind", "FileNo"]
    df["ListKind"] = parts["ListKind"].str.strip()
    df["FileNo"] = parts["FileNo"].astype(int)

    df["id"] = df["id"].astype(int)
    df["Index"] = df["FileNo"] * 1000 + df["id"]

    def to_output_label(kind: str) -> str:
        k = (kind or "").strip().lower()
        return "Naughty" if k.startswith("naugh") else "Nice"

    df["ListLabel"] = df["ListKind"].map(to_output_label)

    cnt = (
        df.groupby(["Name", "ListLabel"], as_index=False)["id"]
        .count()
        .rename(columns={"id": "count"})
    )
    pivot = cnt.pivot_table(index="Name", columns="ListLabel", values="count", fill_value=0)
    pivot = pivot.rename(columns={"Naughty": "naughty_count", "Nice": "nice_count"})
    for col in ("naughty_count", "nice_count"):
        if col not in pivot.columns:
            pivot[col] = 0
    pivot = pivot.reset_index()

    latest = (
        df.sort_values(["Name", "Index"])
        .groupby("Name", as_index=False)
        .tail(1)[["Name", "ListLabel"]]
        .rename(columns={"ListLabel": "latest_label"})
    )

    merged = pivot.merge(latest, on="Name", how="left")

    def decide(row: pd.Series) -> str:
        naughty = int(row.get("naughty_count", 0))
        nice = int(row.get("nice_count", 0))
        if naughty > nice:
            return "Naughty"
        if nice > naughty:
            return "Nice"
        return row.get("latest_label", "Nice") or "Nice"

    merged["Naughty or Nice"] = merged.apply(decide, axis=1)

    out = merged[["Naughty or Nice", "Name"]].reset_index(drop=True)

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


