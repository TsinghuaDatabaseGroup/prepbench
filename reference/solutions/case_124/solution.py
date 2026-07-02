import pandas as pd
from pathlib import Path


def solve(inputs_dir: Path) -> dict[str, pd.DataFrame]:
    gen1_raw = pd.read_csv(inputs_dir / 'input_01.csv')
    evo_groups = pd.read_csv(inputs_dir / 'input_02.csv')
    evolutions = pd.read_csv(inputs_dir / 'input_03.csv')
    mega = pd.read_csv(inputs_dir / 'input_04.csv')
    alolan = pd.read_csv(inputs_dir / 'input_05.csv')
    galarian = pd.read_csv(inputs_dir / 'input_06.csv')
    gigantamax = pd.read_csv(inputs_dir / 'input_07.csv')
    unattainable = pd.read_csv(inputs_dir / 'input_08.csv')
    anime = pd.read_csv(inputs_dir / 'input_09.csv')

    gen1 = gen1_raw.copy()
    gen1['#'] = gen1['#'].ffill().astype(int)
    gen1 = gen1.dropna(subset=['Name'])
    gen1 = gen1.drop(columns=['Type', 'Total', 'HP',
                     'Attack', 'Defense', 'Sp. Atk', 'Sp. Def', 'Speed'])

    gen1_all_names = set(gen1['Name'].unique())

    evo_groups['#'] = evo_groups['#'].astype(str).str.strip().astype(int)
    evo_groups = evo_groups.rename(
        columns={'Starter?': 'Starter', 'Legendary?': 'Legendary'})

    pokemon = pd.merge(gen1, evo_groups, on='#', how='left')

    starters_legendaries = pokemon[(
        pokemon['Starter'] == 1) | (pokemon['Legendary'] == 1)]
    excluded_groups_sl = set(
        starters_legendaries['Evolution Group'].dropna().unique())
    pokemon = pokemon[~pokemon['Evolution Group'].isin(excluded_groups_sl)]

    evolutions = evolutions.rename(
        columns={'Evolving from': 'Evolves from', 'Evolving to': 'Evolves to'})
    cross_gen_evos = evolutions[(~evolutions['Evolves from'].isin(gen1_all_names) & evolutions['Evolves from'].notna()) |
                                (~evolutions['Evolves to'].isin(gen1_all_names) & evolutions['Evolves to'].notna())]
    cross_gen_names = set(cross_gen_evos['Evolves from'].dropna()).union(
        set(cross_gen_evos['Evolves to'].dropna()))
    cross_gen_groups = set(pokemon[pokemon['Name'].isin(
        cross_gen_names)]['Evolution Group'].unique())
    pokemon = pokemon[~pokemon['Evolution Group'].isin(cross_gen_groups)]

    mega['Name'] = (mega['Name']
                    .str.replace(r'^Mega\s+', '', regex=True)
                    .str.replace(r'\s+[XY]$', '', regex=True))
    alolan['Name'] = alolan['Name'].str.replace(r'^Alolan\s+', '', regex=True)
    galarian['Name'] = galarian['Name'].str.replace(
        r'^Galarian\s+', '', regex=True)

    special_form_names = set(mega['Name']).union(set(alolan['Name'])).union(
        set(galarian['Name'])).union(set(gigantamax['Name']))
    special_form_groups = set(pokemon[pokemon['Name'].isin(
        special_form_names)]['Evolution Group'].unique())
    pokemon = pokemon[~pokemon['Evolution Group'].isin(special_form_groups)]

    unattainable_groups = set(pokemon[pokemon['Name'].isin(
        unattainable['Name'])]['Evolution Group'].unique())
    pokemon = pokemon[pokemon['Evolution Group'].isin(unattainable_groups)]

    anime_counts = anime.groupby(
        'Pokemon')['Episode'].nunique().reset_index(name='Appearances')
    group_members = (pokemon.groupby('Evolution Group')['Name']
                     .apply(lambda s: sorted(s.unique()))
                     .reset_index())
    name_group = group_members.explode(
        'Name').rename(columns={'Name': 'Pokemon'})

    grp_epi = (name_group.merge(anime[['Episode', 'Pokemon']], on='Pokemon', how='left')
               .dropna(subset=['Episode'])
               .drop_duplicates(subset=['Evolution Group', 'Episode']))
    group_appearances = (grp_epi.groupby('Evolution Group', as_index=False)['Episode']
                         .nunique()
                         .rename(columns={'Episode': 'Appearances'}))

    group_appearances = group_appearances.sort_values(
        ['Appearances', 'Evolution Group']).reset_index(drop=True)
    group_appearances['The Worst Pokémon'] = group_appearances['Appearances'].rank(
        method='min', ascending=True).astype(int)

    result = group_appearances[['The Worst Pokémon',
                                'Evolution Group', 'Appearances']]

    result['The Worst Pokémon'] = result['The Worst Pokémon'].astype(int)
    result['Appearances'] = result['Appearances'].astype(int)

    result = result.sort_values(
        ['Appearances', 'Evolution Group']).reset_index(drop=True)

    return {'output_01.csv': result}


if __name__ == "__main__":
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"

    cand_dir = task_dir / "cand"
    cand_dir.mkdir(exist_ok=True)

    solutions = solve(inputs_dir)

    for filename, df in solutions.items():
        df.to_csv(cand_dir / filename, index=False, encoding='utf-8')
