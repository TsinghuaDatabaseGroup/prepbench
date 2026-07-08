import pandas as pd
from pathlib import Path

def solve(inputs_dir: Path) -> dict[str, pd.DataFrame]:
    
    df = pd.read_csv(inputs_dir / "input_01.csv")
    
    trait_columns = [
        'Total_body_length',
        'Prosoma_length',
        'Prosoma_width',
        'Prosoma_height',
        'Tibia_I_length',
        'Fang_length'
    ]
    
    for col in trait_columns:
        if col in df.columns:
            df = df[~df[col].astype(str).str.contains(r'\*', na=False)]
            df = df[df[col].astype(str) != '_']
            df = df[df[col].astype(str) != '']
    
    mask = True
    for col in trait_columns:
        if col in df.columns:
            mask = mask & (df[col].astype(str) != '_') & (df[col].astype(str) != '') & (~df[col].isna())
    
    df = df[mask].copy()
    
    for col in trait_columns:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    
    df = df.dropna(subset=trait_columns)
    
    if 'Species' in df.columns:
        df['Species'] = df['Species'].str.replace('_', ' ')
    
    species_counts = df.groupby('Species').size()
    valid_species = species_counts[species_counts >= 10].index
    df = df[df['Species'].isin(valid_species)].copy()
    
    agg_dict = {col: 'mean' for col in trait_columns}
    df_agg = df.groupby('Species')[trait_columns].agg(agg_dict).reset_index()
    
    result_rows = []
    
    for trait_col in trait_columns:
        values = df_agg[trait_col].values
        min_val = values.min()
        max_val = values.max()
        
        if max_val == min_val:
            normalized_values = [0.0] * len(values)
        else:
            normalized_values = (values - min_val) / (max_val - min_val)
        
        trait_name = trait_col.replace('_', ' ')
        
        for idx, row in df_agg.iterrows():
            species = row['Species']
            value = row[trait_col]
            normalized_value = normalized_values[idx]
            
            result_rows.append({
                'Normalised Value': normalized_value,
                'Max Value': max_val,
                'Min Value': min_val,
                'Value': value,
                'Trait': trait_name,
                'Species': species
            })
    
    output_df = pd.DataFrame(result_rows)
    
    output_df = output_df[['Normalised Value', 'Max Value', 'Min Value', 'Value', 'Trait', 'Species']]
    
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

