from __future__ import annotations
from pathlib import Path
import pandas as pd
import numpy as np


def solve(inputs_dir: Path) -> dict[str, pd.DataFrame]:
    inp_path = inputs_dir / "input_01.csv"
    df = pd.read_csv(inp_path, dtype=str, keep_default_na=False)
    df.columns = [c.strip() for c in df.columns]

    def col_idx(name: str) -> int:
        try:
            return df.columns.get_loc(name)
        except KeyError:
            matches = [i for i, c in enumerate(df.columns) if c.split(".")[0] == name]
            if not matches:
                raise
            return matches[0]

    ser_vals = df['Ser.'].replace('', np.nan)
    ser_vals = ser_vals.where(~ser_vals.str.startswith('N', na=False), other=np.nan)
    ser_num = pd.to_numeric(ser_vals, errors='coerce')
    mask_valid = ser_num.notna()
    df = df.loc[mask_valid].copy()
    ser_num = ser_num.loc[mask_valid]

    df['Series'] = ser_num.astype(int)
    df['Week'] = pd.to_numeric(df['Wk.'], errors='coerce').astype(int)

    total_idx = col_idx('Total')
    daily_score_cols = df.columns[total_idx-5:total_idx]
    daily_scores = df[daily_score_cols].apply(pd.to_numeric, errors='coerce').fillna(0).astype(int)
    score = pd.to_numeric(df['Total'], errors='coerce').fillna(0).astype(int)

    rate_idx = col_idx('Rate*')
    daily_place_cols = df.columns[rate_idx+1:rate_idx+6]
    daily_places = df[daily_place_cols].astype(str)

    place_to_pts = {'1st': 4, '2nd': 3, '3rd': 2, '4th': 1}
    daily_points = daily_places.map(lambda x: place_to_pts.get(x.strip(), 0))
    
    points_wo_double = daily_points.sum(axis=1).astype(int)
    
    friday_points = daily_places.iloc[:, -1].map(lambda x: place_to_pts.get(str(x).strip(), 0)).astype(int)
    points_with_double = (points_wo_double + friday_points).astype(int)

    def rank_desc(s: pd.Series) -> pd.Series:
        return s.rank(ascending=False, method='min').astype(int)

    counts_start = rate_idx + 6
    points_week_col = df.columns[counts_start+4]
    rank_week_col = df.columns[counts_start+5]
    def rank_str_to_num(x: str) -> int:
        x = str(x).strip()
        num = ''.join(ch for ch in x if ch.isdigit())
        try:
            return int(num) if num else int(x)
        except Exception:
            return 0
    original_rank = df[rank_week_col].map(rank_str_to_num).astype(int)

    friday_score = daily_scores.iloc[:, -1]
    score_double_friday = (score + friday_score).astype(int)

    out = pd.DataFrame({
        'Series': df['Series'].values,
        'Week': df['Week'].values,
        'Player': df['Player'].values,
        'Original Rank': original_rank.values,
        'Score': score.values,
        'Points': points_with_double.values,
        'Score if double Friday': score_double_friday.values,
        'Points without double points Friday': points_wo_double.values,
    })

    out['Rank without double points Friday'] = out.groupby(['Series', 'Week'])['Points without double points Friday'].transform(rank_desc)
    out['Rank based on Score'] = out.groupby(['Series', 'Week'])['Score'].transform(rank_desc)
    out['Rank if Double Score Friday'] = out.groupby(['Series', 'Week'])['Score if double Friday'].transform(rank_desc)

    def group_winner_change(g: pd.DataFrame, rank_col: str) -> pd.Series:
        orig_set = set(g.loc[g['Original Rank'] == 1, 'Player'].astype(str))
        new_set = set(g.loc[g[rank_col] == 1, 'Player'].astype(str))
        changed = not orig_set.issubset(new_set)
        return pd.Series([changed] * len(g), index=g.index)

    out['Change in winner with no double points Friday?'] = out.groupby(['Series', 'Week'], group_keys=False).apply(lambda g: group_winner_change(g, 'Rank without double points Friday'))
    out['Change in winner based on Score?'] = out.groupby(['Series', 'Week'], group_keys=False).apply(lambda g: group_winner_change(g, 'Rank based on Score'))
    out['Change in winner if Double Score Friday?'] = out.groupby(['Series', 'Week'], group_keys=False).apply(lambda g: group_winner_change(g, 'Rank if Double Score Friday'))

    num_cols = ['Series', 'Week', 'Original Rank', 'Rank without double points Friday',
                'Rank based on Score', 'Rank if Double Score Friday', 'Score', 'Points',
                'Score if double Friday', 'Points without double points Friday']
    for c in num_cols:
        out[c] = pd.to_numeric(out[c], errors='coerce').astype(int)

    for c in [
        'Change in winner with no double points Friday?',
        'Change in winner based on Score?',
        'Change in winner if Double Score Friday?']:
        out[c] = out[c].astype(bool)

    cols = [
        'Series', 'Week', 'Player', 'Original Rank', 'Rank without double points Friday',
        'Change in winner with no double points Friday?', 'Rank based on Score',
        'Change in winner based on Score?', 'Rank if Double Score Friday',
        'Change in winner if Double Score Friday?', 'Score', 'Points',
        'Score if double Friday', 'Points without double points Friday'
    ]
    out = out[cols]

    return {"output_01.csv": out}


if __name__ == "__main__":
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    cand_dir = task_dir / "cand"
    cand_dir.mkdir(parents=True, exist_ok=True)

    outputs = solve(inputs_dir)
    for filename, df in outputs.items():
        df.to_csv(cand_dir / filename, index=False, encoding="utf-8")
