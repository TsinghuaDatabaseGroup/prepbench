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

- Input the data
- Make sure there is a row for every employee and month:
  - We realized that our dataset only includes employees who recorded working hours for each month
  - For example, if an employee only works during the summer (June-August), we wouldn't have a record for them in September-May. However, we still need to count them as part of the staff for September-May
  - For each employee and DC, create one row for each month between their hire_date and their leave_date. If the leave_date is null, use 2023-06-30
  - Be careful of employees who may have left in the past and returned with a new hire_date
  - Be aware that employees may transfer between DCs. When that happens, they'll get a new hire/leave date
- For each DC and month, calculate:
  - The number of unique employee_ids present at the end of the month (the leave_date is null, or the leave_date is on or after the last day of the month). Name this ee_count
  - The number of employees who left during the month (the leave_date is within the month). Name this ee_leaving
- For each DC and month, find:
  - The ee_count last month. Name this ee_count_pm
  - For example, for April 2023, this would be the ee_count for March 2023
  - The ee_count 12 months ago. Name this ee_count_p12.
  - For example, for April 2023, this would be the ee_count for April 2022.
  - The average number of employees this month
  - avg_ee_month = (ee_count_pm + ee_count) / 2. Round to 6 decimal places
  - The average number of employees over the past 12 months
  - avg_ee_p12 = (ee_count_p12 + ee_count) / 2. Round to 6 decimal places
  - The sum of ee_leaving for the past 12 months, ee_leaving_p12
  - For example, for Apr 2023, this would be the sum of ee_leaving for May 2022 to Apr 2023
- Calculate the monthly and p12 turnover. Round both to 2 decimal places.
  - Monthly turnover, turnover_month = ee_leaving / avg_ee_month * 100
  - Prior 12 month turnover, turnover_p12 = ee_leaving_p12 / avg_ee_p12 * 100
- Remove the ee_count_pm and ee_count_p12 columns
- Output the data

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
