## Context

You need a table of Gregorian Easter Sunday dates for a fixed historical range of years. The final deliverable is a simple two-column dataset listing each year from 1700 through 2023 and the corresponding Easter Sunday date, suitable for downstream charting or analysis.

## Requirements

- Input the data (read the provided input file as the task’s starting point), but the required output must ultimately be based on the full year range specified below regardless of the input’s layout.
- Construct the set of years to cover:
  - Include every integer year from 1700 through 2023, inclusive.
  - Ensure there is exactly one output row per year in this range.
- Create a sequential row identifier:
  - Add `Calculation1` as a 1-based sequence (1, 2, 3, …) in ascending year order (so 1700 corresponds to 1 and 2023 corresponds to 324).
- Compute Easter Sunday for each year using the Gregorian (Western) Easter computation (the Anonymous Gregorian algorithm):
  - For each year, derive the Easter month (March=3 or April=4) and day according to the standard algorithm, then construct the date for that year.
- Filter the dataset so that it only includes the required past dates:
  - Keep only years between 1700 and 2023 inclusive.
- Keep only the required fields in the final output:
  - `Calculation1`
  - `Easter Sunday`
- Format the `Easter Sunday` field as text in `DD/MM/YYYY`.
- Output the data.

## Output

- output_01.csv
  - 2 fields:
    - Calculation1
    - Easter Sunday