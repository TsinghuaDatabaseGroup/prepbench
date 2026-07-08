## Context
DC managers want the existing HR dashboard dataset enhanced in two ways: (1) add employee tenure at each distribution center (DC) to the monthly employee-level table, and (2) produce a DC/month demographic summary that is consistent across DCs by including explicit zero-count rows for demographic categories that have no employees in a given month.

## Requirements

- Input the data.
  - Read `input_02.csv` as the monthly employee-level table.
  - Read `input_01.csv` as the employee dimension table (`ee_dim`).

- Using the monthly table, calculate each employee’s tenure for that DC/month record and add it as two new columns.
  - Parse `month_end_date`, `hire_date`, and `leave_date` as dates using the `DD/MM/YYYY` format. Treat blank date strings as missing.
  - Define the tenure end date for each row as the earlier of:
    - `month_end_date`, and
    - `leave_date`
  - Compute `tenure_months` as the number of full months between `hire_date` (start) and the tenure end date (end), using this rule:
    - Start with the month difference: `(end_year - start_year) * 12 + (end_month - start_month)`.
    - If `end_day < start_day`, subtract 1 **unless** the end date is the last day of its month.
    - If required dates are missing such that tenure cannot be computed, set `tenure_months` to 0.
    - Ensure `tenure_months` is not negative (minimum 0).
  - Compute `tenure_years` as full years of tenure: `tenure_years = floor(tenure_months / 12)`.
  - Store `tenure_months` and `tenure_years` as integers.

- Output the updated monthly table with the two new tenure columns.
  - Preserve the original monthly-table row grain (one row per employee per DC per month record).
  - Format `month_end_date`, `hire_date`, and `leave_date` back to `DD/MM/YYYY` text; output blanks for missing dates.
  - The output `month_end_date` must match `DD/MM/YYYY` exactly (zero-padded).
  - Ensure `dc_nbr` is output as an integer.
  - Sort the output deterministically by: `dc_nbr`, `month_end_date`, `employee_id`, `guid`, `hire_date`, `leave_date`, `tenure_months`, `tenure_years`, `age_range`.

- Join the `ee_dim` table to the monthly data to get employee attributes needed for demographic reporting.
  - Join type: left join from the monthly table to `ee_dim`.
  - Join keys: `employee_id` and `guid`.
  - Bring in `nationality`, `gender`, and `generation_name` from `ee_dim` (while `age_range` comes from the monthly table, and `tenure_years` is the derived field).

- Create a summary record for each DC/month/demographic.
  - The output grain for the demographic summary is one row per `(dc_nbr, month_end_date, demographic_type, demographic_detail)`.
  - Build five separate summaries and then union them together:
    1) Generation Name summary
       - `demographic_type` = `"Generation Name"` for all rows in this summary.
       - `demographic_detail` = `generation_name` (as a string).
       - `ee_count` = count of monthly rows in each `(dc_nbr, month_end_date, demographic_detail)` group.
    2) Gender summary
       - `demographic_type` = `"Gender"`.
       - `demographic_detail` = `gender` (as a string).
       - `ee_count` = count of rows per group.
    3) Nationality summary
       - `demographic_type` = `"Nationality"`.
       - `demographic_detail` = `nationality` (as a string).
       - `ee_count` = count of rows per group.
    4) Age Range summary
       - `demographic_type` = `"Age Range"`.
       - `demographic_detail` = `age_range` (as a string, sourced from the monthly table).
       - `ee_count` = count of rows per group.
    5) Tenure summary
       - `demographic_type` = `"Tenure"`.
       - `demographic_detail` = `tenure_years` converted to a string.
       - `ee_count` = count of rows per group.
  - Union (append) these five summary tables into one dataset with columns: `dc_nbr`, `month_end_date`, `demographic_type`, `demographic_detail`, `ee_count`.

- Expand this new dataset so there is a row for every relevant combination of DC/month and demographic category, and fill missing counts with zero.
  - Determine the set of relevant `(dc_nbr, month_end_date)` combinations from the monthly table itself (i.e., include exactly the DC/month pairs that exist in the monthly input).
  - For each demographic type, determine the set of relevant `demographic_detail` values as the distinct non-missing values that appear for that demographic attribute in the enriched monthly data:
    - Generation Name: distinct non-missing `generation_name`
    - Gender: distinct non-missing `gender`
    - Nationality: distinct non-missing `nationality`
    - Age Range: distinct non-missing `age_range`
    - Tenure: distinct non-missing `tenure_years` values, expressed as strings
  - For each demographic type separately, create the Cartesian product of:
    - all relevant `(dc_nbr, month_end_date)` pairs, and
    - that type’s relevant `demographic_detail` values
    This enforces that you only produce relevant `demographic_detail` values for each `demographic_type` (e.g., Tenure rows only use tenure-year details, not generation names).
  - Union these per-type Cartesian-product tables to form the complete set of required output combinations.
  - Left join the actual summarized counts onto this complete set of combinations on `(dc_nbr, month_end_date, demographic_type, demographic_detail)`.
  - If there were no employees in a category for the month, fill `ee_count` with 0 and output it as an integer.
  - Sort the demographic summary deterministically by: `dc_nbr`, `month_end_date`, `demographic_type`, `demographic_detail`.

- Output the demographic summary.
- Output the data.

## Output

- output_01.csv
  - 9 fields:
    - dc_nbr
    - month_end_date
    - employee_id
    - guid
    - hire_date
    - leave_date
    - tenure_months
    - tenure_years
    - age_range
  - month_end_date must be formatted exactly as `DD/MM/YYYY`.

- output_02.csv
  - 5 fields:
    - dc_nbr
    - month_end_date
    - demographic_type
    - demographic_detail
    - ee_count
  - month_end_date must be formatted exactly as `DD/MM/YYYY`.
