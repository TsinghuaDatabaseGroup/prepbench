## Context

The English “Big 6” clubs (Arsenal, Chelsea, Liverpool, Manchester United, Manchester City, and Tottenham Hotspur) were among the teams associated with the proposed European Super League. This task evaluates how the Premier League table would look under two scenarios: (1) the current season as played, and (2) a counterfactual where the Big 6 did not play any matches (i.e., all fixtures involving any of those clubs are removed and the league table is recomputed from the remaining matches).

## Requirements

- Input the data.
- Use `input_01.csv` as the match-fixture source. Each match record must include:
  - the home team name,
  - the away team name,
  - a match result expressed as two integer goal counts separated by a hyphen (e.g., "X - Y").
- Parse the `Result` field to extract home goals and away goals for each match.

### Data ambiguity handling

#### Incomplete matches
- Some match records may have an empty `Result` field, indicating the match has not been played yet.
- **Rule**: Only process matches where the `Result` field contains a valid score (i.e., two integers separated by a hyphen with optional spaces, such as "X - Y" or "X-Y").
- **Action**: Skip all records where the `Result` field is empty or missing. These unplayed matches should not contribute to any team's statistics in either output.

#### Team name matching for Big 6 identification
- The Big 6 teams are identified by exact string matching against the following names:
  - `Arsenal`
  - `Chelsea`
  - `Liverpool`
  - `Man Utd`
  - `Man City`
  - `Spurs`
- **Rule**: Match team names exactly as they appear in the `Home Team` and `Away Team` columns. No normalization or variant handling is required (e.g., "Man Utd" matches only "Man Utd", not "Manchester United" or "Man United").
- **Action**: When filtering matches for Output 02, check if either the `Home Team` or `Away Team` field exactly matches one of the six names listed above.

### Per-match calculations (applies to both outputs)
For every played match:
- Derive `Home Goals` and `Away Goals` by parsing the two numbers in `Result`.
- For each team, create a per-match contribution record (one for the home team and one for the away team) with:
  - Games played (GP) = 1
  - Points (PTS):
    - Win = 3 points
    - Draw = 1 point
    - Loss = 0 points
    - A win/loss is determined by comparing that team’s goals vs the opponent’s goals.
  - Goal difference (GD) = goals scored minus goals conceded for that match.

### Team-level aggregation (applies to both outputs)
- Aggregate the per-match contribution records to one row per `Team`, computing:
  - `Total Games Played` = sum of GP
  - `Total Points` = sum of PTS
  - `Goal Difference` = sum of GD

### Ranking logic (applies to both outputs)
- Assign `Position` based on sorting teams by:
  1) `Total Points` (descending),
  2) `Goal Difference` (descending),
  3) `Team` (ascending) as a deterministic tie-breaker.
- After sorting, set `Position` to consecutive integers starting at 1 in that sorted order.
- Ensure numeric output fields are integers.

### Output 01: current league table
- Using all matches, produce the current league table with the required fields.

### Output 02: league table excluding the Big 6
- Recalculate the league table under the assumption that the Big 6 did not play any games by removing all played matches where either:
  - the home team is one of `{Arsenal, Chelsea, Liverpool, Man Utd, Man City, Spurs}`, or
  - the away team is one of `{Arsenal, Chelsea, Liverpool, Man Utd, Man City, Spurs}`.
- Using only the remaining played matches, repeat the same per-match calculations, aggregation, and ranking logic to produce the updated league table for the remaining clubs.
- Compute `Position Change` for each team in the updated table as:
  - `Position Change` = (that team’s `Position` in Output 01) − (that team’s `Position` in Output 02)
  - This means a positive value indicates the team improved (moved up) after removing the Big 6 fixtures.
- Output the data.

## Output

- output_01.csv
  - 5 fields:
    - Position
    - Team
    - Total Games Played
    - Total Points
    - Goal Difference

- output_02.csv
  - 6 fields:
    - Position Change
    - Position 
    - Team
    - Total Games Played
    - Total Points
    - Goal Difference