## Context
You are determining the “worst” eligible Gen 1 Pokémon evolution group based on how rarely that group appears in the Pokémon anime. A key rule is that eligibility is assessed at the evolution-group level: if any Pokémon in an evolution group meets an exclusion condition, then the entire evolution group is excluded from consideration.

## Requirements
- Input the data from all provided input files.

- Prepare a canonical Gen 1 Pokémon list at one row per Pokémon:
  - Ensure the Pokédex number column (`#`) is populated for each Pokémon entry and treated as an integer.
  - Keep only rows that have a Pokémon name.
  - Retain only the fields needed for downstream logic (`#` and `Name`).

- Prepare the Evolution Group reference so it can be joined to the Gen 1 list:
  - Ensure the Pokédex number (`#`) is an integer suitable for joining.
  - Standardize the Starter and Legendary indicator column names to `Starter` and `Legendary` (so they can be referenced consistently).
  - Join the Evolution Group reference to the Gen 1 list using a left join on `#`, producing a working table of Gen 1 Pokémon with their `Evolution Group`, `Starter`, and `Legendary` attributes.

- Exclude Starter and Legendary Pokémon groups:
  - Identify any evolution group that contains at least one Pokémon flagged as `Starter == 1` or `Legendary == 1`.
  - Remove all Pokémon rows belonging to any such evolution group (i.e., exclude whole groups, not just the flagged Pokémon).

- Using the Evolutions input, exclude groups with cross-generation evolution relationships:
  - Treat the evolution relationship columns as `Evolves from` and `Evolves to` (renaming from the input headers as needed).
  - Build the set of all Gen 1 Pokémon names from the Gen 1 list.
  - Find any evolution records where either `Evolves from` (when non-null) is not in the Gen 1 name set, or `Evolves to` (when non-null) is not in the Gen 1 name set.
  - Collect all Pokémon names appearing in those cross-generation evolution records (both the “from” and “to” sides) and exclude the entire evolution group for any Gen 1 Pokémon whose name is in that set.

- Exclude evolution groups that have any special forms in the provided form lists:
  - Consider the union of the name lists from the Mega, Alolan, Galarian, and Gigantamax inputs.
  - Match those form lists to base Pokémon species names for the purpose of group exclusion:
    - Mega forms should be associated back to the underlying species name (and where applicable, multiple Mega variants for the same species should map to the same base species).
    - Regional forms (Alolan, Galarian) should be associated back to the underlying species name.
    - Gigantamax names are used as provided for matching.
  - If any Gen 1 Pokémon in an evolution group matches (after the above base-species association) a name in any special-form list, exclude the entire evolution group.

- Apply the “unattainable in the most recent games” constraint:
  - Use the unattainable Pokémon name list to identify which remaining evolution groups contain at least one Pokémon in that unattainable list.
  - Keep only those evolution groups (and all Gen 1 Pokémon within them). Discard all other evolution groups.

- Compute anime appearance counts at the evolution-group level and rank groups:
  - From the anime input, treat each row as a Pokémon appearing in an `Episode`.
  - For each remaining evolution group, count the number of distinct episodes in which any member of that group appears:
    - An episode counts at most once per evolution group, even if multiple members of the group appear in the same episode.
  - Produce one output row per remaining evolution group with its distinct-episode count as `Appearances`.
  - Rank evolution groups in ascending order of `Appearances` using competition ranking (i.e., ties receive the same minimum rank, and subsequent ranks skip accordingly) and store this integer rank in `The Worst Pokémon`.
  - Sort the final results by `Appearances` ascending, then by `Evolution Group` ascending.
  - Ensure `The Worst Pokémon` and `Appearances` are integers in the output.

- Output the data exactly as specified.

## Output

- output_01.csv
  - 3 fields:
    - The Worst Pokémon
    - Evolution Group
    - Appearances