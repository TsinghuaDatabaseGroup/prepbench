## Context

You are given a simple car sales extract and need to prepare a monthly summary suitable for use in Tableau. The goal is to create a single month-level date field, calculate total cars sold, and report sales by dealership while retaining the colour-level sales breakdown.

## Requirements

- Input the data from `input_01.csv`.
- Create a Tableau-compatible `Date` field using `When Sold Year` and `When Sold Month`:
  - Construct the date as the first day of the given month and year (i.e., day = 01).
  - Format the resulting date as a string in `DD/MM/YYYY`.
- Calculate total cars sold per record as the sum of the colour columns:
  - `Total Cars Sold` = `Red Cars` + `Silver Cars` + `Black Cars` + `Blue Cars`.
- Aggregate to the required output grain:
  - One output row must represent one `Date` (month) and one `Dealership`.
  - Group by `Date` and `Dealership`, summing `Total Cars Sold`, `Red Cars`, `Silver Cars`, `Black Cars`, and `Blue Cars`.
- Retain the colour sales columns (`Red Cars`, `Silver Cars`, `Black Cars`, `Blue Cars`) in the final output alongside the totals.
- Output the aggregated results and ensure the final column order matches the specified output.
- Write the output rows ordered by `Date` ascending, then `Dealership` ascending.

## Output

- output_01.csv
  - 7 fields:
    - Total Cars Sold
    - Date
    - Dealership
    - Red Cars
    - Silver Cars
    - Black Cars
    - Blue Cars