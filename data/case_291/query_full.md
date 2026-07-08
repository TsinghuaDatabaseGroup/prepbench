## Context

You are given match results for a football league season. The goal is to construct a matchday-by-matchday league table dataset that, for every team on every matchday, shows cumulative (running-total) performance metrics and the team’s league position based on the specified tie-break rules.

## Requirements

- Input the data.
  - Read `input_01.csv`.
  - Use only the match result fields needed to compute team-level match records: `Matchday`, `Home Team`, `Home Score`, `Away Team`, `Away Score`.

- Determine how many points each team gets for each game.
  - For a single team’s match record, assign:
    - 3 points if Goals For > Goals Against
    - 1 point if Goals For = Goals Against
    - 0 points if Goals For < Goals Against

- Create a record for each game, for each team containing:
  - Each match must produce exactly two team-records:
    - Home team record:
      - Team = `Home Team`
      - Goals For = `Home Score`
      - Goals Against = `Away Score`
    - Away team record:
      - Team = `Away Team`
      - Goals For = `Away Score`
      - Goals Against = `Home Score`
  - For each team-record, compute:
    - Goal Difference = Goals For − Goals Against
    - Points using the points rules above
  - Include the match’s `Matchday` in each team-record.
  - Note: there should be 38 records for each of the 20 teams in the league.

- To form your league table for each matchday:
  - Create a running total for each team in the order of the matchdays:
    - Goals For
    - Goals Against
    - Goal Difference
    - Points
  - Running totals must be computed per team by ordering that team’s records by `Matchday` and cumulatively summing each metric through the current matchday.

- Determine Position in the league for each team by matchday. Position determined by (in order of importance):
  - For each `Matchday`, rank all teams using their running totals on that matchday, sorting by:
    1) Points (High to Low)
    2) Goal Difference (High to Low)
    3) Reverse Alphabetical Order of team name (I'm a Tottenham fan)
  - Assign `Position` as 1 for the top-ranked team, 2 for the next, etc., within each matchday.

- Remove any unnecessary data fields.
  - The final dataset must contain only the required output fields listed below.

- Output the data.
  - Write the result to `output_01.csv`.
  - Output one row per Team per Matchday.
  - Order the output rows by `Matchday` (ascending), then `Position` (ascending), then `Team` (ascending), to make the file deterministic.

## Output

- output_01.csv
  - 7 fields:
    - Matchday
    - Team
    - Goals For (RT)
    - Goals Against (RT)
    - Goal Difference (RT)
    - Points (RT)
    - Position