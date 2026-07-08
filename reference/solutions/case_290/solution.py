from __future__ import annotations

from pathlib import Path
from typing import Dict

import pandas as pd


def solve(inputs_dir: Path) -> Dict[str, pd.DataFrame]:
    def parse_cell(cell_text: str, current_matchday: int, source_row_number: int) -> dict | None:
        if not isinstance(cell_text, str) or not cell_text.strip():
            return None

        text = cell_text.strip()

        if text.startswith("Matchday"):
            return None

        raw_lines = [ln.strip() for ln in text.split("\n")]
        lines: list[str] = []
        for ln in raw_lines:
            if not ln:
                continue
            lnu = ln.lower()
            if lnu == "ft":
                continue
            if lnu.startswith("match recap") or lnu.startswith("match highlights"):
                continue
            if "\u25ba" in ln or "►" in ln:
                continue
            lines.append(ln)

        if not lines:
            return None

        date_parsed = None
        date_idx = None
        for j, token in enumerate(lines):
            try:
                cand = pd.to_datetime(token, dayfirst=True, errors="raise")
                date_parsed = cand
                date_idx = j
                break
            except Exception:
                continue
        if date_parsed is None:
            return None

        tokens = lines[date_idx + 1:]

        def is_int_token(s: str) -> bool:
            try:
                int(s)
                return True
            except Exception:
                return False

        i = 0
        while i < len(tokens) and not is_int_token(tokens[i]):
            i += 1
        if i >= len(tokens):
            return None
        home_score = int(tokens[i])
        i += 1

        if i >= len(tokens):
            return None
        home_team = tokens[i]
        i += 1
        if i < len(tokens) and tokens[i] == home_team:
            i += 1

        while i < len(tokens) and not is_int_token(tokens[i]):
            i += 1
        if i >= len(tokens):
            return None
        away_score = int(tokens[i])
        i += 1

        if i >= len(tokens):
            return None
        away_team = tokens[i]
        i += 1
        if i < len(tokens) and tokens[i] == away_team:
            i += 1

        return {
            "Away Score": away_score,
            "Away Team": away_team,
            "Home Score": home_score,
            "Home Team": home_team,
            "Matchday": int(current_matchday) if pd.notna(current_matchday) else None,
            "Source Row Number": int(source_row_number),
            "Date": date_parsed.strftime("%d/%m/%Y"),
        }

    input_file = inputs_dir / "input_01.csv"
    df_raw = pd.read_csv(input_file, header=None, names=["col_a", "col_b"], dtype=str)

    records: list[dict] = []
    current_matchday: int | None = None

    source_counter = 0
    first_row = True
    for _, row in df_raw.iterrows():
        for col in ["col_a", "col_b"]:
            val = row[col]
            if isinstance(val, str) and val.startswith("Matchday"):
                try:
                    part = val.split("Matchday", 1)[1].strip()
                    day_str = part.split("of", 1)[0].strip()
                    current_matchday = int(day_str)
                except Exception:
                    pass

        vals = [row["col_a"], row["col_b"]]
        is_pure_announcer = all(isinstance(v, str) and v.startswith("Matchday") for v in vals) and not any(
            isinstance(v, str) and "FT" in v for v in vals
        )

        if first_row:
            has_any_ft = any(isinstance(v, str) and "FT" in v for v in vals)
            if not has_any_ft:
                pass
            else:
                source_counter += 1
        else:
            source_counter += 1
        first_row = False

        for col in ["col_a", "col_b"]:
            rec = parse_cell(row[col], current_matchday, source_counter)
            if rec is not None and rec.get("Matchday") is not None:
                records.append(rec)

    out_df = pd.DataFrame.from_records(records, columns=[
        "Away Score",
        "Away Team",
        "Home Score",
        "Home Team",
        "Matchday",
        "Source Row Number",
        "Date",
    ])

    numeric_cols = ["Away Score", "Home Score", "Matchday", "Source Row Number"]
    for c in numeric_cols:
        out_df[c] = pd.to_numeric(out_df[c], errors="coerce").astype("Int64").astype("int64")


    return {"output_01.csv": out_df}


if __name__ == "__main__":
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    cand_dir = task_dir / "cand"
    cand_dir.mkdir(parents=True, exist_ok=True)

    outputs = solve(inputs_dir)
    for filename, df in outputs.items():
        (cand_dir / filename).parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(cand_dir / filename, index=False, encoding="utf-8")


