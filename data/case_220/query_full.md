## Context
The Nut House sales data has been provided in a long (row-based) format and includes measures such as price and quantity. The goal is to prepare this dataset so you can analyze performance at the Location level by computing total revenue and the average pack price for each location.

## Requirements
- Input the data from `input_01.csv`.
- Clean up the location names.
- Reshape the data from long to wide so that each measure becomes its own field:
  - Use `Location` and `Nut Type` as the row identifiers.
  - Pivot `Category` to columns and populate values from `Value`.
  - If multiple records exist for the same (`Location`, `Nut Type`, `Category`) combination, keep the first available value for that combination.
- Calculate `Revenue` at the (`Location`, `Nut Type`) level as:
  - `Revenue = Price (£) per pack * Quant per Q`
- Aggregate to the Location level so the output has one row per `Location`, computing:
  - `Revenue` as the sum of `Revenue` across all nut types within the location.
  - `Avg. Price (£) per pack` as the mean of `Price (£) per pack` across all nut types within the location.
- Round `Avg. Price (£) per pack` to 2 decimal places.
- Sort the final results by `Location` in ascending order.
- Output the data.

## Output

- output_01.csv
  - 3 fields:
    - Location
    - Revenue
    - Avg. Price (£) per pack