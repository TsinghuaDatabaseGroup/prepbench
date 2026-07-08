import pandas as pd
from pathlib import Path

def solve(inputs_dir: Path) -> dict[str, pd.DataFrame]:
    travel_df = pd.read_csv(inputs_dir / "input_01.csv")
    
    weekday_cols = ['M', 'Tu', 'W', 'Th', 'F']
    id_vars = ['Student ID']
    
    long_df = travel_df.melt(
        id_vars=id_vars,
        value_vars=weekday_cols,
        var_name='Weekday',
        value_name='Method of Travel'
    )
    
    weekday_map = {
        'M': 'M',
        'Tu': 'Tu',
        'W': 'W',
        'Th': 'Th',
        'F': 'F'
    }
    long_df['Weekday'] = long_df['Weekday'].map(weekday_map)
    
    spelling_map = {
        'Bycycle': 'Bicycle',
        'Bicycle': 'Bicycle',
        'Carr': 'Car',
        'Car': 'Car',
        'Scootr': 'Scooter',
        'Scoter': 'Scooter',
        'Scooter': 'Scooter',
        'Walkk': 'Walk',
        'Wallk': 'Walk',
        'Waalk': 'Walk',
        'WAlk': 'Walk',
        'Walk': 'Walk',
        'Van': 'Van',
        'Aeroplane': 'Aeroplane',
        'Helicopeter': 'Helicopter',
        'Helicopter': 'Helicopter',
        "Mum's Shoulders": "Mum's Shoulders",
        "Dad's Shoulders": "Dad's Shoulders",
        'Hopped': 'Hopped',
        'Skipped': 'Skipped',
        'Jumped': 'Jumped'
    }
    
    def normalize_travel_method(method):
        method = str(method).strip()
        if method in spelling_map:
            return spelling_map[method]
        method_lower = method.lower()
        for key, value in spelling_map.items():
            if key.lower() == method_lower:
                return value
        return method
    
    long_df['Method of Travel'] = long_df['Method of Travel'].apply(normalize_travel_method)
    
    sustainable_methods = {
        'Walk', 'Bicycle', 'Scooter', "Mum's Shoulders", "Dad's Shoulders",
        'Hopped', 'Skipped', 'Jumped'
    }
    
    def classify_sustainability(method):
        return 'Sustainable' if method in sustainable_methods else 'Non-Sustainable'
    
    long_df['Sustainable?'] = long_df['Method of Travel'].apply(classify_sustainability)
    
    grouped = long_df.groupby(['Sustainable?', 'Method of Travel', 'Weekday']).size().reset_index(name='Number of Trips')
    
    trips_per_day = len(travel_df)
    
    grouped['Trips per day'] = trips_per_day
    
    grouped['% of trips per day'] = (grouped['Number of Trips'] / trips_per_day).round(2)
    
    result = grouped[[
        'Sustainable?',
        '% of trips per day',
        'Trips per day',
        'Number of Trips',
        'Weekday',
        'Method of Travel'
    ]]
    
    result = result.sort_values([
        '% of trips per day',
        'Sustainable?',
        'Weekday',
        'Method of Travel'
    ], ascending=[False, True, True, True]).reset_index(drop=True)
    
    return {
        'output_01.csv': result
    }

if __name__ == "__main__":
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    cand_dir = task_dir / "cand"
    cand_dir.mkdir(parents=True, exist_ok=True)
    
    outputs = solve(inputs_dir)
    for filename, df in outputs.items():
        df.to_csv(cand_dir / filename, index=False, encoding='utf-8')

