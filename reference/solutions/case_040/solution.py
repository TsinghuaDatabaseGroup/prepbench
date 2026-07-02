import pandas as pd
from pathlib import Path


def solve(inputs_dir: Path) -> dict[str, pd.DataFrame]:
    
    df_input_01 = pd.read_csv(inputs_dir / "input_01.csv")
    df_input_02 = pd.read_csv(inputs_dir / "input_02.csv")
    
    three_words_col = "Which three words would you use describe to Sudzilla? (separate with a comma)"
    
    word_form_map = {
        'alarm': 'alarm', 'bad': 'bad', 'beardy': 'beardy', 'beef jerky': 'beef jerky',
        'boring': 'boring', 'bubbly': 'bubbly', 'cerulean': 'Cerulean', 'challenging': 'challenging',
        'clean': 'Clean', 'cleaning': 'cleaning', 'cleansing': 'Cleansing', 'creativity': 'creativity',
        'cretaceous': 'Cretaceous', 'crowded': 'crowded', 'damp': 'damp', 'dangerous': 'Dangerous',
        'deflating': 'deflating', 'dirty': 'dirty', 'eastenders': 'Eastenders', 'ecclesiastical': 'Ecclesiastical',
        'effulgent': 'Effulgent', 'english': 'English', 'fast moving': 'fast moving', 'feckless': 'Feckless',
        'felt': 'felt', 'feminine': 'Feminine', 'fizz-less': 'fizz-less', 'flat': 'Flat',
        'flirty': 'flirty', 'foamy': 'Foamy', 'food': 'food', 'foodies': 'Foodies',
        'fragrant': 'fragrant', 'fresh': 'fresh', 'frothy': 'frothy', 'fun': 'Fun',
        'fuzzy': 'Fuzzy', 'gamechanger': 'Gamechanger', 'go somewhere else': 'Go somewhere else', 'hollyoaks': 'Hollyoaks',
        'i': 'I', 'in': 'in', 'innovative': 'Innovative', 'inspirational': 'Inspirational',
        'inspiring': 'Inspiring', 'intense': 'Intense', 'interactive': 'interactive', 'invigorating': 'Invigorating',
        'joyous': 'Joyous', 'jurassic': 'Jurassic', 'lachrymose': 'Lachrymose', 'loud': 'Loud',
        'marketing': 'marketing', 'messy': 'messy', 'minty.': 'Minty.', 'monsterous': 'Monsterous',
        'murky': 'Murky', 'neighbours': 'Neighbours', 'nonsense': 'nonsense', 'not': 'Not',
        'outrageous': 'Outrageous', 'overpowering': 'overpowering', 'overrated': 'overrated', 'party': 'party',
        'provence': 'Provence', 'really': 'really', 'salubrious': 'Salubrious', 'scintillating': 'Scintillating',
        'seismic': 'Seismic', 'service': 'service', 'slippery': 'slippery', 'smooth': 'smooth',
        'soap': 'soap', 'soapy': 'Soapy', 'squeaky': 'Squeaky', 'sterile': 'Sterile',
        'sudcellent': 'Sudcellent', 'suddy': 'suddy', 'sudriffic': 'Sudriffic', 'sudtastic': 'Sudtastic',
        'sudzarific': 'Sudzarific', 'superb': 'Superb', 'synergy': 'Synergy', 'terrifying': 'Terrifying',
        'theatrical': 'Theatrical', 'triassic': 'Triassic', 'vibrant': 'vibrant', 'waste': 'waste',
        'well-paced': 'Well-paced', 'wet': 'Wet', 'wild': 'wild'
    }
    
    df = df_input_02.copy()
    
    rating_col = "On a scale of 0-10, how would you rate Sudzilla?"
    
    promoters = (df[rating_col] >= 9).sum()
    detractors = (df[rating_col] <= 6).sum()
    total_respondents = len(df)
    
    nps_score = ((promoters - detractors) / total_respondents) * 100
    
    nps_df = pd.DataFrame({
        "NPS Score": [round(nps_score, 1)],
        "Total Respondents": [total_respondents],
        "Promoter": [promoters],
        "Detractor": [detractors]
    })
    
    
    df["Timestamp"] = pd.to_datetime(df["Timestamp"])
    
    
    food_rating_map = {
        "Horrendous": 1,
        "Just about edible but I was hungry": 2,
        "Some good, some not so good": 3,
        "Yum!": 4,
        "Give the team a Michelin star!!": 5
    }
    
    def map_food_rating(val):
        if pd.isna(val) or val == "":
            return None
        return food_rating_map.get(val, None)
    
    breakfast_col = "How would you rate the food at Sudzilla (breakfast)?"
    lunch_col = "How would you rate the food at Sudzilla (lunch)?"
    dinner_col = "How would you rate the food at Sudzilla (dinner)?"
    
    df["breakfast_rating"] = df[breakfast_col].apply(map_food_rating)
    df["lunch_rating"] = df[lunch_col].apply(map_food_rating)
    df["dinner_rating"] = df[dinner_col].apply(map_food_rating)
    
    df["Food Rating Score"] = df[["breakfast_rating", "lunch_rating", "dinner_rating"]].mean(axis=1)
    
    opening_keynote_col = "On a scale of 0-10, how would you rate the opening keynote?"
    closing_keynote_col = "On a scale of 0-10, how would you rate the closing keynote?"
    
    df["Keynote Rating Score"] = df[[opening_keynote_col, closing_keynote_col]].mean(axis=1)
    
    expanded_rows = []
    
    for idx, row in df.iterrows():
        words_str = row[three_words_col]
        
        if pd.isna(words_str) or words_str == "":
            words_list = [""]
        else:
            words_list = [w.strip() for w in str(words_str).split(",")]
        
        seen_words = set()
        for word in words_list:
            word_clean = word
            if word and word[-1] in '.,!?;:' and word.lower() != 'minty.':
                word_clean = word.rstrip('.,!?;:')
            
            word_normalized = word_form_map.get(word_clean.lower(), word_clean)
            
            word_lower = word_normalized.lower()
            if word_lower in seen_words:
                continue
            seen_words.add(word_lower)
            
            new_row = row.copy()
            new_row["Which three words would you use describe to Sudzilla? (separate with a comma) Split"] = word_normalized
            expanded_rows.append(new_row)
    
    df_expanded = pd.DataFrame(expanded_rows)
    
    
    output_02_cols = [
        "Which three words would you use describe to Sudzilla? (separate with a comma) Split",
        "Keynote Rating Score",
        "Food Rating Score",
        "Timestamp",
        rating_col,
        "...why?",
        "What was your favourite giveaway at Sudzilla?",
        "What was your favourite 'Soap Box' (breakout / customer speaker) session?"
    ]
    
    rename_map = {
        "...why?": "___why?",
        rating_col: "On a scale of 0-10, how would you rate Sudzilla?"
    }
    
    df_output_02 = df_expanded[output_02_cols].copy()
    df_output_02 = df_output_02.rename(columns=rename_map)

    def format_timestamp(ts):
        return ts.strftime("%-m/%-d/%Y %-I:%M:%S %p")
    
    df_output_02["Timestamp"] = df_output_02["Timestamp"].apply(format_timestamp)
    
    if "What was your favourite giveaway at Sudzilla?" in df_output_02.columns:
        df_output_02["What was your favourite giveaway at Sudzilla?"] = df_output_02["What was your favourite giveaway at Sudzilla?"].apply(lambda x: x.strip() if isinstance(x, str) else x)
    soapbox_col = "What was your favourite 'Soap Box' (breakout / customer speaker) session?"
    if soapbox_col in df_output_02.columns:
        df_output_02[soapbox_col] = df_output_02[soapbox_col].apply(lambda x: x.strip() if isinstance(x, str) else x)

    df_output_02["Keynote Rating Score"] = df_output_02["Keynote Rating Score"].round(1)
    df_output_02["Food Rating Score"] = df_output_02["Food Rating Score"].round(9)

    df_output_02 = df_output_02.drop_duplicates(keep='first')
    
    return {
        "output_01.csv": nps_df,
        "output_02.csv": df_output_02
    }


if __name__ == "__main__":
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    cand_dir = task_dir / "cand"
    
    cand_dir.mkdir(exist_ok=True)
    
    results = solve(inputs_dir)
    
    for filename, df in results.items():
        output_path = cand_dir / filename
        df.to_csv(output_path, index=False, encoding='utf-8')
        print(f"Saved {filename}")
