## Context

You have four input CSV files that together contain monthly utility/maintenance cost line items for multiple schools. The goal is to consolidate these files into a single monthly, per-school dataset where each row represents one school in one month, with costs broken out by category and a computed total.

## Requirements

- Input the data from the four CSV files (the `input_*.csv` files) and consolidate them into one combined dataset by stacking all rows (do not deduplicate).
- Treat the combined input as a set of cost line items with (at minimum) the following required columns:
  - `School Name`
  - `Year`
  - `Month`
  - `Name` (the cost category name)
  - `Value` (the cost amount)
- Transform the data so that the output grain is **one row per School Name × Year × Month**, with separate numeric columns for each cost category:
  - Pivot the data wider using `School Name`, `Year`, and `Month` as the row identifiers; use `Name` to create the category columns; and use `Value` as the values.
  - If multiple rows exist for the same `School Name`/`Year`/`Month`/`Name`, sum their `Value` amounts.
  - Ensure the following four category columns exist in the result; if a category is missing for a given row (or absent entirely in the input), its value must be `0`:
    - `Gas Cost`
    - `Electricity Cost`
    - `Water Cost`
    - `Maintenance Cost`
  - Treat missing or non-numeric category values as `0`, then store these four category columns as integers.
- Calculate `Total Cost` for each row as the integer sum of:
  - `Gas Cost + Electricity Cost + Water Cost + Maintenance Cost`
- Create a `Date` field representing the month as the first day of that month, formatted exactly as `DD/MM/YYYY`:
  - Convert `Month` to a month number by first mapping English month names (`January`–`December`) to `1`–`12`.
  - If `Month` is not an English month name, interpret it as a numeric month value instead.
  - Construct the date using `Year` (as an integer), the derived month number, and day `1`, then format as `DD/MM/YYYY`.
- Order the dataset by month for each school by sorting rows by:
  1) `School Name` ascending, then
  2) `Year` ascending, then
  3) month number ascending (derived from `Month` as above).
- After sorting, create a `Sort` field that enumerates rows within each `School Name` in the sorted order:
  - `Sort = 1` for the first row of each school, increasing by 1 for each subsequent row for that school.
- Output the final dataset with exactly the required columns in the specified order.

## Output

- output_01.csv
  - 8 fields:
    - Sort
    - School Name
    - Date
    - Total Cost
    - Gas Cost
    - Electricity Cost
    - Water Cost
    - Maintenance Cost