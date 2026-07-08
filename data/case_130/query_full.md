## Context
You are working with the Allchains bike store sales data and need to restructure it into a pivoted, store-level summary similar to an Excel Pivot Table. The goal is to report, for each store, the total number of items sold overall and the breakdown of items sold by product category.

## Requirements
- Input the data from `input_01.csv`.
- Remove any rows that contain returns, defined as rows where the `Status` field equals `Return to Manufacturer`.
- Remove the `Status` and `Date` fields so subsequent steps operate only on the store, item, and quantity information.
- Find the total items sold for each store by grouping by `Store` and summing `Number of Items`. Name this store-level total field exactly `Items sold per store`.
- Pivot the remaining sales data from long to wide format so that:
  - Each output row represents one `Store`.
  - The pivoted columns are based on `Item`.
  - The values aggregated into those columns are the sum of `Number of Items` for each (`Store`, `Item`) combination.
  - If a store has no sales for a given item, the corresponding pivoted value must be `0`.
- Combine the pivoted item columns with the store-level total (`Items sold per store`) by joining on `Store` (keeping only stores present in both results).
- Ensure the final output contains exactly the six fields listed in the Output section, in the same order.
- Output the data.

## Output

- output_01.csv
  - 6 fields:
    - Items sold per store
    - Wheels
    - Tyres
    - Saddles
    - Brakes
    - Store