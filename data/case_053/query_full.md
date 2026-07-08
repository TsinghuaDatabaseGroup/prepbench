## Context
Customer and employee records may be removed over time (e.g., for GDPR reasons), which makes it harder to report historical “how many employees were active at a point in time.” The goal is to reconstruct, for each reporting month, how many employees were still employed at the end of that month and to summarize salary metrics for those active employees.

## Requirements
- Input the data.
  - Use the “current employees” file and the “past employees” file as the sources of employee records.
  - Use the “reporting dates” file as the source of the reporting months to build the monthly scaffold.
- Create a full list of employees by combining current and past employees into a single employee list (do not deduplicate unless the inputs already guarantee uniqueness).
- Create an end/leave date for current employees who have not yet left:
  - Set their **Leave Date** to **1st March 2020**. This date is used only to support the monthly active-employee logic.
- Ensure the employee and reporting date fields are in usable types for date comparisons and arithmetic:
  - Parse **Join Date** and **Leave Date** as dates.
  - Convert **Salary** to a numeric amount by removing currency symbols/thousands separators as needed and casting to an integer amount.
- Create a scaffold of reporting months from the reporting dates input:
  - For each record in the reporting dates file, parse **Month** (formatted like abbreviated-month and year) into a **MonthStart** date.
  - Derive **MonthEnd** as the calendar month-end date corresponding to **MonthStart**.
- Join employees to the scaffold so that each employee can be evaluated against each reporting month:
  - Perform a cross join between the full employee list and the reporting months scaffold (i.e., every employee paired with every reporting month).
- Determine whether an employee is counted as “in employment” for a given reporting month using end-of-month status:
  - An employee is considered active for a month if:
    - **Join Date <= MonthEnd**, and
    - **Leave Date > MonthEnd** (strictly after month end).
  - This enforces the requirement that if an employee leaves in that month (i.e., on or before that month’s end), they are removed from reporting within the month of leaving.
- Form the measures for analysis at the monthly grain (one output row per reporting month that has at least one active employee under the above rules):
  - **Current Employees**: count of active employees in that month.
  - **Total Monthly Salary**: sum of **Salary** across active employees in that month.
  - **Avg Salary per Current Employee**: `Total Monthly Salary / Current Employees`, rounded to 9 decimal places.
- Format the month label for output:
  - Output **Month** as a date string in `M/D/YYYY` style (month/day without leading zeros).
  - The date should represent the first day of the reporting month (i.e., output the **MonthStart** date that was derived from parsing the input **Month** field).
- Output the data:
  - Provide the required CSV with the specified fields and names.
  - Order rows chronologically by month.

## Output

- output_01.csv
  - 4 fields:
    - Total Monthly Salary
    - Month
    - Current Employees
    - Avg Salary per Current Employee