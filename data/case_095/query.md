## Context
Ever since Jonathan's EPIC week 3 2020 challenge on building the National Basketball Association's (NBA) standings from game results have data preppers started sweating at the mere sight of a game's result. Well as we come to the close of 2020, it's time to face those fears and battle once again with game results to help find insights. This week's challenge is inspired by a visualisation by Tableau Zen Master Rob Radburn (@robradburn) who created an alternate way to look at how the race where Lewis Hamilton won this season's championship. Being more of an NBA fan, I wanted to explore what stories exist within an NBA season. The challenge this week is to take the 2018/19 season (last non-Covid effected season) games and turn those data points into something that can allow you to create something similar to Rob's excellent view. I used Prep Builder to prepare the data for this view.

## Requirements

- Input the data
- Determine who won each game
- Work out the order of each team's games
- Work out each team's cumulative wins after each of their 82 games in the season
- Compare the team's to each other.
  - Rank 1 is the most wins by that game number
  - Rank 30 is the least wins by that game number
  - In event of a tie, rank the team alphabetically (A > Z)
- Output the data

## Output

- output_01.csv
  - 4 fields:
    - Rank1
    - Win
    - Game Number per Team
    - Team
