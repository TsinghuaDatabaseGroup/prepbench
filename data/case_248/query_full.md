## Context

You are given a CSV export of project-related lines where the `Project` column mixes (a) project header rows that contain the project name and (b) financial transaction rows whose `Project` text indicates a transaction type (e.g., invoice or expense). The goal is to produce a per-project summary of total invoiced amount, total cost, and resulting profit.

## Requirements

- Input the data from `input_01.csv`.
- Derive a clean `Project Name` for each financial transaction row based on the `Project` field:
  - Treat a row as a “project name row” when `Project` is present and does **not** represent a financial transaction label (financial transaction labels are rows where `Project` starts with `Invoice` or `Expense`).
  - Create a `Project Name` column by taking the value from each project name row and propagating (fill down / forward-fill) that project name to subsequent rows until the next project name row appears.
  - This fill-down step is the required way to “fill in the field if there are any nulls” for project naming.
- Ensure `Cost` and `Invoiced Amount` are treated as numeric values (non-numeric values should be handled as missing for the purposes of filtering and aggregation).
- Remove any project header/name-only rows that do not contain any `Cost` or `Invoiced Amount` values:
  - Specifically, exclude rows where **both** `Cost` and `Invoiced Amount` are missing.
- For each `Project Name`, compute:
  - Total `Invoiced Amount` as the sum of `Invoiced Amount` across that project’s remaining rows.
  - Total `Cost` as the sum of `Cost` across that project’s remaining rows.
- Compute `Profit` per project as:
  - `Profit = Invoiced Amount - Cost` (using the aggregated totals).
- Output the final dataset at the project level (one row per `Project Name`) with the required columns and order.

## Output

- output_01.csv
  - 4 fields:
    - Project Name
    - Invoiced Amount
    - Cost
    - Profit