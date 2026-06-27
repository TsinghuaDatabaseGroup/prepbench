## Context
The sales team needs a downloadable view of the top-performing liquid products, broken down by size and scent, for each store. The workflow should derive the necessary product attributes from the product description, calculate store-level top 10 combinations by sales value, and then provide store-specific outputs (equivalent to a user selecting a store).

## Requirements
- Input the data from `input_01.csv`.
- Derive two fields from `Product Name` by splitting on the first occurrence of the delimiter `" - "`:
  - `Product Type` = the text before the delimiter.
  - `Size` = the text after the delimiter.
- Only keep rows where `Product Type` equals `"Liquid"`.
- Aggregate (sum) `Sale Value` at the following grain (one row per unique combination):
  - `Store Name` × `Size` × `Scent Name`.
- For each `Store Name`, rank the aggregated `Size` + `Scent Name` combinations by aggregated `Sale Value` in descending order:
  - Use a dense ranking approach (ties share the same rank, and the next rank increments by 1).
  - Store this as `Rank of Product & Scent by Store` and represent it as an integer.
- Keep only ranks 1 through 10 (i.e., rows where `Rank of Product & Scent by Store` ≤ 10). If a store has fewer than 10 ranked combinations, keep all available rows.
- Round the aggregated `Sale Value` to the nearest 10 using the transformation:
  - `Sale Value = round(Sale Value / 10) * 10`
  - The `round` function uses standard rounding (round half up): values at exactly 0.5 are rounded up. For example, 2.5 rounds to 3, and -2.5 rounds to -2.
  - Represent the result as an integer.
- Treat the store as the selectable parameter by producing store-specific outputs:
  - Generate six separate outputs, each filtered to exactly one store in this fixed mapping:
    - `output_01.csv` = Chelsea  
    - `output_02.csv` = Dulwich  
    - `output_03.csv` = Lewisham  
    - `output_04.csv` = Notting Hill  
    - `output_05.csv` = Shoreditch  
    - `output_06.csv` = Wimbledon
  - Ensure each output contains only the chosen store for that file.
- Within each store-specific output, sort rows by `Rank of Product & Scent by Store` ascending.
- Output the data with exactly the required five fields in each file.

## Output

- output_01.csv
  - 5 fields:
    - Store Name
    - Rank of Product & Scent by Store
    - Scent Name
    - Size
    - Sale Value

- output_02.csv
  - 5 fields:
    - Store Name
    - Rank of Product & Scent by Store
    - Scent Name
    - Size
    - Sale Value

- output_03.csv
  - 5 fields:
    - Store Name
    - Rank of Product & Scent by Store
    - Scent Name
    - Size
    - Sale Value

- output_04.csv
  - 5 fields:
    - Store Name
    - Rank of Product & Scent by Store
    - Scent Name
    - Size
    - Sale Value

- output_05.csv
  - 5 fields:
    - Store Name
    - Rank of Product & Scent by Store
    - Scent Name
    - Size
    - Sale Value

- output_06.csv
  - 5 fields:
    - Store Name
    - Rank of Product & Scent by Store
    - Scent Name
    - Size
    - Sale Value