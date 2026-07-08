## Context

Many organizations maintain a centralized “reporting calendar” that maps each calendar date to the organization’s internal reporting structure. This task is to generate such a reporting-date table for a user-selected calendar year, using the following business rules:

- The reporting year begins on the Monday strictly before February 1st.
- Each reporting month contains exactly 4 reporting weeks.

The resulting table should allow any calendar date in the selected year to be enriched with its corresponding reporting year, reporting month, reporting week, and reporting day number.

## Requirements

- Input the data.
  - Read `inputs/input_01.csv` and use the value in the `Year` field (first row) as the selected calendar year to generate the calendar.
- Create a way for the user to choose which calendar year they want to get the reporting dates for.
  - The selected calendar year is driven by the input `Year` value.
- Make sure to have a row for each date in the selected year.
  - Generate one row per calendar date from January 1 through December 31 of the selected year (inclusive).
  - Output grain: one row represents one calendar date in the selected calendar year.
- Create a field for the Reporting Year (based off the above logic).
  - Define the start of a reporting year `Y` as the Monday strictly before February 1 of calendar year `Y`.
    - If February 1 falls on a Monday, the start is the Monday one week earlier (i.e., 7 days before February 1).
  - For each calendar date `d` in the selected calendar year:
    - If `d` is on or after the reporting-year start date for the selected calendar year, set `Reporting Year = selected_year`.
    - Otherwise, set `Reporting Year = selected_year - 1`.
- Create a field for the Reporting Day.
  - For each calendar date `d`, compute the start date of its assigned `Reporting Year` (per the rule above).
  - Set `Reporting Day = (d - start_date_of_assigned_reporting_year) + 1`, where the difference is measured in whole days and Day 1 is the reporting-year start Monday.
- Create a field for the Reporting Week.
  - Set `Reporting Week = ceil(Reporting Day / 7)`.
- Create a field for the Reporting Month.
  - Each month contains exactly 4 weeks.
  - Set `Reporting Month = ceil(Reporting Week / 4)`.
- Output the data.
  - Format `Calendar Date` as `DD/MM/YYYY`.
  - Write the output to `output_01.csv` with the fields in the specified order.

## Output

- output_01.csv
  - 5 fields:
    - Calendar Date
    - Reporting Year
    - Reporting Month
    - Reporting Week
    - Reporting Day