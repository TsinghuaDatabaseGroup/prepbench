## Context
Continue the prior week’s multiplication-grid puzzle by producing a multiplication table in a tabular format. The workflow should read the provided input file, construct a multiplication grid, and write the resulting table to an output CSV.

## Requirements
- Input the data from `input_01.csv`.
- Create a parameter that controls the size of the multiplication grid (the maximum multiplier and multiplicand). For this task run, set this parameter to **4**, producing a 4×4 multiplication grid.
- Generate the output table at the following grain: **one row per base number** from 1 through the grid-size parameter (inclusive).
  - Create a `Number` column containing integers from 1 to the grid-size parameter.
  - Create one column for each integer from 1 to the grid-size parameter (inclusive). Each such column must be named exactly as that integer (as a string in the header), and its values must be computed as:
    - value in column `k` = `Number * k`, for each row’s `Number` and each `k` in 1..grid size.
- Output the data to the specified CSV with exactly the required column set and names.

## Output

- output_01.csv
  - 5 fields:
    - Number
    - 1
    - 2
    - 3
    - 4