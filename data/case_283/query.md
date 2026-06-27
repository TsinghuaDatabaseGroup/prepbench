## Requirements

- Input the data
- Filter out the years where the championship did not take place
- Ensure the Year field is numeric
- Reshape the data so there is a row for each Champion, for each Year, even where there are 2 winners in the Doubles
- Make sure it's clear which tournament they were the Champion of: Either Men's Singles, Women's Singles, Men's Doubles, Women's Doubles or Mixed Doubles
- For each Champion, calculate the most recent win across tournaments
- Bring the data together so it's clear for each Champion how many of each tournament they've won
- Filter the data to only include Champions who have won both Singles and Doubles tournaments
- Create a calculation for the Total Championships each Champion has won
- Rank the Champions in descending order of their Total Championships
- Create a field to indicate the Gender of each Champion
- Output the data

## Output

- output_01.csv
  - 10 fields:
    - Rank
    - Champion
    - Gender
    - Total Championships
    - Women's Singles
    - Men's Singles
    - Women's Doubles
    - Mixed Doubles
    - Men's Doubles
    - Most Recent Win
