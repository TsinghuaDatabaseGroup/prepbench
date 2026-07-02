import pandas as pd
from pathlib import Path

def solve(inputs_dir: Path) -> dict[str, pd.DataFrame]:
    teachers_df = pd.read_csv(inputs_dir / "input_01.csv")
    students_df = pd.read_csv(inputs_dir / "input_02.csv")
    rooms_df = pd.read_csv(inputs_dir / "input_03.csv")
    hours_df = pd.read_csv(inputs_dir / "input_04.csv")
    
    students_expanded = []
    for _, row in students_df.iterrows():
        subjects = str(row['Subject']).split('/')
        for subject in subjects:
            students_expanded.append({
                'Name': row['Name'],
                'Age': row['Age'],
                'Subject': subject.strip()
            })
    students_expanded_df = pd.DataFrame(students_expanded)
    
    def get_age_group(age):
        if 13 <= age <= 14:
            return '13-14'
        elif 15 <= age <= 16:
            return '15-16'
        elif 17 <= age <= 18:
            return '17-18'
        else:
            return None
    
    students_expanded_df['Age Group'] = students_expanded_df['Age'].apply(get_age_group)
    students_expanded_df = students_expanded_df.dropna(subset=['Age Group'])
    
    students_by_subject_age = students_expanded_df.groupby(['Subject', 'Age Group']).size().reset_index(name='Student Count')
    
    room_capacity = rooms_df.groupby('Subjects')['Capacity'].sum().reset_index()
    room_capacity.columns = ['Subject', 'Total Capacity']
    
    students_by_subject_age = students_by_subject_age.merge(
        hours_df, on='Age Group', how='left'
    )
    students_by_subject_age = students_by_subject_age.merge(
        room_capacity, on='Subject', how='left'
    )
    
    import math
    students_by_subject_age['Classes Needed'] = (
        students_by_subject_age['Student Count'] / 
        students_by_subject_age['Total Capacity']
    ).apply(lambda x: math.ceil(x))
    
    students_by_subject_age['Teaching Hours'] = (
        students_by_subject_age['Classes Needed'] * 
        students_by_subject_age['Hours teaching per week']
    )
    
    classes_required = students_by_subject_age.groupby('Subject')['Classes Needed'].sum().reset_index()
    classes_required['Classes required'] = classes_required.apply(
        lambda row: row['Classes Needed'] + (2 if row['Subject'] == 'Physics' else 1),
        axis=1
    )
    classes_required = classes_required[['Subject', 'Classes required']]
    
    total_hours_needed = students_by_subject_age.groupby('Subject')['Teaching Hours'].sum().reset_index()
    total_hours_needed['Total Teaching Hours needed'] = total_hours_needed.apply(
        lambda row: row['Teaching Hours'] + (6 if row['Subject'] == 'Physics' else 1),
        axis=1
    )
    total_hours_needed = total_hours_needed[['Subject', 'Total Teaching Hours needed']]
    
    
    def count_working_days(days_str):
        if pd.isna(days_str):
            return 0
        days = str(days_str).split(',')
        return len([d for d in days if d.strip()])
    
    teachers_df['Working Days Count'] = teachers_df['Working Days'].apply(count_working_days)
    teachers_df['Weekly Hours'] = teachers_df['Working Days Count'] * 6
    
    def parse_age_range(age_str):
        if pd.isna(age_str):
            return []
        parts = str(age_str).split('-')
        if len(parts) == 2:
            start = int(parts[0])
            end = int(parts[1])
            return list(range(start, end + 1))
        return []
    
    teachers_df['Ages List'] = teachers_df['Ages Taught'].apply(parse_age_range)
    
    teacher_subject_hours = []
    
    for _, teacher_row in teachers_df.iterrows():
        teacher_name = teacher_row['Name']
        subject = teacher_row['Subject']
        weekly_hours = teacher_row['Weekly Hours']
        
        teacher_subjects = teachers_df[teachers_df['Name'] == teacher_name]['Subject'].unique()
        num_subjects = len(teacher_subjects)
        
        hours_per_subject = weekly_hours / num_subjects if num_subjects > 0 else 0
        
        teacher_subject_hours.append({
            'Subject': subject,
            'Teacher Hours': hours_per_subject
        })
    
    if teacher_subject_hours:
        teacher_hours_df = pd.DataFrame(teacher_subject_hours)
        potential_teachers_hours = teacher_hours_df.groupby('Subject')['Teacher Hours'].sum().reset_index()
        potential_teachers_hours.columns = ['Subject', 'Potential Teachers Hours']
    else:
        potential_teachers_hours = pd.DataFrame(columns=['Subject', 'Potential Teachers Hours'])
    
    result = total_hours_needed.merge(
        potential_teachers_hours, on='Subject', how='outer'
    ).merge(
        classes_required, on='Subject', how='outer'
    )
    
    result['Potential Teachers Hours'] = result['Potential Teachers Hours'].fillna(0)
    result['Total Teaching Hours needed'] = result['Total Teaching Hours needed'].fillna(0)
    result['Classes required'] = result['Classes required'].fillna(0)
    
    result['% utilised'] = (
        result['Total Teaching Hours needed'] / 
        result['Potential Teachers Hours'] * 100
    ).round().astype(int)
    
    result.loc[result['Potential Teachers Hours'] == 0, '% utilised'] = 0
    
    output = result[[
        'Subject',
        'Potential Teachers Hours',
        'Total Teaching Hours needed',
        'Classes required',
        '% utilised'
    ]].copy()
    
    output = output.sort_values('Subject').reset_index(drop=True)
    
    output['Potential Teachers Hours'] = output['Potential Teachers Hours'].astype(int)
    output['Total Teaching Hours needed'] = output['Total Teaching Hours needed'].astype(int)
    output['Classes required'] = output['Classes required'].astype(int)
    output['% utilised'] = output['% utilised'].astype(int)
    
    return {'output_01.csv': output}

if __name__ == "__main__":
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    cand_dir = task_dir / "cand"
    cand_dir.mkdir(parents=True, exist_ok=True)
    
    outputs = solve(inputs_dir)
    for filename, df in outputs.items():
        df.to_csv(cand_dir / filename, index=False, encoding='utf-8')

