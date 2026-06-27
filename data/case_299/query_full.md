## Context

MiniBytes wants a monthly summary of sales revenue and return/refund activity. The report should show, for each month in 2023, the total sales revenue for items sold in that month and the return/refund metrics based on items returned in that month.

## Requirements

- Input the data from `inputs/input_01.csv`.
- Treat `Date Sold` and `Date Returned` as calendar dates.
- For any record where both `Date Sold` and `Date Returned` are present and `Date Sold` is later than `Date Returned`, swap the two dates so that `Date Sold` is not after `Date Returned`.
- Calculate `Days to Return` for each record as the integer number of days between `Date Sold` and `Date Returned` (`Date Returned - Date Sold`). This value is only defined for records with a return date.
- Compute a per-record refund amount based on `Days to Return` and the sale `Price`:
  - If `Days to Return` is 60 days or fewer (inclusive), refund the full `Price`.
  - If `Days to Return` is from 61 to 100 days (inclusive), refund half of `Price`, rounded to the nearest penny (2 decimals) at the per-record level.
  - If `Days to Return` is more than 100 days, refund 0.
  - If `Days to Return` is missing, the refund is treated as missing (not contributing to return-value totals).
- Produce one monthly output table at the grain of **one row per month** for all months January through December 2023 (i.e., include all 12 months even if some months have no activity). Represent each month by its first calendar day.
- Calculate monthly metrics as follows:
  - **Revenue**: for each month, sum `Price` over all records with `Date Sold` in that month.
  - **Total Returns Value**: for each month, sum the computed refund amounts over all records with `Date Returned` in that month (refunds are counted in the month the return happens; missing refund amounts do not contribute to the sum).
  - **Number of Returns**: for each month, count the number of records with `Date Returned` in that month (regardless of `Date Sold`).
  - **Avg Days to Return**: for each month, average `Days to Return` over records returned in that month (ignoring records where `Days to Return` is missing).
- For months with no returns (no records with `Date Returned` in that month), leave `Total Returns Value`, `Number of Returns`, and `Avg Days to Return` blank.
- All values should be rounded to 2 decimal places (apply to `Revenue`, `Total Returns Value`, and `Avg Days to Return`).
- Format the output `Date` as `DD/MM/YYYY` (the first day of each month).
- Output the data.

## Output

- output_01.csv
  - 5 fields:
    - Date
    - Revenue
    - Total Returns Value
    - Number of Returns
    - Avg Days to Return