## Context
After a successful HR Month at the end of 2022, Kelly has returned with more real-life challenges for us! Over the next few challenges, we'll be using fake employee data for a small network of distribution centers. The data is fake, but the challenges are based on real people analytics challenges.

In this challenge, we have two HR tables: one that contains the list of employees (with their name, DOB, etc.), and one that contains a monthly snapshot of which employees worked at each DC during the month.

We want to be able to join the two tables, but sometimes the employee_id is missing from one (or both!) of the tables. We do have a second ID (the guid), but sometimes that is missing as well! Fortunately, we have at least one of those IDs present for each record.

The goal for this challenge is to fill in the missing IDs in both tables, so they can be joined later.

Note: throughout this month, you'll see the abbreviations, "ee", which is short for employee, and "DC" which is short for distribution center

## Requirements

- Input the data
- Create a lookup table:
  - Find the unique employee_id / guid combinations in each table
  - Union the results together and remove any duplicates
  - Filter out any rows where one of the IDs is missing
- Join the main table with the lookup table on employee_id (make sure to keep all records from the original table, whether or not they match)
- If the guid is missing from the main table, replace it with the guid from the lookup table.
- Join the result to the lookup table on guid (make sure to keep all records from the original table, whether or not they match)
- If the employee_id is missing from the main table, replace it with the value from the lookup table
- Repeat previous steps for both the employee table and the monthly table.
- Make sure that there are no nulls in the employee_id and guid fields in both tables
- Output the data

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
