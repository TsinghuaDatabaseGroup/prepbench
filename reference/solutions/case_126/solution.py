from pathlib import Path
from typing import Dict, List, Tuple
import pandas as pd
import numpy as np


def _parse_percent_to_counts(percent_series: pd.Series, total_slots: int = 1000) -> List[int]:
    perc = pd.to_numeric(percent_series, errors="coerce").fillna(0.0)
    raw = perc * total_slots / 100.0
    floors = np.floor(raw).astype(int)
    remainder = raw - floors

    current_sum = int(floors.sum())
    need = total_slots - current_sum
    counts = floors.tolist()

    if need > 0:
        order = np.argsort(-remainder.values)
        for idx in order[:need]:
            counts[int(idx)] += 1
    elif need < 0:
        order = np.argsort(remainder.values)
        for idx in order[: -need]:
            take = min(counts[int(idx)], 1)
            counts[int(idx)] -= take
    return counts


essential_cols = ["Seed", "1", "2", "3", "4"]


def solve(inputs_dir: Path) -> Dict[str, pd.DataFrame]:
    odds_path = inputs_dir / "input_01.csv"
    seeds_path = inputs_dir / "input_02.csv"

    odds = pd.read_csv(odds_path)
    teams = pd.read_csv(seeds_path)

    odds = odds[essential_cols].copy()
    odds = odds.sort_values("Seed").reset_index(drop=True)
    teams = teams.sort_values("Seed").reset_index(drop=True)

    pick_cols = ["1", "2", "3", "4"]
    number_range = np.arange(1, 1000 + 1)

    number_to_seed: Dict[str, List[int]] = {}

    for col in pick_cols:
        counts = _parse_percent_to_counts(odds[col])
        mapping: List[int] = []
        for seed, cnt in zip(odds["Seed"].tolist(), counts):
            if cnt > 0:
                mapping.extend([int(seed)] * int(cnt))
        if len(mapping) < 1000:
            seeds_cycle = odds["Seed"].tolist()
            i = 0
            while len(mapping) < 1000:
                mapping.append(int(seeds_cycle[i % len(seeds_cycle)]))
                i += 1
        elif len(mapping) > 1000:
            mapping = mapping[:1000]
        number_to_seed[col] = mapping

    winning_numbers = {"1": 282, "2": 95, "3": 378, "4": 48}

    lottery_rows: List[Tuple[int, int, str]] = []

    for pick_str in pick_cols:
        win_num = winning_numbers[pick_str]
        seed = number_to_seed[pick_str][win_num - 1]
        team_name = teams.loc[teams["Seed"] == seed, "Team"].iloc[0]
        lottery_rows.append((int(pick_str), int(seed), str(team_name)))

    remaining_rows: List[Tuple[int, int, str]] = []
    actual_pick = 5
    for seed in teams["Seed"].tolist():
        if actual_pick > 14:
            break
        team_name = teams.loc[teams["Seed"] == seed, "Team"].iloc[0]
        remaining_rows.append((actual_pick, int(seed), str(team_name)))
        actual_pick += 1

    all_rows = lottery_rows + remaining_rows
    out_df = pd.DataFrame(all_rows, columns=["Actual Pick", "Original", "Team"])

    out_df["Actual Pick"] = pd.to_numeric(out_df["Actual Pick"], downcast="integer")
    out_df["Original"] = pd.to_numeric(out_df["Original"], downcast="integer")
    out_df["Team"] = out_df["Team"].astype(str)

    return {
        "output_01.csv": out_df
    }


if __name__ == "__main__":
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"

    cand_dir = task_dir / "cand"
    cand_dir.mkdir(parents=True, exist_ok=True)

    outputs = solve(inputs_dir)

    for filename, df in outputs.items():
        (cand_dir / filename).parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(cand_dir / filename, index=False, encoding="utf-8")
