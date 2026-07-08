## Context

Chin & Beard Suds Co’s management team suspects pay and bonus issues in some Northern stores and wants supporting datasets to investigate two themes: (1) whether any employees are being paid outside the agreed corporate pay ranges and/or are in an incorrect pay band relative to their role, and (2) whether bonuses are a small share of salary. The analysis must respect contractual conditions for bonus eligibility and should be performed as of 1 October 2019.

## Requirements

- Input the data.
- Use all provided inputs:
  - Two staff files (treated as separate store extracts) and combined into a single staff list:
    - `input_01.csv`, assign `Store = "Sheffield Store"` for all rows.
    - `input_02.csv`, assign `Store = "Leeds Store"` for all rows.
  - One pay-range file: `input_03.csv`.
  - One store sales / target file: `input_04.csv`.
- Parse and type required fields:
  - Treat `Start Date` and `End Date` as dates (with `End Date` allowed to be blank/null for active employees).
  - Treat `Salary` as numeric.
- Limit the staff population to employees who were employed at any time during calendar year 2019 (i.e., their employment period overlaps 2019):
  - Keep a staff row if `Start Date` is on or before 2019-12-31 AND (`End Date` is null OR `End Date` is on or after 2019-01-01).
- Interpret pay ranges from `input_03.csv`:
  - Split the `Range` field into numeric `Salary Range Minimum` and `Salary Range Maximum` (inclusive bounds). Remove any currency symbols (e.g., £) and commas before parsing.
  - Treat `Bonus amount` and `% above target for bonus` as numeric fields (the percent field is retained for outputs but is not used to calculate any bonus amounts). Remove any currency symbols and commas from `Bonus amount` before parsing.
  - For each employee, determine the single matching salary range index where `Salary` falls within `[Salary Range Minimum, Salary Range Maximum]` (inclusive). If no range matches, treat the employee as “outside the pay bands”.
- Determine store-level quarterly target attainment from `input_04.csv`:
  - The columns with date-time headers (e.g., `2019-01-01 00:00:00`, `2019-02-01 00:00:00`) represent monthly sales data for the corresponding month. Extract the month from each date-time column header to identify which month the column represents.
  - For each store, compute whether quarterly sales meet or exceed `Quarterly Target` for each quarter:
    - Q1 uses the sum of the three monthly columns for Jan–Mar 2019: columns with headers `2019-01-01 00:00:00` (January), `2019-02-01 00:00:00` (February), and `2019-03-01 00:00:00` (March).
    - Q2 uses Apr–Jun 2019: columns with headers `2019-04-01 00:00:00` (April), `2019-05-01 00:00:00` (May), and `2019-06-01 00:00:00` (June).
    - Q3 uses Jul–Sep 2019: columns with headers `2019-07-01 00:00:00` (July), `2019-08-01 00:00:00` (August), and `2019-09-01 00:00:00` (September).
  - Align store naming to staff by appending `" Store"` to the store name in the sales file before matching to staff `Store`.
- Apply contractual bonus eligibility rules (as-of date is 1 October 2019, so only Q1–Q3 are considered):
  - A bonus for a given quarter is earned only if both conditions are true:
    1) The employee is still employed on the 1st day of the final month of that quarter:
       - Q1 check date: 2019-03-01
       - Q2 check date: 2019-06-01
       - Q3 check date: 2019-09-01
       (Employee is employed on that date if `Start Date` is on/before the check date AND (`End Date` is null OR `End Date` is on/after the check date).)
    2) The employee’s store met its sales target for that quarter.
  - For each employee, count the number of eligible quarters among Q1–Q3 (`eligible_count` in {0,1,2,3}).
  - Compute annual 2019 bonus actually due as:
    - `Bonus amount` (output) = (bonus-per-quarter from the matched salary range; if no matched range then 0) × `eligible_count`.
  - Compute bonus as a percentage of salary as:
    - `% Bonus of Salary` = round( (`Bonus amount` / `Salary`) × 100, 9 decimal places ).
    - If the employee’s salary does not fall within any salary range, `% Bonus of Salary` must be null/blank.
  - Employees paid outside the salary ranges must receive no bonus under this logic (bonus amount becomes 0 because there is no matching range).
- Build two outputs:
  1) A per-employee bonus summary for all included staff (both stores) after the 2019 employment filter.
  2) An outlier file focused on the Leeds store only, containing:
     - Employees whose salary is outside all pay bands (“Incorrect Pay”).
     - Employees whose salary falls within a pay band, but whose stated `Role` disagrees with an “assumed position” derived from the matched salary range:
       - If `Salary Range Minimum` ≥ 40,000 → assumed position `"Area Manager"`.
       - Else if `Salary Range Minimum` ≥ 30,000 → assumed position `"Manager"`.
       - Else → assumed position `"Team Member"`.
     - For both outlier categories, set `Correct Salary for Role?` to `False` and set `End Date` to the assumed “today” date of 01/10/2019 (formatted as `dd/mm/YYYY`).
     - For employees outside all ranges, leave the salary-range and bonus-range fields blank/null as specified in the output schema; set `Assumed Position based on Salary Range` to `"Team Member"` and `Pay Status` to `"Incorrect Pay"`.
     - For role-mismatch outliers (in-range), populate salary-range and bonus-range fields from the matched range; set `Pay Status` to `"Assumed Correct Pay"`.
     - Format `Start Date` and the output `End Date` as `dd/mm/YYYY` in this outlier output.
- Output the data.

## Output

- output_01.csv
  - 5 fields:
    - % Bonus of Salary
    - Bonus amount
    - Store
    - Name
    - Total Salary

- output_02.csv
  - 14 fields:
    - Correct Salary for Role?
    - Assumed Position based on Salary Range
    - Pay Status
    - End Date
    - Salary Range Minimum
    - Salary Range Maximum
    - Bonus amount
    - Range
    - % above target for bonus
    - Role
    - Start Date
    - Salary
    - Store
    - Name