## Context
All stores were instructed to remove specific products listed in a “Recalled Items” table from shelves. The recall was announced on 13/05/2025, and stores had one week to complete the removal, meaning the deadline was 20/05/2025.

## Requirements
- Input the data.
- Use the “Recalled Items” list to identify which store records relate to recalled products:
  - Read `input_01.csv` as the store-level activity table and `input_02.csv` as the recalled-items list.
  - From the recalled-items list, use only the fields `Category` and `Product ID`.
  - Keep only records from `input_01.csv` whose (`Category`, `Product ID`) pair appears in the recalled-items list (an inner join on `Category` and `Product ID`).
- Treat the `Date` field as a date/time.
- Define constants:
  - Recall announcement date = 13/05/2025.
  - Recall deadline date = 20/05/2025 (inclusive for “On Target”).
- Item-level timing and status logic (applied to the recalled-product records):
  - For records with a non-missing removal `Date`, compute **days to removal** as the elapsed time from 13/05/2025 to the removal `Date`, in days (use total seconds divided by 86,400; this may be fractional).
  - Assign a **Status** per record based on removal completion:
    - If `Date` is missing: `Incomplete`
    - Else if `Date` is on or before 20/05/2025: `On Target`
    - Else: `Overdue`
- Output 1 (store ranking by average removal speed):
  - Consider only recalled-product records with a non-missing removal `Date`.
  - For each `Store`, compute the mean of `days to removal` across that store’s recalled-product records.
  - Convert each store’s mean into two integer fields:
    - `Days to Removal` = floor of the mean days.
    - `Hours to Removal` = the fractional remainder converted to hours and rounded to the nearest whole hour (i.e., round((mean − floor(mean)) × 24)).
    - If rounding produces `Hours to Removal = 24`, increment `Days to Removal` by 1 and set `Hours to Removal` to 0.
  - Rank stores from fastest to slowest by their mean `days to removal` (ascending). Break ties by `Store` ascending. Use a stable ranking such that the first row after sorting has Rank = 1, second has Rank = 2, etc.
  - Create an output containing only the required fields for `output_01.csv`.
- Overdue-days calculation (for `Overdue` and `Incomplete` only):
  - For each `Store`, define that store’s **snapshot date** as the maximum non-missing `Date` present for that store among recalled-product records.
  - For records with `Status = Overdue`: `days_overdue` = (removal `Date` − 20/05/2025) in days (total seconds / 86,400).
  - For records with `Status = Incomplete`: compute `days_overdue` using the store snapshot date instead of a removal date:
    - If the snapshot date is missing or earlier than 20/05/2025, use 20/05/2025 as the snapshot date.
    - `days_overdue` = (effective snapshot date − 20/05/2025) in days.
- Output 2 (store overdue summary):
  - Filter to only recalled-product records where `Status` is `Overdue` or `Incomplete`.
  - For each `Store`:
    - `Avg Days Overdue` = the mean of `days_overdue`, rounded to the nearest whole number using half-up rounding (i.e., values ending in .5 round up).
    - `Quantity` = the sum of the `Quantity` field across the store's filtered records.
  - Create an output containing only the required fields for `output_02.csv`.
- Output the data files exactly as specified below.

## Output

- output_01.csv
  - 4 fields:
    - Rank
    - Store
    - Days to Removal
    - Hours to Removal

- output_02.csv
  - 3 fields:
    - Store
    - Avg Days Overdue
    - Quantity