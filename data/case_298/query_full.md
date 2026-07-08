## Context
The goal is to identify the worst-selling items within each product category (with particular focus on home, groceries, beauty, electronics, and clothes) by comparing each item’s sales contribution against the total sales for its category. The result should retain only those items that collectively account for the bottom 15% of sales within each category.

## Requirements
- Input the data from `input_01.csv`.
- Treat each input record as an individual product sales record and compute its sales value:
  - Create a `Sales` field as `Price * Quantity`.
- Calculate total sales at the category level:
  - Group by `Category` and compute `Category Total Sales` as the sum of `Sales` within each category.
  - Attach (join/merge) `Category Total Sales` back onto each original record by matching on `Category` (left join so all original records are retained prior to filtering).
- Work out the percentage of total for each record within its category:
  - Compute `% of Total` as `Sales / Category Total Sales` (a decimal proportion, not multiplied by 100).
- Identify the records that make up the bottom 15% of each category’s sales:
  - Within each `Category`, sort records by `Sales` ascending (worst sellers first).
  - Compute `Cumulative %` within each `Category` as the cumulative sum of `% of Total` following that ascending-`Sales` order.
  - Filter to records where `Cumulative % <= 0.15` (inclusive).
- Remove unnecessary fields and format for output:
  - Keep only: `Category`, `Product`, `Product ID`, `Price`, `Sales`, `% of Total`.
  - Round `% of Total` to 2 decimal places.
  - Sort the final output by `Category` ascending and then `Sales` ascending.
- Output the data to the required file.

## Output

- output_01.csv
  - 6 fields:
    - Category
    - Product
    - Product ID
    - Price
    - Sales
    - % of Total