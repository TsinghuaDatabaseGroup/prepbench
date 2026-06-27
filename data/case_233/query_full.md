## Context
You are working with two HR datasets for a network of distribution centers: (1) an employee “dimension” table containing employee attributes (name, DOB, etc.) and (2) a monthly snapshot table indicating which employees worked at each distribution center at each month end. These tables are intended to be joinable, but either `employee_id` or `guid` can be missing in a given record. Each record is expected to have at least one of these identifiers present.

The task is to populate missing `employee_id` and `guid` values in both tables using the identifier relationships that appear in either table, so that both identifiers are non-null in both outputs.

## Requirements
- Input the data.
  - Use `input_01.csv` as the employee table and `input_02.csv` as the monthly snapshot table.
  - Read fields without coercing identifier/date formats (treat values as text so original formatting is preserved).

- Create a lookup table of valid identifier mappings:
  - From each input table, select only the two columns `employee_id` and `guid`.
  - Union (append) the pairs from both tables into one combined list.
  - Remove duplicate pairs based on the full (`employee_id`, `guid`) combination.
  - Keep only rows where **both** `employee_id` and `guid` are present (exclude any pair where either side is missing).  
    - Note: rows where both identifiers are missing should not contribute to the mapping.

- Fill missing IDs in the employee table (apply the same two-step process described below to the full employee table, keeping all original rows):
  1. Fill missing `guid` using `employee_id`:
     - Left join the employee table to the lookup table on `employee_id` (retain every row from the employee table, whether matched or not).
     - If the employee table’s `guid` is missing, replace it with the lookup table’s `guid` from the join; otherwise keep the original `guid`.
     - Remove any temporary/join helper columns created for this step.
  2. Fill missing `employee_id` using `guid`:
     - Left join the result to the lookup table on `guid` (retain every row from the employee table, whether matched or not).
     - If the employee table’s `employee_id` is missing, replace it with the lookup table’s `employee_id` from the join; otherwise keep the original `employee_id`.
     - Remove any temporary/join helper columns created for this step.

- Fill missing IDs in the monthly snapshot table:
  - Repeat the same two-step filling process as above (first fill `guid` from `employee_id`, then fill `employee_id` from `guid`), using left joins and only replacing values when the target field is missing.
  - Preserve the original row set and all non-ID fields from the monthly snapshot table.

- Ensure completeness:
  - After filling, ensure there are **no nulls** in `employee_id` and `guid` in both resulting tables.

- Output the data:
  - Produce the two output files with the exact columns and ordering specified below.

## Output

- output_01.csv
  - 10 fields:
    - employee_id
    - guid
    - first_name
    - last_name
    - date_of_birth
    - nationality
    - gender
    - email
    - hire_date
    - leave_date

- output_02.csv
  - 6 fields:
    - employee_id
    - guid
    - dc_nbr
    - month_end_date
    - hire_date
    - leave_date