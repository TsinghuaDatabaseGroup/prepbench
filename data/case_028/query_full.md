## Context

Chin & Beard Suds Co has recorded observational data for a small set of employees, logged in short intervals throughout a working day. For each interval, the observation notes (a) whether the employee was on task, (b) the manager’s proximity, and (c) who the employee interacted with most. The data is currently stored in a wide/checkbox-style layout that is not convenient for Tableau, and the interval timestamps must be converted into concrete date-times using each employee’s initial observation start time and the sequence of interval durations.

## Requirements

- Input the data from `input_01.csv`.

- Interpret the file’s first row as the true header row:
  - Use the values in the first row to rename the existing columns (only where the first-row cell is non-empty after stripping).
  - Remove that first row from the data so that all remaining rows are observation records.

- Work at the grain of **one row per employee per observation interval**.

- Retain only the following source fields needed for the transformation:
  - Base fields: `Employee`, `Observation Start Time`, `Observation Interval`, `Observation Length (mins)`
  - Interaction indicator fields: `Manager`, `Coworker`, `Customer`, `No One`
  - Task indicator fields: `On Task`, `Off Task`
  - Manager proximity indicator fields: `Next to (<2m)`, `Close to (<5m)`, `Further(>5m)`

- For each observation row, collapse the indicator/checkbox fields into single categorical fields by selecting the column name marked with `X`:
  - **Interaction**: among `Manager`, `Coworker`, `Customer`, `No One`, set `Interaction` to the name of the column that contains `X`.
    - If none of these columns contains `X`, set `Interaction` to an empty string.
  - **Task Engagement**: among `On Task`, `Off Task`, set `Task Engagement` to the name of the column that contains `X`.
    - If none of these columns contains `X`, set `Task Engagement` to an empty string.
  - **Manager Proximity**: among `Next to (<2m)`, `Close to (<5m)`, `Further(>5m)`, set `Manager Proximity` to the name of the column that contains `X`.
    - If none of these columns contains `X`, set `Manager Proximity` to `NA`.

- Convert the following fields to integers (invalid/non-numeric values are coerced in the same way as numeric parsing with coercion, then cast to integer):
  - `Observation Length (mins)` → integer
  - `Observation Interval` → integer

- Calculate an **actual date-time** for each interval’s `Observation Start Time` as follows:
  - First, order records by `Employee` ascending, then `Observation Interval` ascending (this ordering defines the interval sequence per employee).
  - Use a constant base date of **2019-08-16**.
  - For each `Employee`, treat that employee’s first (in the ordered sequence) `Observation Start Time` value as the employee’s base time-of-day.
  - For each row within an employee, compute the offset in minutes as the cumulative sum of prior intervals’ `Observation Length (mins)` (i.e., the first interval has offset 0; each subsequent interval adds the previous interval length).
  - Set `Observation Start Time` to: base date + employee base time-of-day + computed offset (in minutes).
  - Format the resulting timestamp as a string in the exact format: `DD/MM/YYYY HH:MM:SS`.

- Produce the final output with exactly the following columns (in this order):
  1) `Task Engagement`
  2) `Manager Proximity`
  3) `Interaction`
  4) `Employee`
  5) `Observation Start Time`
  6) `Observation Length (mins)`
  7) `Observation Interval`

- Sort the final output rows by the following keys in ascending order (to match required output ordering):
  1) `Task Engagement`
  2) `Manager Proximity`
  3) `Interaction`
  4) `Employee`
  5) `Observation Start Time`
  6) `Observation Length (mins)`
  7) `Observation Interval`

- Output the data.

## Output

- output_01.csv
  - 7 fields:
    - Task Engagement
    - Manager Proximity
    - Interaction
    - Employee
    - Observation Start Time
    - Observation Length (mins)
    - Observation Interval