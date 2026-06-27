## Context
- The analysis focuses on World Cup and Continental Championships (Goal Scorers table is only available for these)
- The goal is to determine the most exciting 15-minute interval to watch a match, how it varies by competition, and if it has changed over years

## Requirements
- Input the data
- Filter out Qualification rounds from the Results table
- Split out the Football Association and Competition from the tournament field (e.g., UEFA Euro → UEFA as Football Association, Euro as Competition; not all tournaments have Football Association info)
- Join to the International Competitions table (include all 8 competitions; ensure correct Football Association and Competition for CONCACAF Championship)
- Create a field for the Decade the competition took place in
- Filter the data to 1950s onwards
- Create a Match ID field so every row in the data has a unique identifier
- Calculate the number of matches in each Decade, in each Competition
- Filter out goals that cannot be assigned to a time segment and join the Goal Scorers table to the dataset
- Join on the Segment table based on what segment of time the goal was scored in (e.g., 25 minutes → 15-30 segment)
- Count how many goals were scored in each Segment, for each Competition and Decade
- Calculate the Expected number of Goals for each Segment, Competition and Decade
- Output the data

## Output

- output_01.csv
  - 6 fields:
    - Competition
    - Decade
    - Segment
    - Total Goals
    - Matches in a Decade per Competition
    - Expected number of Goals
