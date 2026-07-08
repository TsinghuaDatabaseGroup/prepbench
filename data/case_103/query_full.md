## Context
You have five separate store-level sales extracts (one per store) and a sixth file containing quarterly sales targets. The goal is to combine the store data into a single dataset, reshape it to a tidy (long) format, aggregate sales to the Store-by-Quarter level, join in the quarterly targets, and then compute each store’s variance to target and rank stores within each quarter.

## Requirements
- Input the data from the six provided CSV files:
  - Store sales: `input_01.csv` through `input_05.csv`
  - Targets: `input_06.csv`
- Union the five store sales inputs into one dataset.
  - Add a `Store` field to each store file before unioning, using this mapping:
    - `input_01.csv` → `Manchester`
    - `input_02.csv` → `London`
    - `input_03.csv` → `Leeds`
    - `input_04.csv` → `York`
    - `input_05.csv` → `Birmingham`
  - After the union, keep only the fields needed for subsequent steps (at minimum `Date`, `Store`, and the product sales columns).
- Pivot the product columns from wide to long:
  - Treat `Date` and `Store` as identifier columns.
  - Convert all other columns in the unioned store dataset into rows, producing:
    - a column named `Customer Type - Product` containing the original product column names
    - a numeric column renamed to `Products Sold` containing the corresponding values
- Split `Customer Type - Product` into two fields:
  - `Customer Type`
  - `Product`
  - After splitting, do not carry forward `Customer Type - Product` into later steps.
- Convert `Date` into a quarter number:
  - Create `Quarter` as the calendar quarter (1–4) derived from `Date`.
- Aggregate sales to the Store-by-Quarter grain:
  - Group by `Store` and `Quarter`
  - Compute `Products Sold` as the sum of `Products Sold` within each group
  - At this stage, each row represents one store in one quarter.
- Add and join the targets data:
  - Join the aggregated Store-by-Quarter results to the targets file on (`Store`, `Quarter`) using an inner join.
  - Retain `Target` from the targets file, and retain `Store`, `Quarter`, and aggregated `Products Sold` from the store data.
  - This join should yield 20 rows in total.
  - Remove any duplicate or redundant fields created by the join.
- Calculate performance metrics:
  - `Variance to Target` = `Products Sold` − `Target`
  - `Rank`: within each `Quarter`, rank stores by `Variance to Target` in descending order (higher variance = better rank).
    - Use dense ranking so tied variances share the same rank and the next rank increments by 1.
- Finalize the output:
  - Ensure the output contains exactly the required fields.
  - Sort the final output by `Quarter` ascending, then `Rank` ascending.
  - Output the data.

## Output

- output_01.csv
  - 6 fields:
    - Quarter
    - Rank
    - Store
    - Products Sold
    - Target
    - Variance to Target