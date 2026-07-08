from __future__ import annotations
import pandas as pd
from pathlib import Path


def solve(inputs_dir: Path) -> dict[str, pd.DataFrame]:
    evolutions_df = pd.read_csv(inputs_dir / "input_01.csv")
    stats_df = pd.read_csv(inputs_dir / "input_02.csv")

    evolutions_df = evolutions_df[
        (evolutions_df['Stage_2'].notna()) &
        (evolutions_df['Stage_2'] != '')
    ].copy()

    stats_df = stats_df.drop(columns=['height', 'weight', 'evolves_from'])

    combat_cols = ['hp', 'attack', 'defense',
                   'special_attack', 'special_defense', 'speed']
    stats_melted = stats_df.melt(
        id_vars=['name', 'pokedex_number', 'gen_introduced'],
        value_vars=combat_cols,
        var_name='combat_factors',
        value_name='Values'
    )


    evolutions_df = evolutions_df.copy()
    evolutions_df['Stage_2'] = evolutions_df['Stage_2'].fillna('')
    evolutions_df['Stage_3'] = evolutions_df['Stage_3'].fillna('')

    stage_1_join = evolutions_df.merge(
        stats_melted,
        left_on='Stage_1',
        right_on='name',
        how='inner'
    )
    stage_1_join = stage_1_join.rename(columns={
        'pokedex_number': 'stage_1_pokedex_number',
        'gen_introduced': 'stage_1_gen_introduced',
        'Values': 'stage_1_Values'
    })
    stage_1_join = stage_1_join.drop(columns=['name'])

    stage_2_join = stage_1_join.merge(
        stats_melted[['name', 'combat_factors', 'Values']],
        left_on=['Stage_2', 'combat_factors'],
        right_on=['name', 'combat_factors'],
        how='inner',
        suffixes=('', '_stage2')
    )
    stage_2_join = stage_2_join.rename(columns={
        'Values': 'stage_2_Values'
    })
    stage_2_join = stage_2_join.drop(columns=['name'])

    stage_2_join['Stage_3_filled'] = stage_2_join['Stage_3'].fillna('')

    stage_3_notna = stage_2_join[stage_2_join['Stage_3_filled'] != ''].copy()
    stage_3_na = stage_2_join[stage_2_join['Stage_3_filled'] == ''].copy()

    if len(stage_3_notna) > 0:
        stage_3_notna_joined = stage_3_notna.merge(
            stats_melted[['name', 'combat_factors', 'Values']],
            left_on=['Stage_3_filled', 'combat_factors'],
            right_on=['name', 'combat_factors'],
            how='left',
            suffixes=('', '_stage3')
        )
        stage_3_notna_joined = stage_3_notna_joined.rename(columns={
            'Values': 'stage_3_Values'
        })
        stage_3_notna_joined = stage_3_notna_joined.drop(
            columns=['name', 'Stage_3_filled'])
    else:
        stage_3_notna_joined = pd.DataFrame()

    if len(stage_3_na) > 0:
        stage_3_na['stage_3_Values'] = pd.NA
        stage_3_na = stage_3_na.drop(columns=['Stage_3_filled'])
        stage_3_join = pd.concat(
            [stage_3_notna_joined, stage_3_na], ignore_index=True)
    else:
        stage_3_join = stage_3_notna_joined


    stage_3_join['final_combat_power_temp'] = stage_3_join.apply(
        lambda row: row['stage_3_Values'] if (
            pd.notna(row['stage_3_Values']) and
            pd.notna(row['Stage_3']) and
            row['Stage_3'] != ''
        ) else row['stage_2_Values'],
        axis=1
    )

    stage_3_join = stage_3_join.rename(columns={
        'stage_1_Values': 'initial_combat_power_temp'
    })

    aggregated = stage_3_join.groupby([
        'Stage_1', 'Stage_2', 'Stage_3',
        'stage_1_pokedex_number', 'stage_1_gen_introduced'
    ]).agg({
        'initial_combat_power_temp': 'sum',
        'final_combat_power_temp': 'sum'
    }).reset_index()

    aggregated = aggregated.rename(columns={
        'stage_1_pokedex_number': 'pokedex_number',
        'stage_1_gen_introduced': 'gen_introduced',
        'initial_combat_power_temp': 'initial_combat_power',
        'final_combat_power_temp': 'final_combat_power'
    })

    def calc_increase(row):
        result = (row['final_combat_power'] -
                  row['initial_combat_power']) / row['initial_combat_power']
        formatted = f'{result:.15g}'
        return float(formatted)

    aggregated['combat_power_increase'] = aggregated.apply(
        calc_increase, axis=1)

    aggregated = aggregated.sort_values(
        'combat_power_increase', ascending=True).reset_index(drop=True)

    aggregated['pokedex_number'] = aggregated['pokedex_number'].astype(int)
    aggregated['gen_introduced'] = aggregated['gen_introduced'].astype(int)
    aggregated['initial_combat_power'] = aggregated['initial_combat_power'].astype(
        int)
    aggregated['final_combat_power'] = aggregated['final_combat_power'].astype(
        int)


    aggregated['Stage_3'] = aggregated['Stage_3'].fillna('')
    aggregated['Stage_2'] = aggregated['Stage_2'].fillna('')

    output_df = aggregated[[
        'Stage_1', 'Stage_2', 'Stage_3',
        'pokedex_number', 'gen_introduced',
        'initial_combat_power', 'final_combat_power', 'combat_power_increase'
    ]]

    return {
        'output_01.csv': output_df
    }


if __name__ == "__main__":
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    cand_dir = task_dir / "cand"
    cand_dir.mkdir(parents=True, exist_ok=True)

    outputs = solve(inputs_dir)
    for name, df in outputs.items():
        df = df.copy()
        df['Stage_3'] = df['Stage_3'].fillna('')
        df['Stage_2'] = df['Stage_2'].fillna('')
        df.to_csv(cand_dir / name, index=False, encoding='utf-8')
