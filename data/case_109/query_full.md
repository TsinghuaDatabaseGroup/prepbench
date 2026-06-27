## Context
The goal is to assign each Pokémon (restricted to Generations I–III) to an Evolution Group so that selecting any Pokémon allows you to see its immediate pre-evolution (if any), its immediate evolution(s) (if any), and the evolution details associated with each immediate evolution. The Evolution Group should be named after the first Pokémon in that evolution line.

## Requirements
- Input the data.

- Limit the Pokémon list to the scope of this challenge (Generations I–III only):
  - Keep only Pokémon whose Pokédex number is an integer and is less than or equal to 386.
    - Data cleaning for Pokédex number: Trim leading/trailing whitespace from the "#" field, then parse it as a numeric value. If the parsed value contains a decimal point (e.g., "003.1"), it is not an integer and should be excluded. Only values that parse to integers (after trimming) and are ≤ 386 should be kept.
  - Exclude mega evolutions by filtering out Pokémon whose name begins with the word "Mega" (while not excluding unrelated names that merely start with similar letters).

- Some Pokémon have more than one Type, but Types are not used in this challenge:
  - Remove the Type field (i.e., do not carry Type into the outputs).
  - Ensure there is exactly one retained stats row per Pokémon Name (if multiple rows exist for the same Name, keep a single row).
    - When multiple rows exist for the same Pokémon Name (due to multiple Types), after removing the Type field, all rows for that Name will have identical values in the remaining fields. In this case, keep any one of these rows (they are equivalent after Type removal).

- Bring in information about what each Pokémon evolves to (its immediate next evolution(s)):
  - Use the evolution dataset to attach “Evolving to”, “Level”, “Condition”, and “Evolution Type” for each evolution edge where the current Pokémon is the “Evolving from” value.
  - Filter the evolution relationships so that “Evolving to” is within the filtered Gen I–III Pokémon set (≤ 386 and non-mega). (Do not require “Evolving from” to be within the set.)
  - If there are multiple evolution records for the same (“Evolving from”, “Evolving to”) pair, keep only one record.

- Bring in information about what each Pokémon evolves from (its immediate pre-evolution):
  - For each Pokémon in the filtered Gen I–III list, attach a single “Evolving from” value based on the evolution relationships (where the Pokémon appears as “Evolving to”).
  - Ensure that all 386 Pokémon are retained even if they have no pre-evolution and/or no evolutions; in such cases, the corresponding evolution fields must be null/blank as appropriate.

- Define the output grain explicitly:
  - Produce one row per Pokémon per immediate “Evolving to” option.
  - If a Pokémon has no immediate evolutions, still output exactly one row for that Pokémon with “Evolving to” blank and the evolution-detail fields not populated.

- Create a calculation for the Evolution Group:
  - For each Pokémon, determine the first Pokémon in its evolution line by repeatedly following “Evolving from” links upward until no further pre-evolution is available.
  - Set “Evolution Group” to that first Pokémon’s name.

- Populate "First Evolution" only for third-stage Pokémon:
  - Identify Pokémon that are at least the third stage in an evolution chain (i.e., they have an "Evolving from", and that parent itself has an "Evolving from").
  - For those third-stage Pokémon only, set "First Evolution" to the first Pokémon in the chain (the same value used for "Evolution Group"); otherwise leave "First Evolution" blank.

- Some duplication may have occurred with all our joins:
  - Ensure no two output rows are exactly the same across all output fields (drop exact duplicates).

- Output the data.

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