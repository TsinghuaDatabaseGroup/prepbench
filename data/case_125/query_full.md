## Context
Create rolling weekly revenue totals and averages for Prep Air. The rolling week is defined as a 7-row window centered on each date: the date itself plus the three preceding dates and three following dates (where available). Produce results both per destination and as an overall “All destinations” view, then combine them into a single output.

## Requirements
- Input the data from `input_01.csv`.
- Treat `Date` as a calendar date parsed using day-first format (DD/MM/YYYY).
- Compute a 7-row, center-aligned rolling window (3 rows before + current row + 3 rows after) with `min_periods = 1`, so rows near the start/end that do not have 7 available rows still remain included.
- Per-destination rolling metrics:
  - For each `Destination`, sort records by `Date` ascending.
  - For each row (a specific destination on a specific date), compute:
    - **Rolling Week Total** = rolling sum of `Revenue` over the 7-row centered window within that destination.
    - **Rolling Week Avg** = rolling mean of `Revenue` over the same window.
  - This produces up to 7 contributing rows per date within each destination when 7 rows exist; if fewer rows exist around a date (e.g., at the beginning), compute using the available rows only.
- Overall (“All”) rolling metrics:
  - First aggregate across all destinations by `Date` to produce, for each date:
    - `Daily Total` = sum of `Revenue` across all records on that date.
    - `Daily Count` = number of records on that date.
  - Sort dates ascending, then compute a 7-row, center-aligned rolling window across dates:
    - `Rolling Total Sum` = rolling sum of `Daily Total`.
    - `Rolling Count Sum` = rolling sum of `Daily Count`.
    - **Rolling Week Total** (overall) = `Rolling Total Sum`.
    - **Rolling Week Avg** (overall) = `Rolling Total Sum / Rolling Count Sum` (i.e., the average revenue per record across the entire rolling window, not the average of daily totals).
  - Set `Destination` to exactly `All` for these rows.
- Pull the per-destination results and the overall (“All”) results together into a single dataset by appending (unioning) the rows; do not deduplicate.
- Remove any additional fields not required for the final output; keep only:
  - `Destination`, `Date`, `Rolling Week Avg`, `Rolling Week Total`.
- Apply final formatting:
  - Round `Rolling Week Avg` to 9 decimal places.
  - Round `Rolling Week Total` to a whole number and output it as an integer.
  - Format `Date` as a text string in `DD/MM/YYYY`.
- Output the data.

## Output

- output_01.csv
  - 4 fields:
    - Destination
    - Date
    - Rolling Week Avg
    - Rolling Week Total