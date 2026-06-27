## Context

The Sales Team at AllChains record monthly bike sales in trackers where each salesperson’s name is placed on a “footer” row at the end of their monthly block, rather than repeated on each transaction row. The October tracker also contains each salesperson’s year-to-date (YTD) starting total in these footer rows. The goal is to standardize October and November into one tidy dataset with salesperson names filled on every row, bike types reshaped into a single column, and a YTD total populated for both months using October’s YTD information.

## Requirements

- Input the data from the two monthly tracker files (October and November).
- Identify the salesperson “footer” rows within each monthly tracker as the rows where:
  - `Date` is blank/missing, and
  - `Salesperson` is present.
- Fill in the `Salesperson` name for every non-footer transaction row within each monthly tracker by propagating the footer-row name upward to all rows in that block (so every transaction row is assigned the correct salesperson).
- Remove the footer rows from the transactional dataset after using them for salesperson assignment (they should not appear as output rows).
- From the October tracker only, extract each salesperson’s initial YTD value from their footer row:
  - For each footer row, take the numeric YTD value found in the non-key columns (i.e., not `RowID`, `Date`, or `Salesperson`).
  - Build a per-salesperson mapping `Initial YTD` from these October footer rows.
- For both October and November transaction rows:
  - Keep the bike sales columns for exactly three bike types: `Road`, `Gravel`, and `Mountain`.
  - Parse `Date` as a calendar date using day/month/year (`%d/%m/%Y`).
  - Treat bike-type sales as integers.
- Combine (append) the October and November transaction rows into a single dataset.
- Reshape the combined dataset from wide to long so that:
  - `Bike Type` is a single column containing one of `Road`, `Gravel`, or `Mountain`,
  - `Sales` is the corresponding value for that bike type,
  - The output grain is **one row per Salesperson × Date × Bike Type** across both months.
- Join the October-derived `Initial YTD` onto all long-format rows using a left join on `Salesperson`. If a salesperson has no matched `Initial YTD`, treat their initial YTD as 0.
- Create `YTD Total` as follows:
  - For rows in October (month = 10): `YTD Total = Initial YTD` (constant per salesperson across October rows).
  - For rows in November (month = 11): first compute `NovSum` = total November `Sales` summed across all November rows for each `Salesperson` (summing across all dates and bike types), then set `YTD Total = Initial YTD + NovSum`. This November `YTD Total` must be the same value on every November row for that salesperson.
- Format `Date` in the output as `dd/mm/YYYY`.
- Ensure the final output is ordered deterministically by:
  1) `Salesperson` ascending,
  2) `Date` ascending,
  3) `Bike Type` in the explicit order: `Gravel`, then `Road`, then `Mountain`.
- Output the data.

## Output

- output_01.csv
  - 5 fields:
    - Salesperson
    - Date
    - Bike Type
    - Sales
    - YTD Total