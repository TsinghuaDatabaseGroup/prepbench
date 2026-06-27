## Context

You are analyzing the 2018 Tour de France final results to identify the strongest teams based on how far their riders finished behind the overall leader. The goal is to compute each team’s average time gap to the leader, keep only teams with enough finishers, and return the top-performing teams by this metric.

## Requirements

- Input the data.
- Use the 2018 Tour de France results as your input (from `input_01.csv`). Treat each input row as one rider’s result, including at least the fields needed to identify the rider, their team, and their time gap to the leader.
- Convert all time-gap values to seconds before doing any calculations, then express gaps in minutes for reporting and averaging:
  - Interpret a gap value of `-` as a zero gap (the leader).
  - Otherwise, parse the gap as a signed time duration and convert to total seconds, then to minutes.
- For each team:
  - Count the number of riders present in the results for that team (this is the “Number of Riders”).
  - Compute the team’s average gap to the leader in minutes as the arithmetic mean of the riders’ gap minutes.
  - Convert the team average gap in minutes to an integer by taking the floor (rounding down).
- Have seven or more riders complete the tour: keep only teams with `Number of Riders >= 7`.
- Determine the best teams by average gap:
  - Sort eligible teams by `Team Avg Gap in Mins` ascending, then by `Team` ascending as a tie-breaker.
  - Select only the top 2 teams after sorting.
- Output the data.

## Output

- output_01.csv
  - 3 fields:
    - Team Avg Gap in Mins
    - Team
    - Number of Riders