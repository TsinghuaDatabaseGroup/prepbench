## Context
The aim of this challenge is to group Pokémon into Evolution Groups. Why? So that when we select any Pokémon, we can see all the information about what they evolved from, what they will evolve to etc. In the example below, Bulbasaur evolves into Ivysaur, who then evolves into Venusaur. Choose another Pokémon like Flareon and we can see it evolves from Eevee, who has multiple evolution possibilities.

## Requirements

- Input the data
- Our Pokémon dataset actually contains too many Pokémon:
  - We're only interested in Pokémon up to Generation III, which is up to (and including) number 386
  - This means we're also not interested in mega evolutions so we can filter Pokémon whose name start with "Mega"
- Some Pokémon have more than one Type. We aren't interested in Types for this challenge so remove this field and ensure we have one row per Pokémon
- Now we want to bring in information about what our Pokémon evolve to
  - Warning! In our Evolution dataset, we still have Pokémon beyond Gen III. You'll need to filter these out too, from both the evolved from and evolved to fields
- Bring in information about what a Pokémon evolves from
  - Ensure that we have all 386 of our Pokémon, with nulls if they don't have a pre-evolved form or if they don't evolve
- Finally, for Pokémon that have 3 evolutions, we want to know what the First Evolution is in their Evolution Group
- Some duplication may have occurred with all our joins, ensure no 2 rows are exactly the same
- Create a calculation for our Evolution Group
  - The Evolution Group will be named after the First Evolution e.g. in the above example, Bulbasaur is the name of the Evolution Group
- Output the data

## Output

- output_01.csv
  - 16 fields:
    - Evolution Group
    - #
    - Name
    - Total
    - HP
    - Attack
    - Defense
    - Special Attack
    - Special Defense
    - Speed
    - Evolving from
    - Evolving to
    - Level
    - Condition
    - Evolution Type
    - First Evolution
