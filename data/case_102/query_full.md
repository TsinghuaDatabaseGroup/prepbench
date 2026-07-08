## Context
We need to prepare accessory sales reporting for a bike store chain with five stores (London, Leeds, York, Manchester, Birmingham). The same table structure is provided for each store, and the goal is to reshape the data from wide “customer type + product” columns into a tidy format, derive calendar quarters from the sale date, and then produce two aggregated outputs.

Although the business description refers to an Excel workbook with five worksheets, the provided inputs for this task are five separate files representing those worksheets.

## Requirements
- Input the data:
  - Read the five provided input files and combine them into a single dataset by stacking rows (union all).
  - Add a `Store` column to each file before combining, using this mapping:
    - `input_01.csv` → `Manchester`
    - `input_02.csv` → `London`
    - `input_03.csv` → `Leeds`
    - `input_04.csv` → `York`
    - `input_05.csv` → `Birmingham`
- Turn `Date` into `Quarter`:
  - Parse `Date` as a date and derive `Quarter` as the calendar quarter number (1–4) corresponding to that date.
- Pivot 'New' columns and 'Existing' columns:
  - Reshape from wide to long so that all columns other than `Date`, `Store`, and `Quarter` are pivoted into rows.
  - The pivot must produce:
    - A single column containing the former headers (name it `Customer_Product`).
    - A single measure column for the values (name it `Products Sold`).
- Split the former column headers to form:
  - Split `Customer_Product` on the delimiter `" - "` into exactly two fields:
    - `Customer Types` (the part before the delimiter, e.g., New vs Existing)
    - `Product` (the part after the delimiter)
- Rename the measure created by the Pivot as 'Products Sold':
  - Ensure the pivoted values column is named exactly `Products Sold`.
  - Ensure `Products Sold` is numeric and store the result as an integer.
- Create a Store column from the data:
  - Ensure `Store` is present as defined in the input mapping above and is carried through the transformations.
- Remove any unnecessary data fields:
  - After splitting, drop the original `Date` and `Customer_Product` fields.
  - Keep only the fields needed for aggregation and output.
- Aggregate to form two separate outputs of the number of products sold by:
  - Output 1: group by `Product` and `Quarter`, summing `Products Sold`.
  - Output 2: group by `Store`, `Customer Types`, and `Product`, summing `Products Sold`.
  - For deterministic output ordering, sort:
    - Output 1 by `Product` ascending, then `Quarter` ascending.
    - Output 2 by `Store` ascending, then `Customer Types` ascending, then `Product` ascending.
- Output the data:
  - Write the two required CSV outputs with exactly the specified fields and names.

## Output

- output_01.csv
  - 3 fields:
    - Product
    - Quarter
    - Products Sold

- output_02.csv
  - 4 fields:
    - Store
    - Customer Types
    - Product
    - Products Sold