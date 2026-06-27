## Context
- The input data is a single spreadsheet containing three sheets: salaries, tenure, and amount paid.
- All managers have received paychecks up to 5th June 2024 (present date).

## Requirements
- Input the data
- Clean the manager names in the Salaries and Tenures sheets so they match
- Bring together the Salaries and Tenures datasets
- Calculate the tenure (number of days) of each manager’s employment
  - Hint: For current employees, see what happens when you change the datatype of “End Date”
  - For the output, the End Date for current employees is set to 5th June 2024
- Using salary and tenure, calculate the Expected Total Salary of each manager (rounded to the nearest whole number)
- Join the data from the Amount Paid sheet
- Filter the output table to only include managers whose pay received does not match their expected pay
- Remove unnecessary fields
- Output the data

## Output

- output_01.csv
  - 4 fields:
    - Name
    - Salary
    - Expected Total Salary
    - Amount Paid
