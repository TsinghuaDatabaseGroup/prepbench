## Requirements

- Input the data
- Bring all the files together into 1 dataset
- We'll only be using 7 fields for this challenge:
  - Tournament
  - Date
  - Series
  - Round
  - Winner
  - Loser
  - Comment
- Filter to Grand Slam matches only
- We are only concerned with matches where Murray, Nadal, Federer or Djokovic played so filter to only these matches
- Remember they could be in the Winner field or the Loser field
- Categorise these matches as Win or Loss for each of our Players of Interest
- We only want to compare the first 200 matches that each player won and see losses up to the 200th win. Filter the dataset accordingly and number the wins
- For each win, we want to know the number of days that have passed since the previous win
- Output the data

## Output

- output_01.csv
  - 10 fields:
    - Player of Interest
    - Tournament
    - Round
    - Date
    - Win/Loss
    - Win Number
    - Days Since Last Win
    - Winner
    - Loser
    - Comment
