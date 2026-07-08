## Context
You are given manager payroll information split across three tabular inputs corresponding to three spreadsheet sheets: **Salaries**, **Tenure**, and **Amount Paid**. The objective is to identify **current managers** whose total pay received to date does not match what would be expected based on their salary and length of employment, assuming pay is calculated through **5th June 2024 (the present date)**.

## Requirements
- Input the data from the three sources:
  - Salaries (contains each manager’s salary)
  - Tenure (contains each manager’s start and end date information)
  - Amount Paid (contains each manager’s total pay received)
- Standardize manager names so the Name field matches across all three inputs (apply the same name-cleaning approach to each dataset before joining).
- Prepare tenure information:
  - Create an **Is Current** indicator that is true when the tenure record’s **End Date** is marked as “current” (case-insensitive comparison after basic whitespace handling).
  - Convert **Start Date** and **End Date** to date types.
  - For **current** managers, set the **End Date** used for calculations and output purposes to **5th June 2024**.
  - Compute **Tenure** as the number of days between End Date and Start Date:
    - `Tenure (days) = End Date − Start Date`, measured in whole days.
- Bring together the Salaries and Tenure datasets:
  - Join Tenure to Salaries on **Name** using an **inner join**.
  - Assume the relationship is one-to-one by Name (each Name appears at most once in each of these inputs).
- Using salary and tenure, calculate **Expected Total Salary** for each manager:
  - `Expected Total Salary = round( (Tenure / 365) * Salary )`
  - Round to the nearest whole number using half-to-even behavior (i.e., values exactly halfway between integers round to the nearest even integer), and store the result as an integer.
- Join the Amount Paid data:
  - Join the combined tenure/salary data to Amount Paid on **Name** using an **inner join**.
  - Assume the relationship is one-to-one by Name.
- Filter to the final exception list:
  - Keep only managers who are **current** (`Is Current` is true), and
  - whose **Amount Paid** does **not** equal their **Expected Total Salary**.
- Remove unnecessary fields so the output contains only the required columns.
- Output the data.

## Output

- output_01.csv
  - 4 fields:
    - Name
    - Salary
    - Expected Total Salary
    - Amount Paid