## Context
You are given quarterly sales and profit data for five consecutive years (2018–2022). The goal is to produce a yearly summary table that reports total Sales and total Profits for each year.

## Requirements
- Input the data.
  - Read all input files matching `input_*.csv`.
  - Each input file contains at least the fields `Sales` and `Profits`, with one row per quarter (or similar periodic breakdown) within that year.
  - Assign years to files based on filename sort order: the first file corresponds to 2018, the second to 2019, the third to 2020, the fourth to 2021, and the fifth to 2022.

- Union tables together.
  - For each input file, produce one aggregated record for its assigned year (see aggregation rules below), then append (union/concatenate) these yearly records into a single output table (do not deduplicate).

- Remove the units from the sales field to convert the data type to the whole number.
  - Convert each `Sales` value into an integer amount before aggregation:
    - Treat missing values as 0.
    - Remove thousands separators (commas) if present.
    - Support magnitude suffixes on the value:
      - If the value ends with `K`/`k`, multiply the numeric part by 1,000.
      - If the value ends with `M`/`m`, multiply the numeric part by 1,000,000.
      - Otherwise, use a multiplier of 1.
    - After applying the multiplier, round to the nearest whole number and cast to an integer.

- Repeat this process for the profits field.
  - Apply the same parsing and integer conversion logic to `Profits` as described for `Sales`.

- Aggregate sales and profits by year.
  - For each year/file, sum the parsed integer `Sales` values across all rows in that file to get yearly `Sales`.
  - For each year/file, sum the parsed integer `Profits` values across all rows in that file to get yearly `Profits`.
  - The output grain must be one row per year (five rows total, one for each year 2018–2022).

- Output the data.
  - Produce a single CSV with the required fields and field order.

## Output

- output_01.csv
  - 3 fields:
    - Year
    - Sales
    - Profits