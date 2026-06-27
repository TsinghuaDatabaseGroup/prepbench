## Context
Chin & Beard Suds Co receives sales data for two South West London stores (Clapham and Wimbledon) split across multiple small daily files. The goal is to combine these files into a single consistent dataset, remove any exact duplicate records caused by reporting issues, and then quantify how each scent and each day contributes to each store’s overall sales (both volume and value). Weekday labels should be replaced with the corresponding full date.

## Requirements
- Input the data from the provided CSV files:
  - Sales files:
    - Clapham: `input_01.csv` to `input_05.csv`
    - Wimbledon: `input_07.csv` to `input_11.csv`
  - Date list file: `input_06.csv`, containing a `Dates` column to be used as full-date labels (keep the date values as provided, as text).
- Assign store and date to each sales file’s rows:
  - Add a `Store` field with value `Clapham` for all rows from `input_01.csv`–`input_05.csv`, and `Wimbledon` for all rows from `input_07.csv`–`input_11.csv`.
  - Add a `Dates` field to each file so that each of the five daily sales files per store is paired to one date from `input_06.csv` based on a fixed positional mapping:
    - Read the five `Dates` values from `input_06.csv` in file order into a list `D1..D5`.
    - If there are exactly five dates, reorder them to: `[D5, D1, D4, D2, D3]`.
    - Pair this reordered list in order with each store’s five files in ascending file number (first date to `input_01.csv` / `input_07.csv`, second date to `input_02.csv` / `input_08.csv`, etc.).
- Combine all store-day files into one dataset.
- Remove duplicates by dropping rows that are identical across all fields (i.e., after `Store` and `Dates` have been attached).
- Compute each store’s total sales across all dates (after deduplication):
  - `Total_Volume` = sum of `Sales Volume` for the store
  - `Total_Value` = sum of `Sales Value` for the store
- Work out the percentage of:
  - Scent sales per Store's Total Sales Values and Volumes:
    - For each `(Store, Scent)`, sum `Sales Volume` and `Sales Value` across all dates.
    - Compute:
      - `Scent % of Store Sales Volumes` = (scent volume sum / store `Total_Volume`), rounded to 2 decimal places
      - `Scent % of Store Sales Values` = (scent value sum / store `Total_Value`), rounded to 2 decimal places
  - Weekday sales per Store Total Sales Values and Volumes, using full dates (not weekday names):
    - For each `(Store, Dates)`, sum `Sales Volume` and `Sales Value`.
    - Compute:
      - `Weekday % of Store Sales Volumes` = (date volume sum / store `Total_Volume`), rounded to 2 decimal places
      - `Weekday % of Store Sales Value` = (date value sum / store `Total_Value`), rounded to 2 decimal places
- Replace Weekday with full date by using the `Dates` field as the day identifier in the weekday-based output.
- Output the two required files with exactly the specified fields.

## Output

- output_01.csv
  - 4 fields:
    - Store
    - Scent
    - Scent % of Store Sales Volumes
    - Scent % of Store Sales Values

- output_02.csv
  - 4 fields:
    - Store
    - Dates
    - Weekday % of Store Sales Volumes
    - Weekday % of Store Sales Value