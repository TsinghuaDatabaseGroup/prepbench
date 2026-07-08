import pandas as pd
from pathlib import Path
from datetime import datetime


def solve(inputs_dir: Path) -> dict[str, pd.DataFrame]:
    input_file = inputs_dir / "input_01.csv"
    df = pd.read_csv(input_file)
    
    df["Pupil's Name"] = df["pupil last name"] + ", " + df["pupil first name"]
    
    df["Parent First Name"] = df.apply(
        lambda row: row["Parental Contact Name_1"] if row["Parental Contact"] == 1 
        else row["Parental Contact Name_2"], axis=1
    )
    
    df["Parental Contact Full Name"] = df["pupil last name"] + ", " + df["Parent First Name"]
    
    df["Parental Contact Email Address"] = (
        df["Parent First Name"] + "." + 
        df["pupil last name"] + "@" + 
        df["Preferred Contact Employer"] + ".com"
    )
    
    def calculate_academic_year(date_str):
        birth_date = datetime.strptime(date_str, "%m/%d/%Y")
        birth_year = birth_date.year
        birth_month = birth_date.month
        birth_day = birth_date.day
        
        if birth_month > 9 or (birth_month == 9 and birth_day >= 1):
            academic_start_year = birth_year
        else:
            academic_start_year = birth_year - 1
        
        
        if academic_start_year >= 2014:
            return 1
        elif academic_start_year == 2013:
            return 2
        elif academic_start_year == 2012:
            return 3
        elif academic_start_year == 2011:
            return 4
        else:
            return 2014 - academic_start_year + 1
    
    df["Academic Year"] = df["Date of Birth"].apply(calculate_academic_year)
    
    output_df = df[[
        "Academic Year",
        "Pupil's Name",
        "Parental Contact Full Name",
        "Parental Contact Email Address"
    ]].copy()
    
    output_df["Academic Year"] = output_df["Academic Year"].astype(int)
    
    return {
        "output_01.csv": output_df
    }


if __name__ == "__main__":
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    cand_dir = task_dir / "cand"
    
    cand_dir.mkdir(parents=True, exist_ok=True)
    
    outputs = solve(inputs_dir)
    
    for filename, df in outputs.items():
        output_path = cand_dir / filename
        df.to_csv(output_path, index=False, encoding="utf-8")

