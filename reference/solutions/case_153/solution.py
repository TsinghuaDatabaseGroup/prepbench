import pandas as pd
from pathlib import Path
from datetime import datetime


def solve(inputs_dir: Path) -> dict[str, pd.DataFrame]:
    input_file = inputs_dir / "input_01.csv"
    df = pd.read_csv(input_file)
    
    df["Pupil Name"] = df["pupil first name"] + " " + df["pupil last name"]
    
    df["Date of Birth"] = pd.to_datetime(df["Date of Birth"], format="%m/%d/%Y")
    
    df["This Year's Birthday"] = pd.to_datetime(df["Date of Birth"].apply(
        lambda x: datetime(2022, x.month, x.day)
    ))
    
    df["Weekday"] = df["This Year's Birthday"].dt.day_name()
    
    def get_cake_date(row):
        if row["Weekday"] in ["Saturday", "Sunday"]:
            weekday_num = row["This Year's Birthday"].weekday()
            if weekday_num == 5:
                days_back = 1
            else:
                days_back = 2
            return row["This Year's Birthday"] - pd.Timedelta(days=days_back)
        else:
            return row["This Year's Birthday"]
    
    df["Cake Date"] = df.apply(get_cake_date, axis=1)
    df["Cake Needed On"] = df["Cake Date"].dt.day_name()
    
    month_names = {
        1: "January", 2: "February", 3: "March", 4: "April",
        5: "May", 6: "June", 7: "July", 8: "August",
        9: "September", 10: "October", 11: "November", 12: "December"
    }
    df["Month"] = df["Cake Date"].dt.month.map(month_names)
    
    count_df = df.groupby(["Month", "Cake Needed On"]).size().reset_index(name="BDs per Weekday and Month")
    
    df = df.merge(count_df, on=["Month", "Cake Needed On"], how="left")
    
    df["Date of Birth"] = df["Date of Birth"].dt.strftime("%d/%m/%Y")
    df["This Year's Birthday"] = df["This Year's Birthday"].dt.strftime("%d/%m/%Y")
    
    output_df = df[[
        "Pupil Name",
        "Date of Birth",
        "This Year's Birthday",
        "Cake Needed On",
        "Month",
        "BDs per Weekday and Month"
    ]].copy()
    
    return {"output_01.csv": output_df.reset_index(drop=True)}


if __name__ == "__main__":
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    cand_dir = task_dir / "cand"
    cand_dir.mkdir(parents=True, exist_ok=True)
    
    outputs = solve(inputs_dir)
    for filename, df in outputs.items():
        df.to_csv(cand_dir / filename, index=False, encoding="utf-8")

