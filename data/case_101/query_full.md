## Context
You are preparing bike order data to identify top-selling brands and compare outcomes across brands. The task focuses on (1) deriving required metrics that are not directly stored in the input and (2) aggregating the data so each output row represents a clearly defined business entity (a brand/type summary or a brand/store summary). The deliverable is two compact summary tables suitable for quick tabular review.

## Requirements
- Input the data from `inputs/input_01.csv`.
- Clean up the `Model` field to derive `Brand` by keeping only the letter characters that represent the bike brand (i.e., extract the contiguous uppercase-letter brand code from `Model`).
- Compute `Order Value` at the row level as:
  - `Order Value = Value per Bike * Quantity`
- Calculate `Days to Ship` at the row level as the day difference between the shipping date and the order date:
  - Parse `Order Date` and `Shipping Date` using the date format `dd/mm/YYYY`.
  - `Days to Ship = Shipping Date - Order Date` measured in whole days.
- Create the first aggregated output where each row represents a unique `(Brand, Bike Type)` combination:
  - Group by `Brand` and `Bike Type`.
  - Compute:
    - `Quantity Sold` = sum of `Quantity`
    - `Order Value` = sum of `Order Value`
    - `Avg Bike Value per Brand` = mean of `Value per Bike` within the group
  - Round `Avg Bike Value per Brand` to 1 decimal place.
- Create the second aggregated output where each row represents a unique `(Brand, Store)` combination:
  - Group by `Brand` and `Store`.
  - Compute:
    - `Total Quantity Sold` = sum of `Quantity`
    - `Total Order Value` = sum of `Order Value`
    - `Avg Days to Ship` = mean of `Days to Ship` within the group
  - Round `Avg Days to Ship` to 1 decimal place.
- Output the data to the required files with exactly the specified fields.

## Output

- output_01.csv
  - 5 fields:
    - Brand
    - Bike Type
    - Quantity Sold
    - Order Value
    - Avg Bike Value per Brand

- output_02.csv
  - 5 fields:
    - Brand
    - Store
    - Total Quantity Sold
    - Total Order Value
    - Avg Days to Ship