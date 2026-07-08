## Context
Allchains Bike Stores have been fundraising in one of their stores by offering customers the option to donate to charity when buying a new bike. Donations have only been totalled at sporadic points throughout each month, so the data represents cumulative totals recorded on some dates rather than a complete daily series. The goal is to estimate how much is being raised per day across the full fundraising period and determine whether customers are more generous on particular weekdays.

This task uses Tableau Prep Builder’s **New Rows** capability (released in Prep Builder **version 2021.3**). Use that version or later (unless you plan to scaffold missing dates yourself).

## Requirements
- Input the data from `input_01.csv` and use the fields:
  - `Date` (provided as day/month/year)
  - `Total Raised to date` (cumulative total recorded on that date)
- Convert `Date` to a true date using the day/month/year interpretation, then identify the **earliest** and **latest** dates present.
- Create new rows for **every missing calendar date** between the earliest and latest dates (inclusive), so the dataset has one row per day over the full continuous date range.
- For each date in the completed daily series, populate `Total Raised to date` as the **most recently recorded cumulative total on or before that day**:
  - If a day exists in the original input, use its recorded `Total Raised to date`.
  - If a day was newly created (or has no recorded total), carry forward the latest prior known total.
  - If there is no prior known total (i.e., before the first recorded total), use `0`.
- Calculate `Days into fund raising` for each row as the number of days since the earliest date in the dataset:
  - `Days into fund raising = Date - start_date` measured in whole days.
  - The first day (start date) must be `0` (e.g., “1st Jan would be 0”).
- Calculate `Value raised per day` for each row as:
  - `Value raised per day = Total Raised to date / Days into fund raising`
  - For `Days into fund raising = 0`, `Value raised per day` must be blank/null (not zero).
- Work out the weekday for each date using the weekday name (e.g., Monday, Tuesday, etc.).
- Compute `Avg raised per weekday` as the average of `Value raised per day` for each weekday, excluding null values (so the day with `Days into fund raising = 0` does not contribute).
- Prepare the final output with these additional rules:
  - The output should contain one row per calendar date in the continuous date range, but the `Date` field in the output must contain the **weekday name** (not the actual calendar date).
  - Sort the output first by weekday in this fixed order:
    1) Wednesday, 2) Tuesday, 3) Sunday, 4) Saturday, 5) Monday, 6) Thursday, 7) Friday
  - Within each weekday group, sort rows by `Days into fund raising` in **descending** order.
  - Round `Avg raised per weekday` and `Value raised per day` to **9 decimal places**.
  - Ensure `Days into fund raising` and `Total Raised to date` are integers in the output.
- Output the data.

## Output

- output_01.csv
  - 5 fields:
    - Avg raised per weekday
    - Value raised per day
    - Days into fund raising
    - Date
    - Total Raised to date