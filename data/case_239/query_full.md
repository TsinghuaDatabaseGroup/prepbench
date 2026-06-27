## Context

Chin & Beard Suds Co. (C&BSCo) runs regular 5-a-side football tournaments across its London branches. In the source system, a player’s “Total Matches” value is overwritten after each tournament to reflect their updated lifetime total, which makes it hard to know how much experience they had *before* each specific tournament. Your task is to reconstruct each player’s experience going into each tournament using the tournament-by-tournament match increments.

## Requirements

- Input the data.
  - Use `inputs/input_01.csv` as the source.
  - Treat each row as one player’s record for a specific tournament (i.e., for a given `Team`, `Player ID`, and `Tournament Date`).
- Compute `Experience at beginning of Tournament` for every row.
  - Perform the calculation separately for each `(Team, Player ID)` combination.
  - Within each `(Team, Player ID)` group, order records by `Tournament Date` ascending (chronological order). Interpret `Tournament Date` as a date in `YYYY-MM-DD` format for sorting and calculation purposes.
  - For each row, compute the reverse running total of `Matches Played in Tournament` from the current tournament through the latest tournament for that player (i.e., sum of `Matches Played in Tournament` for the current row and all later dates in the same group).
  - Set:
    - `Experience at beginning of Tournament` = `Total Matches` − (reverse running total of `Matches Played in Tournament`, inclusive of the current tournament).
- Format and typing rules required for the output:
  - Output `Tournament Date` as text formatted exactly as `DD/MM/YYYY`.
  - Ensure `Player ID`, `Total Matches`, `Experience at beginning of Tournament`, and `Matches Played in Tournament` are integers in the output.
- Output the data.

## Output

- output_01.csv
  - 6 fields:
    - Team
    - Player ID
    - Total Matches
    - Tournament Date
    - Experience at beginning of Tournament
    - Matches Played in Tournament