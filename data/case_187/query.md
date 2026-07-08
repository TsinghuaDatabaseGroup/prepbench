## Requirements

- Input the data
- The main challenge is to solve this using only employee_data input
- Create a Calendar Table
  - Create a date range for the calendar
    - This should be dynamic to handle new data
    - The start of the range should be the based on the year of the earliest date
      - If earliest date is 06/01/2021, the start date should be 01/01/2021
    - The end of the range should be the last day of the year for the latest date in the data set
      - If the latest date is 06/01/2022, the end date should be 31/12/2022
  - Generate a row for every day between the start and end date to get a calendar table
- Create a field containing the full name for each employee
- Get a unique list of employees with their full name, first/last name fields, and employee id
- Join the list to the calendar table
  - You should have a table with one row per employee per day
- Join the new calendar table to the main table
  - One row per employee per day, even on days where the employee wasn’t scheduled
- Create a flag if the employee was scheduled on the day
- Handle any null values
- Output the data

## Output

- output_01.csv
  - 6 fields:
    - scheduled_date
    - emp_id
    - full_name
    - first_name
    - last_name
    - scheduled
