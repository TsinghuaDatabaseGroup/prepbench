## Context

Chin & Beard Suds Co wants to hard-code a 7-day moving average of daily sales so it can be used in Tableau calculations earlier in the order of operations than a typical table calculation. The focus is daily sales at the start of 2019, and the moving average should represent the average sales over the current day plus the six preceding days.

## Requirements

- Input the data from `input_01.csv`, treating each record as a daily sales record containing at least `Date` and `Sales`.
- Ensure the calculations follow true chronological order:
  - Interpret `Date` as a calendar date in `DD/MM/YYYY` format.
  - Sort the data by this parsed date in ascending order before any window calculation is applied.
- Determine the weekly average sales for the current day and the previous six:
  - Compute `Moving Avg Sales` as the rolling mean of `Sales` over a 7-row window aligned to the current row (i.e., current day plus the 6 immediately prior days in the sorted order).
  - Do not create a moving average if it isn't the average of seven days’ sales:
    - For any row that does not have a full 7-day window available (the first 6 chronological rows), `Moving Avg Sales` must be left blank/null (i.e., not computed).
  - Round `Moving Avg Sales` to 2 decimal places.
- Clean-up the data for output by removing unnecessary columns:
  - Do not include intermediate/helper fields (such as any parsed-date field used for sorting) in the final output.
  - Output `Date` as text formatted exactly as `DD/MM/YYYY`.
- Output the data to the specified file.

## Output

- output_01.csv
  - 3 fields:
    - Date
    - Sales
    - Moving Avg Sales