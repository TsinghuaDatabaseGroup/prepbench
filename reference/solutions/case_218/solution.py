import pandas as pd
from pathlib import Path
from datetime import datetime

def solve(inputs_dir: Path) -> dict[str, pd.DataFrame]:
    easter_file = inputs_dir / "input_01.csv"
    df_easter = pd.read_csv(easter_file)
    
    full_moon_file = inputs_dir / "input_02.csv"
    df_moon = pd.read_csv(full_moon_file, skipinitialspace=True)
    df_moon.columns = [c.strip() for c in df_moon.columns]
    for col in df_moon.columns:
        if df_moon[col].dtype == object:
            df_moon[col] = df_moon[col].astype(str).str.strip()
    
    df_easter["Easter Sunday"] = pd.to_datetime(df_easter["Easter Sunday"], format="%d/%m/%Y")
    df_easter["Year"] = df_easter["Easter Sunday"].dt.year
    df_easter = df_easter[(df_easter["Year"] >= 1900) & (df_easter["Year"] <= 2023)].copy()
    
    df_moon["Full Moon Date"] = pd.to_datetime(df_moon["Date"], format="%d %B %Y", errors="coerce")
    df_moon["Year"] = df_moon["Full Moon Date"].dt.year
    df_moon = df_moon[(df_moon["Year"] >= 1900) & (df_moon["Year"] <= 2023)].copy()
    
    def parse_interesting_event(time_str):
        if pd.isna(time_str):
            return None
        time_str = str(time_str)
        if "[+]" in time_str:
            return "Blue moon"
        elif "[*]" in time_str and "[**]" not in time_str:
            return "Partial Lunar Eclipse"
        elif "[**]" in time_str:
            return "Total Lunar Eclipse"
        else:
            return None
    
    df_moon["Interesting Event"] = df_moon["Time"].apply(parse_interesting_event)
    
    results = []
    for _, easter_row in df_easter.iterrows():
        easter_date = easter_row["Easter Sunday"]
        easter_year = easter_row["Year"]
        
        moon_candidates = df_moon[
            (df_moon["Full Moon Date"] <= easter_date) &
            (df_moon["Full Moon Date"] >= pd.Timestamp(easter_year - 1, 1, 1))
        ].copy()
        
        if len(moon_candidates) == 0:
            continue
        
        moon_candidates["Days Before"] = (easter_date - moon_candidates["Full Moon Date"]).dt.days
        moon_candidates = moon_candidates[moon_candidates["Days Before"] >= 0]
        if len(moon_candidates) == 0:
            continue
        
        closest_moon = moon_candidates.loc[moon_candidates["Days Before"].idxmin()]
        days_between = closest_moon["Days Before"]
        interesting_event = closest_moon["Interesting Event"]
        
        results.append({
            "Year": easter_year,
            "Days Between": days_between,
            "Interesting Event": interesting_event
        })
    
    df_results = pd.DataFrame(results)
    
    def get_most_interesting_event(events):
        events = events.dropna().unique()
        if len(events) == 0:
            return None
        priority = {
            "Total Lunar Eclipse": 1,
            "Partial Lunar Eclipse": 2,
            "Blue moon": 3,
        }
        sorted_events = sorted(events, key=lambda x: priority.get(x, 999))
        return sorted_events[0]
    
    df_agg = df_results.groupby("Days Between").agg({
        "Year": ["count", "min", "max"],
        "Interesting Event": get_most_interesting_event
    }).reset_index()
    
    df_agg.columns = ["Days Between Full Moon & Easter Sunday", "Number of Occurrences", "Min Year", "Max Year", "Most Interesting event"]
    
    df_agg = df_agg[[
        "Days Between Full Moon & Easter Sunday",
        "Number of Occurrences",
        "Most Interesting event",
        "Min Year",
        "Max Year"
    ]]
    
    df_agg["Days Between Full Moon & Easter Sunday"] = df_agg["Days Between Full Moon & Easter Sunday"].astype(int)
    df_agg["Number of Occurrences"] = df_agg["Number of Occurrences"].astype(int)
    df_agg["Min Year"] = df_agg["Min Year"].astype(int)
    df_agg["Max Year"] = df_agg["Max Year"].astype(int)
    df_agg["Most Interesting event"] = df_agg["Most Interesting event"].replace({None: ""})
    
    df_agg = df_agg.sort_values("Days Between Full Moon & Easter Sunday").reset_index(drop=True)
    
    return {
        "output_01.csv": df_agg
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

