## Context
Data Source Bank (DSB) must assign each new customer to a UK “reporting day” based on the next UK working day. UK reporting days exclude weekends and UK bank holidays. DSB also reports monthly totals on the last UK reporting day of each calendar month; customers whose (assigned) reporting date falls on that last reporting day are counted in the following reporting month. Republic of Ireland (ROI) data has already been processed using ROI working-day rules, but it must be aligned to the UK reporting schedule for DSB’s regulatory reporting. The final deliverable compares UK and ROI reporting-month assignments and flags misalignments.

## Requirements
- Input the data from:
  - `input_01.csv`: UK new customers, including at minimum `Date` and `New Customers`.
  - `input_02.csv`: ROI new customers already on an ROI reporting schedule, including at minimum `Reporting Date`, `Reporting Month`, `Reporting Day`, and `New Customers`.
  - `input_03.csv`: UK bank holidays, including at minimum `Year` and `Date`.

- Data cleaning and ambiguity resolution:
  - For `input_01.csv`:
    - Parse `Date` as a date in `YYYY-MM-DD` format.
    - Treat `New Customers` as integers (sum operations may produce integers).
  - For `input_02.csv`:
    - Parse `Reporting Date` and `Reporting Month` as dates in `YYYY-MM-DD` format.
    - Treat `New Customers` and `Reporting Day` as integers.
  - For `input_03.csv`:
    - Convert `Year` from float to integer (e.g., `2022.0` → `2022`). If `Year` is null or missing, skip the row (do not use it to build the holiday list).
    - Parse `Date` as a date in `YYYY-MM-DD` format. If `Date` is null or missing, skip the row (do not use it to build the holiday list).
    - Only process rows where both `Year` and `Date` are present and valid. Rows with missing `Year` or missing `Date` should be excluded from the UK bank-holiday list construction.

- Build a UK bank-holiday date list from `input_03.csv`:
  - Create a holiday date field `UK Bank Holiday` by combining:
    - the `Year`, and
    - the month-and-day component from `Date`.
  - Keep distinct `UK Bank Holiday` dates only.

- Prepare UK new-customer reporting dates (UK schedule):
  - Parse the UK `Date` as a date.
  - Join UK customers to the UK bank-holiday list on `Date = UK Bank Holiday` (left join).
  - Create a `Reporting Day` flag for each UK `Date`:
    - `N` if the date is a weekend (Saturday or Sunday),
    - `N` if the date is a UK bank holiday,
    - otherwise `Y`.
  - For every UK `Date`, assign a `Reporting Date` equal to the next UK reporting day on or after that `Date` (i.e., the smallest date ≥ `Date` where `Reporting Day = Y`).
    - Construct the reporting-day calendar across the full continuous date range from the minimum to the maximum UK `Date` so this “next reporting day” lookup is defined for every day in the range.

- Aggregate UK customers to the reporting-date grain:
  - Group by `Reporting Date` and sum `New Customers`.
  - Define `Month` as the calendar month start of `Reporting Date` (month truncation).
  - For each `Month`, compute `Last Day` as the maximum `Reporting Date` within that `Month`.
  - Compute `Reporting Month` for each `Reporting Date` using DSB’s rule:
    - If `Reporting Date` is strictly less than `Last Day` for its `Month`, then `Reporting Month = <full month name>-<4-digit year>` of `Reporting Date`.
    - If `Reporting Date` equals `Last Day` for its `Month`, then `Reporting Month = <full month name>-<4-digit year>` of (`Reporting Date` plus 1 month).
  - Filter out all rows where `Reporting Month` equals `January-2024`.
  - Compute `Reporting Day` (day index within the reporting month):
    - Within each `Reporting Month`, sort by `Reporting Date` ascending and assign sequential integers starting at 1.

- Align ROI data to the UK reporting schedule:
  - Parse ROI `Reporting Date` and ROI `Reporting Month` as dates.
  - Convert ROI `Reporting Month` (a month-start date) to a string formatted as `<month abbreviation>-<2-digit year>`, using the following month abbreviation mapping:
    - January → `Jan`
    - February → `Feb`
    - March → `Mar`
    - April → `Apr`
    - May → `May`
    - June → `Jun`
    - July → `Jul`
    - August → `Aug`
    - September → `Sept` (not `Sep`)
    - October → `Oct`
    - November → `Nov`
    - December → `Dec`
    - Extract the 2-digit year from the date (e.g., `2023-09-01` → `Sept-23`).
  - Rename ROI fields so outputs clearly distinguish ROI vs UK:
    - `New Customers` → `ROI New Customers`
    - `Reporting Month` → `ROI Reporting Month`
    - `Reporting Day` → `ROI Reporting Day`
  - Preserve the original ROI reporting date as `ROI Reporting Date`, then overwrite `Reporting Date` to be the next UK reporting day on or after `ROI Reporting Date` using the same “next reporting day” mapping derived from the UK calendar.
  - Aggregate ROI data to the (UK-aligned) reporting-date grain:
    - Group by the aligned `Reporting Date`.
    - Sum `ROI New Customers`.
    - For `ROI Reporting Month`, keep the first value in input order within each aligned `Reporting Date`.

- Combine UK and ROI on aligned `Reporting Date`:
  - Join the UK aggregated table and the ROI aggregated table on `Reporting Date` using a right join that preserves the full set of UK reporting dates after the January-2024 filter.
  - Replace null customer counts with 0 for both `New Customers` and `ROI New Customers`.
  - Remove rows where `Reporting Date` is 2023-12-29 or 2023-12-30.
  - Create `Misalignment Flag`:
    - Set to `X` if the first three characters of UK `Reporting Month` differ from the first three characters of `ROI Reporting Month`.
    - Otherwise set to an empty string.
  - Format `Reporting Date` as `DD/MM/YYYY` in the final output.
  - Sort the final output by `Reporting Date` ascending.

- Output the data.

## Output

- output_01.csv
  - 7 fields:
    - Misalignment Flag
    - Reporting Month
    - Reporting Day
    - Reporting Date
    - New Customers
    - ROI New Customers
    - ROI Reporting Month