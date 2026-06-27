## Context

You are given a single input CSV containing employee milestone records. Some rows omit the repeated "Employee" and "Work Level" values, which should be carried forward from the most recent prior row where they are present. The goal is to produce an output file while preserving the intended original row sequence.

## Requirements

- Input the data from `inputs/input_01.csv`.
- **Ambiguity Resolution**: Handle the ambiguity where some rows omit repeated "Employee" and "Work Level" values:
  - Fill down the `Employee` field:
    - For each row, if `Employee` is missing, set it to the last non-missing `Employee` value from the rows above (forward-fill).
  - Fill down the `Work Level` field:
    - For each row, if `Work Level` is missing, set it to the last non-missing `Work Level` value from the rows above (forward-fill).
    - After filling down, ensure `Work Level` is an integer value (cast to integer).
- Ensure `Date` is output as text in `DD/MM/YYYY` format:
  - If the processing environment interprets `Date` as a date type, convert it back to a text representation formatted as `DD/MM/YYYY`.
  - Otherwise, keep `Date` as text.
- Reorder the data to preserve the intended original row sequence:
  - The output order is determined by sorting rows by `Record ID` in ascending order.
  - This ensures a deterministic ordering that preserves the intended sequence (if the input is already sorted by `Record ID`, the order remains unchanged; if not, sorting by `Record ID` establishes the canonical order).
- Output the data as a single CSV containing the specified fields.

## Output

- output_01.csv
  - 5 fields:
    - Record ID
    - Employee
    - Work Level
    - Stage
    - Date