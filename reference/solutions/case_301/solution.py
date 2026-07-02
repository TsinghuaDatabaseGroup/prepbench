
import pandas as pd
from pathlib import Path


def solve(inputs_dir: Path) -> dict[str, pd.DataFrame]:
    df_footfall = pd.read_csv(inputs_dir / "input_01.csv", na_values='-')
    df_locations = pd.read_csv(inputs_dir / "input_02.csv")
    df_stations = pd.read_csv(inputs_dir / "input_03.csv")

    def process_footfall(df: pd.DataFrame) -> pd.DataFrame:
        df.rename(columns={'Characteristic': 'Attraction'}, inplace=True)

        df.dropna(inplace=True)

        id_vars = ['Attraction']
        value_vars = ['2019', '2020', '2021',
                      '2022', '2023']
        df_melted = df.melt(id_vars=id_vars, value_vars=value_vars,
                            var_name='Year', value_name='Attraction Footfall')

        df_melted['Attraction Footfall'] = df_melted['Attraction Footfall'] * 1000
        df_melted['Year'] = df_melted['Year'].astype(int)

        avg_footfall = df_melted.groupby(
            'Attraction')['Attraction Footfall'].mean().reset_index()
        avg_footfall.rename(
            columns={'Attraction Footfall': '5 Year Avg Footfall'}, inplace=True)
        df_merged = pd.merge(df_melted, avg_footfall, on='Attraction')

        df_merged['Attraction Rank'] = df_merged['5 Year Avg Footfall'].rank(
            method='dense', ascending=False).astype(int)

        output_df = df_merged[['Attraction Rank', 'Attraction',
                               '5 Year Avg Footfall', 'Year', 'Attraction Footfall']]
        return output_df

    def process_locations(df: pd.DataFrame) -> pd.DataFrame:
        df[['Attraction Latitude', 'Attraction Longitude']
           ] = df['Lat, Longs'].str.split(', ', expand=True)

        output_df = df[['Attraction Name',
                        'Attraction Latitude', 'Attraction Longitude']].copy()
        output_df['Attraction Latitude'] = pd.to_numeric(
            output_df['Attraction Latitude'])
        output_df['Attraction Longitude'] = pd.to_numeric(
            output_df['Attraction Longitude'])
        return output_df

    def process_stations(df: pd.DataFrame) -> pd.DataFrame:
        df_selected = df[['Station', 'Right_Latitude',
                          'Right_Longitude']].copy()

        df_selected.drop_duplicates(inplace=True)

        df_selected.rename(columns={
            'Right_Latitude': 'Station Latitude',
            'Right_Longitude': 'Station Longitude'
        }, inplace=True)
        return df_selected

    output_01 = process_footfall(df_footfall)
    output_02 = process_locations(df_locations)
    output_03 = process_stations(df_stations)

    return {
        "output_01.csv": output_01,
        "output_02.csv": output_02,
        "output_03.csv": output_03
    }


if __name__ == "__main__":
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"

    cand_dir = task_dir / "cand"
    cand_dir.mkdir(exist_ok=True)

    solutions = solve(inputs_dir)

    for filename, df in solutions.items():
        df.to_csv(cand_dir / filename, index=False, encoding='utf-8')

    print(f"Generated {len(solutions)} files in {cand_dir}")
