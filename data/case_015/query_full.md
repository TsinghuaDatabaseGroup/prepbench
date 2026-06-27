## Context

You are given multiple input CSV files representing sales transactions from different firm regions. The goal is to consolidate these transactions into a single view, compute how much each transaction contributes to (a) the total sales for the same product within its region and (b) the total firmwide sales for that product, and then exclude transactions that represent the only purchase of that product within their region.

## Requirements

- Input the data.
- Treat each `input_*.csv` file as a separate region source and append all rows into one combined transactions table.
  - Assign the `Region` value based on the input file number:
    - `input_01.csv` → `Central`
    - `input_02.csv` → `East`
    - `input_03.csv` → `North`
    - `input_04.csv` → `South`
    - `input_05.csv` → `West`
- Parse `Order Date` as a date using day/month/year (`%d/%m/%Y`), and output it formatted back to `%d/%m/%Y`.
- Pull a list of clients purchases together across all their regions (i.e., work from the combined transactions dataset containing all regions).
- For each transaction row, compute product totals and contribution percentages using `Stock` as the product identifier:
  - Compute **Total Regional Sales** per `(Region, Stock)` as the sum of `Sales` across all transactions in that region for that stock.
  - Compute **Total Sales** per `Stock` as the sum of `Sales` across all regions for that stock.
  - Determine the % of total sales each transaction makes up:
    - **% of Regional Sales** = `(Sales / Total Regional Sales) * 100`
    - **% of Total Sales** = `(Sales / Total Sales) * 100`
- The final file should only contain sales that are not the only purchase of that share:
  - Exclude any transaction where `Sales` equals `Total Regional Sales` for that transaction’s `(Region, Stock)` (i.e., where that transaction accounts for 100% of that stock’s regional sales).
- Apply numeric formatting for the final output:
  - Round `% of Regional Sales` and `% of Total Sales` to 12 decimal places.
  - Round `Sales`, `Total Regional Sales`, and `Total Sales` to 2 decimal places.
- Sort the final output rows by:
  1) `Region` in this specific order: `South`, `Central`, `North`, `West`, `East`
  2) `Customer ID` ascending
  3) `Stock` ascending
- Output the data as specified below, with one row per retained transaction and exactly the listed columns.

## Output

- output_01.csv
  - 11 fields:
    - % of Regional Sales
    - % of Total Sales
    - Region
    - Customer ID
    - First Name
    - Last Name
    - Sales
    - Order Date
    - Stock
    - Total Regional Sales
    - Total Sales