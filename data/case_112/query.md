## Context
Open play goal scoring prowess in the Premier League 2015-2020. This week we want to create a data set that allows us to analyse 'Open Play Goals' scored. We will rank the players overall and by their position.

## Requirements

- Input the data
- Remove all goalkeepers from the data set
- Remove all records where appearances =0
- In this challenge we are interested in the goals scored from open play
  - Create a new “Open Play Goals” field (the goals scored from open play is the number of goals scored that weren’t penalties or freekicks)
  - Note some players will have scored free kicks or penalties with their left or right foot
  - Be careful how Prep handles null fields!
  - Rename the original Goals scored field to Total Goals Scored
- Calculate the totals for each of the key metrics across the whole time period for each player
- Create an open play goals per appearance field across the whole time period
- Rank the players for the amount of open play goals scored across the whole time period, we are only interested in the top 20 (including those that are tied for position) – Output1
- Rank the players for the amount of open play goals scored across the whole time period by position, we are only interested in the top20 (including those tied for position) – Output2
- Output the data

## Output

- output_01.csv
  - 10 fields:
    - Open Play Goals
    - Goals with right foot
    - Goals with left foot
    - Position
    - Appearances
    - Rank
    - Total Goals
    - Open Play Goals/Game
    - Headed goals
    - Name

- output_02.csv
  - 10 fields:
    - Rank by Position
    - Open Play Goals
    - Goals with right foot
    - Goals with left foot
    - Position
    - Appearances
    - Total Goals
    - Open Play Goals/Game
    - Headed goals
    - Name
