import pandas as pd
from pathlib import Path

def solve(inputs_dir: Path) -> dict[str, pd.DataFrame]:
    input_file = inputs_dir / "input_01.csv"
    df = pd.read_csv(input_file)
    
    def normalize_date(date_str):
        if pd.isna(date_str) or date_str == '':
            return date_str
        try:
            dt = pd.to_datetime(date_str, dayfirst=True, errors='coerce')
            if pd.isna(dt):
                parts = str(date_str).split('/')
                if len(parts) == 3:
                    d, m, y = parts
                    if len(y) == 2:
                        y = '20' + y if int(y) < 50 else '19' + y
                    d = d.zfill(2)
                    m = m.zfill(2)
                    return f"{d}/{m}/{y}"
            return dt.strftime('%d/%m/%Y')
        except:
            return date_str
    
    df["Date"] = df["Date"].apply(normalize_date)
    
    unnamed_col = df.columns[-1]
    
    split_parts = df[unnamed_col].str.split(" - ", n=2, expand=True)
    df["Coach"] = split_parts[0].str.strip()
    df["Calories"] = split_parts[1].str.strip().astype(int)
    df["Music Type"] = split_parts[2].str.strip()
    
    df["Music Type"] = df["Music Type"].str.title()
    
    df["Mins"] = df["Value"]
    
    param_music_type = "Everything Rock"
    param_coach = "Kym"
    param_top_n = 5
    
    filtered = df[
        (df["Music Type"] == param_music_type) & 
        (df["Coach"] == param_coach)
    ].copy()
    
    filtered = filtered.sort_values("Calories", ascending=False)
    
    filtered = filtered.head(param_top_n)
    
    filtered["Rank"] = range(1, len(filtered) + 1)
    
    output = filtered[[
        "Rank",
        "Coach",
        "Calories",
        "Music Type",
        "Date",
        "Mins"
    ]].copy()
    
    output = output.reset_index(drop=True)
    
    return {
        "output_01.csv": output
    }

if __name__ == "__main__":
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    cand_dir = task_dir / "cand"
    cand_dir.mkdir(parents=True, exist_ok=True)
    
    outputs = solve(inputs_dir)
    for filename, df in outputs.items():
        df.to_csv(cand_dir / filename, index=False, encoding="utf-8")

