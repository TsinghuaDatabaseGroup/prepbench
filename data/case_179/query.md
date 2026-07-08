## Context
One of the hardest challenges with data preparation is recording something that doesn't happen. There are some neat tricks and techniques to do exactly this so here's your chance to practice. Chin & Beard Suds Co. (C&BSCo) is trying to find how many days none of their stores actually sold any products. Thankfully for C&BSCo there aren't too many but the management team want to know which day of the week the non-sales days most commonly happen on.

## Requirements

- Input the data
- Convert any data types required (nb. certain Steps in Prep Builder can only utilise limited data types)
- Create a new row for each day that doesn't have a sale
- Remove any date record where a sale occurred
- Create a column for Day of the Week
- For each day of the week, count the numbers of dates where there were no sales
- Rename the count field as Number of Days
- Output the data

## Output

- output_01.csv
  - 2 fields:
    - Day of the Week
    - Number of Days
