## Context

You are preparing a summarized view of soap sales. Starting from a transactional input file, you will derive product attributes from the product description, split the data into Bar vs Liquid products, standardize the quantity representation within each product type, and then aggregate sales and order counts by store, region, and quantity. The order of the data fields and rows does not matter unless stated in the requirements.

## Requirements

- Input the data from `input_01.csv`.
- Ensure `Sale Value` is treated as numeric for aggregation.
- Separate out the `Product Name` field into two components:
  - `Product Type`: the text before the delimiter `" - "`.
  - `Quantity`: the text after the delimiter `" - "`.
- Create two paths in your flow based on `Product Type`:
  - One path for `Product Type = "Liquid"`.
  - One path for `Product Type = "Bar"`.
- For each path, standardize the `Quantity` field to a numeric value:
  - **Liquid path (ensure every value is in millilitres):**
    - Extract the numeric magnitude from the `Quantity` text (allowing decimals).
    - Extract the alphabetic unit from the `Quantity` text.
    - Convert the numeric magnitude to millilitres as follows:
      - If the unit indicates litres (`L`/`l`), multiply the magnitude by 1000.
      - Otherwise, keep the magnitude as-is (assumed already in millilitres).
    - Represent the resulting `Quantity` as an integer.
  - **Bar path:**
    - Extract the integer numeric value from the `Quantity` text.
    - Represent `Quantity` as an integer.
- For each path, aggregate to the grain of one row per unique combination of:
  - `Store Name`, `Region`, and standardized numeric `Quantity`.
- For each `(Store Name, Region, Quantity)` group, compute:
  - `Sale Value`: the sum of `Sale Value` across all rows in the group.
  - `Present in N orders`: the count of distinct `Order ID` values in the group (i.e., number of unique orders represented).
- Round the aggregated `Sale Value` to 2 decimal places.
- Output exactly the following fields (and only these fields) for each output:
  - `Quantity`, `Store Name`, `Region`, `Sale Value`, `Present in N orders`.
- Output files:
  - `output_01.csv` must contain the aggregated results for **Bar** soaps.
  - `output_02.csv` must contain the aggregated results for **Liquid** soaps.

## Output

- output_01.csv
  - 5 fields:
    - Quantity
    - Store Name
    - Region
    - Sale Value
    - Present in N orders

- output_02.csv
  - 5 fields:
    - Quantity
    - Store Name
    - Region
    - Sale Value
    - Present in N orders