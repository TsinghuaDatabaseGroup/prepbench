## Context
You are preparing Major Tiddlywinks Championship results data for analysis and visualization. The source file contains event-level identifiers and descriptions, competitor details (including an optional association), per-game scores, and overall results. A “pot-out” (also written “potout”) is indicated in the source scores by an asterisk (`*`).

## Requirements
- Input the data from `input_01.csv`. Treat the literal string `NA` as a missing value.
- Create an `Event id` field by extracting the trailing integer at the end of the `event` field (the last run of digits in the string).
- Parse the `Competitors` field into:
  - `Competitor Name`: the name portion before an association, if present.
  - `Association`: the text inside parentheses at the end of the string, if present; otherwise leave as null.
- Convert score/points strings that may include vulgar fraction characters into numeric decimals using:
  - `½` = 0.5
  - `⅓` = 0.33… (round to 2 decimal places when present)
  - `⅔` = 0.66… (round to 2 decimal places when present)
  - The fraction character may appear appended to an integer (e.g., `4½`).
- For the first Games Output:
  - Reshape the data from wide to long so the output grain is **one row per non-null, parseable game score** for each combination of `Event id`, competitor, and game.
  - Use the game columns `G2, G3, G4, G5, G6, G7, G8, G1` (in that order) when creating the long-form rows; `Game Order` must contain the source game column name (e.g., `G3`).
  - Potouts are denoted by a `*` at the end of the raw game value. Create a boolean `Potout` field that is `True` when the raw value ends with `*`, otherwise `False`. Remove the `*` before numeric parsing.
  - Clean the `Score` field so that any vulgar fractions are translated to decimals (as described above), producing a numeric value.
  - Exclude rows where the raw game value is missing or where no numeric score can be parsed after removing the `*` and applying fraction handling.
  - Keep the `note` field; if `note` is missing, output it as an empty string.
- For the second Results Output:
  - Remove the Games fields (i.e., do not include any per-game columns).
  - Clean the `Points` field from `Pts` so that any vulgar fractions are translated to decimals (as described above), producing a numeric value.
  - Extract the `Event Start Date` from the event description by finding the first date-like substring matching `D Month YYYY` (e.g., `18 October 2019`) within the description text, and convert it to a date type using day-first interpretation.
  - Create `Event Description` from the source `description`, standardizing line breaks to `\n` and trimming whitespace on each line; if the description is missing, output it as an empty string.
  - Ensure the field names are easy to understand by using the output field names exactly as specified.
  - For `Wins`, `Losses`, and `Ties`, use the source fields `W`, `L`, and `T` respectively; if missing, treat as 0, and output as integers.
- Sorting:
  - In both outputs, sort rows by `Event id` in descending order, keeping the original row order stable within each `Event id` (and, for the Games output, keeping game rows in the specified `G2...G1` sequence per competitor as generated).
- Output the data to the two required CSV files.

## Output

- output_01.csv
  - 6 fields:
    - Event id
    - Game Order
    - Competitor Name
    - Score
    - Potout
    - note

- output_02.csv
  - 10 fields:
    - Event id
    - Competitor Name
    - Event
    - Event Start Date
    - Event Description
    - Association
    - Points
    - Wins
    - Losses
    - Ties