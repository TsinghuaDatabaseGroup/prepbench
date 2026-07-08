## Context
In this week's Preppin' Data we're collaborating with #GamesNightViz on their latest challenge Power Ups. We'll be diving into the Pokédex to explore how Pokémon combat stats change when they evolve.

## Requirements

- Input the data
- From pkmn_stats dataset remove the columns height, weight and evolves from
- Pivot (wide to long) pkmn stats so that hp, attack, defense, special_attack, special_defense, and speed become a column called 'combat_factors'
- Using the evolutions data look up the combat_factors for each Pokémon at each stage, making sure that the combat_factors match across the row, i.e. we should be able to see the hp for Bulbasaur, Ivysaur and Venusaur on one row
- Remove any columns for 'pokedex_number' and 'gen_introduced' that were from joins at Stage 2 & 3
- If a Pokémon doesn't evolve remove it from the dataset
- Find the combat power values relating to the Pokémon's last evolution stage
- Sum together each Pokémon's combat_factors
- Find the percentage increase in combat power from the first & last evolution stage
- Sort the dataset, ascending by percentage increase
  - If using Tableau Prep, consider introducing a field to manage this sort and then hide it
- Output the data
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
