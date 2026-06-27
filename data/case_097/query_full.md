## Context

Because the NBA season structure has been altered, estimate how much total flight time each of the 30 teams will spend traveling during the season under a simplified scheduling model. The simplified assumptions are:

- Within a team’s own conference: 1.5 games at home and 1.5 games away versus each opponent.
- Versus the opposing conference: 1 game at home and 1 game away versus each opponent.

Using a city-to-city travel-time matrix and a list of teams with their conferences/divisions, compute the total travel time attributable to each team’s away games and identify which teams travel the most and least (the output should provide the totals needed for that comparison).

## Requirements

- Input the data:
  - Read `input_01.csv` as a travel-time matrix between cities (rows = origin city, columns = destination city; cells contain a travel duration).
  - Read `input_02.csv` as the team reference table containing each team’s `Team`, `Conference`, and `Division`.

- Make the matrix more useable:
  - Reshape the travel matrix into a long/lookup table with one row per ordered city pair: `(From city, To city, Travel Mins)`, where `From` is taken from the first column of the matrix and `To` comes from the original column headers.

- Calculate the travel time in minutes:
  - Convert each duration value into a numeric number of minutes (`Travel Mins`).
  - Interpret duration strings containing hours and/or minutes (e.g., “Xh” and/or “Ym”) as `60*X + Y` minutes; if no duration is provided, treat it as 0 minutes.

- Apply the travel time between each city:
  - From `input_02.csv`, rename fields to `Home Team`, `Home Conference`, and `Home Division`.
  - Derive each team’s home city (`Home City`) from `Home Team` by taking the team name without its final word.
  - Create an “away team” copy of the same team list with fields `Away Team`, `Away Conference`, `Away Division`, and `Away City` (derived the same way).
  - Generate all ordered matchups via a cross join between home teams and away teams, then exclude self-matchups (`Home Team` ≠ `Away Team`).
  - Join the matchup pairs to the travel lookup on `(Home City, Away City)` using a left join to attach `Travel Mins` for each ordered pair. If a matchup has no matching travel-time entry, set its `Travel Mins` to 0.

- Determine how many games each team will play against each other:
  - For each ordered matchup, set `Away Games` based on conferences:
    - If `Home Conference` equals `Away Conference`, then `Away Games = 1.5`.
    - Otherwise, `Away Games = 1.0`.
  - Compute `Travel Contribution = Travel Mins * Away Games` for each ordered matchup (representing the home team’s travel minutes attributable to away games against that opponent under the simplified model).

- Aggregate all travel time per team:
  - Group by `Home Team`, `Home Conference`, and `Home Division`.
  - Sum `Travel Contribution` to produce total `Travel Mins` per team.

- Output the data:
  - Produce one row per team (grain: one row per `Home Team`) with total `Travel Mins`, and keep the team’s conference and division alongside it.
  - Sort the final output by `Home Team` in ascending order.

## Output

- output_01.csv
  - 4 fields:
    - Travel Mins
    - Home Team
    - Home Conference
    - Home Division