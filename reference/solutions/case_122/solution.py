
import pandas as pd
from pathlib import Path
import numpy as np


def solve(inputs_dir: Path) -> dict[str, pd.DataFrame]:
    prep_air_df = pd.read_csv(inputs_dir / 'input_01.csv')
    other_airlines_df = pd.read_csv(inputs_dir / 'input_02.csv')
    all_airlines_df = pd.concat(
        [prep_air_df, other_airlines_df], ignore_index=True)

    response_counts = all_airlines_df['Airline'].value_counts()
    airlines_to_keep = response_counts[response_counts >= 50].index
    df_filtered = all_airlines_df[all_airlines_df['Airline'].isin(
        airlines_to_keep)].copy()

    def classify_response(score):
        if score <= 6:
            return 'Detractor'
        elif score <= 8:
            return 'Passive'
        else:
            return 'Promoter'

    score_col = 'How likely are you to recommend this airline?'
    if score_col not in df_filtered.columns:
        for cand in df_filtered.columns:
            if 'recommend' in cand.lower() and ('likely' in cand.lower() or 'recommend' in cand.lower()):
                score_col = cand
                break
    df_filtered['Category'] = df_filtered[score_col].apply(classify_response)

    category_counts = df_filtered.groupby(
        ['Airline', 'Category']).size().unstack(fill_value=0)
    total_responses = category_counts.sum(axis=1)

    for cat in ['Promoter', 'Detractor', 'Passive']:
        if cat not in category_counts.columns:
            category_counts[cat] = 0

    percent_promoters = (category_counts['Promoter'] / total_responses) * 100
    percent_detractors = (category_counts['Detractor'] / total_responses) * 100

    nps_scores = np.floor(percent_promoters) - np.floor(percent_detractors)
    nps_df = nps_scores.reset_index(name='NPS')

    avg_nps = nps_df['NPS'].mean()
    std_dev_nps = nps_df['NPS'].std(ddof=1)

    nps_df['Z-Score'] = ((nps_df['NPS'] - avg_nps) / std_dev_nps).round(2)

    prep_air_output = nps_df[nps_df['Airline'] == 'Prep Air'].copy()

    prep_air_output['NPS'] = prep_air_output['NPS'].astype(int)

    return {'output_01.csv': prep_air_output[['Airline', 'NPS', 'Z-Score']]}


if __name__ == "__main__":
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    cand_dir = task_dir / "cand"

    cand_dir.mkdir(exist_ok=True)

    results = solve(inputs_dir)

    for filename, df in results.items():
        df.to_csv(cand_dir / filename, index=False, encoding='utf-8')

    print(f"Solution script finished. Outputs are in {cand_dir}")
