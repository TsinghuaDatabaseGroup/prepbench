from __future__ import annotations

from pathlib import Path
from typing import Dict

import re
import pandas as pd


def solve(inputs_dir: Path) -> Dict[str, pd.DataFrame]:
    def clean_total_points(val: str) -> int:
        if pd.isna(val):
            return None
        m = re.findall(r"\d+", str(val))
        return int(m[0]) if m else None

    def split_value_and_pos(text: str) -> tuple[str, float | None]:
        s = str(text)
        m = re.match(r"^(.*?)(?:\(([-+]?\d+)\))?$", s)
        if not m:
            return s, None
        value = m.group(1).strip()
        pos = m.group(2)
        return value, (float(pos) if pos is not None else None)

    events = pd.read_csv(inputs_dir / "input_01.csv")
    raw = pd.read_csv(inputs_dir / "input_02.csv")

    if "800.1" in raw.columns:
        raw = raw.drop(columns=["800.1"])

    raw = raw.rename(columns={
        "POS": "Position",
        "ATHLETE": "Athlete",
        "NAT": "Nationality",
        "POINTS": "Total Points",
    })

    raw[["Position", "Athlete", "Nationality", "Total Points"]] = (
        raw[["Position", "Athlete", "Nationality", "Total Points"]].ffill()
    )

    raw["Total Points"] = raw["Total Points"].map(clean_total_points)

    event_cols = ["100H", "HJ", "SP", "200", "LJ", "JT", "800"]
    melted = raw.melt(
        id_vars=["Position", "Athlete", "Nationality", "Total Points", "Breakdown"],
        value_vars=event_cols,
        var_name="Event",
        value_name="Value",
    )

    score = melted[melted["Breakdown"] == "Event Score"][
        ["Position", "Athlete", "Nationality", "Total Points", "Event", "Value"]
    ].rename(columns={"Value": "Event Points"})

    perf = melted[melted["Breakdown"] == "Event Time/Distance"][
        ["Position", "Athlete", "Nationality", "Total Points", "Event", "Value"]
    ].rename(columns={"Value": "Event Time/Distance"})

    rolling = melted[melted["Breakdown"] == "Rolling Total"][
        ["Position", "Athlete", "Nationality", "Total Points", "Event", "Value"]
    ].rename(columns={"Value": "Rolling Total"})

    df = score.merge(perf, on=["Position", "Athlete", "Nationality", "Total Points", "Event"], how="inner")
    df = df.merge(rolling, on=["Position", "Athlete", "Nationality", "Total Points", "Event"], how="inner")

    df = df.merge(events, on="Event", how="left")

    event_perf = df["Event Time/Distance"].map(lambda x: split_value_and_pos(x))
    perf_values = [v for v, _ in event_perf]
    perf_values = ["" if str(v).strip().upper() == "NM" else v for v in perf_values]
    df["Event Time/Distance"] = perf_values
    df["Event Position"] = [p for _, p in event_perf]

    rolling_parsed = df["Rolling Total"].map(lambda x: split_value_and_pos(x))
    df["Rolling Total Points"] = [float(v) if v != "" else None for v, _ in rolling_parsed]
    df["Position After Event"] = [p for _, p in rolling_parsed]

    df["Event Points"] = pd.to_numeric(df["Event Points"], errors="coerce")
    df["Position"] = pd.to_numeric(df["Position"], errors="coerce")
    df["Event No."] = pd.to_numeric(df["Event No."], errors="coerce")

    out = df[[
        "Position",
        "Athlete",
        "Nationality",
        "Total Points",
        "Event Name",
        "Event Type",
        "Event No.",
        "Event Time/Distance",
        "Event Points",
        "Event Position",
        "Rolling Total Points",
        "Position After Event",
    ]].copy()

    out = out.sort_values(by=["Position", "Event No."], kind="mergesort").reset_index(drop=True)

    out.insert(0, "Sort", range(1, len(out) + 1))

    return {"output_01.csv": out}


if __name__ == "__main__":
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    cand_dir = task_dir / "cand"
    cand_dir.mkdir(parents=True, exist_ok=True)

    outputs = solve(inputs_dir)
    for filename, data in outputs.items():
        out_path = cand_dir / filename
        data.to_csv(out_path, index=False, encoding="utf-8")


