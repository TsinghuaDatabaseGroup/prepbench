## Requirements

- Input the data
- Recreate the logic to form a data set of:
  - Matchday
  - Team
  - Goals For (definition: goals scored by the team in the record)
  - Goals Against (definition: goals conceded by the team in the record)
  - Goal Difference (Goals For - Goals Against)
  - Points
- Create calculations to capture the last 5 games results (the current matchday game and the previous four games)
  - The format should be:
    - [Result 4 games ago][Result 3 games ago][Result 2 games ago][Result 1 game ago][Current matchday result] as a string
    - If a game result hadn't occurred (i.e. only 3 games had been played as it's matchday 3, replace any non-results with a hyphen (-) character)
- Create a field to contain the Latest Result for the team
  - [Goals For-Goals Against]
- Create Running Totals in order of the match days per team for:
  - Goal Difference
  - Points
- Determine Position based on:
  - Points (High to Low)
  - Goal Difference (High to Low)
  - Reverse Alphabetical Order of team name (I'm a Tottenham fan)
- Output the data

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
