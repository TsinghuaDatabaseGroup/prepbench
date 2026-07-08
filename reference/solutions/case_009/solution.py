from __future__ import annotations
from pathlib import Path
import pandas as pd
import re


def solve(inputs_dir: Path) -> dict[str, pd.DataFrame]:
    tweets_path = inputs_dir / "input_01.csv"
    stops_path = inputs_dir / "input_02.csv"

    df = pd.read_csv(tweets_path)
    stops = pd.read_csv(stops_path)
    def norm(w): return re.sub(r"[^A-Za-z]", "", w).lower()
    stop_norm_set = set(map(norm, stops['Word']))

    output_rows = [
        {'Words': tok, 'Tweet': t}
        for t in df['Tweet'].str.replace('@C&BSudsCo', '', regex=False)
        for tok in dict.fromkeys(re.sub(r"[^A-Za-z ]", "", t).split())
        if norm(tok) not in stop_norm_set
    ]

    out_df = pd.DataFrame(output_rows, columns=['Words', 'Tweet'])

    return {"output_01.csv": out_df}


if __name__ == "__main__":
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    cand_dir = task_dir / "cand"
    cand_dir.mkdir(parents=True, exist_ok=True)

    result = solve(inputs_dir)
    for fname, df in result.items():
        (cand_dir / fname).parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(cand_dir / fname, index=False, encoding='utf-8')
