## Context
Chin & Beard Suds Co stores purchases in a wide format where each customer may have multiple product columns (and matching sales columns). The task is to reshape this into a more logical, line-item structure with one product per row, while also parsing the single Address field into separate address components and standardizing product names.

## Requirements
- Input the data from `input_01.csv`.
- Reshape the purchase data from wide to long so that products are stored in a single `Product` column and their corresponding amounts are stored in a single `Sales` column:
  - Treat `Product 1` with `Sales` as one potential line item.
  - Treat `Product 2` with `Sales.1` as a second potential line item.
  - Stack/append these two sets of line items together so the output contains one row per customer-product line item.
  - Exclude any stacked rows where `Product` is missing (so only actual purchased products remain).
- Clean the product names to remove punctuation by replacing hyphens (`-`) with a single space in `Product`.
- From the `Address` field, create the address columns required in the output:
  - Split `Address` into four components in this order: `Property Info`, `Town`, `Postal Code`, `Country`, based on the expected comma-separated structure “Property Info, Town, Postal Code, Country”.
  - Derive `Property Number` by extracting the numeric portion from `Property Info` and store it as an integer.
- Ensure `Sales` is an integer in the output.
- Output the data with exactly the fields listed below, in the listed order.

## Output

- output_01.csv
  - 7 fields:
    - Property Number
    - Town
    - Postal Code
    - Country
    - Customer
    - Product
    - Sales