## Requirements

- Input the data
- Add the player names to their poker events
- Create a column to count when the player finished 1st in an event
- Replace any nulls in prize_usd with zero
- Find the dates of the players first and last events
- Use these dates to calculate the length of poker career in years (with decimals)
- Create an aggregated view to find the following player stats:
  - Number of events they've taken part in
  - Total prize money
  - Their biggest win
  - The percentage of events they've won
  - The distinct count of the country played in
  - Their length of career
- Reduce the data to name, number of events, total prize money, biggest win, percentage won, countries visited, career length
**Creating a Pizza Plot / Coxcomb chart output:**
- Using the player stats to create two pivot tables
  - a pivot of the raw values
  - a pivot of the values ranked from 1-100, with 100 representing the highest value
  - Note: we're using a ranking method that averages ties, pay particular attention to countries visited!
- Join the pivots together
- Output the data

## Output

- output_01.csv
  - 4 fields:
    - name
    - metric
    - raw_value
    - scaled_value
