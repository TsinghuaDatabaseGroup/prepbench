## Context
Chin & Beard Suds Co. wants to understand each dedicated sales employee’s tenure with the company and the total employment cost incurred for them, combining salary and performance bonus, summarized by each year they were employed.

## Requirements
- Input the data from `input_01.csv`.
- Interpret the `Date` field as a calendar date (day-first) and derive `Reporting Year` as the calendar year extracted from `Date`.
- Create an `Employment Range` field for each employee (`Name`) that captures their full tenure across all available records:
  - For each `Name`, find the minimum and maximum `Date`.
  - Format each as `MMM yyyy` and concatenate as `MMM yyyy to MMM yyyy`.
  - Attach this `Employment Range` back to each row for that `Name` (join on `Name`).
- Produce a yearly summary at the grain of **one row per employee per reporting year** (group by `Name`, `Reporting Year`, and `Employment Range`) and compute:
  - **Number of months they worked** in that reporting year as the count of records (rows) for that employee-year.
  - **Their salary they will have received** for that reporting year by:
    - Taking the employee’s annual salary value for that year (use the first value within the employee-year group).
    - Converting annual salary to a monthly amount by dividing by 12.
    - Multiplying by the number of months worked (row count) in that year.
  - **Their sales total for the year** as the sum of `Sales` within the employee-year.
- For each employee, calculate `Tenure by End of Reporting Year` as the cumulative sum of `months worked` across reporting years in ascending `Reporting Year` order.
- Determine the bonus payments the person will have received each year:
  - `Yearly Bonus` = 5% of that year’s sales total.
- Round `Salary Paid` and `Yearly Bonus` to two decimal places.
- Add `Salary Paid` and `Yearly Bonus` together to form `Total Paid`.
- Output the data.

## Output

- output_01.csv
  - 7 fields:
    - Name
    - Employment Range
    - Reporting Year
    - Tenure by End of Reporting Year
    - Salary Paid
    - Yearly Bonus
    - Total Paid