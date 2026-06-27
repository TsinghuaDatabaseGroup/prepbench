## Context
SuperBytes pays manager salaries on a weekly schedule. Each manager has a fixed annual salary for the duration of their employment period, and that salary may change only when a manager is replaced. SuperBytes needs (1) the total manager-salary cost per week since founding and (2) the share of annual company expenses attributable to manager salaries.

## Requirements
- Input the data from:
  - `input_01.csv` (manager employment and salary history), using the fields **Start Date**, **End Date**, and **Salary**.
  - `input_02.csv` (annual company expenses), using the fields **Year** and **Expenses**.
- Treat any manager record whose **End Date** indicates the employee is current as ending on **12th June 2024**.
- Convert each manager’s annual **Salary** to a weekly amount using **52 weeks per year**:
  - `weekly_salary = annual_salary / 52`
- For each manager record, create a row for every week the manager receives their salary, using these rules to define the weekly payment dates:
  - Parse **Start Date** and **End Date** as calendar dates.
  - **Week definition**: A week runs from Sunday to Saturday (Sunday is the first day of the week).
  - Align the start date forward to the next Sunday (or keep it if it is already a Sunday).
  - Align the end date backward to the most recent Sunday (or keep it if it is already a Sunday).
  - Generate one row per week date at a 7-day frequency from aligned start through aligned end, inclusive. If the aligned start date and aligned end date are the same (both are the same Sunday), generate exactly one row for that week.
  - Exclude manager records from expansion if start date, end date, or salary is missing/invalid, or if the aligned end date is earlier than the aligned start date.
- For the first output (weekly totals):
  - Group the expanded weekly rows by **Week** (the weekly payment date) and sum weekly salary across all managers to compute **Salary Payments** for that week.
  - Round **Salary Payments** to **2 decimal places**.
  - Output **Week** formatted as `DD/MM/YYYY`.
- For the second output (annual percentage of expenses):
  - Assign each expanded weekly row to a calendar **Year** based on the year of its **Week** date.
  - Sum weekly salary by **Year** to compute total manager salary payments per year, and round this annual total to **2 decimal places** before calculating the percentage.
  - Join annual manager-salary totals to `input_02.csv` annual expenses using an **inner join on Year** (keep only years present in both datasets).
  - Compute **% Spent on Manager Salaries** as:
    - `(annual_manager_salaries / annual_expenses) * 100`
    - Round to **1 decimal place**.
- Output the data:
  - Weekly output sorted by Week ascending.
  - Annual output sorted by Year ascending.

## Output

- output_01.csv
  - 2 fields:
    - Week
    - Salary Payments

- output_02.csv
  - 2 fields:
    - Year
    - % Spent on Manager Salaries