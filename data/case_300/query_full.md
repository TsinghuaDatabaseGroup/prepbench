## Context

SuperBytes tracks weekly inventory levels by store and product. The goal is to infer weekly sales and replenishment behavior from the recorded “Quantity Available” snapshots, then summarize sales and ordering cadence for each product within each store.

## Requirements

- Input the data:
  - Read the weekly inventory snapshots from `input_01.csv`, parsing `Inventory Date` as a date.
  - Read the product lookup from `input_02.csv` to obtain `Category` and `Product` for each `Product ID`.

- Join the tables together and remove unnecessary fields:
  - Perform a left join from the computed store–product summary to the product lookup on `Product ID` so that all store–product combinations present in the inventory data are retained even if product metadata is missing.
  - Keep only the fields required for the final output (Store, Category, Product, and the three summary metrics).

- Identify weeks where orders were placed for new stock:
  - Define an “order trigger” week as any week where the recorded `Quantity Available` (for that week’s snapshot) is **10 or less**.
  - This trigger is used only for calculating the ordering-frequency metric (see below).

- Calculate how much stock was ordered in these weeks (restock-to-30 policy):
  - Process inventory snapshots in chronological order within each `Store` + `Product ID`.
  - For each week after the first observed week for that `Store` + `Product ID`, treat the prior week’s ending stock as the previous snapshot’s `Quantity Available`:
    - If the prior week’s `Quantity Available` is **≤ 10**, then at the start of the current week the store receives an order of `30 − (prior week Quantity Available)`.
    - Otherwise, the order received for the current week is `0`.
  - For the first observed week in each `Store` + `Product ID` series, set the ordered quantity to `0` (no prior-week information is used to generate an order).

- Calculate the Quantity Sold each week, taking into consideration the new stock that has been ordered:
  - For each week in each `Store` + `Product ID` series, compute weekly units sold as:
    - `Sold = max(0, (prior week Quantity Available) + (order received this week) − (current week Quantity Available))`
  - For the first observed week, use the first week’s `Quantity Available` as the “prior week” quantity for this calculation (and the order received is `0`), ensuring the first week’s sold quantity evaluates to `0`.

- Across the dataset calculate summary metrics for each Product in each Store:
  - Output grain must be **one row per `Store` + `Product ID`** (enriched with `Category` and `Product` from the lookup).
  - Compute:
    - `Total Quantity Sold`: sum of weekly `Sold` over all weeks in the series.
    - `Avg Quantity Sold per Week`: mean of weekly `Sold` over all weeks in the series.
    - `Avg Order Frequency`: average number of weeks between order-trigger weeks, computed as:
      - `Weeks / Orders`
      - where `Weeks` is the number of weekly snapshots (rows) for that `Store` + `Product ID`,
      - and `Orders` is the count of weeks where `Quantity Available <= 10` (based on the current week’s snapshot).
      - If `Orders` is `0`, set `Avg Order Frequency` to `0.0`.

- Round these values to 1 decimal place:
  - Round `Avg Quantity Sold per Week` to 1 decimal place.
  - Round `Avg Order Frequency` to 1 decimal place.
  - Do not round `Total Quantity Sold`.

- Output the data:
  - Write the final dataset to the specified output file with the specified fields.

## Output

- output_01.csv
  - 6 fields:
    - Store
    - Category
    - Product
    - Total Quantity Sold
    - Avg Quantity Sold per Week
    - Avg Order Frequency