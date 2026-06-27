## Context
You have weekly snapshot extracts of open (not-yet-delivered) customer orders. Each weekly snapshot lists all orders that are still open as of that reporting week. The goal is to combine these snapshots into a single dataset that tracks each order over time and classifies its weekly status as:
- **New Order** the first week the order appears in the snapshots,
- **Unfulfilled Order** any subsequent week the order still appears (i.e., remains open),
- **Fulfilled** the week immediately after the last week the order appears (i.e., the first week it is no longer listed as open).

Because the snapshots only contain open orders, the “Fulfilled” week must be generated as an additional row per order rather than coming directly from an input snapshot.

## Requirements
- Input the data.
  - Read the five weekly snapshot files: `input_01.csv` through `input_05.csv`.
  - Treat `Orders` as a text identifier (not a number) so it can be grouped consistently.
  - Parse `Sale Date` as a date.

- Create one complete data set by stacking (unioning) all snapshot rows from all input files into a single table.

- Use the source table/file identity (the “Table Names” concept) to create `Reporting Date`.
  - Assign a fixed reporting date to each input snapshot based on which weekly file it came from:
    - `input_01.csv` → 2021-01-01  
    - `input_02.csv` → 2021-01-08  
    - `input_03.csv` → 2021-01-15  
    - `input_04.csv` → 2021-01-22  
    - `input_05.csv` → 2021-01-29  
  - Attach this `Reporting Date` to every row from that snapshot before combining snapshots.

- Find the minimum and maximum reporting date where an order appeared in the reports.
  - Group by `Orders`.
  - Compute:
    - `first_report` = minimum `Reporting Date` for that order across all snapshots.
    - `last_report` = maximum `Reporting Date` for that order across all snapshots.

- Apply the order status logic at the row level for rows that come directly from snapshots (i.e., rows in the stacked dataset).
  - For each snapshot row:
    - If `Reporting Date` equals `first_report`, set `Order Status` = `New Order`.
    - Otherwise, set `Order Status` = `Unfulfilled Order`.

- Add one week on to the maximum date to show when an order was fulfilled by, and generate “Fulfilled” rows.
  - For each order, create one additional candidate row with:
    - `Reporting Date` = `last_report` + 7 days
    - `Order Status` = `Fulfilled`
  - Only keep this generated “Fulfilled” row if its `Reporting Date` is not later than the latest reporting week available in the input snapshots (i.e., it must be `<=` the maximum `Reporting Date` present in the combined snapshot data). If it would fall after the last available reporting week, do not output a fulfilled row for that order.

- Populate `Sale Date` for the generated “Fulfilled” rows.
  - For each order, carry forward its sale date by taking the minimum `Sale Date` observed for that `Orders` value in the stacked snapshots and using that value in the generated fulfilled row.

- Pull the data sets together.
  - Combine:
    - all classified snapshot rows (“New Order” and “Unfulfilled Order”), and
    - all retained generated fulfilled rows,
    into one final output dataset.

- Remove any unnecessary fields.
  - The final dataset must contain only the four output fields listed below, with no helper columns (such as first/last report dates).

- Output formatting requirements.
  - Output grain: one row per order per reporting week where it appears in a snapshot, plus at most one additional “Fulfilled” row per order (subject to the reporting-week constraint above).
  - Format both `Sale Date` and `Reporting Date` as `DD/MM/YYYY` text values in the final output.

- Output the data.

## Output

- output_01.csv
  - 4 fields:
    - Order Status
    - Orders
    - Sale Date
    - Reporting Date