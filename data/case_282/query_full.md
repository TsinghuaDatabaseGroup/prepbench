## Context

You are preparing a stage-level Tour de France dataset focused on Mark Cavendish’s participation. The goal is to combine stage metadata (including stage type and distance) with (1) whether Cavendish won each stage and (2) Cavendish’s overall Tour de France finishing positions (general classification and points) for the corresponding year.

## Requirements

- Input the data.
  - Use the stages table as the base (one row per Tour de France stage for a given year).
  - Use the stage type lookup table to translate stage type IDs into stage type labels.
  - Use the wins table to identify which Tour de France stages Cavendish won.
  - Use the grand tour starts table to retrieve Cavendish’s Tour de France finishing positions by year.

- Join together the Stages and Stage Type table.
  - Left-join the stages data to the stage type lookup so every stage remains present even if its type does not match.
  - Join key: the stage’s stage-type identifier to the lookup’s stage-type identifier.
  - After the join, keep a single stage type field representing the stage type label, and remove any duplicate join fields created by the join.

- Create a field called `Time Trial ?` to determine if the stage was a Time Trial.
  - Derive `Time Trial?` from the stage description:
    - If the stage is labeled as an Individual Time Trial (ITT), set `Time Trial?` to `Individual`.
    - If the stage is labeled as a Team Time Trial (TTT), set `Time Trial?` to `Team`.
    - Otherwise set `Time Trial?` to a blank value.

- Create an `Origin - Destination` field and a `Stage Number` field.
  - `Stage Number`:
    - If the stage is a Prologue, set `Stage Number` to `0`.
    - Otherwise extract the numeric stage number from the stage description.
    - Exclude rows where a stage number cannot be derived.
  - `Origin - Destination`:
    - Derive from the stage description as the origin-to-destination portion (the part after the separator in the stage description, when present).

- Exclude non-racing days from the stages data.
  - Remove rest day rows before producing the final output.

- Join in the `Wins` data, keeping all stages and adding details only where Cavendish won.
  - Prepare the wins data so it can join to the stage-level dataset:
    - Keep only wins that correspond to Tour de France stages.
    - Derive `Year` from the win date.
    - Derive `Stage Number` from the win’s race description.
    - Deduplicate wins to one record per (`Year`, `Stage Number`) for joining.
  - Left-join wins to the stage dataset on (`Year`, `Stage Number`) so all stages are retained.
  - Create `Stages Won?` (named `Stage Won?` in the output) from the wins match:
    - Set to `Yes` when a matching win exists for that (`Year`, `Stage Number`).
    - Otherwise leave blank (NULL/empty).

- Input the Grand Tour Starts but keep only the Tour de France starts.
  - Filter the grand tour starts data to include only Tour de France records.

- Rename fields in the Tour de France starts data:
  - Rename `GC` to `General Classification Finishing Position`.
  - Rename `Points` to `Points Finishing Position`.
  - Retain only `Year` (season), `General Classification Finishing Position`, and `Points Finishing Position` for the join.

- Join the races started to the overall stage dataset to provide the finishing positions.
  - Left-join the Tour de France starts data to the stage-level dataset by `Year` so every stage remains present even if a year has no matching finishing-position record.

- Remove all duplicate fields created within the joins.
  - Ensure the final dataset has only one field for each required output column (no duplicated key columns or suffixed join artifacts).

- Output the data.
  - The final output must be stage-grain (one row per stage per year) with the exact fields listed in the Output section.

## Output

- output_01.csv
  - 9 fields:
    - Stage Won?
    - Stage Number
    - Origin - Destination
    - Time Trial?
    - General Classification Finishing Position
    - Points Finishing Position
    - Year
    - KM
    - Stage Type