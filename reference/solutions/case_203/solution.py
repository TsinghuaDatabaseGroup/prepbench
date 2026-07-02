from __future__ import annotations

from pathlib import Path
import pandas as pd

def solve(inputs_dir: Path) -> dict[str, pd.DataFrame]:
    employees_df = pd.read_csv(inputs_dir / "input_01.csv")
    teams_df = pd.read_csv(inputs_dir / "input_02.csv")

    employees_df['hierarchy_level'] = employees_df['employee_id_hierarchy'].str.count(r'\|') - 1

    filtered_employees = employees_df[
        (employees_df['department'] != 'Executives') &
        (~employees_df['title'].str.contains('Administrator', na=False))
    ].copy()

    filtered_employees['level_rank'] = filtered_employees.groupby('department')['hierarchy_level'].rank(method='dense', ascending=True)
    sub_dept_heads = filtered_employees[filtered_employees['level_rank'] == 2].copy()

    sub_dept_heads['subdept_team_id'] = sub_dept_heads['dependent_team_ids'].str.split('|').str[1]
    dept_to_subdepts = sub_dept_heads.groupby('department')['subdept_team_id'].apply(list).to_dict()

    def find_employee_subdept(row):
        department = row['department']
        subdept_ids = dept_to_subdepts.get(department)

        if not subdept_ids:
            return None

        team_hierarchy = row['team_hierarchy'] if isinstance(row['team_hierarchy'], str) else ''
        dependent_teams = row['dependent_team_ids'] if isinstance(row['dependent_team_ids'], str) else ''

        for sub_id in subdept_ids:
            if sub_id and (sub_id in team_hierarchy or sub_id in dependent_teams):
                return sub_id
        return None

    employees_df['subdept_team_id'] = employees_df.apply(find_employee_subdept, axis=1)

    final_df = pd.merge(employees_df, teams_df, left_on='subdept_team_id', right_on='team_id', how='left')

    final_df = final_df.rename(columns={
        'team_id_x': 'team_id',
        'team_name_x': 'team_name',
        'team_name_y': 'subdept_name'
    })

    final_cols = [
        'position_id', 'employee_id', 'title', 'department', 'supervisor_id',
        'team_id', 'direct_reports', 'team_name', 'team_hierarchy',
        'employee_id_hierarchy', 'dependent_team_ids', 'hierarchy_level',
        'subdept_team_id', 'subdept_name'
    ]
    
    output_df = final_df[final_cols]

    return {"output_01.csv": output_df}


if __name__ == "__main__":
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    cand_dir = task_dir / "cand"
    cand_dir.mkdir(parents=True, exist_ok=True)

    outputs = solve(inputs_dir)
    for fname, df in outputs.items():
        out_path = cand_dir / fname
        df.to_csv(out_path, index=False, encoding="utf-8")
