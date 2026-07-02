from __future__ import annotations
from pathlib import Path
import pandas as pd


def solve(inputs_dir: Path) -> dict[str, pd.DataFrame]:
    frames = []
    if inputs_dir.exists() and inputs_dir.is_dir():
        for p in sorted(inputs_dir.glob("*.csv")):
            try:
                frames.append(pd.read_csv(p))
            except Exception:
                continue
    if not frames:
        out = pd.DataFrame(columns=[
            "Animal Type",
            "Adopted, Returned to Owner or Transferred",
            "Other",
        ])
        return {"output_01.csv": out}

    df = pd.concat(frames, ignore_index=True)

    cols = {c.strip(): c for c in df.columns}

    animal_col = None
    for cand in [
        "Animal Type", "animal_type", "animal type",
    ]:
        if cand in cols:
            animal_col = cols[cand]
            break
    outcome_col = None
    for cand in [
        "Outcome Type", "outcome_type", "outcome type", "Outcome", "outcome",
    ]:
        if cand in cols:
            outcome_col = cols[cand]
            break

    if animal_col is None or outcome_col is None:
        raise ValueError(
            "Required columns not found: need Animal Type and Outcome Type")

    df[animal_col] = df[animal_col].astype(str)
    mask_cd = df[animal_col].str.strip().str.title().isin(["Cat", "Dog"])
    df_cd = df.loc[mask_cd, [animal_col, outcome_col]].copy()

    def map_group(x: str) -> str:
        if pd.isna(x):
            return "Other"
        s = str(x).strip().title()
        if s in {"Adoption", "Adopted"}:
            return "Adopted, Returned to Owner or Transferred"
        if s in {"Return To Owner", "Returned To Owner"}:
            return "Adopted, Returned to Owner or Transferred"
        if s in {"Transfer", "Transferred"}:
            return "Adopted, Returned to Owner or Transferred"
        return "Other"

    df_cd["group"] = df_cd[outcome_col].map(map_group)

    df_cd["AnimalTypeNorm"] = df_cd[animal_col].str.strip().str.title()

    totals = df_cd.groupby("AnimalTypeNorm").size().rename(
        "Total").reset_index()
    grp = (
        df_cd.groupby(["AnimalTypeNorm", "group"])
        .size()
        .rename("cnt")
        .reset_index()
        .merge(totals, on="AnimalTypeNorm", how="left")
    )
    grp["pct"] = grp["cnt"] / grp["Total"] * 100.0

    pivot = (
        grp.pivot(index="AnimalTypeNorm", columns="group", values="pct")
        .fillna(0.0)
        .reset_index()
    )

    pos_col = "Adopted, Returned to Owner or Transferred"
    other_col = "Other"
    if pos_col not in pivot.columns:
        pivot[pos_col] = 0.0
    if other_col not in pivot.columns:
        pivot[other_col] = 0.0

    pivot = pivot.rename(columns={"AnimalTypeNorm": "Animal Type"})

    order = ["Dog", "Cat"]
    pivot["_order"] = pivot["Animal Type"].apply(
        lambda x: order.index(x) if x in order else len(order))
    pivot = pivot.sort_values(["_order", "Animal Type"]).drop(
        columns=["_order"]).reset_index(drop=True)

    pivot[pos_col] = pivot[pos_col].astype(float).round(1)
    pivot[other_col] = pivot[other_col].astype(float).round(1)

    out = pivot[["Animal Type", pos_col, other_col]].copy()

    return {"output_01.csv": out}


if __name__ == "__main__":
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    cand_dir = task_dir / "cand"
    cand_dir.mkdir(parents=True, exist_ok=True)

    outputs = solve(inputs_dir)
    for fname, df in outputs.items():
        (cand_dir / fname).parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(cand_dir / fname, index=False, encoding="utf-8")
