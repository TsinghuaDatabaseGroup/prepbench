from pathlib import Path
from typing import Dict

import pandas as pd


def solve(inputs_dir: Path) -> Dict[str, pd.DataFrame]:
    overview_path = inputs_dir / "input_04.csv"
    df = pd.read_csv(overview_path)

    base_columns = [
        "Country",
        "2023 SDG Index Score",
        "2023 SDG Index Rank",
        "Regions used for the SDR",
    ]

    df = df[df["Country"].notna()].copy()
    df["_row_order"] = range(len(df))

    extra_columns = [col for col in df.columns if col not in base_columns + ["_row_order"]]
    if len(extra_columns) % 2 != 0:
        raise ValueError("Unexpected number of SDG columns; expected pairs of value and trend columns.")

    long_frames = []
    value_map = {
        "green": "Goal Achieved",
        "yellow": "Challenges Remaining",
        "orange": "Significant Challenges",
        "red": "Major Challenges",
        "grey": "Insufficient",
        "Goal Achieved": "Goal Achieved",
        "Challenges Remaining": "Challenges Remaining",
        "Significant Challenges": "Significant Challenges",
        "Major Challenges": "Major Challenges",
        "Insufficient": "Insufficient",
    }
    trend_map = {
        "↑": "On Track",
        "➚": "Moderately Increasing",
        "→": "Stagnating",
        "↓": "Decreasing",
        "On Track": "On Track",
        "Moderately Increasing": "Moderately Increasing",
        "Stagnating": "Stagnating",
        "Decreasing": "Decreasing",
    }

    for idx in range(0, len(extra_columns), 2):
        value_col = extra_columns[idx]
        trend_col = extra_columns[idx + 1]
        goal_name = value_col.strip()

        subset = df[base_columns + ["_row_order", value_col, trend_col]].copy()
        subset["SDG Name"] = goal_name
        subset = subset.rename(columns={value_col: "SDG Value", trend_col: "SDG Trend"})
        subset["goal_order"] = idx // 2
        long_frames.append(subset)

    result = pd.concat(long_frames, ignore_index=True)
    result = result.sort_values(["_row_order", "goal_order"], kind="mergesort")
    result = result.drop(columns=["_row_order", "goal_order"]).reset_index(drop=True)

    result["SDG Value"] = result["SDG Value"].map(value_map).fillna(result["SDG Value"])
    result["SDG Trend"] = result["SDG Trend"].map(trend_map).fillna(result["SDG Trend"])

    ordered_columns = base_columns + ["SDG Name", "SDG Value", "SDG Trend"]
    result = result[ordered_columns]

    score_series = pd.to_numeric(result["2023 SDG Index Score"], errors="coerce")
    result["2023 SDG Index Score"] = score_series.round(9)
    rank_series = pd.to_numeric(result["2023 SDG Index Rank"], errors="coerce").astype("Int64")
    result["2023 SDG Index Rank"] = rank_series

    return {"output_01.csv": result}


if __name__ == "__main__":
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    cand_dir = task_dir / "cand"
    cand_dir.mkdir(exist_ok=True)

    outputs = solve(inputs_dir)
    for filename, dataframe in outputs.items():
        output_path = cand_dir / filename
        dataframe.to_csv(output_path, index=False)

