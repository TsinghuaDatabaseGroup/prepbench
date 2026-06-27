## Context
All stores were told the items in the ‘Recalled Items’ table needed to be removed from shelves on 13/05/2025. They were given 1 week to recall all the items (i.e. this must have been completed by 20/05/2025).

## Requirements
- Input the data
- Calculate how long it has taken for each item to be removed, based off the day the recall was announced (13/05/2025)
- Categorise items that were recalled on or by 20/05/2025 as ‘On Target’, those that were recalled after that date as ‘Overdue’, and those that haven’t been removed from the shelves yet as ‘Incomplete’
- Calculate and rank stores by how long it takes them on average to remove the recalled items
- Convert the average time it has taken for each store to remove recalled items to 2 fields for days and hours (e.g. 6.5 days would be 6 days and 12 hours)
- Create an output for this
- For items in the ‘Overdue’ and ‘Incomplete’ categories, calculate how many days overdue they are
- Calculate how long, on average, each store is overdue, as well as how many items each store has to remove
- Round to the nearest whole number
- Create an output for this
- Output the data

## Output

- output_01.csv
  - 4 fields:
    - Rank
    - Store
    - Days to Removal
    - Hours to Removal

- output_02.csv
  - 3 fields:
    - Store
    - Avg Days Overdue
    - Quantity
