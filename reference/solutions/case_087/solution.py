import pandas as pd
from pathlib import Path
from datetime import datetime, timedelta
import re


def solve(inputs_dir: Path) -> dict[str, pd.DataFrame]:
    apac_df = pd.read_csv(inputs_dir / "input_01.csv")
    emea_df = pd.read_csv(inputs_dir / "input_02.csv")
    am_df = pd.read_csv(inputs_dir / "input_03.csv")
    
    apac_df["Location"] = "APAC"
    emea_df["Location"] = "EMEA"
    am_df["Location"] = "AM"
    
    all_df = pd.concat([apac_df, emea_df, am_df], ignore_index=True)
    
    base_date = datetime(2020, 10, 7, 14, 0, 0)
    
    def parse_time(time_str):
        parts = time_str.split(":")
        hours = int(parts[0])
        minutes = int(parts[1])
        seconds = int(parts[2])
        return base_date + timedelta(hours=hours, minutes=minutes, seconds=seconds)
    
    all_df["Local DateTime"] = all_df["Time"].apply(parse_time)
    
    def to_gmt(row):
        if row["Location"] == "APAC":
            return row["Local DateTime"] - timedelta(hours=11)
        elif row["Location"] == "EMEA":
            return row["Local DateTime"] - timedelta(hours=1)
        else:
            return row["Local DateTime"] + timedelta(hours=5)
    
    all_df["Date (GMT)"] = all_df.apply(to_gmt, axis=1)
    
    all_df = all_df.sort_values(["Location", "Who", "Date (GMT)"])
    
    all_df["Is First Comment"] = (
        (all_df["Who"] != "Carl Allchin") & 
        (all_df.groupby(["Location", "Who"]).cumcount() == 0)
    )
    
    all_df["Is Carl First"] = (
        (all_df["Who"] == "Carl Allchin") &
        (all_df.groupby(["Location", "Who"]).cumcount() == 0)
    )
    
    def parse_location(comment, location):
        if pd.isna(comment):
            return None, None, None
        
        comment = str(comment).strip()
        
        first_time = bool(re.search(r'first\s+time', comment, re.IGNORECASE))
        
        comment_clean = re.sub(r'first\s+time[.,]?', '', comment, flags=re.IGNORECASE).strip()
        comment_clean = re.sub(r'\.$', '', comment_clean).strip()
        
        parts = [p.strip() for p in comment_clean.split(",")]
        
        if len(parts) >= 2:
            city = parts[0].strip()
            country_or_state = parts[1].strip()
            
            if location == "AM":
                us_states = {
                    "AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA",
                    "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD",
                    "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ",
                    "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC",
                    "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"
                }
                if country_or_state.upper() in us_states or len(country_or_state) == 2:
                    country = "United States"
                    state = country_or_state
                else:
                    country = country_or_state
                    state = None
            else:
                country = country_or_state
                state = None
            
            return city, country, first_time
        elif len(parts) == 1:
            return parts[0], None, first_time
        else:
            return None, None, first_time
    
    location_info = all_df[all_df["Is First Comment"]].apply(
        lambda row: parse_location(row["Comment"], row["Location"]), axis=1
    )
    
    location_df = pd.DataFrame(
        location_info.tolist(),
        columns=["City", "Country", "First Time"],
        index=all_df[all_df["Is First Comment"]].index
    )
    
    all_df = all_df.merge(
        location_df[["City", "Country", "First Time"]],
        left_index=True,
        right_index=True,
        how="left"
    )
    
    all_df["City"] = all_df.groupby(["Location", "Who"])["City"].ffill()
    all_df["Country"] = all_df.groupby(["Location", "Who"])["Country"].ffill()
    all_df["First Time Indicator"] = all_df.groupby(["Location", "Who"])["First Time"].ffill()
    
    def clean_country(country):
        if pd.isna(country):
            return None
        country_str = str(country).strip()
        return " ".join(country_str.split())
    
    all_df["Country"] = all_df["Country"].apply(clean_country)
    
    def clean_city(city):
        if pd.isna(city):
            return None
        city_str = str(city).strip()
        return " ".join(city_str.split())
    
    all_df["City"] = all_df["City"].apply(clean_city)
    
    def classify_comment(row):
        if row["Is First Comment"] or row["Is Carl First"]:
            return None
        if row["Who"] == "Carl Allchin":
            return "Answer"
        if "@" in str(row["Comment"]):
            return "Answer"
        if "?" in str(row["Comment"]):
            return "Question"
        return "Answer"
    
    all_df["Question or Answer"] = all_df.apply(classify_comment, axis=1)
    
    output_1 = all_df[all_df["Question or Answer"].notna()].groupby(
        ["Question or Answer", "Location"]
    ).size().reset_index(name="Instances")
    output_1 = output_1[["Instances", "Question or Answer", "Location"]]
    output_1 = output_1.sort_values(["Location", "Question or Answer"])
    
    output_2 = all_df[all_df["Is First Comment"]].copy()
    
    output_2["Who"] = output_2["Who"].str.strip()
    
    output_2 = output_2[
        output_2["City"].notna() & 
        output_2["Country"].notna()
    ].copy()
    
    exclude_names = {"Arsene Xie", "Leona Lai", "Jenny Martin", "Rosario Gauna"}
    output_2 = output_2[~output_2["Who"].isin(exclude_names)].copy()
    
    output_2 = output_2[[
        "Date (GMT)",
        "Location",
        "City",
        "First Time Indicator",
        "Country",
        "Who"
    ]].copy()
    
    output_2["Date (GMT)"] = output_2["Date (GMT)"].dt.strftime("%d/%m/%Y %H:%M:%S")
    
    output_2["First Time Indicator"] = output_2["First Time Indicator"].fillna(0).astype(int)
    
    output_2 = output_2.sort_values(["Location", "Date (GMT)", "Who"])
    
    return {
        "output_01.csv": output_1.reset_index(drop=True),
        "output_02.csv": output_2.reset_index(drop=True)
    }


if __name__ == "__main__":
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    cand_dir = task_dir / "cand"
    cand_dir.mkdir(parents=True, exist_ok=True)
    
    outputs = solve(inputs_dir)
    for filename, df in outputs.items():
        df.to_csv(cand_dir / filename, index=False, encoding="utf-8")
