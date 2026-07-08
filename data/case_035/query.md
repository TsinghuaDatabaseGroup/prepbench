## Context
This week's challenge builds on our Supply Chain challenge of last week. Last we created a data set that enabled us to understand how our stock levels were going to recover from their zero position (that's right, we emptied our warehouse). This week we are looking at whether those recovering stock position is going to enable to meet the requests from of our stores of stock top-ups. Using last week's output of stock levels and when they became available (also provided as an input sheet this week)...

## Requirements

- Input the data
- Form a running total of our stock levels for each product & scent.
- Form a running total of the requested quantities for each product & scent.
- Compare stock levels to determine:
  - Are any products held in stock not actually needed by any stores? If so, how much surplus stock do we have for these?
  - Which store requests can be met on their requested date? If a request can’t be met in time, how long does the store have to wait?
- Output the data

## Output

- output_01.csv
  - 4 fields:
    - Supplier
    - Product
    - Scent
    - Surplus Product

- output_02.csv
  - 9 fields:
    - Store
    - Product
    - Scent
    - Supplier
    - Quantity Requested
    - Date Required
    - Stock Ready?
    - Date Fulfilled
    - Days Request Delayed
