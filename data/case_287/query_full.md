## Context
You need to produce a single, correctly ordered list of Pokémon Trading Card Game cards from the Gym Heroes and Gym Challenge era. The ordering must follow the Kanto gym sequence by leader, then within each leader follow a strict hierarchy: the Gym Leader card first, then that leader’s Gym card, then the remaining associated Trainer cards (by card number), and finally that leader’s Pokémon cards (by Pokédex order, using Pokémon level as a tie-breaker when a leader has multiple cards for the same Pokémon). Any Trainer cards that are not associated with a leader must be placed at the end as “Leftover Trainers”, ordered by card number, and if card numbers tie then Gym Heroes must come before Gym Challenge.

## Requirements
- Input the 4 csv files.
- Treat the two card sources as two input tables:
  - **Trainer Cards Input** (input_01.csv): contains trainer cards, including a `Leader` field where present.
  - **Pokémon Cards Input** (input_02.csv): contains Pokémon cards with fields including set name, card number, card name, and Pokémon level.
- For the Pokémon Cards Input:
  - Standardize the Pokémon-card fields to use `Gym Set` (from `set_name`), `Number` (from `number`), and `Card` (from `name`).
  - Separate the Gym Leader and Pokémon name from the `Card` text into two fields:
    - `Leader` = the leader name portion
    - `Pokemon Name` = the Pokémon name portion
- Use the Pokémon Input (input_04.csv) to bring in Pokédex information:
  - Rename fields to `Pokemon Name` and `Pokedex_Num` (from `Name` and `Pokédex #` respectively).
  - Ensure there is at most one Pokédex row per `Pokemon Name` before joining (do not duplicate any rows in the Pokémon cards as a result of this lookup).
  - Left-join Pokédex data onto Pokémon cards by `Pokemon Name` to obtain `Pokedex_Num`. If no match exists, keep the Pokémon card row and treat its `Pokedex_Num` as 0 for sorting purposes.
- Combine the Trainer Cards Input with the processed Pokémon cards into one table, aligning columns by name.
- Use the `Table Names` field to identify the `Card Type` as either `Pokemon` or `Trainer` (the final output must contain a `Card Type` field with these values).
- Any rows that do not have a `Leader` must be assigned the leader value `"Leftover Trainers"` (this applies to trainer cards with missing leader).
- Combine the combined card table with the Leader Order Input (input_03.csv):
  - Left-join on `Leader` to bring in the leader’s gym `Order`.
  - If a leader has no matching gym order, treat its `Order` as 999 so those rows sort after all ordered gym leaders.
- Implement the full sorting logic to match the required hierarchy:
  1. Sort by gym leader order: ascending `Order` (with 999 last).
  2. Within each leader, enforce the following card-type hierarchy via an explicit sort key:
     - For non-leftover leaders:
       - Gym Leader card first (a trainer card where `Card` exactly equals `Leader`)
       - Gym card second (a trainer card whose `Card` indicates it is a Gym card)
       - Other trainer cards third
       - Pokémon cards last
     - For `"Leftover Trainers"` (trainer cards only): treat all as “other trainer cards” within the leftover group.
  3. Within the trainer-card portion for a leader, sort trainer cards by ascending card `Number`.
  4. For `"Leftover Trainers"` trainer cards only, when two cards have the same `Number`, place `Gym Heroes` before `Gym Challenge`.
  5. Within the Pokémon-card portion for a leader, sort by ascending `Pokedex_Num`, then by ascending Pokémon `level` (from the bottom-left level on the card) as a tie-breaker, and then by ascending card `Number` as a final tie-breaker.
- After sorting, generate `Sort Order` as a 1-based sequential index in the final sorted order.
- Remove unnecessary fields and keep only the required output fields.
- Output the 1 csv file.

## Output

- output_01.csv
  - 6 fields:
    - Sort Order
    - Leader
    - Gym Set
    - Number
    - Card
    - Card Type