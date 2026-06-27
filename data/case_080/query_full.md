## Context
Chin & Beard Suds Co wants to revisit the assumption that each Scent sells 100 bars per day on average. The goal is to estimate each Scent’s typical daily demand from historical sales, convert that into a revised weekly ordering quantity, and then recompute profitability under this new ordering policy. Finally, compare the revised profitability to the prior profitability to quantify the impact by Scent.

## Requirements
- Input the data from the three provided CSV files:
  - Daily sales data (including `Date`, `Scent Code`, and daily revenue as `Daily Sales`)
  - Scent reference data (including `Scent Code`, `Scent`, `Price`, and `Cost`)
  - Weekly ordering data (including `Date` and `Units Ordered`), where `Date` represents the week start date
- Parse `Date` fields as dates in both the daily sales and weekly ordering inputs.
- Enrich daily sales with `Scent`, `Price`, and `Cost` by left-joining the scent reference table onto daily sales using `Scent Code`.
- Derive daily **Units Sold** for each daily sales record as:
  - `Units Sold = Daily Sales / Price`
- Convert daily records into Wednesday-based business weeks by creating a `Week Start` date for each daily record:
  - `Week Start` is the Wednesday on or before the record’s `Date` (i.e., weeks run Wednesday–Tuesday).
- Aggregate daily sales into a weekly summary at the grain of (`Week Start`, `Scent Code`, `Scent`, `Price`, `Cost`), computing:
  - `Weekly Units Sold` = sum of `Units Sold` within the week
  - `Weekly Sales` = sum of `Daily Sales` within the week
- Bring in the original weekly ordering quantity by left-joining the weekly summary to the orders table on `Week Start` (note: this join is only on week, not on scent).
- Using the original `Units Ordered`, compute original weekly waste and profit for each weekly/scent row:
  - `Waste = Units Ordered - Weekly Units Sold`
  - `Waste Cost = Cost * Waste`
  - `Original Profit = Weekly Sales - Waste Cost`
- Calculate the **Average Units Sold each day for each Scent** by taking the mean of the daily `Units Sold` values grouped by `Scent Code` across all available days in the input.
- Round the average daily units per scent **upwards to the nearest whole number** (ceiling).
- Round that ceiling value **to the nearest 10** using standard rounding to the nearest multiple of 10 as implemented by `round` (i.e., ties at exactly halfway are rounded to the nearest even multiple of 10).
- Multiply the rounded-to-10 daily value by 7 to obtain the revised weekly ordering quantity per scent:
  - `New Units Per Week = (Rounded-to-10 daily units) * 7`
- Use this `New Units Per Week` as the new constant `Units Ordered` value for that scent for every week, and recompute waste and profit under the new scenario:
  - `New Waste = New Units Ordered - Weekly Units Sold`
  - For negative `New Waste` (meaning demand exceeded the new ordered quantity and stock would run out):
    - Set `New Waste Cost` to 0 (no waste when stock runs out).
    - Adjust weekly sales downward to reflect the stock-out constraint:
      - `Adjusted Weekly Sales = New Units Ordered * Price`
  - For non-negative `New Waste`:
    - `New Waste Cost = New Waste * Cost`
    - `Adjusted Weekly Sales = Weekly Sales`
  - `New Profit = Adjusted Weekly Sales - New Waste Cost`
- Aggregate results to the Scent level (one row per `Scent`) by summing across all weeks:
  - `Total Profit` = sum of `Original Profit`
  - `New Profit` = sum of `New Profit`
  - `Difference = New Profit - Total Profit`
- Round `Total Profit`, `New Profit`, and `Difference` to 2 decimal places.
- Output the final table sorted by `Scent` in ascending order.
- Output the data.

## Output

- output_01.csv
  - 4 fields:
    - Scent
    - Total Profit
    - New Profit
    - Difference