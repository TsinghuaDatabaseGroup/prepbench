## Requirements

- Input the data
- Determine how many points each team gets for each game
- Create a record for each game, for each team containing:
  - Matchday
  - Team
  - Goals For (definition: goals scored by the team in the record)
  - Goals Against (definition: goals conceded by the team in the record)
  - Goal Difference (Goals For - Goals Against)
  - Points (3 points for a win, 1 point for a draw and 0 points for a loss)
  Note: there should be 38 records for each of the 20 teams in the league
- To form your league table for each matchday:
  - Create a running total for each team in the order of the matchdays:
    - Goals For
    - Goals Against
    - Goal Difference
    - Points
- Determine Position in the league for each team by matchday. Position determined by (in order of importance):
  - Points (High to Low)
  - Goal Difference (High to Low)
  - Reverse Alphabetical Order of team name (I'm a Tottenham fan)
- Remove any unnecessary data fields
- Output the data

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
