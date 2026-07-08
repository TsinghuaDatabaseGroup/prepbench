## Context
Chin & Beard Suds Co needs to restock stores and must plan around supplier delivery commitments that are defined by a weekday and a specific occurrence of that weekday within each month (e.g., the 1st Tuesday of the month). The goal is to combine a delivery-rule table with a calendar/date scaffold so future analysis can quantify how much stock is scheduled to arrive on each delivery date through the end of the year.

## Requirements
- Input the data
  - Load the **Date Scaffold** from `input_01.csv`, ensuring the `Date` field is parsed as a true date.
  - Load the **Delivery Schedule** rules from `input_02.csv`, which provides at least:
    - `Delivery Schedule` (text describing the nth weekday of the month),
    - `Product`, `Scent`, `Supplier`, `Quantity`.

- Date Scaffold: create date parts needed for joining
  - For each row in the date scaffold, derive:
    - **Weekday**: the weekday name of `Date` (e.g., Monday, Tuesday, etc.).
    - **Month Name**: the month name of `Date`.
    - **Week number** and **Month** components as needed to support the “week number within the month” logic (you may derive Year and numeric Month to compute within-month sequencing deterministically).
    - **Week number within the month** (nth occurrence of a weekday within that month): for each combination of (Year, Month, Weekday), assign `1` to the earliest date in that month with that weekday, `2` to the next, and so on.

- Delivery Schedule: extract join keys from the rule text
  - From each `Delivery Schedule` value, extract:
    - the **week number within the month** as an integer `n` (e.g., 1 from “1st …”),
    - the **weekday** name as written in the schedule.
  - Treat each rule row independently; preserve the original rule row order as a tie-breaker for final sorting when multiple rules map to the same date.

- Join the two datasets
  - Perform an **inner join** between:
    - the date scaffold enriched with (Weekday, week number within the month), and
    - the rules enriched with (weekday, n),
    - matching on: `DateScaffold.Weekday = Rules.weekday` AND `DateScaffold.(week number within the month) = Rules.n`.
  - If a rule has no matching dates in the scaffold, it produces no output rows.
  - If multiple rules match the same date, output one row per matching rule.

- Finalize and output
  - The output grain must be: **one row per (delivery date × delivery rule match)**.
  - Format `Date` as a string in **DD/MM/YYYY**.
  - Ensure `Quantity` is numeric.
  - Sort the final output by:
    1) `Date` ascending,
    2) original rule order ascending,
    3) `Product` ascending,
    4) `Scent` ascending.
  - Output the data.

## Output

- output_01.csv
  - 7 fields:
    - Month Name
    - Weekday
    - Date
    - Product
    - Scent
    - Supplier
    - Quantity