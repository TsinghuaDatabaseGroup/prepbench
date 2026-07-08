## Context
Analyze penalty shootouts from the FIFA World Cup and the UEFA European Championships (Euros) since 1976, focusing on (1) which countries are most successful in shootouts, (2) which penalty positions are most successful, and (3) which countries are most successful at converting individual penalties.

## Requirements
- Input the data.
  - Use `input_01.csv` as World Cup shootout data and `input_02.csv` as Euros shootout data.
  - Append the two datasets into a single combined dataset and add a `Competition` identifier based on the source file (`World Cup` vs `Euros`).

- Determine what competition each penalty was taken in.
  - Set `Competition = "World Cup"` for rows originating from `input_01.csv`.
  - Set `Competition = "Euros"` for rows originating from `input_02.csv`.

- Clean any fields, correctly format the date the penalty was taken, & group the two German countries (eg, West Germany & Germany).
  - Standardize team naming so that `West Germany` is treated as `Germany` anywhere it appears as a team (e.g., in winner/loser team fields).
  - No output in this task requires a date field; do not derive any metrics from dates. (If a date field exists in the inputs, it is not used in the required outputs.)

- Construct the penalty-attempt fact set used for penalty-based calculations (outputs 02 and 03).
  - Treat each input row as potentially containing up to two penalty attempts for the same `Penalty Number`: one for the shootout winner’s team and one for the shootout loser’s team.
  - For the winning team’s attempt:
    - `Team` is the (cleaned) shootout `Winner`.
    - `Penalty Number` is the kick order number for that row.
    - Outcome is parsed from the “winning team taker” field:
      - classify as `scored` if it indicates “Penalty scored”
      - classify as `missed` if it indicates “Penalty missed”
      - otherwise treat as not a valid penalty attempt for scoring analysis
  - For the losing team’s attempt:
    - `Team` is the (cleaned) shootout `Loser`.
    - `Penalty Number` is the kick order number for that row.
    - Outcome is parsed from the “losing team taker” field using the same `scored` / `missed` logic.
  - For penalty-based aggregations, include only penalty attempts where both `Penalty Number` is present as a valid number and outcome is classified as either `scored` or `missed`.

- Rank the countries on the following (shootout-level; output_01).
  - Identify unique shootouts using the combination of `Competition`, shootout identifier (`No.`), `Winner`, and `Loser` (after applying the Germany grouping rule).
  - For each unique shootout:
    - Count 1 total shootout for the winner and 1 total shootout for the loser.
    - Count 1 shootout win for the winner and 0 shootout wins for the loser.
  - Aggregate by `Team` to compute:
    - `Total Shootouts` = total shootouts participated in
    - `Shootouts` = shootouts won
    - `Shootout Win %` = round( (Shootouts / Total Shootouts) * 100 ) to the nearest whole percent (stored as an integer)
  - Exclude teams who have never won a shootout (i.e., `Shootouts` must be > 0).
  - Compute `Win % Rank` as a dense rank on `Shootout Win %` in descending order (highest percentage = rank 1).
  - Sort the final output as follows (to break ties deterministically):
    1) `Win % Rank` ascending
    2) `Shootout Win %` descending
    3) `Total Shootouts` descending
    4) `Team` ascending

- What is the most and least successful time to take a penalty? (penalty-number-level; output_02)
  - Using the penalty-attempt fact set, aggregate by `Penalty Number` to compute:
    - `Penalties Scored` = count of attempts with outcome `scored`
    - `Penalties Missed` = count of attempts with outcome `missed`
    - `Total Penalties` = `Penalties Scored` + `Penalties Missed`
    - `Penalty Scored %` = round( (Penalties Scored / Total Penalties) * 100 ) to the nearest whole percent (stored as an integer)
  - Exclude any penalty numbers with `Total Penalties` = 0.
  - Compute `Rank` as a dense rank on `Penalty Scored %` in descending order (highest percentage = rank 1).
  - Sort the final output as follows:
    1) `Rank` ascending
    2) `Penalty Scored %` descending
    3) `Total Penalties` descending
    4) `Penalty Number` ascending

- Penalties scored % by country (team-level; output_03)
  - Using the penalty-attempt fact set, aggregate by `Team` to compute:
    - `Penalties Scored` = count of attempts with outcome `scored`
    - `Penalties Missed` = count of attempts with outcome `missed`
    - `Total` = `Penalties Scored` + `Penalties Missed`
    - `% Total Penalties Scored` = round( (Penalties Scored / Total) * 100 ) to the nearest whole percent (stored as an integer)
  - Exclude any teams with `Total` = 0.
  - Compute `Penalties Scored %Rank` as a dense rank on `% Total Penalties Scored` in descending order (highest percentage = rank 1).
  - Sort the final output as follows:
    1) `Penalties Scored %Rank` ascending
    2) `% Total Penalties Scored` descending
    3) `Penalties Scored` descending
    4) `Team` ascending

- Output the data.

## Output

- output_01.csv
  - 5 fields:
    - Win % Rank
    - Shootout Win %
    - Total Shootouts
    - Shootouts
    - Team

- output_02.csv
  - 6 fields:
    - Rank
    - Penalty Scored %
    - Penalties Scored
    - Penalties Missed
    - Total Penalties
    - Penalty Number

- output_03.csv
  - 5 fields:
    - Penalties Scored %Rank
    - % Total Penalties Scored
    - Penalties Missed
    - Penalties Scored
    - Team