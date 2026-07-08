## Context
Turnover is a commonly-used HR metric that measures employee churn, or how quickly employees move in and out of the organization.

Using the provided dataset, the HR manager has asked us to calculate the monthly and prior-12-month turnover for each DC and month.

There are many ways to calculate turnover, but for this exercise, we'll use:
[# employees leaving during the period] / [avg # employees during the period] * 100%
where [avg # employees] = ([# employees at the end of the prior period] + [# employees at the end of the current period]) / 2

Example:
Employees at the end of Dec 2022 = 90
Employees at the end of Jan 2023 = 110
Employees leaving during Jan 2023 = 5
Avg employees in Jan 2023 = (90 + 110) / 2 = 100
Turnover in Jan 2023 = 5 / 100 * 100% = 5%

However, before we can calculate the turnover, we need to fix a data quality issue.

## Requirements
- Input the data from `input_01.csv`. Treat `hire_date` and `leave_date` as dates (day-first).
- Standardize the employee-month coverage so there is a row for every employee stint and month:
  - The source data only includes months where employees recorded working hours, but turnover requires counting employees even in months where they worked zero hours.
  - Employees can have multiple employment stints (e.g., they leave and later return) and can transfer between DCs; each distinct stint must be treated separately.
  - Define a "stint" as a unique combination of:
    - `dc_nbr`
    - `employee_id`
    - the hire month (i.e., `hire_date` truncated to the first day of its calendar month)
  - For each stint, generate one row per calendar month-end date from the stint's `hire_date` month through the stint's end month (inclusive), where:
    - the stint end date is `leave_date` if present, otherwise use the placeholder date `2023-06-30`
    - the generated month identifier is the month-end date (e.g., 31-Jan, 28/29-Feb, etc.)
- For each generated stint-month row, compute two flags:
  - Active at month end: `leave_date` is null OR `leave_date` is on or after the month-end date.
  - Left in month: `leave_date` is not null AND `leave_date` occurs in the same calendar month as the month-end date.
- Aggregate to DC-month level (one output row per `dc_nbr` and `month_end_date`):
  - `ee_count`: sum of the “active at month end” flag across all stint-month rows in that DC and month.
  - `ee_leaving`: sum of the “left in month” flag across all stint-month rows in that DC and month.
- Ensure a continuous monthly timeline per DC:
  - For each `dc_nbr`, create a complete sequence of month-end dates from that DC’s earliest month-end date present in the aggregated results through its latest month-end date (inclusive).
  - Left-join the aggregated DC-month metrics to this timeline; for DC-months with no observed records, set `ee_count = 0` and `ee_leaving = 0`.
- For each DC, compute prior-period metrics in month order:
  - `ee_count_pm`: prior month’s `ee_count` (lag 1 within `dc_nbr`).
  - `ee_count_p12`: `ee_count` from 12 months prior (lag 12 within `dc_nbr`).
  - `avg_ee_month = (ee_count_pm + ee_count) / 2`, rounded to 6 decimal places using half-up rounding.
  - `avg_ee_p12 = (ee_count_p12 + ee_count) / 2`, rounded to 6 decimal places using half-up rounding.
  - `ee_leaving_p12`: rolling 12-month sum of `ee_leaving` within `dc_nbr` using a 12-month window that requires 12 months of history (i.e., it is null until a full 12 months are available).
- Calculate turnover metrics and rounding:
  - Monthly turnover: `turnover_month = ee_leaving / avg_ee_month * 100`
    - If `avg_ee_month` is null or equals 0, set `turnover_month` to null.
    - Otherwise, round to 2 decimal places using half-up rounding.
  - Prior 12 month turnover: `turnover_p12 = ee_leaving_p12 / avg_ee_p12 * 100`
    - If `avg_ee_p12` is null or equals 0, or if `ee_leaving_p12` is null, set `turnover_p12` to null.
    - Otherwise, round to 2 decimal places using half-up rounding.
- Remove the intermediate lag columns `ee_count_pm` and `ee_count_p12` from the final output.
- Output formatting:
  - Format `month_end_date` as `DD/MM/YYYY`.
- Output the data.

## Output

- output_01.csv
  - 9 fields:
    - dc_nbr
    - month_end_date
    - ee_count
    - ee_leaving
    - ee_leaving_p12
    - avg_ee_month
    - avg_ee_p12
    - turnover_month
    - turnover_p12