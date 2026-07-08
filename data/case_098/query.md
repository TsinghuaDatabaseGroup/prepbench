## Context
This week's challenge comes from the winner of the Prepstar award at this year's Tableau Conference and member of the SportsVizSunday team - Kate Brown. Kate recently created a viz all about the history of the USGA Women's US Open but before creating in Tableau Desktop she had to prepare the data in Tableau Prep to make this possible. In the viz Kate has used Polygons to create a square for each round and each year. So for this week's challenge we are going to see what data prep is required to create polygons just like in the viz!

## Requirements

- Input the data
- Join both data tables.
- Calculate the total **par score** and **round par score** for each year. The par score is the predetermined number of strokes that a golfer should require to complete a round. The tournament is made up of4 rounds, with the lowest number of shots being the winner.
- Next we need to create a square for each round for each year (4 squares a year). Each of the squares should be sized relative to the par score (smaller the better).
  - These steps are described in Kevin Flerlage's blog - Yes Polygons so you can follow the workings here to help you out!
- Create a field to determine the decade of each year. This will be used to split the years into different rows.
- For each Decade, find the highest and lowest total score and round score.
- Output the data

## Output

- output_01.csv
  - 17 fields:
    - Column
    - Row
    - Decade
    - Round to Par
    - Y Coordinate Polygon
    - X Coordinate Polygon
    - Round Colors
    - Point
    - Round Score
    - Round Num
    - Player
    - Country
    - Venue
    - Location
    - Round Par
    - Total
    - Year

- output_02.csv
  - 5 fields:
    - Decade
    - Min Round Score
    - Max Round Score
    - Min Total Score
    - Max Total Score
