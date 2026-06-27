## Context
The HR analyst used the available dataset to build a dashboard. The DC managers found it very useful, and they requested some new features.
First, we need to add the employee's tenure (how many months and years they have worked at that particular DC) to the dataset.
Second, the HR analyst would like to keep the reports consistent from DC to DC, so they requested an aggregated dataset that fills in zeroes if a DC does not have any employees in a specific demographic group each month. For example, DC #1 did not have any employees in the 60-64 years age group for the month of February 2019, so we need to add a row for that combination, with 0 employees.

## Requirements

- Input the data
- Using the monthly table, calculate each employee's tenure
  - For the tenure_months, we want to know the number of full months between the employee's hire_date and either the month_end_date or leave_date - whichever is soonest
  - For the tenure_years, we want to translate the tenure_months into full years
    - i.e. 32 month would be 2 years of tenure
- Output the updated monthly table with the two new tenure columns
- Join the ee_dim table to the monthly data on employee_id to get the employee attributes, gender, nationality, and generation
- Create a summary record for each DC/month/demographic:
  - For each DC, month, and generation name, count the number of employees
  - Name the employee count "ee_count"
  - Rename the generation_name column to "demographic_detail"
  - Add a new column, demographic_type, which will have the same string in every row, "Generation Name"
  - Repeat above steps for gender, nationality, age_range, and tenure_years
  - Union all of the demographic summaries into one dataset
- Expand this new dataset so there is a row for every combination of DC/month_end_date, and demographic_type/demographic_detail
  - Only include the relevant months for each DC (for example, DC 6 did not open until November 2019, so don't include records earlier than that for DC 6.
  - Only include relevant details for each demographic. For example, you shouldn't have any records where the demographic_type is "Tenure" and the demographic_detail is a generation name.
- If there were no employees in a category for the month, fill the ee_count with zero
- Output the demographic summary
- Output the data

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
