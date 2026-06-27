## Context

Allchains tracks each employee’s monthly sales in one worksheet and their monthly sales targets in another. The goal is to combine these sources to identify employees whose average performance is materially below target, and to report both their average monthly sales and how often they meet or exceed the target across the available months.

## Requirements

- Input the data from:
  - `input_01.csv`: monthly sales by employee, with identifier columns `Store` and `Employee` plus one column per month of sales values.
  - `input_02.csv`: monthly targets by employee, including `Store`, `Employee`, and `Monthly Target`.

- Reshape the sales data to a monthly (long) form so each record represents one employee’s sales for one month (keeping `Store` and `Employee` as identifiers and treating every other column in `input_01.csv` as a month).

- Calculate **Average Monthly Sales** for each `(Store, Employee)` as the mean of that employee’s monthly sales values across all available month columns in `input_01.csv`.
  - Round the resulting average to the nearest whole number and store it as an integer in `Avg monthly Sales`.

- Clean the `Store` field in the Targets data so it matches the store naming used in the Sales data:
  - Define the valid store names as the distinct `Store` values present in `input_01.csv`.
  - For each `Store` value in `input_02.csv`, if it is not an exact match to a valid store name, map it deterministically to the single “closest” valid store name based on minimum string edit distance; if there is a tie, choose the tied store name that is alphabetically first.

- Join targets onto the per-employee average sales metrics using a left join on `(Store, Employee)` after store-name cleaning, bringing in `Monthly Target`.
  - For any `(Store, Employee)` without a matching target, treat `Monthly Target` as missing.

- For employees with an available `Monthly Target`, compute **% of months target met**:
  - Using the long-form monthly sales data joined to targets on `(Store, Employee)`, consider only months where `Monthly Target` is present.
  - A month is counted as “target met” when `Sales >= Monthly Target`.
  - For each `(Store, Employee)`, compute:  
    `% of months target met = round(100 * (months_met / months_total))`  
    where `months_met` is the count of months meeting/exceeding target and `months_total` is the count of months with a non-missing target.
  - Round this percentage to the nearest whole number and store it as an integer.

- Filter the final employee list so that only employees who are **below 90% of their target on average** remain:
  - Keep only rows where `Monthly Target` is present, and where:  
    `Avg monthly Sales < 0.9 * Monthly Target`.

- Output one row per remaining `(Store, Employee)` with the required fields, and sort the output by `Store` ascending then `Employee` ascending (stable ordering).

- Output the data.

## Output

- output_01.csv
  - 5 fields:
    - Store
    - Employee
    - Avg monthly Sales
    - % of months target met
    - Monthly Target