import pandas as pd
from pathlib import Path
import re

def solve(inputs_dir: Path) -> dict[str, pd.DataFrame]:
    
    results = []
    
    df2 = pd.read_csv(inputs_dir / "input_02.csv")
    for idx, row in df2.iterrows():
        data_str = str(row['Data'])
        if pd.isna(data_str) or data_str == 'nan' or not data_str.strip():
            continue
        
        lines = data_str.strip().split('\n')
        if len(lines) >= 2:
            time_str = lines[0].strip()
            temp_str = lines[1].strip()
            
            temp_match = re.search(r'(-?\d+)', temp_str)
            temperature = int(temp_match.group(1)) if temp_match else None
            
            precip = None
            if len(lines) >= 3:
                precip_match = re.search(r'Chance of Rain(\d+)%', lines[2])
                if precip_match:
                    precip = int(precip_match.group(1))
            else:
                precip_match = re.search(r'Chance of Rain(\d+)%', temp_str)
                if precip_match:
                    precip = int(precip_match.group(1))
            
            results.append({
                'Forecast Type': 'Next 5 Hours',
                'Date or Time': time_str,
                'Temperature': temperature,
                'Max Temp': None,
                'Min Temp': None,
                'Precipitation Chance': precip
            })
    
    df3 = pd.read_csv(inputs_dir / "input_03.csv")
    for idx, row in df3.iterrows():
        data_str = str(row['Data'])
        if pd.isna(data_str) or data_str == 'nan' or not data_str.strip():
            continue
        
        lines = [l.strip() for l in data_str.strip().split('\n') if l.strip()]
        if len(lines) >= 1:
            date_str = lines[0].strip()
            
            temperature = None
            max_temp = None
            min_temp = None
            precip = None
            
            temp_values = []
            for line in lines[1:]:
                precip_match = re.search(r'Chance of Rain(\d+)%', line)
                if precip_match:
                    precip = int(precip_match.group(1))
                else:
                    temp_matches = re.findall(r'(-?\d+)', line)
                    temp_values.extend([int(t) for t in temp_matches])
            
            if date_str == 'Today':
                if len(temp_values) >= 1:
                    min_temp = temp_values[0]
            else:
                if len(temp_values) >= 2:
                    max_temp = temp_values[0]
                    min_temp = temp_values[1]
                elif len(temp_values) == 1:
                    max_temp = temp_values[0]
            
            results.append({
                'Forecast Type': 'Next 5 Days',
                'Date or Time': date_str,
                'Temperature': temperature,
                'Max Temp': max_temp,
                'Min Temp': min_temp,
                'Precipitation Chance': precip
            })
    
    output_df = pd.DataFrame(results)
    
    output_df['Temperature'] = output_df['Temperature'].astype('Int64')
    output_df['Max Temp'] = output_df['Max Temp'].astype('Int64')
    output_df['Min Temp'] = output_df['Min Temp'].astype('Int64')
    output_df['Precipitation Chance'] = output_df['Precipitation Chance'].astype('Int64')
    
    output_df = output_df.reset_index(drop=True)
    
    return {
        'output_01.csv': output_df
    }

if __name__ == "__main__":
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    cand_dir = task_dir / "cand"
    cand_dir.mkdir(parents=True, exist_ok=True)
    
    outputs = solve(inputs_dir)
    for filename, df in outputs.items():
        df.to_csv(cand_dir / filename, index=False, encoding='utf-8')

