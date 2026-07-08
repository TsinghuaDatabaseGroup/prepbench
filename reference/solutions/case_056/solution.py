from pathlib import Path
import pandas as pd

def solve(inputs_dir: Path) -> dict[str, pd.DataFrame]:
    df = pd.read_csv(inputs_dir / "input_01.csv")


    same_initial = df['Title'].str[0] == df['LastName'].str[0]
    df = df[((df['Priority'] == 1) & same_initial) | ((df['Priority'] != 1) & ~same_initial)]

    df = df[~((df['LastName'].isin(['Bevens', 'Dimmadome'])) & 
              (df['Product'].isin(['Chamomile Bar', 'Hibiscus Soap-on-a-Rope'])))]
    
    df = df[~((df['Title'] == 'Reverend') & ((df['Product'] == 'Rose Bar') | (df['Priority'] == 2)))]

    df = df[~((df['LastName'] == 'Dimmadome') & (df['Title'] == 'Doctor'))]
    df = df[~((df['Title'] == 'Baroness') & (df['Product'] == 'Hibiscus Soap-on-a-Rope'))]

    df = df[~((df['Title'] == 'Sergeant') & (~df['Priority'].isin([1, 3])))]
    df = df[~((df['Product'] == 'Lemon Gel') & (~df['Priority'].isin([1, 3])))]
    df = df[~((df['Title'] == 'Sergeant') & (df['Product'] != 'Hibiscus Soap-on-a-Rope'))]
    df = df[~((df['Product'] == 'Rose Bar') & (~df['Priority'].isin([2, 4])))]

    titles = set(df['Title'])
    last_names = ['Bevens', 'Shadwell', 'Dimmadome', 'Rotzenheimer']
    products = set(df['Product'])
    priorities = set(df['Priority'])

    by_last = {ln: df[df['LastName'] == ln] for ln in last_names}

    solutions = []
    for _, r_b in by_last['Bevens'].iterrows():
        for _, r_s in by_last['Shadwell'].iterrows():
            if (r_s['Title'] == r_b['Title']) or (r_s['Product'] == r_b['Product']) or (r_s['Priority'] == r_b['Priority']):
                continue
            for _, r_d in by_last['Dimmadome'].iterrows():
                if r_b['Priority'] != r_d['Priority'] + 1:
                    continue
                if (r_d['Title'] in [r_b['Title'], r_s['Title']] or
                    r_d['Product'] in [r_b['Product'], r_s['Product']] or
                    r_d['Priority'] in [r_b['Priority'], r_s['Priority']]):
                    continue
                for _, r_r in by_last['Rotzenheimer'].iterrows():
                    titles_set = {r_b['Title'], r_s['Title'], r_d['Title'], r_r['Title']}
                    prods_set = {r_b['Product'], r_s['Product'], r_d['Product'], r_r['Product']}
                    prios_set = {r_b['Priority'], r_s['Priority'], r_d['Priority'], r_r['Priority']}
                    if not (len(titles_set) == len(prods_set) == len(prios_set) == 4):
                        continue

                    cand = pd.concat([r_b.to_frame().T, r_s.to_frame().T, r_d.to_frame().T, r_r.to_frame().T], ignore_index=True)

                    cond1 = (
                        ((cand['Priority'] == 1) & (cand['Title'].str[0] == cand['LastName'].str[0])).sum() == 1
                        and (((cand['Priority'] != 1) & (cand['Title'].str[0] == cand['LastName'].str[0])).sum() == 0)
                    )
                    if not cond1:
                        continue
                    ser = cand[cand['Title'] == 'Sergeant'].iloc[0]
                    if ser['Priority'] not in [1, 3] or ser['Product'] != 'Hibiscus Soap-on-a-Rope':
                        continue
                    rev = cand[cand['Title'] == 'Reverend'].iloc[0]
                    if rev['Product'] == 'Rose Bar' or rev['Priority'] == 2:
                        continue
                    p_rose = cand.loc[cand['Product'] == 'Rose Bar', 'Priority'].iloc[0]
                    p_lemon = cand.loc[cand['Product'] == 'Lemon Gel', 'Priority'].iloc[0]
                    if p_rose != p_lemon + 1:
                        continue
                    if (cand[(cand['LastName'] == 'Dimmadome') & (cand['Title'] == 'Doctor')].shape[0] > 0 or
                        cand[(cand['Title'] == 'Baroness') & (cand['Product'] == 'Hibiscus Soap-on-a-Rope')].shape[0] > 0):
                        continue

                    solutions.append(cand)
    
    if not solutions:
        raise RuntimeError('No solution found under constraints')

    final_df = solutions[0].sort_values('Priority').reset_index(drop=True)

    return {"output_01.csv": final_df}

if __name__ == "__main__":
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    cand_dir = task_dir / "cand"
    cand_dir.mkdir(exist_ok=True)

    solution_dfs = solve(inputs_dir)
    for filename, df in solution_dfs.items():
        df.to_csv(cand_dir / filename, index=False)