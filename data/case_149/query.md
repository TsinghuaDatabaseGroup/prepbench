## Context
Uh-oh, looks like the Sales Team at AllChains have gone rouge with their trackers again. They can't even maintain consistency month to month! And what's the idea with having the Salesperson names at the end of each month?
This challenge was inspired by a dataset my colleague Ollie encountered, except that dataset didn't have a RowID. If you think of a way to solve this challenge without a RowID we'd love to hear about it!

## Requirements

- Input the data
- Fill in the Salesperson names for each row (the name appears at the bottom of each monthly grouping)
- Bring out the YTD information from the October tracker and use it to create YTD totals for November too
- Reshape the data so all the bike types are in a single column
- Output the data

## Output

- output_01.csv
  - 5 fields:
    - Salesperson
    - Date
    - Bike Type
    - Sales
    - YTD Total
