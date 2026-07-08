## Context
Remember: once a Pokémon meets a condition, their whole evolution group is excluded from consideration. For example, since there is a Mega Beedrill, Weedle and Kakuna cannot be the worst Pokémon since they all belong to the Weedle evolution group.

## Requirements

- Input the data
- Clean up the list of Gen 1 Pokémon so we have 1 row per Pokémon
- Clean up the Evolution Group input so that we can join it to the Gen 1 list
  - Filter out Starter and Legendary Pokémon
- Using the Evolutions input, exclude any Pokémon that evolves from a Pokémon that is not part of Gen 1 or can evolve into a Pokémon outside of Gen 1
- Exclude any Pokémon with a mega evolution, Alolan, Galarian or Gigantamax form
- It's not possible to catch certain Pokémon in the most recent games. These are the only ones we will consider from this point on
- We're left with 10 evolution groups. Rank them in ascending order of how many times they've appeared in the anime to see who the worst Pokémon is!
- Output the data

## Output

- output_01.csv
  - 3 fields:
    - The Worst Pokémon
    - Evolution Group
    - Appearances
