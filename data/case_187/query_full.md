## Context

You are given a single employee scheduling dataset and need to produce a daily employee-by-calendar view that includes every employee on every day in a dynamically generated date range, including days when an employee has no scheduled record. The result must be created using only the provided employee scheduling input.

## Requirements

- Input the data.
  - Use only the single provided employee scheduling input file (no additional reference tables).

- Interpret the scheduling date.
  - Parse `scheduled_date` as a calendar date using the month/day/year pattern (MM/DD/YYYY).

- Create a Calendar Table (dynamic date range).
  - Determine the earliest scheduled date and the latest scheduled date from the parsed `scheduled_date`.
  - Set the calendar start date to **January 1** of the year containing the earliest scheduled date.
    - Example rule: if the earliest date is 06/01/2021, the start date is 01/01/2021.
  - Set the calendar end date to **December 31** of the year containing the latest scheduled date.
    - Example rule: if the latest date is 06/01/2022, the end date is 31/12/2022.
  - Generate one row per day for every date between the start and end dates, inclusive.

- Create employee identity fields.
  - Create `full_name` as `first_name + ' ' + last_name`.
  - Create a unique list of employees containing exactly: `emp_id`, `first_name`, `last_name`, `full_name`.
    - Uniqueness is defined by the combination of these four fields.

- Expand to one row per employee per day.
  - Perform a cross join between the full calendar table and the unique employee list so the grain becomes **one row per employee per calendar day**.

- Mark whether the employee was scheduled on that day.
  - From the original input, create a distinct set of scheduled occurrences at grain **(emp_id, scheduled_date)** and add a boolean flag `scheduled = True`.
    - If multiple input rows exist for the same `(emp_id, scheduled_date)`, treat them as a single scheduled occurrence.
  - Left join this scheduled-occurrence set onto the employee-by-day table using keys `(emp_id, scheduled_date)` (based on the parsed date value).
  - Handle null values:
    - For any employee-day with no match, set `scheduled` to `False`.

- Final formatting and typing for output.
  - Output `scheduled_date` as a string formatted `M/D/YYYY` (month and day without leading zeros).
  - Ensure `emp_id` is an integer and `scheduled` is boolean.
  - Sort the final output by `scheduled_date` ascending, then `emp_id` ascending.

- Output the data.

## Output

- output_01.csv
  - 6 fields:
    - scheduled_date
    - emp_id
    - full_name
    - first_name
    - last_name
    - scheduled