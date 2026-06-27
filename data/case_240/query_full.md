## Context

You have two separate order extracts (two input files representing different months). The goal is to combine them into a single order-level dataset, derive an order date from the source file, assign a sequential row identifier from the first combined record to the last, and calculate how each order’s quantity compares to the previous order for the same customer and book.

## Requirements

- Input the data from both input files and add a row identifier:
  - Read `input_02.csv` and `input_01.csv`.
  - Treat each input row as one order line; the final output must contain one row per input row after combining both files.
- Use the file name to create a Date field:
  - All rows from `input_02.csv` must have `Date = "01/07/2023"` (as text in `DD/MM/YYYY` format).
  - All rows from `input_01.csv` must have `Date = "01/08/2023"` (as text in `DD/MM/YYYY` format).
- Pull the two tables together:
  - Append the July file (`input_02.csv`) first, then append the August file (`input_01.csv`), keeping all rows (no de-duplication).
- Create a sequence ID for the first order through to the last:
  - Create `Sequence ID` as a 1-based integer assigned in the combined table’s original appended order (first row = 1, next = 2, … through the final row).
  - Do not manually type an ordering in Excel; the sequence must be derived programmatically from the combined row order.
- Create a field to determine how the current order differed to the previous order:
  - Ensure `Quantity` is treated as an integer.
  - For each `Customer` + `Book` combination, order rows by `Date` ascending; if multiple rows share the same `Customer`, `Book`, and `Date`, use `Sequence ID` ascending to break ties.
  - Compute `Bigger Order?` as:  
    `Bigger Order? = Quantity - (previous Quantity for the same Customer and Book in the above order)`
  - If there is no previous order for that `Customer` + `Book` (i.e., the first row in that group), `Bigger Order?` must be blank/null.
- Output the data:
  - After computing `Bigger Order?`, return the dataset to global `Sequence ID` ascending order and output only the required fields.

## Output

- output_01.csv
  - 6 fields:
    - Customer
    - Book
    - Date
    - Sequence ID
    - Quantity
    - Bigger Order?