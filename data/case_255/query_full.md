## Context
You need to analyse historical challenge metadata to understand which techniques/themes have been used most often, and how usage varies by challenge level. The goal is to standardise inconsistent free-text theme labels into a consolidated set of techniques, then produce a priority view to guide future challenge creation.

## Requirements
- Input the data from `input_01.csv`.
- Treat each input record as a single challenge that includes:
  - `Level` (the challenge difficulty/category used for the level breakdown), and
  - `Themes` (a comma-separated list of themes/techniques applied in that challenge).
- Split the `Themes` field on commas so that each theme/technique becomes its own value.
  - After splitting, reshape the data to a long format so there is one row per (challenge, theme) combination.
  - Exclude rows where the resulting theme value is missing or empty.
- Group the themes together to account for inaccuracies by standardising theme values into consolidated technique names.
  - Apply a predefined, two-pass normalisation using mapping tables that convert known variants (e.g., plural vs singular, minor wording differences, and other inconsistencies) into canonical technique labels.
  - Any theme value not present in the mapping tables must remain unchanged.
- Aggregate to determine how many challenges each canonical `Technique` appears in, broken down by `Level`.
  - Count occurrences after the split/long reshape (i.e., count rows in the long data for each Technique–Level combination).
- Reshape to a wide format with one row per `Technique` and separate columns for the four levels:
  - `Beginner`, `Intermediate`, `Advanced`, and `3-in-1`.
  - If a level does not occur for a technique, leave that level column as null/missing (do not force it to zero).
- Create a `Total` field for each `Technique` equal to the sum of the four level columns, treating missing values as 0 for the purpose of this sum, and store `Total` as an integer.
- Rank techniques using `Priority` based on `Total` using a dense rank in ascending order (smallest `Total` gets `Priority` 1; ties share the same priority), and store `Priority` as an integer.
- Sort the final output by `Priority` ascending.
- Output the data.

## Output

- output_01.csv
  - 7 fields:
    - Priority
    - Technique
    - Beginner
    - Intermediate
    - Advanced
    - 3-in-1
    - Total