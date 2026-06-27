## Context
Prepare a team-by-team view of the 2018/19 NBA regular season that tracks each team’s cumulative wins game-by-game and, at each game number, ranks all teams against one another. The result should support building a visualization of how the standings race evolves over the season.

## Requirements
- Input the data.
  - Read and append (union) all provided monthly game log CSV files whose names match `input_*.csv`.
  - From each file, use the game-level fields needed to identify the two teams, the final points for each team, the game date, and the listed start time.
  - Data cleaning:
    - Date format normalization: The date field may appear in different formats across files (e.g., "2018-10-16" or "2019-04-01 00:00:00"). Parse all date values to a standard date format (YYYY-MM-DD), extracting only the date portion if a datetime string is provided. Ignore any time component in the date field itself.
    - Time format parsing: The "p" suffix in the start time field indicates PM (e.g., "8:00p" means 8:00 PM). Remove the "p" suffix and treat the time as PM when converting to 24-hour format for ordering.
  - Exclude any game records where either team name is missing or either final points value is missing or non-numeric (since the winner cannot be determined).

- Determine who won each game.
  - For each game, compare the visitor team’s points to the home team’s points:
    - If the visitor points are greater than the home points, the visitor is the winner.
    - If the home points are greater than the visitor points, the home is the winner.
    - If the points are equal, treat the visitor as the winner.
  - Convert each game into two team-level records (one for the visitor team and one for the home team) with an `Is Win` indicator equal to 1 for the winning team’s record and 0 for the losing team’s record.

- Work out the order of each team's games.
  - Create a game timestamp for ordering by combining the calendar date with the listed start time (ET).
    - If the start time cannot be interpreted, fall back to using the calendar date at midnight for ordering.
  - For each team, sort that team’s games in ascending order by:
    1) team name, then
    2) game timestamp, then
    3) opponent name (alphabetical) as a deterministic tie-breaker when timestamps are the same.
  - Limit each team to its first 82 games after this ordering (regular season only).

- Work out each team's cumulative wins after each of their 82 games in the season.
  - Within each team (after applying the 82-game limit), assign `Game Number per Team` as the sequential game index starting at 1 in the sorted order.
  - Compute `Win` as the cumulative sum of `Is Win` within each team across increasing `Game Number per Team`.

- Compare the team's to each other.
  - For each `Game Number per Team` value (1 through 82), rank all teams based on their cumulative `Win` after that game number:
    - Rank 1 is the most wins by that game number.
    - Rank 30 is the least wins by that game number.
    - In event of a tie, rank the team alphabetically (A > Z).
  - Implement ranking by sorting teams within each game number by `Win` descending, then `Team` ascending, and assigning consecutive ranks starting at 1.

- Output the data.
  - Output one row per team per game number (i.e., up to 30 rows for each `Game Number per Team` from 1 to 82), containing the team’s cumulative wins and its rank at that game number.

## Output

- output_01.csv
  - 4 fields:
    - Rank1
    - Win
    - Game Number per Team
    - Team