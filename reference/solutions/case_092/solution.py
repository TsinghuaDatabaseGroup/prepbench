import pandas as pd
from pathlib import Path
import re
from datetime import datetime


def solve(inputs_dir: Path) -> dict[str, pd.DataFrame]:
    
    incidents_df = pd.read_csv(inputs_dir / "input_01.csv")
    categories_df = pd.read_csv(inputs_dir / "input_02.csv")
    
    month_map = {
        'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6,
        'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12
    }
    
    def parse_incident(incident_str):
        pattern = r'^(.+?)\s+(?:at|near)\s+(.+?)\s+on\s+(.+?),\s+(.+)$'
        match = re.match(pattern, incident_str)
        
        if match:
            aircraft = match.group(1).strip()
            location = match.group(2).strip()
            date_str = match.group(3).strip()
            description = match.group(4).strip()
            
            date_pattern = r'(\w+)\s+(\d+)(?:st|nd|rd|th)?\s+(\d{4})'
            date_match = re.match(date_pattern, date_str)
            
            if date_match:
                month_str = date_match.group(1)
                day = int(date_match.group(2))
                year = int(date_match.group(3))
                
                month = month_map.get(month_str, 1)
                formatted_date = f"{day:02d}/{month:02d}/{year}"
            else:
                formatted_date = date_str
            
            return {
                'Aircraft': aircraft,
                'Location': location,
                'Date': formatted_date,
                'Incident Description': description
            }
        else:
            return {
                'Aircraft': '',
                'Location': '',
                'Date': '',
                'Incident Description': incident_str
            }
    
    parsed_data = []
    for _, row in incidents_df.iterrows():
        parsed = parse_incident(row['Incident'])
        parsed_data.append(parsed)
    
    output_02_df = pd.DataFrame(parsed_data)
    output_02_df = output_02_df[['Date', 'Location', 'Aircraft', 'Incident Description']]
    
    category_mapping = {
        'Attendants': 'Attendant',
        'Pressurize': 'Pressure',
        'Pressurization': 'Pressure',
        'Pressurized': 'Pressure',
    }
    
    categories_list = categories_df['Category'].tolist()
    normalized_categories = {}
    for cat in categories_list:
        normalized_categories[cat.lower()] = cat
    
    incident_categories = []
    for desc in output_02_df['Incident Description']:
        desc_lower = desc.lower()
        matched_categories = []
        
        for cat_key, cat_name in normalized_categories.items():
            if cat_key in desc_lower:
                matched_categories.append(cat_name)
        
        if 'attendant' in desc_lower or 'attendants' in desc_lower:
            if 'Attendant' not in matched_categories:
                matched_categories.append('Attendant')
        if 'pressure' in desc_lower or 'pressurize' in desc_lower or 'pressurization' in desc_lower:
            if 'Pressure' not in matched_categories:
                matched_categories.append('Pressure')
        
        if 'takeoff' in desc_lower or 'take off' in desc_lower:
            if 'Takeoff' not in matched_categories:
                matched_categories.append('Takeoff')
        if 'landing' in desc_lower:
            if 'Landing' not in matched_categories:
                matched_categories.append('Landing')
        if 'runway' in desc_lower:
            if 'Runway' not in matched_categories:
                matched_categories.append('Runway')
        if 'engine' in desc_lower or 'engines' in desc_lower:
            if 'Engine' not in matched_categories:
                matched_categories.append('Engine')
        if 'thrust' in desc_lower:
            if 'Thrust' not in matched_categories:
                matched_categories.append('Thrust')
        if 'turbulence' in desc_lower:
            if 'Turbulence' not in matched_categories:
                matched_categories.append('Turbulence')
        if 'bird' in desc_lower:
            if 'Bird' not in matched_categories:
                matched_categories.append('Bird')
        if 'electrical' in desc_lower or 'electrical' in desc_lower:
            if 'Electrical' not in matched_categories:
                matched_categories.append('Electrical')
        
        incident_categories.append(matched_categories)
    
    category_counts = {}
    for categories in incident_categories:
        for cat in categories:
            category_counts[cat] = category_counts.get(cat, 0) + 1
    
    category_list = []
    for cat in categories_list:
        count = category_counts.get(cat, 0)
        category_list.append({'Category': cat, 'Number of Incidents': count})
    
    output_01_df = pd.DataFrame(category_list)
    output_01_df = output_01_df[output_01_df['Number of Incidents'] > 0]
    output_01_df = output_01_df.sort_values('Category').reset_index(drop=True)
    
    return {
        'output_01.csv': output_01_df,
        'output_02.csv': output_02_df
    }


if __name__ == "__main__":
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    cand_dir = task_dir / "cand"
    cand_dir.mkdir(parents=True, exist_ok=True)
    
    outputs = solve(inputs_dir)
    for filename, df in outputs.items():
        df.to_csv(cand_dir / filename, index=False, encoding='utf-8')















