## Context
We want to analyze Liverpool FC's lineup data to understand what positions players are playing in, and how many goals were scored with different formations. We have three data sources:
1. Position List (input_01.csv). This provides us with data about the formations that Liverpool have used, and how player numbers mapped to positions and position types.
2. Player List (input_02.csv). A list of all players at Liverpool, and their preferred position group. The numbers at the start of the string is their squad number, and not the position number from the lineup table.
3. Lineup Data (input_03.csv). Match lineup data including formations, results, and player positions.

## Requirements

### Output 1
Calculate how many goals Liverpool and their Opposition scored in each game.
Answer the following question:
For each Liverpool and Opposition formation, what were the average Goals Scored/Conceded for each combination?

### Output 2
Clean the Player List, so we are left with Player Name & Preferred Position Type.
Position Types are:
- G = Goalkeeper
- D = Defender
- M = Midfielder
- A = Attacker

Join the Line-up, Formation Positions, and Player List tables.
Work out what the substitutes position is when he enters the field. We will assume that if a sub is made, the formation doesn't change, and the player is a direct replacement in the same position. Therefore, the sub off position will equal the sub on position.

Answer the following questions:
- How many times did each player play in each position?
- How many minutes did they play in each position?
- A player has a preferred type of position, how many times did they play not in that position type (Out of Position)?

## Output

- output_01.csv
  - 7 fields:
    -  Formation
    - Oppo Form.
    - Games Played
    - Liverpool Goals
    - Avg Goals Scored
    - Opposition Goals
    - Avg Goals Conceded

- output_02.csv
  - 6 fields:
    - Player Name
    - Position Type
    - Position Name
    - No Times Played
    - Mins Played
    - Games OoP
