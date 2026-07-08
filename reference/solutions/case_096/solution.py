import pandas as pd
from pathlib import Path
import re


def clean_email(email: str) -> str:
    if pd.isna(email):
        return email
    
    email = str(email).strip()
    email = email.replace(',', '.')
    email = email.replace('!', '.')
    
    return email


def solve(inputs_dir: Path) -> dict[str, pd.DataFrame]:
    df = pd.read_csv(inputs_dir / "input_01.csv")
    
    df['Email'] = df['Email'].apply(clean_email)
    
    df_sorted = df.sort_values('Secret Santa').reset_index(drop=True)
    
    n = len(df_sorted)
    result_rows = []
    
    for i in range(n):
        santa_name = df_sorted.iloc[i]['Secret Santa']
        santa_email = df_sorted.iloc[i]['Email']
        
        santee_idx = (i + 1) % n
        santee_name = df_sorted.iloc[santee_idx]['Secret Santa']
        
        email_subject = "Secret Santa"
        email_body = f"{santa_name} the results are in your secret santee is: {santee_name}. Good luck finding a great gift!"
        
        result_rows.append({
            'Email': santa_email,
            'Email Subject': email_subject,
            'Email Body': email_body
        })
    
    result = pd.DataFrame(result_rows)
    
    result = result.iloc[::-1].reset_index(drop=True)
    
    return {
        "output_01.csv": result
    }


if __name__ == "__main__":
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    cand_dir = task_dir / "cand"
    cand_dir.mkdir(parents=True, exist_ok=True)
    
    outputs = solve(inputs_dir)
    for filename, df in outputs.items():
        df.to_csv(cand_dir / filename, index=False, encoding='utf-8')

