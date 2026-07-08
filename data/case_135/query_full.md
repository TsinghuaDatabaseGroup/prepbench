## Context
You have been asked to produce an Excel-style pivot table summary of weekly sales. The goal is to transform transaction-level sales records into a store-level summary that shows units sold by item category, along with a per-store total, while excluding manufacturer returns.

## Requirements
- Input the data from `input_01.csv`.
- Exclude any records that represent returns to the manufacturer:
  - Filter out rows where the `Status` field equals `Return to Manufacturer`.
- Create a pivoted (wide) summary at the **Store** level:
  - Output grain: **one row per Store**.
  - For each Store, compute the **sum** of `Number of Items` for each `Item` category.
  - If a Store has no sales for a given item category, the value for that category must be `0`.
- Create a total for each Store of all items sold:
  - Compute `Items sold per store` as the row-wise sum of the item-category columns: `Wheels + Tyres + Saddles + Brakes`.
- Output the data with columns exactly as specified and in the specified order.

## Output

- output_01.csv
  - 6 fields:
    - Items sold per store
    - Wheels
    - Tyres
    - Saddles
    - Brakes
    - Store