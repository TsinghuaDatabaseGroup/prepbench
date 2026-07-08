## Context

You are given a simple table of stores, their sales targets, and a “Store Manager” value that is only populated on the first row of each manager’s block. The intended interpretation is that when “Store Manager” is blank, it should inherit the most recent non-blank manager name from the row above. The goal is to programmatically “fill down” the manager name so the table contains no missing manager assignments and remains robust if more rows/managers are added in the future.

## Requirements

- Input the data from `input_01.csv`.
- Treat each row as representing one store with its associated sales target and manager.
- Fill missing values in the `Store Manager` column by carrying forward the last non-null `Store Manager` value from the preceding rows (i.e., a forward fill down the column in row order).
  - This must work generically for any number of managers and stores if the table grows.
  - No manual entry or hardcoding of individual data points is allowed.
- Do not use a Script Step; use a standard, repeatable “fill down/forward fill” style operation to implement the logic.
- Ensure the final output contains no nulls in the required output fields:
  - After filling `Store Manager`, remove any rows that still have missing values in any of the required output columns.
- If a `Row ID` column is present, remove it before producing the output.
- Produce the output by keeping only the required three fields and ensuring their types are consistent:
  - `Store Manager` as text
  - `Store` as text
  - `Sales Target` as an integer
- Output the data.

## Output

- output_01.csv
  - 3 fields:
    - Store Manager
    - Store
    - Sales Target