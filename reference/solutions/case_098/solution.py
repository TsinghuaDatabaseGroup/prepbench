import re
from pathlib import Path
from typing import Dict

import numpy as np
import pandas as pd


def solve(inputs_dir: Path) -> Dict[str, pd.DataFrame]:

    def parse_to_par(value: object) -> float:
        if pd.isna(value):
            return np.nan
        text = str(value).strip()
        if not text:
            return np.nan
        text = text.replace("\u2212", "-")
        text = text.replace("\u2012", "-")
        text = text.replace("\u2013", "-")
        text = text.replace("\u2014", "-")
        text = text.replace("\xa0", "")
        text = re.sub(r"(?i)po", "", text)
        text = text.replace(" ", "")
        upper = text.upper()
        if upper in {"E", "EVEN"}:
            return 0.0
        match = re.search(r"[-+]?\d+", text)
        if match:
            return float(match.group(0))
        return np.nan

    winners = pd.read_csv(inputs_dir / "input_01.csv")
    for col in ["Champion", "Country", "Venue", "Location"]:
        winners[col] = winners[col].astype(str).str.replace("\xa0", " ", regex=False).str.strip()
    winners["Year"] = pd.to_numeric(winners["Year"], errors="coerce")
    winners = winners.dropna(subset=["Year"])
    winners["Year"] = winners["Year"].astype(int)
    winners = winners[["Year", "Country", "Venue", "Location"]]

    rounds = pd.read_csv(inputs_dir / "input_02.csv")
    rounds = rounds.rename(
        columns={
            "to par": "to_par",
            "round 1": "Round 1",
            "round 2": "Round 2",
            "round 3": "Round 3",
            "round 4": "Round 4",
            "total": "Total",
            "year": "Year",
            "player": "Player",
        }
    )
    rounds["Player"] = rounds["Player"].astype(str).str.strip()
    numeric_cols = ["Round 1", "Round 2", "Round 3", "Round 4", "Total", "Year"]
    rounds[numeric_cols] = rounds[numeric_cols].apply(pd.to_numeric, errors="coerce")
    rounds = rounds.dropna(subset=["Year", "Total"])
    rounds["Year"] = rounds["Year"].astype(int)
    rounds["Total"] = rounds["Total"].astype(int)
    rounds["to_par_num"] = rounds.get("to_par", pd.Series(index=rounds.index)).apply(parse_to_par)
    rounds["Round Par"] = (rounds["Total"] - rounds["to_par_num"]) / 4
    rounds["Round Par"] = rounds["Round Par"].round(0).astype(int)

    combined = rounds.merge(
        winners,
        on="Year",
        how="left",
        validate="one_to_one",
    )

    round_columns = ["Round 1", "Round 2", "Round 3", "Round 4"]
    long_df = combined.melt(
        id_vars=[
            "Year",
            "Player",
            "Country",
            "Venue",
            "Location",
            "Total",
            "Round Par",
        ],
        value_vars=round_columns,
        var_name="Round Num",
        value_name="Round Score",
    )
    long_df = long_df.dropna(subset=["Round Score"])
    long_df["Round Score"] = long_df["Round Score"].astype(int)
    long_df["Round Par"] = long_df["Round Par"].astype(int)
    long_df["Round to Par"] = long_df["Round Score"] - long_df["Round Par"]
    long_df["Total"] = long_df["Total"].astype(int)
    long_df["Decade"] = (long_df["Year"] // 10) * 10
    min_decade = long_df["Decade"].min()
    long_df["Row"] = ((long_df["Decade"] - min_decade) // 10) + 1
    long_df["Column"] = long_df["Year"] - long_df["Decade"] + 1
    long_df["Round Number"] = long_df["Round Num"].str.extract(r"(\d+)").astype(int)
    round_color_map = {1: "A", 2: "B", 3: "C", 4: "D"}
    long_df["Round Colors"] = long_df["Round Number"].map(round_color_map)

    coeffs = {
        1: {
            "Point1": (0, 1),
            "Point2": (0, 0),
            "Point3": (1, 0),
            "Point4": (1, 1),
        },
        2: {
            "Point1": (-1, 1),
            "Point2": (-1, 0),
            "Point3": (0, 0),
            "Point4": (0, 1),
        },
        3: {
            "Point1": (-1, 0),
            "Point2": (-1, -1),
            "Point3": (0, -1),
            "Point4": (0, 0),
        },
        4: {
            "Point1": (0, 0),
            "Point2": (0, -1),
            "Point3": (1, -1),
            "Point4": (1, 0),
        },
    }

    point_frames = []
    sqrt_scores = np.sqrt(long_df["Round Score"].astype(float))
    for point in ["Point1", "Point2", "Point3", "Point4"]:
        sub = long_df.copy()
        multipliers = sub["Round Number"].map(lambda r: coeffs[r][point])
        y_mult = multipliers.apply(lambda m: m[0])
        x_mult = multipliers.apply(lambda m: m[1])
        sub["Y Coordinate Polygon"] = np.round(sqrt_scores * y_mult, 9)
        sub["X Coordinate Polygon"] = np.round(sqrt_scores * x_mult, 9)
        sub["Point"] = point
        point_frames.append(sub)

    polygons = pd.concat(point_frames, ignore_index=True)

    point_order = {"Point1": 0, "Point2": 1, "Point3": 2, "Point4": 3}
    round_order = {"Round 1": 1, "Round 2": 2, "Round 3": 3, "Round 4": 4}
    polygons["_point_order"] = polygons["Point"].map(point_order)
    polygons["_round_order"] = polygons["Round Num"].map(round_order)
    polygons = polygons.sort_values(
        by=["_point_order", "_round_order", "Year"],
        ascending=[True, True, False],
    ).drop(columns=["_point_order", "_round_order"]).reset_index(drop=True)

    polygons_output = polygons[
        [
            "Column",
            "Row",
            "Decade",
            "Round to Par",
            "Y Coordinate Polygon",
            "X Coordinate Polygon",
            "Round Colors",
            "Point",
            "Round Score",
            "Round Num",
            "Player",
            "Country",
            "Venue",
            "Location",
            "Round Par",
            "Total",
            "Year",
        ]
    ]

    summary_total = (
        combined.assign(Decade=(combined["Year"] // 10) * 10)
        .groupby("Decade", as_index=False)
        .agg(
            **{
                "Min Total Score": ("Total", "min"),
                "Max Total Score": ("Total", "max"),
            }
        )
    )
    summary_round = (
        long_df.groupby("Decade", as_index=False)
        .agg(
            **{
                "Min Round Score": ("Round Score", "min"),
                "Max Round Score": ("Round Score", "max"),
            }
        )
    )
    summary = (
        summary_round.merge(summary_total, on="Decade", how="inner")
        .sort_values("Decade")
        .reset_index(drop=True)
    )

    outputs = {
        "output_01.csv": polygons_output,
        "output_02.csv": summary[
            [
                "Decade",
                "Min Round Score",
                "Max Round Score",
                "Min Total Score",
                "Max Total Score",
            ]
        ],
    }
    return outputs


if __name__ == "__main__":
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    cand_dir = task_dir / "cand"
    cand_dir.mkdir(parents=True, exist_ok=True)

    results = solve(inputs_dir)
    for filename, df in results.items():
        df.to_csv(cand_dir / filename, index=False, encoding="utf-8")
