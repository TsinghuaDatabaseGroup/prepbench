from pathlib import Path
import pandas as pd
import numpy as np


def solve(inputs_dir: Path) -> dict[str, pd.DataFrame]:
    df_trainer = pd.read_csv(inputs_dir / "input_01.csv")
    df_poke_cards = pd.read_csv(inputs_dir / "input_02.csv")
    df_leader_order = pd.read_csv(inputs_dir / "input_03.csv")
    df_pokedex = pd.read_csv(inputs_dir / "input_04.csv")


    df_pokedex.rename(columns={"Name": "Pokemon Name",
                      "Pokédex #": "Pokedex_Num"}, inplace=True)
    df_pokedex = df_pokedex.drop_duplicates(subset=["Pokemon Name"])
    df_pokedex["Pokedex_Num"] = pd.to_numeric(
        df_pokedex["Pokedex_Num"], errors='coerce').fillna(0).astype(int)

    df_trainer['Card Type'] = 'Trainer'
    df_trainer['Leader'] = df_trainer['Leader'].fillna('Leftover Trainers')
    df_trainer['Number'] = pd.to_numeric(df_trainer['Number'], errors='coerce')
    df_trainer['SortKey1'] = np.select(
        [
            (df_trainer['Leader'] != 'Leftover Trainers') & (
                df_trainer['Card'] == df_trainer['Leader']),
            (df_trainer['Leader'] != 'Leftover Trainers') & (
                df_trainer['Card'].str.contains(' Gym', na=False))
        ],
        [1, 2],
        default=3
    )
    df_trainer['Pokedex_Num'] = 0
    df_trainer['level'] = 0

    df_poke_cards.rename(
        columns={"set_name": "Gym Set", "number": "Number", "name": "Card"}, inplace=True)
    df_poke_cards['Card Type'] = 'Pokemon'
    df_poke_cards['Number'] = pd.to_numeric(
        df_poke_cards['Number'], errors='coerce')
    df_poke_cards['level'] = pd.to_numeric(
        df_poke_cards['level'], errors='coerce')

    name_parts = df_poke_cards['Card'].str.extract(r"([^']+)'s\s+(.*)")
    df_poke_cards['Leader'] = name_parts[0]
    df_poke_cards['Pokemon Name'] = name_parts[1]
    df_poke_cards['Leader'] = df_poke_cards['Leader'].fillna(
        'Leftover Trainers')

    df_poke_cards = pd.merge(df_poke_cards, df_pokedex[[
                             'Pokemon Name', 'Pokedex_Num']], on='Pokemon Name', how='left')
    df_poke_cards['Pokedex_Num'] = pd.to_numeric(
        df_poke_cards['Pokedex_Num'], errors='coerce').fillna(0).astype(int)
    df_poke_cards['SortKey1'] = 4

    combined_df = pd.concat([df_trainer, df_poke_cards], ignore_index=True)

    combined_df = pd.merge(combined_df, df_leader_order,
                           on='Leader', how='left')

    combined_df['Order'] = pd.to_numeric(
        combined_df['Order'], errors='coerce').fillna(999).astype(int)

    combined_df['Trainer_Sort_Num'] = np.where(
        combined_df['Card Type'] == 'Trainer', combined_df['Number'], np.inf)
    combined_df['Pokedex_Sort_Num'] = np.where(
        combined_df['Card Type'] == 'Pokemon', combined_df['Pokedex_Num'], np.inf)

    combined_df['Set_Order'] = np.where(
        (combined_df['Leader'] == 'Leftover Trainers') & (
            combined_df['Card Type'] == 'Trainer'),
        np.where(combined_df['Gym Set'] == 'Gym Heroes', 1, 2),
        0
    )

    sorted_df = combined_df.sort_values(
        by=['Order', 'SortKey1', 'Trainer_Sort_Num',
            'Set_Order', 'Pokedex_Sort_Num', 'level', 'Number'],
        ascending=[True, True, True, True, True, True, True],
        na_position='last'
    ).reset_index(drop=True)

    sorted_df['Sort Order'] = sorted_df.index + 1

    sorted_df['Number'] = sorted_df['Number'].astype(int)

    output_df = sorted_df[["Sort Order", "Leader",
                           "Gym Set", "Number", "Card", "Card Type"]]

    return {"output_01.csv": output_df}


if __name__ == "__main__":
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    cand_dir = task_dir / "cand"
    cand_dir.mkdir(parents=True, exist_ok=True)

    outputs = solve(inputs_dir)
    for filename, df in outputs.items():
        df.to_csv(cand_dir / filename, index=False, encoding="utf-8")
