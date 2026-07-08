from __future__ import annotations
from pathlib import Path
from typing import Dict
import pandas as pd
import numpy as np


def solve(inputs_dir: Path) -> dict[str, pd.DataFrame]:
    input_files = sorted([p for p in inputs_dir.glob("*.csv")])
    if not input_files:
        raise FileNotFoundError("No input CSV files found in inputs directory")

    use_cols = [
        "Name",
        "Position",
        "Appearances",
        "Goals",
        "Headed goals",
        "Goals with right foot",
        "Goals with left foot",
        "Penalties scored",
        "Freekicks scored",
    ]

    frames = []
    for fp in input_files:
        df = pd.read_csv(fp, usecols=lambda c: c in use_cols, dtype=str)
        for c in use_cols:
            if c not in df.columns:
                df[c] = np.nan
        frames.append(df[use_cols].copy())

    raw = pd.concat(frames, ignore_index=True)

    raw["Name"] = raw["Name"].astype(str).str.strip()
    raw["Position"] = raw["Position"].astype(str).str.strip()

    raw = raw[raw["Position"].str.lower() != "goalkeeper"].copy()

    num_cols = [
        "Appearances",
        "Goals",
        "Headed goals",
        "Goals with right foot",
        "Goals with left foot",
        "Penalties scored",
        "Freekicks scored",
    ]

    for c in num_cols:
        raw[c] = (
            raw[c]
            .astype(str)
            .str.replace(",", "", regex=False)
            .str.replace("%", "", regex=False)
        )
        raw[c] = pd.to_numeric(raw[c], errors="coerce")

    raw = raw[raw["Appearances"].fillna(0) > 0].copy()

    for c in [
        "Goals",
        "Headed goals",
        "Goals with right foot",
        "Goals with left foot",
        "Penalties scored",
        "Freekicks scored",
    ]:
        raw[c] = raw[c].fillna(0)

    agg = (
        raw.groupby(["Name", "Position"], as_index=False)
        .agg(
            {
                "Appearances": "sum",
                "Goals": "sum",
                "Headed goals": "sum",
                "Goals with right foot": "sum",
                "Goals with left foot": "sum",
                "Penalties scored": "sum",
                "Freekicks scored": "sum",
            }
        )
    )

    agg["Open Play Goals"] = (
        agg["Goals"].fillna(0) - agg["Penalties scored"].fillna(0) -
        agg["Freekicks scored"].fillna(0)
    )

    for c in [
        "Appearances",
        "Goals",
        "Headed goals",
        "Goals with right foot",
        "Goals with left foot",
        "Open Play Goals",
    ]:
        agg[c] = agg[c].round(0).astype(int)

    agg["Open Play Goals/Game"] = (agg["Open Play Goals"] /
                                   agg["Appearances"]).round(9)

    agg = agg.rename(columns={"Goals": "Total Goals"})

    base_cols = [
        "Open Play Goals",
        "Goals with right foot",
        "Goals with left foot",
        "Position",
        "Appearances",
        "Total Goals",
        "Open Play Goals/Game",
        "Headed goals",
        "Name",
    ]
    base = agg[base_cols].copy()

    base["Rank"] = base["Open Play Goals"].rank(
        method="min", ascending=False).astype(int)
    out1 = base[base["Rank"] <= 20].copy()
    out1 = out1[
        [
            "Open Play Goals",
            "Goals with right foot",
            "Goals with left foot",
            "Position",
            "Appearances",
            "Rank",
            "Total Goals",
            "Open Play Goals/Game",
            "Headed goals",
            "Name",
        ]
    ].sort_values(["Rank", "Name"]).reset_index(drop=True)

    base2 = base.copy()
    base2["Rank by Position"] = (
        base2.groupby("Position")["Open Play Goals"].rank(
            method="min", ascending=False).astype(int)
    )
    out2 = base2[base2["Rank by Position"] <= 20].copy()
    out2 = out2[
        [
            "Rank by Position",
            "Open Play Goals",
            "Goals with right foot",
            "Goals with left foot",
            "Position",
            "Appearances",
            "Total Goals",
            "Open Play Goals/Game",
            "Headed goals",
            "Name",
        ]
    ].sort_values(["Position", "Rank by Position", "Name"]).reset_index(drop=True)

    return {
        "output_01.csv": out1,
        "output_02.csv": out2,
    }


if __name__ == "__main__":
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    cand_dir = task_dir / "cand"
    cand_dir.mkdir(parents=True, exist_ok=True)

    out = solve(inputs_dir)
    for fname, df in out.items():
        df.to_csv(cand_dir / fname, index=False, encoding="utf-8")
