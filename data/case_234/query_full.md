## Context

HR wants additional age-related groupings added so reporting can be done without retaining employees’ exact dates of birth in the delivered datasets. Generation assignment must follow Pew generation definitions provided in a separate generation lookup.

## Requirements

- Input the data.
  - Use the employee dimension file (employees), the monthly employee activity file (monthly), and the generation definitions file (generations).

- Prepare generation labels (Pew definitions).
  - From the generations input, create a new column `generation_name` that concatenates the generation name and its applicable birth-year bounds:
    - If both `start_year` and `end_year` are present: `"{generation} ({start_year}-{end_year})"` (e.g., `"Generation X (1965-1980)"`).
    - If `start_year` is missing and `end_year` is present: `"{generation} (born in or before {end_year})"`.
    - If `end_year` is missing and `start_year` is present: `"{generation} (born in or after {start_year})"`.

- Derive each employee’s birth year.
  - Parse `date_of_birth` into a date and compute `birth_year` as the year component of that parsed date.

- Assign each employee a generation.
  - For each employee, find the generation row where:
    - (`start_year` is missing OR `start_year` ≤ `birth_year`) AND
    - (`end_year` is missing OR `end_year` ≥ `birth_year`)
    - Bounds are inclusive.
  - Use the `generation_name` from the matching generation row.
  - If an employee’s birth date is missing (or cannot be parsed into a valid date), set `generation_name` to **`"Not Provided"`**.
  - If no generation definition matches a non-missing `birth_year`, also set `generation_name` to **`"Not Provided"`**.
  - If multiple generation rows match, select the first matching row in the generation definitions’ existing order.

- Build the employee output dataset (for HR reporting without date of birth).
  - Output one row per employee, retaining the original employee fields required in `output_01.csv` and replacing the date of birth with `generation_name` (do not include `date_of_birth` or `birth_year` in the output).
  - Sort the final `output_01.csv` rows by `employee_id` ascending (stable sort).

- Join monthly data to employee attributes and compute age bands.
  - Join the monthly data to the employee data using a left join on **both** `employee_id` and `guid`, keeping all monthly rows even if no employee match exists.
  - Parse `month_end_date` into a date.
  - Compute the employee’s age in full years as of `month_end_date`:
    - `age_years = month_end_date.year - date_of_birth.year`, minus 1 if the month/day of `month_end_date` occurs before the month/day of the birthday in that year.
    - If either `date_of_birth` or `month_end_date` is missing or cannot be parsed, `age_years` is considered missing.
  - Compute `age_range` in 5-year increments:
    - If `age_years` is missing: **`"Not Provided"`**.
    - If `age_years` < 20: `"Under 20 years"`.
    - If `age_years` is between 20 and 69 inclusive: bucket into 5-year ranges with labels `"20-24 years"`, `"25-29 years"`, etc., where:
      - `bucket_start = floor(age_years / 5) * 5`, but not less than 20
      - `bucket_end = bucket_start + 4`
      - `age_range = "{bucket_start}-{bucket_end} years"`
    - If `age_years` ≥ 70: `"70+ years"`.

- Build the monthly age-bucket output dataset.
  - Output one row per monthly input row, augmented with `age_range` and the specified employee fields brought through the join.
  - Sort the final `output_02.csv` rows by `employee_id`, then `month_end_date`, then `dc_nbr`, all ascending (stable sort).

- Output the data.

## Output

- output_01.csv
  - 10 fields:
    - employee_id
    - guid
    - first_name
    - last_name
    - generation_name
    - nationality
    - gender
    - email
    - hire_date
    - leave_date

- output_02.csv
  - 7 fields:
    - employee_id
    - age_range
    - guid
    - dc_nbr
    - month_end_date
    - hire_date
    - leave_date