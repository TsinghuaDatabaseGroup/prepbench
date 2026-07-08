## Context
You have multiple input files containing tennis match results. The goal is to build a single analysis dataset focused on Grand Slam matches involving four specific players (Murray, Nadal, Federer, Djokovic), classify each relevant match as a win or loss from each player’s perspective, and then restrict the timeline to cover only the period up to each player’s 200th win (and any losses occurring up to that point). For each win, you will also compute the number of days since that player’s previous win.

## Requirements
- Input the data.
- Bring all the files together into 1 dataset by vertically concatenating all provided input CSV files into one unified table (do not deduplicate).
- We'll only be using 7 fields for this challenge; after combining files, keep only:
  - Tournament
  - Date
  - Series
  - Round
  - Winner
  - Loser
  - Comment

### Data Cleaning and Ambiguity Resolution
Before applying filters and transformations, perform the following data cleaning steps:
- **Missing value normalization**: Treat empty strings, "NA", "N/A", "-", "null" (case-insensitive) as missing values (NA).
- **String trimming**: Remove leading and trailing whitespace from all string fields. Normalize multiple consecutive spaces to a single space.
- **Date parsing**: Input dates are in `YYYY-MM-DD` format. Parse and validate dates; handle any parsing errors appropriately.
- **Type consistency**: Ensure `Date` is parsed as a date type for proper sorting and calculations.

**Player name matching rules**:
- For the four players of interest (Murray, Nadal, Federer, Djokovic), match against the following name formats in the `Winner` and `Loser` fields:
  - **Murray**: Match "Murray A." (exact match, case-sensitive).
  - **Nadal**: Match both "Nadal R." and "Nadal-Parera R." (both formats represent the same player; early career records may use "Nadal-Parera R.").
  - **Federer**: Match "Federer R." (exact match, case-sensitive).
  - **Djokovic**: Match "Djokovic N." (exact match, case-sensitive).
- Player name matching is case-sensitive and requires exact match of the full name format (including the initial and period).

**Grand Slam identification rules**:
- A match is considered a Grand Slam if either condition is met:
  - `Series` field exactly equals "Grand Slam" (case-sensitive, exact match).
  - `Tournament` field exactly equals one of the following four tournament names (case-sensitive, exact match):
    - "Australian Open"
    - "French Open"
    - "Wimbledon"
    - "US Open"
- Matching is case-sensitive and requires exact string match (no partial matching or case-insensitive matching).

- Filter to Grand Slam matches only using the rules above.
- We are only concerned with matches where Murray, Nadal, Federer or Djokovic played, so filter to only these matches using the player name matching rules above.
  - Remember they could be in the Winner field or the Loser field.
- Expand/represent matches from the perspective of each Player of Interest:
  - For each of the four players, take all filtered matches where that player appears in either `Winner` or `Loser`.
  - Add `Player of Interest` field with the player's standardized name. Use the following standardized names (matching the GT format):
    - `Federer R.` (for matches involving "Federer R.")
    - `Murray A.` (for matches involving "Murray A.")
    - `Nadal R.` (for matches involving either "Nadal R." or "Nadal-Parera R.")
    - `Djokovic N.` (for matches involving "Djokovic N.")
  - Categorise these matches as Win or Loss for each Player of Interest:
    - `Win/Loss` = "Win" if `Winner` field exactly matches one of the name formats for that Player of Interest (as specified in the player name matching rules); otherwise "Loss".
  - Note: if a match involves two players of interest, it should appear once for each applicable Player of Interest (one row per player perspective).
- We only want to compare the first 200 matches that each player won and see losses up to the 200th win. Filter the dataset accordingly and number the wins:
  - For each Player of Interest, sort their matches by `Date` ascending, then `Tournament`, then `Round` (stable ordering).
  - Identify that player’s first 200 wins in this order (or all wins if fewer than 200).
  - Define the cutoff date for that player as the `Date` of their 200th win (or their last available win if fewer than 200).
  - Keep all of that player’s matches with `Date` less than or equal to this cutoff date (this includes losses up to and including the cutoff date).
  - Assign `Win Number` only on win rows, counting wins sequentially (1, 2, 3, …) in the same chronological order; leave `Win Number` blank for loss rows.
- For each win, we want to know the number of days that have passed since the previous win:
  - Compute `Days Since Last Win` only on win rows as the difference in days between the current win’s `Date` and the previous win’s `Date` for the same Player of Interest (intervening losses do not affect the prior-win reference).
  - Leave `Days Since Last Win` blank for the first win and for all loss rows.
- Format and ordering rules for the final output:
  - Format `Date` as `DD/MM/YYYY`.
  - `Win Number` and `Days Since Last Win` must be integer-valued where present and blank where not applicable.
  - Sort the final combined output by Player of Interest in this order: Federer, Murray, Nadal, Djokovic; then by `Date` ascending within each player.
- Output the data.

## Output

- output_01.csv
  - 10 fields:
    - Player of Interest
    - Tournament
    - Round
    - Date
    - Win/Loss
    - Win Number
    - Days Since Last Win
    - Winner
    - Loser
    - Comment