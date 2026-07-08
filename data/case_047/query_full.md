## Context

Chin & Beard Suds Co. needs an automated profit statement suitable for board reporting. The source data is arranged as a three-level hierarchy of line items (top-level categories, sub-categories, and detailed items). The task is to compute rolled-up profit totals at each parent level, populate those totals into the appropriate rows, and format the item labels with indentation to reflect the hierarchy.

## Requirements

- Input the data from `input_01.csv`.
  - The input contains at least:
    - `Item`: a text label that begins with a numeric hierarchical code (e.g., `X`, `X.X`, `X.X.X`).
    - `Profit`: a numeric value for detailed items; parent rows may be blank/null.
- Identify each row’s hierarchy level from the numeric code at the start of `Item`:
  - Level 1: `X` (one numeric segment)
  - Level 2: `X.X` (two numeric segments)
  - Level 3: `X.X.X` (three numeric segments)
- Ensure `Profit` is treated as numeric for calculation (blank/unparseable values should be treated as null).
- Find the profit sub-totals for `X.X` items:
  - For each Level 2 row, compute the sum of `Profit` across its Level 3 children (rows whose numeric code starts with the Level 2 code followed by a dot, i.e., `X.X.`).
  - If at least one Level 3 child exists, replace the Level 2 row’s `Profit` with this sum; otherwise leave its existing `Profit` unchanged.
- Find the profit totals for `X` items:
  - For each Level 1 row, compute the sum of `Profit` across its Level 2 children (rows whose numeric code starts with the Level 1 code followed by a dot, i.e., `X.`).
  - If at least one Level 2 child exists, replace the Level 1 row’s `Profit` with this sum; otherwise leave its existing `Profit` unchanged.
- Add the relevant values to the relevant items by replacing the nulls (i.e., parent rows should receive their rolled-up totals as described above).
- Add the leading spaces to `Item` to visually indicate hierarchy (do not manually rename; apply a function-based transformation):
  - 5 spaces for `X.X` items (Level 2)
  - 10 spaces for `X.X.X` items (Level 3)
  - No leading spaces for `X` items (Level 1)
- Preserve the original row order from the input in the output.
- Output only the final `Item` and `Profit` fields, with `Profit` expressed as an integer.

## Output

- output_01.csv
  - 2 fields:
    - Item
    - Profit