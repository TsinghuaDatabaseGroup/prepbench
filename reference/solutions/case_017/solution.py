from __future__ import annotations
from pathlib import Path
from typing import Dict
import pandas as pd


def solve(inputs_dir: Path) -> Dict[str, pd.DataFrame]:
    input_file = inputs_dir / "input_01.csv"
    df = pd.read_csv(input_file)
    pref_col = "Voting Preferences"

    candidates = sorted(set("".join(df[pref_col])))

    fptp_winner = df[pref_col].str[0].value_counts().idxmax()

    def av_winner(ballots: pd.Series) -> str:
        remaining = set(candidates)
        total = len(ballots)
        pref_lists = ballots.apply(list)

        while len(remaining) > 1:
            first_valid = pref_lists.apply(
                lambda prefs: next(c for c in prefs if c in remaining)
            )
            counts = first_valid.value_counts()

            winner = counts.idxmax()
            if counts[winner] > total / 2:
                return winner

            min_votes = counts.min()
            to_eliminate = counts[counts == min_votes].index.min()
            remaining.remove(to_eliminate)

        return next(iter(remaining))

    av_w = av_winner(df[pref_col])

    N = len(candidates)
    borda_df = df[pref_col].apply(list).explode().reset_index(name='candidate')
    borda_df['rank'] = borda_df.groupby('index').cumcount() + 1
    borda_df['points'] = N - borda_df['rank'] + 1
    borda_scores = borda_df.groupby('candidate')['points'].sum()
    borda_winner = borda_scores.idxmax()

    out_df = pd.DataFrame({
        "Voting System": ["FPTP", "Borda", "AV"],
        "Winner": [fptp_winner, borda_winner, av_w],
    })

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
