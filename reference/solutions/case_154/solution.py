import pandas as pd
from pathlib import Path

def solve(inputs_dir: Path) -> dict[str, pd.DataFrame]:
    grades_df = pd.read_csv(inputs_dir / "input_01.csv")
    students_df = pd.read_csv(inputs_dir / "input_02.csv")
    
    merged_df = grades_df.merge(
        students_df[['id', 'gender']], 
        left_on='Student ID', 
        right_on='id', 
        how='inner'
    )
    
    subject_cols = ['Maths', 'English', 'Spanish', 'Science', 'Art', 'History', 'Geography']
    
    id_vars = ['Student ID', 'gender']
    melted_df = pd.melt(
        merged_df[id_vars + subject_cols],
        id_vars=id_vars,
        value_vars=subject_cols,
        var_name='Subject',
        value_name='Score'
    )
    
    melted_df['Score'] = pd.to_numeric(melted_df['Score'], errors='coerce')
    
    avg_scores = melted_df.groupby('Student ID')['Score'].mean().reset_index()
    avg_scores.columns = ['Student ID', "Student's Avg Score"]
    avg_scores["Student's Avg Score"] = avg_scores["Student's Avg Score"].round(1)
    avg_scores["Student's Avg Score"] = avg_scores["Student's Avg Score"].apply(
        lambda v: "" if pd.isna(v) else (str(int(v)) if float(v).is_integer() else f"{v:.1f}")
    )
    
    melted_df['Passed'] = (melted_df['Score'] >= 75).astype(int)
    
    passed_counts = melted_df.groupby('Student ID')['Passed'].sum().reset_index()
    passed_counts.columns = ['Student ID', 'Passed Subjects']
    
    gender_df = melted_df[['Student ID', 'gender']].drop_duplicates()
    gender_df.columns = ['Student ID', 'Gender']
    
    result = avg_scores.merge(passed_counts, on='Student ID', how='inner')
    result = result.merge(gender_df, on='Student ID', how='inner')
    
    result = result[['Passed Subjects', "Student's Avg Score", 'Student ID', 'Gender']]
    
    result = result.sort_values('Student ID').reset_index(drop=True)
    
    return {
        "output_01.csv": result
    }

if __name__ == "__main__":
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    cand_dir = task_dir / "cand"
    cand_dir.mkdir(parents=True, exist_ok=True)
    
    outputs = solve(inputs_dir)
    for name, df in outputs.items():
        df.to_csv(cand_dir / name, index=False, encoding='utf-8')
