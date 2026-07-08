import pandas as pd
from pathlib import Path
import re
from datetime import datetime

def solve(inputs_dir: Path) -> dict[str, pd.DataFrame]:
    df_flights = pd.read_csv(inputs_dir / "input_01.csv")
    df_cities = pd.read_csv(inputs_dir / "input_02.csv")
    
    def clean_city_name(city):
        city = re.sub(r'[–-][A-Z][A-Za-z\']*$', '', city)
        city = re.sub(r'/.*$', '', city)
        return city.strip()
    
    df_flights['From'] = df_flights['From'].apply(clean_city_name)
    df_flights['To'] = df_flights['To'].apply(clean_city_name)
    
    df_flights['Route'] = df_flights['From'] + ' - ' + df_flights['To']
    
    def extract_distance_km(dist_str):
        match = re.search(r'([\d,]+)\s*km', dist_str)
        if match:
            return int(match.group(1).replace(',', ''))
        return None
    
    def extract_distance_mi(dist_str):
        match = re.search(r'\(([\d,]+)\s*mi', dist_str)
        if match:
            return int(match.group(1).replace(',', ''))
        return None
    
    df_flights['Distance - km'] = df_flights['Distance'].apply(extract_distance_km)
    df_flights['Distance - mi'] = df_flights['Distance'].apply(extract_distance_mi)
    
    df_flights['Rank'] = df_flights['Distance - km'].rank(method='dense', ascending=False).astype(int)
    
    if pd.api.types.is_datetime64_any_dtype(df_flights['Scheduled duration']):
        df_flights['Scheduled duration'] = df_flights['Scheduled duration'].dt.strftime('%H:%M:%S')
    else:
        df_flights['Scheduled duration'] = df_flights['Scheduled duration'].astype(str)
    
    def parse_date(date_str):
        try:
            for fmt in ['%b %d, %Y', '%B %d, %Y']:
                try:
                    dt = datetime.strptime(date_str, fmt)
                    return dt.strftime('%d/%m/%Y')
                except:
                    continue
            dt = datetime.strptime(date_str, '%d/%m/%Y')
            return dt.strftime('%d/%m/%Y')
        except:
            return date_str
    
    df_flights['First flight'] = df_flights['First flight'].astype(str).apply(parse_date)
    
    df_from = df_cities[['City', 'Lat', 'Lng']].copy()
    df_from.columns = ['From', 'From Lat', 'From Lng']
    df_flights = df_flights.merge(df_from, on='From', how='left')
    
    df_to = df_cities[['City', 'Lat', 'Lng']].copy()
    df_to.columns = ['To', 'To Lat', 'To Lng']
    df_flights = df_flights.merge(df_to, on='To', how='left')
    
    output_columns = [
        'Rank', 'From', 'To', 'Route', 'Airline', 'Flight number',
        'Distance - mi', 'Distance - km', 'Scheduled duration', 'Aircraft',
        'First flight', 'From Lat', 'From Lng', 'To Lat', 'To Lng'
    ]
    
    df_output = df_flights[output_columns].copy()
    
    df_output['First flight'] = df_output['First flight'].astype(str)
    
    df_output = df_output.sort_values('Rank').reset_index(drop=True)
    
    return {
        'output_01.csv': df_output
    }

if __name__ == "__main__":
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    cand_dir = task_dir / "cand"
    cand_dir.mkdir(parents=True, exist_ok=True)
    
    outputs = solve(inputs_dir)
    for filename, df in outputs.items():
        df.to_csv(cand_dir / filename, index=False, encoding='utf-8')

