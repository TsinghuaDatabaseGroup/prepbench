## Context
You have four separate league tables (NBA, NFL, Premier League, and Rugby Aviva Premiership) and need to combine them into a single cross-sport comparison. The goal is to (1) rank teams within each sport using sport-specific tie-break rules, (2) standardize performance within each sport using z-scores, and (3) produce an overall cross-sport ranking that is primarily driven by z-scores and uses sport-specific percentile rank for tie-breaking.

## Requirements
- Input the data from the four provided league-table files (one per sport).
- Standardize/define a common set of fields across sports, including:
  - `Team` (team name as text)
  - `Sport` (sport identifier derived from the source table name; remove the word “Results” if present, and use the resulting sport names consistently: `NBA`, `NFL`, `Premier League`, `Rugby Aviva Premiership`)
  - `Ranking Field` (the primary metric used to rank teams within each sport)
- Define the `Ranking Field` by sport:
  - NBA: `Ranking Field = Wins`
  - NFL: `Ranking Field = Wins`
  - Premier League: `Ranking Field = Points`
  - Rugby Aviva Premiership: `Ranking Field = Points`
- Define and/or calculate tie-breaking fields by sport (used only to break ties within the sport ranking):
  - Premier League:
    - Tie Breaker 1 = Wins
    - Tie Breaker 2 = Goals Scored
  - NFL:
    - Tie Breaker 1 = Points Differential
    - Tie Breaker 2 = Points For
    - Points Differential = Points For − Points Against
  - NBA:
    - Use Conference Wins and Games Behind as tie-breaking fields derived from the provided columns:
      - Conference Wins = the wins component of the conference record string formatted as `Wins-Losses`
      - Games Behind = numeric games-behind value
    - Apply tie-breaking in this order to produce the sport rank: Conference Wins first, then Games Behind (with lower Games Behind ranking higher).
  - Rugby Aviva Premiership:
    - Tie Breaker 1 = Wins (W)
    - Tie Breaker 2 = Points Differential (PD)
- Ensure all computed and ranking-relevant fields use correct numeric types for calculation:
  - Ranking fields and integer count-style measures (e.g., wins, points for/against, goals scored, points differential) must be numeric.
  - NBA Games Behind must be numeric (float).
- For each sport, calculate a `Sport Rank` for teams within that sport using a deterministic sort and competition-style ranking:
  - Sort teams within the sport by the sport’s ranking keys in the specified priority order:
    - Primary: `Ranking Field` descending (higher is better)
    - Then sport-specific tie breakers in their priority order, where applicable:
      - Premier League: Wins descending, then Goals Scored descending
      - NFL: Points Differential descending, then Points For descending
      - NBA: Conference Wins descending, then Games Behind ascending (lower is better)
      - Rugby: Wins descending, then Points Differential descending
  - Assign `Sport Rank` as a competition rank: teams with identical values across all ranking keys receive the same rank; the next distinct set of key values receives the next rank number based on sorted position (i.e., ranks can repeat for ties).
- Bring all sports into one combined dataset by stacking the standardized per-sport datasets (same column names aligned by meaning).
- For each sport, calculate the z-score for each team using the sport’s `Ranking Field`:
  - Use the formula:  
    $$z=\cfrac{x-u}{o}$$  
    where:
    - \(x\) = team’s `Ranking Field`
    - \(u\) = mean `Ranking Field` within the sport
    - \(o\) = standard deviation of `Ranking Field` within the sport (sample standard deviation; if the standard deviation is 0, set z-scores to 0 for that sport)
- Calculate a `Sport Specific Percentile Rank` for each team:
  - $$\text{Sport Specific Percentile Rank}=1-\cfrac{\text{Sport Specific Rank}}{\text{Number of Team in Sport}}$$
  - Use `Sport Rank` as the Sport Specific Rank, and the number of teams as the count of rows/teams within that sport in the combined dataset.
- Create a `Cross Sport Rank` across all teams (all sports combined):
  - Order all rows by:
    1) `z-score` descending  
    2) `Sport Specific Percentile Rank` descending  
    3) `Ranking Field` descending  
    4) `Team` ascending (to ensure deterministic ordering)
  - Assign `Cross Sport Rank` as a competition rank based on (`z-score`, `Sport Specific Percentile Rank`) only:
    - teams with the same `z-score` and the same `Sport Specific Percentile Rank` share the same `Cross Sport Rank`;
    - otherwise, the next distinct pair receives the next rank number based on sorted position.
- Remove unnecessary fields so that each output contains only the required columns.
- Output the required files.

## Output

- output_01.csv
  - 6 fields:
    - Sport
    - Cross Sport Rank
    - Team
    - z-score
    - Ranking Field
    - Sport Specific Percentile Rank

- output_02.csv
  - 2 fields:
    - Sport
    - Avg Cross Sport Rank