from __future__ import annotations
from pathlib import Path
import pandas as pd
import re
from typing import Dict


def solve(inputs_dir: Path) -> dict[str, pd.DataFrame]:
    input_path = inputs_dir / "input_01.csv"
    df = pd.read_csv(input_path)

    df = df.replace({"NA": pd.NA})

    def extract_event_id(s: str) -> int:
        m = re.search(r"(\d+)\s*$", str(s))
        return int(m.group(1)) if m else pd.NA

    df["Event id"] = df["event"].apply(extract_event_id)

    def split_competitor(s: str) -> tuple[str, str | None]:
        s = str(s)
        m = re.match(r"^(.*?)\s*\(([^)]+)\)\s*$", s)
        if m:
            return m.group(1), m.group(2)
        return s, None

    comp_assoc = df["Competitors"].apply(split_competitor)
    df["Competitor Name"] = comp_assoc.apply(lambda x: x[0])
    df["Association"] = comp_assoc.apply(lambda x: x[1])

    frac_map = {
        "½": 0.5,
        "⅓": 1/3,
        "⅔": 2/3,
    }

    def parse_number_with_fraction(val: object) -> tuple[float | None, bool]:
        if pd.isna(val):
            return None, False
        s = str(val)
        potout = False
        if s.endswith("*"):
            potout = True
            s = s[:-1]
        s = s.strip()
        if s == "":
            return None, potout
        base_num = 0.0
        m = re.match(r"^\s*(-?\d+(?:\.\d+)?)?\s*([\u00BC-\u00BE\u2150-\u215E])?\s*$", s)
        if m:
            if m.group(1) is not None:
                base_num = float(m.group(1))
            frac_char = m.group(2)
            if frac_char:
                base_num += frac_map.get(frac_char, 0.0)
            if any(ch in s for ch in ("⅓", "⅔")):
                base_num = round(base_num + 1e-12, 2)
            return base_num, potout
        try:
            num = float(s)
            return num, potout
        except Exception:
            return None, potout

    game_cols = [c for c in ["G2","G3","G4","G5","G6","G7","G8","G1"] if c in df.columns]

    games_rows = []
    for _, row in df.iterrows():
        event_id = row["Event id"]
        competitor = row["Competitor Name"]
        note = row.get("note", None)
        for gcol in game_cols:
            val = row.get(gcol, pd.NA)
            if pd.isna(val):
                continue
            score, pot = parse_number_with_fraction(val)
            if score is None:
                continue
            games_rows.append({
                "Event id": int(event_id),
                "Game Order": gcol,
                "Competitor Name": competitor,
                "Score": float(score),
                "Potout": bool(pot),
                "note": note if pd.notna(note) else "",
            })

    out1 = pd.DataFrame(games_rows, columns=["Event id","Game Order","Competitor Name","Score","Potout","note"])


    def parse_event_start_date(desc: object) -> pd.Timestamp | pd.NaT:
        if pd.isna(desc):
            return pd.NaT
        s = str(desc)
        m = re.search(r"(\d{1,2} \w+ \d{4})", s)
        if not m:
            return pd.NaT
        date_str = m.group(1)
        try:
            return pd.to_datetime(date_str, dayfirst=True)
        except Exception:
            return pd.NaT

    points_parsed = df["Pts"].apply(lambda v: parse_number_with_fraction(v)[0])
    def round_if_thirds(x: float | None, raw: object) -> float | None:
        if x is None:
            return None
        s = str(raw)
        if any(ch in s for ch in ("⅓", "⅔")):
            return round(float(x) + 1e-12, 2)
        return float(x)

    points = [round_if_thirds(x, r) for x, r in zip(points_parsed.tolist(), df["Pts"].tolist())]

    def normalize_desc(desc: object) -> str:
        if pd.isna(desc):
            return ""
        s = str(desc).replace("\r\n", "\n").replace("\r", "\n")
        parts = [p.strip() for p in s.split("\n")]
        return "\n".join(parts)

    event_desc_norm = df["description"].apply(normalize_desc)

    out2 = pd.DataFrame({
        "Event id": df["Event id"].astype(int),
        "Competitor Name": df["Competitor Name"],
        "Event": df["event"],
        "Event Start Date": event_desc_norm.apply(parse_event_start_date),
        "Event Description": event_desc_norm,
        "Association": df["Association"],
        "Points": pd.Series(points, dtype=float),
        "Wins": df["W"].astype("Int64").fillna(0).astype(int),
        "Losses": df["L"].astype("Int64").fillna(0).astype(int),
        "Ties": df["T"].astype("Int64").fillna(0).astype(int),
    }, columns=[
        "Event id","Competitor Name","Event","Event Start Date","Event Description","Association","Points","Wins","Losses","Ties"
    ])

    out2 = out2.sort_values(["Event id"], ascending=False, kind="stable")

    out1 = out1.sort_values(["Event id"], ascending=False, kind="stable")

    return {
        "output_01.csv": out1.reset_index(drop=True),
        "output_02.csv": out2.reset_index(drop=True),
    }


if __name__ == "__main__":
    import sys
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    cand_dir = task_dir / "cand"
    cand_dir.mkdir(exist_ok=True)

    outputs = solve(inputs_dir)

    for fname, df in outputs.items():
        (cand_dir / fname).parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(cand_dir / fname, index=False, encoding="utf-8")

