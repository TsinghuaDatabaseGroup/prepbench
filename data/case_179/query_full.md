## Context
Chin & Beard Suds Co. (C&BSCo) wants to measure “non-events” in its sales history: the days on which none of its stores sold any products. Management specifically wants to know which day of the week these no-sales days most commonly occur on.

## Requirements
- Input the data from `input_01.csv`.
- Convert any data types required so that the sale timestamp can be treated as a true datetime and a date-only value can be derived from it (noting that some preparation steps may require specific data types).
- From the sales timestamp field, derive a **date-only** field (calendar date, ignoring time-of-day). If multiple sales occur on the same calendar date, that date still counts as a single “sales day”.
- Determine the inclusive calendar date range covered by the data, defined as the minimum derived date through the maximum derived date.
- Create a new row for **every** calendar day in that inclusive range (i.e., a complete daily calendar at 1-day frequency).
- Remove any date record where a sale occurred (i.e., exclude all calendar dates that appear in the set of sales dates). The remaining dates represent days with no sales.
- Create a column for **Day of the Week** for each remaining no-sales date, using the full weekday name (Monday through Sunday).
- For each day of the week, count the number of dates where there were no sales.
- Rename the count field as **Number of Days**.
- Sort the final results in weekday order: Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday.
- Output the data.

## Output

- output_01.csv
  - 2 fields:
    - Day of the Week
    - Number of Days