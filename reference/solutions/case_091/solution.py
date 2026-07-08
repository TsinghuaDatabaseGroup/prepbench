import pandas as pd
from pathlib import Path

def solve(inputs_dir: Path) -> dict[str, pd.DataFrame]:
    sales = pd.read_csv(inputs_dir / "input_01.csv")
    targets = pd.read_csv(inputs_dir / "input_02.csv")
    projections_raw = pd.read_csv(inputs_dir / "input_03.csv")
    airports = pd.read_csv(inputs_dir / "input_04.csv")

    airports['Country'] = airports['Country'].str.strip()
    airports['Airport Code'] = airports['Airport Code'].str.strip()
    projections_raw['Country'] = projections_raw['Country'].str.strip()

    def parse_change_to_multiplier(change_str):
        if pd.isna(change_str):
            return 1.0
        parts = change_str.strip().split(' ')
        value = int(parts[1])
        if parts[0].lower() == 'minus':
            value = -value
        return 1.0 + (value / 100.0)

    projections = projections_raw.copy()
    projections['Q1'] = 1.0
    projections['Q2'] = projections['Q1-Q2 change %'].apply(parse_change_to_multiplier)
    projections['Q3'] = projections['Q1-Q3 change %'].apply(parse_change_to_multiplier)
    projections['Q4'] = projections['Q1-Q4 change %'].apply(parse_change_to_multiplier)

    projections_long = projections.melt(
        id_vars=['Country'],
        value_vars=['Q1', 'Q2', 'Q3', 'Q4'],
        var_name='Quarter',
        value_name='Projection'
    )
    projections_long.rename(columns={'Country': 'Destination Country'}, inplace=True)

    q1_sales = sales.groupby(['Origin', 'Destination'], as_index=False)['Value'].sum()
    q1_sales.rename(columns={'Value': 'Q1 Value'}, inplace=True)
    
    q1_targets = targets.groupby(['Origin', 'Destination'], as_index=False)['Value'].sum()
    q1_targets.rename(columns={'Value': 'Q1 Target'}, inplace=True)

    q1_data = q1_sales.merge(q1_targets, on=['Origin', 'Destination'])
    q1_data = q1_data.merge(airports, left_on='Origin', right_on='Airport Code', how='left')
    q1_data.rename(columns={'Country': 'Origin Country'}, inplace=True)
    q1_data.drop(['Airport Code', 'Airport'], axis=1, inplace=True)
    
    q1_data = q1_data.merge(airports, left_on='Destination', right_on='Airport Code', how='left')
    q1_data.rename(columns={'Country': 'Destination Country'}, inplace=True)
    q1_data.drop(['Airport Code', 'Airport'], axis=1, inplace=True)

    projected_data = q1_data.merge(projections_long, on='Destination Country')
    projected_data['Projected Value'] = projected_data['Q1 Value'] * projected_data['Projection']
    projected_data['Projected Target'] = projected_data['Q1 Target'] * projected_data['Projection']

    yearly_summary = projected_data.groupby(
        ['Origin', 'Origin Country', 'Destination', 'Destination Country'],
        as_index=False
    )[['Projected Value', 'Projected Target']].sum()
    yearly_summary.rename(columns={'Projected Value': 'Value', 'Projected Target': 'Target Value'}, inplace=True)

    final_df = yearly_summary
    final_df['Variance to Target'] = final_df['Value'] - final_df['Target Value']
    
    numeric_cols = ['Value', 'Target Value', 'Variance to Target']
    for col in numeric_cols:
        final_df[col] = final_df[col].round(2)

    output_df = final_df[[
        'Origin',
        'Origin Country',
        'Destination',
        'Destination Country',
        'Value',
        'Target Value',
        'Variance to Target'
    ]]

    return {"output_01.csv": output_df}

if __name__ == "__main__":
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    
    cand_dir = task_dir / "cand"
    cand_dir.mkdir(exist_ok=True)
    
    results = solve(inputs_dir)
    
    for filename, df in results.items():
        df.to_csv(cand_dir / filename, index=False, encoding='utf-8')
