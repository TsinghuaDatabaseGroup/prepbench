## Requirements

- Input the data
- Split out the *Number in Series* field into *Film Order* and *Total Films in Series*
- Work out the average rating for each trilogy
- Work out the highest ranking for each trilogy
- Rank the trilogies based on the average rating and use the highest ranking metric to break ties (make sure you haven't rounded the numeric fields yet!)
  - We have noticed a slight error in the way that Tableau Prep is calculating this rank, so don't worry if your output is different to ours, we are investigating!
- Remove the word *trilogy* from the Trilogy field
- Bring the 2 datasets together by the ranking fields
- Output the data

## Output

- output_01.csv
  - 7 fields:
    - Trilogy Ranking
    - Trilogy
    - Trilogy Average
    - Film Order
    - Title
    - Rating
    - Total Films in Series
