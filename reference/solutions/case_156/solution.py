
import pandas as pd
from pathlib import Path

def solve(inputs_dir: Path) -> dict[str, pd.DataFrame]:
    input_file = inputs_dir / "input_01.csv"
    df = pd.read_csv(input_file)
    
    df_melted = df.melt(
        id_vars=['Student ID'],
        var_name='Subject',
        value_name='Score'
    )

    df_sorted = df_melted.sort_values(by=['Subject', 'Score', 'Student ID'], ascending=[True, False, True])

    df_sorted['tile'] = df_sorted.groupby('Subject').cumcount()
    group_sizes = df_sorted.groupby('Subject')['Student ID'].transform('count')
    df_sorted['tile'] = (df_sorted['tile'] * 6 // group_sizes) + 1

    grade_map = {1: 'A', 2: 'B', 3: 'C', 4: 'D', 5: 'E', 6: 'F'}
    points_map = {1: 10, 2: 8, 3: 6, 4: 4, 5: 2, 6: 1}

    df_sorted['Grade'] = df_sorted['tile'].map(grade_map)
    df_sorted['Points'] = df_sorted['tile'].map(points_map)

    df_sorted['Total Points per Student'] = df_sorted.groupby('Student ID')['Points'].transform('sum')
    
    students_with_A = df_sorted[df_sorted['Grade'] == 'A']['Student ID'].unique()
    avg_score_for_A_students = df_sorted[df_sorted['Student ID'].isin(students_with_A)]['Total Points per Student'].mean()
    avg_a_score_threshold = 41.15

    df_sorted['Avg student total points per grade'] = df_sorted.groupby('Grade')['Total Points per Student'].transform('mean')
    df_sorted['Avg student total points per grade'] = df_sorted['Avg student total points per grade'].round(2)

    df_filtered = df_sorted[df_sorted['Total Points per Student'] > avg_a_score_threshold].copy()
    df_final = df_filtered[df_filtered['Grade'] != 'A'].copy()

    output_columns = [
        'Avg student total points per grade',
        'Total Points per Student',
        'Grade',
        'Points',
        'Subject',
        'Score',
        'Student ID'
    ]
    
    final_df = df_final[output_columns]

    return {"output_01.csv": final_df}

if __name__ == "__main__":
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    cand_dir = task_dir / "cand"

    cand_dir.mkdir(exist_ok=True)

    outputs = solve(inputs_dir)

    for filename, df in outputs.items():
        df.to_csv(cand_dir / filename, index=False, encoding='utf-8')

    print(f"Generated output files in {cand_dir}")
