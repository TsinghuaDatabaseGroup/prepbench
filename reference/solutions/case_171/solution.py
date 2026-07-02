import pandas as pd
from pathlib import Path
import re

def solve(inputs_dir: Path) -> dict[str, pd.DataFrame]:
    registrations = pd.read_csv(inputs_dir / "input_01.csv")
    sessions_lookup = pd.read_csv(inputs_dir / "input_02.csv")
    online_attendees = pd.read_csv(inputs_dir / "input_03.csv")
    inperson_attendees = pd.read_csv(inputs_dir / "input_04.csv")
    
    def normalize_attendance_type(value):
        value_str = str(value).strip().lower()
        if 'online' in value_str or value_str == 'onlyne' or value_str == 'onlin':
            return 'Online'
        elif 'person' in value_str or 'persn' in value_str or 'persoon' in value_str or (value_str.startswith('im person')):
            return 'In Person'
        else:
            return value_str
    
    registrations['Online/In Person'] = registrations['Online/In Person'].apply(normalize_attendance_type)
    
    def extract_company(email):
        match = re.search(r'@([^.]+)', str(email))
        if match:
            return match.group(1)
        return ''
    
    registrations['Company'] = registrations['Email'].apply(extract_company)
    
    registrations['Sessions Registered'] = registrations.groupby(['First Name', 'Last Name', 'Email', 'Online/In Person'])['Session ID'].transform('count')
    
    registrations = registrations.merge(sessions_lookup, on='Session ID', how='left')
    
    inperson_reg = registrations[registrations['Online/In Person'] == 'In Person'].copy()
    
    inperson_merged = inperson_reg.merge(
        inperson_attendees,
        on=['Session', 'First Name', 'Last Name'],
        how='left',
        indicator=True
    )
    
    inperson_not_attended = inperson_merged[inperson_merged['_merge'] == 'left_only'].copy()
    inperson_not_attended = inperson_not_attended.drop(columns=['_merge'])
    
    online_reg = registrations[registrations['Online/In Person'] == 'Online'].copy()
    
    online_merged = online_reg.merge(
        online_attendees,
        on=['Session', 'Email'],
        how='left',
        indicator=True
    )
    
    online_not_attended = online_merged[online_merged['_merge'] == 'left_only'].copy()
    online_not_attended = online_not_attended.drop(columns=['_merge'])
    
    inperson_not_attended = inperson_not_attended.rename(columns={'Session': 'Session not attended'})
    online_not_attended = online_not_attended.rename(columns={'Session': 'Session not attended'})
    
    combined = pd.concat([inperson_not_attended, online_not_attended], ignore_index=True)
    
    combined['Sessions Not Attended'] = combined.groupby(['First Name', 'Last Name', 'Email', 'Online/In Person'])['Session not attended'].transform('count')
    
    combined['Not Attended %'] = (combined['Sessions Not Attended'] / combined['Sessions Registered'] * 100).round(2)
    
    output = combined[[
        'Company',
        'First Name',
        'Last Name',
        'Email',
        'Online/In Person',
        'Session not attended',
        'Not Attended %'
    ]].copy()
    
    output['Not Attended %'] = output['Not Attended %'].astype(float)
    
    return {
        'output_01.csv': output
    }

if __name__ == "__main__":
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    cand_dir = task_dir / "cand"
    cand_dir.mkdir(parents=True, exist_ok=True)
    
    outputs = solve(inputs_dir)
    for filename, df in outputs.items():
        df.to_csv(cand_dir / filename, index=False, encoding='utf-8')

