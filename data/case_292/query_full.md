## Context

You are given a match results file where each row represents a single fixture on a given matchday, with a home team, an away team, and their respective scores. The goal is to produce a standings-style dataset at the matchday level that shows, for each team after each matchday game they have played, their running totals, latest scoreline, a compact form string for their most recent five results, and their league position based on specified tie-break rules.

## Requirements

- Input the data from `inputs/input_01.csv`.

- Recreate the logic to form a dataset at the grain of **one row per team per match played** (i.e., each fixture produces two rows: one for the home team and one for the away team), with the following base fields:
  - **Matchday**: the matchday of the fixture.
  - **Team**: the team name for the row (home team for the home-side row; away team for the away-side row).
  - **Goals For** (definition: goals scored by the team in the record):
    - For the home-side row: Home Score
    - For the away-side row: Away Score
  - **Goals Against** (definition: goals conceded by the team in the record):
    - For the home-side row: Away Score
    - For the away-side row: Home Score
  - **Goal Difference** = Goals For − Goals Against
  - **Points** computed per match result:
    - 3 points if Goals For > Goals Against
    - 1 point if Goals For = Goals Against
    - 0 points if Goals For < Goals Against

- Create calculations to capture the last 5 games results for each team, ordered by matchday, where the 5-game window includes the current matchday game and the previous four games for that team.
  - First derive a single-character result per match for each team:
    - `W` if Goals For > Goals Against
    - `D` if Goals For = Goals Against
    - `L` if Goals For < Goals Against
  - The “Last 5 games” field must be a 5-character string in this exact order:
    - [Result 4 games ago][Result 3 games ago][Result 2 games ago][Result 1 game ago][Current matchday result]
  - If fewer than 5 games have been played by that team up to the current row, pad the string on the **left** with hyphen (`-`) characters so the total length remains 5 (e.g., matchday 3 for a team yields two leading `-` characters followed by the three results).

- Create a field to contain the Latest Result for the team in the current match:
  - `Latest Result` = `[Goals For]-[Goals Against]` (as a string).

- Create Running Totals in matchday order per team for:
  - `Goal Difference (RT)` = cumulative sum of Goal Difference over the team’s matches up to and including the current row.
  - `Points (RT)` = cumulative sum of Points over the team’s matches up to and including the current row.

- Determine `Position` separately within each Matchday by ranking teams using these tie-breakers in order:
  1) `Points (RT)` (High to Low)  
  2) `Goal Difference (RT)` (High to Low)  
  3) Reverse alphabetical order of `Team` name (i.e., Z to A)  
  Assign Position values as consecutive integers starting at 1 for the highest-ranked team on that matchday.

- Output the data.

## Output

- output_01.csv
  - 7 fields:
    - Matchday
    - Position
    - Team
    - Goal Difference (RT)
    - Points (RT)
    - Latest Result
    - Last 5 games