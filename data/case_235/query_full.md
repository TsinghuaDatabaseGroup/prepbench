## Context

HR needs to add generation and age groupings to employee data for reporting, so that exact birth dates can be removed. Generation classifications follow Pew Research definitions.

## Requirements

- Input employee data from `input_01.csv`, monthly data from `input_02.csv`, and generation definitions from `input_03.csv`.
- Build `generation_name` from the generations table:
  - Format: "{generation} ({start_year}-{end_year})" when both years exist.
  - Format: "{generation} (born in or before {end_year})" when only end_year exists.
  - Format: "{generation} (born in or after {start_year})" when only start_year exists.
- Parse `date_of_birth` from employee data using format `DD/MM/YYYY`.
- Extract `birth_year` from the parsed date.
- Join employees to generations where `start_year <= birth_year <= end_year` (treating null bounds as unbounded). Take the first match if multiple.
- If `date_of_birth` is missing, set `generation_name` to "Not Provided".
- Output 1 (`output_01.csv`): Employee data with generation names. Columns: `employee_id`, `guid`, `first_name`, `last_name`, `generation_name`, `nationality`, `gender`, `email`, `hire_date`, `leave_date`.
- Join monthly data to employee data on (`employee_id`, `guid`).
- Calculate employee age in full years as of `month_end_date`:
  - Age = years difference, minus 1 if the birthday has not occurred yet in that year.
- Calculate `age_range` in 5-year increments:
  - Under 20: "Under 20 years"
  - 20-69: "{start}-{end} years" where start = floor(age/5)*5, end = start+4, with floor clamped at 20.
  - 70+: "70+ years"
  - Missing birth date: "Not Provided"
- Output 2 (`output_02.csv`): Columns: `employee_id`, `age_range`, `guid`, `dc_nbr`, `month_end_date`, `hire_date`, `leave_date`.

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
