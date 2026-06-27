## Context
This challenge explores how Pokémon combat stats change as they evolve. Using a Pokédex-style stats table and an evolutions mapping, produce an output that compares total combat power at the first evolution stage versus the final evolution stage, and quantifies the percentage increase.

## Requirements
- Input the data.
- Use the evolutions dataset (input_01.csv) to define each evolution line with fields Stage_1, Stage_2, and Stage_3, and use the Pokémon stats dataset (input_02.csv) to obtain combat-stat values per Pokémon.
- From the Pokémon stats dataset remove the columns height, weight and evolves from.
- Pivot (wide to long) the Pokémon stats so that these six columns become row-level combat factors:
  - hp, attack, defense, special_attack, special_defense, speed  
  The resulting long table must contain:
  - the Pokémon identifier fields (name, pokedex_number, gen_introduced)
  - a column called combat_factors holding the stat name
  - a numeric value for that stat (one row per Pokémon per combat factor).
- If a Pokémon doesn't evolve, remove it from the dataset. Treat “doesn't evolve” as having no Stage_2 value (null or empty).
- Using the evolutions data, look up combat-factor values for each evolution stage such that combat_factors align across stages (i.e., for a given evolution line and a given combat_factors value, Stage_1, Stage_2, and (if present) Stage_3 values are on the same row):
  - Join Stage_1 to the long stats on Stage_1 = name (inner join).
  - Join Stage_2 to the long stats on Stage_2 = name AND combat_factors match (inner join).
  - Join Stage_3 to the long stats on Stage_3 = name AND combat_factors match, but only when Stage_3 is present; otherwise leave Stage_3 unmatched. Implement this so that evolution lines with a blank Stage_3 remain in the results.
- Remove any columns for 'pokedex_number' and 'gen_introduced' that were from joins at Stage 2 & 3. Retain pokedex_number and gen_introduced from the Stage_1 Pokémon only.
- Find the combat power values relating to the Pokémon's last evolution stage, at the combat-factor level:
  - If Stage_3 is present and has a matched combat-factor value, use the Stage_3 value as the final-stage value for that combat factor.
  - Otherwise, use the Stage_2 value as the final-stage value for that combat factor.
- Sum together each Pokémon’s combat_factors to compute:
  - initial_combat_power = sum of Stage_1 combat-factor values across the six combat factors
  - final_combat_power = sum of final-stage combat-factor values across the six combat factors  
  The output grain must be one row per evolution line (Stage_1–Stage_2–Stage_3) using Stage_1’s pokedex_number and gen_introduced.
- Find the percentage increase in combat power from the first & last evolution stage using:
  - combat_power_increase = (final_combat_power - initial_combat_power) / initial_combat_power
  - Ensure the numeric result is represented deterministically (do not round to a fixed number of decimals; preserve floating precision consistently).
- Sort the dataset, ascending by percentage increase.
  - If using Tableau Prep, consider introducing a field to manage this sort and then hide it.
- Ensure Stage_2 and Stage_3 are output as empty strings (not nulls) when they are missing.
- Output the data.
- Which Pokémon stats decrease from evolving?

## Output

- output_01.csv
  - 8 fields:
    - Stage_1
    - Stage_2
    - Stage_3
    - pokedex_number
    - gen_introduced
    - initial_combat_power
    - final_combat_power
    - combat_power_increase