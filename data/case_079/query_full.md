## Context
Chin & Beard Suds Co restocks its soap inventory on a weekly cadence: each Wednesday starts a new inventory week (Wednesday through the following Tuesday). The company wants to quantify how many bars are wasted under this process and what that implies for profitability, and then rank scents from most to least profitable overall.

## Requirements
- Input the data from the three provided CSV files:
  - Daily sales transactions (includes `Date`, `Scent Code`, and `Daily Sales`).
  - Scent attributes (includes `Scent Code`, `Scent`, `Price`, and `Cost`).
  - Weekly orders placed on Wednesdays (includes `Date` and `Units Ordered`).
- Treat the note “Edit 20/08 - Final 3 days in July Removed from Daily Sales” as an instruction to use the daily sales file as provided (i.e., no additional manual adjustment beyond loading the current input file).
- Parse `Date` fields as dates in both the daily sales and orders inputs.
- Join daily sales to scent attributes using a left join on `Scent Code` so that each daily sales row has its corresponding `Scent`, `Price`, and `Cost`.
- Calculate `Units Sold` for each daily sales row as:
  - `Units Sold = Daily Sales / Price`
- Assign each daily sales date to an inventory week defined as Wednesday–Tuesday by computing a `Week Start` date:
  - `Week Start` is the Wednesday that begins the Wednesday–Tuesday week containing the sales `Date`.
- For each combination of `Week Start`, `Scent Code`, `Scent`, `Price`, and `Cost`, compute weekly totals:
  - `Weekly Units Sold` = sum of `Units Sold` across all days in that week for that scent.
  - `Weekly Sales` = sum of `Daily Sales` across all days in that week for that scent.
- Prepare the weekly orders data by treating the orders `Date` as `Week Start` (each row represents the Wednesday order for that week).
- Join weekly totals to weekly orders using a left join on `Week Start` (apply the same weekly `Units Ordered` value to all scents in that week). If a week has no matching order record, keep the weekly totals and leave `Units Ordered` missing.
- For each weekly scent row, calculate:
  - `Waste = Units Ordered - Weekly Units Sold`
  - `Waste Cost = Cost * Waste`
  - `Profit = Weekly Sales - Waste Cost`
- Aggregate to scent-level profitability:
  - For each `Scent`, compute `Total Profit` as the sum of `Profit` across all weeks.
- Rank scents by `Total Profit` from highest to lowest:
  - Sort by `Total Profit` descending.
  - Assign `Profitability Rank` as sequential integers starting at 1 in that sorted order.
- Output the final ranked scent table.

## Output

- output_01.csv
  - 3 fields:
    - Profitability Rank
    - Scent
    - Total Profit