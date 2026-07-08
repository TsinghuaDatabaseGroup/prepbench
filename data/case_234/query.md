## Context

Now that all of the missing IDs have been filled in, HR would like us to add several age groupings to the dataset for reporting, so the employee's exact date of birth can be removed from the dataset.

For this challenge, we will be using the Pew definitions for each generation.

## Requirements

- Input the data
- Add a new column, generation_name, which includes the generation name and the start/end years, example: "Generation X (1965-1980)"
  - If the generation doesn't have a start year, the text should be "(born in or before XXXX)"
  - If the generation doesn't have an end year, the text should be "(born in or after XXXX)"
- Calculate the employee's birth year from the date_of_birth
- Join the employee data and generation data to get the generation name for each employee
  - If the employee's birth date is missing, the generation_name should be "Not Provided"
- Join the monthly data to the employee data on employee_id.
- Calculate the employee's age (in full years) as of the month_end_date.
- Calculate the employee's age range, in 5-year increments, and name that column age_range:
  - Employees under 20 should be grouped into "Under 20 years"
  - Employees between 20 and 69 should be grouped into 5-year increments ("20-24 years", "25-29 years", etc.)
  - Employees 70 and over should be grouped into "70+ years"
  - If the employee's birth date is missing, the age_range should be "Not Provided"
- Output the data

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
