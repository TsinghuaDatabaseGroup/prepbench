## Context
Create a classic 9×9 multiplication grid (times table). The provided input file contains the boundary numbers that define the inclusive range to use (expected to be 1 through 9).

## Requirements
- Input the data from `input_01.csv`.
  - The input contains a column named `Numbers`; use it only to determine the minimum and maximum values present.
- Create a 9x9 multiplication table based on the inclusive integer range from `min(Numbers)` to `max(Numbers)`.
  - Generate one output row per integer `i` in this range (inclusive), with `Number = i`.
  - For each integer `j` in the same range, create a column named with `j` (as text) whose value is `i * j`.
- Ensure the output columns are ordered as: `Number`, then `1`, `2`, `3`, `4`, `5`, `6`, `7`, `8`, `9`.
- Output the data to the specified file.

## Output

- output_01.csv
  - 10 fields:
    - Number
    - 1
    - 2
    - 3
    - 4
    - 5
    - 6
    - 7
    - 8
    - 9