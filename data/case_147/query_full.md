## Context
Finance needs a tidy, analysis-ready dataset from a single input file that contains multiple semi-structured tables (one per branch) laid out in blocks. Each branch’s block contains a set of measures and multiple year columns, with some measures recorded in thousands or millions. The goal is to extract each branch table, reshape it to a consistent row-based structure, and compute correctly scaled numeric values.

## Requirements
- Input the data from `input_01.csv` (a semi-structured extract of the original workbook).
- Extract each data table within the file by splitting the input into contiguous “blocks” separated by fully blank rows (rows where every column is null). Treat each non-empty block as one branch table.
- Extract the branch name from each block:
  - The branch name is taken from the first row of the block, second column (i.e., row 1 / column 2 within that block).
- Identify the year columns for each block from the first row of the block, starting in the third column onward:
  - Use the non-null header cells only.
  - Remove the text prefix `Year ` from these header values so the recorded year becomes the year number (e.g., `Year 2021` → `2021`).
- Create a row per measure and year (i.e., unpivot each branch table):
  - Treat the measure name column as the measure identifier.
  - Convert each year column into rows with fields for Recorded Year and the recorded Value.
  - Append the extracted Branch to every resulting row.
- Remove the suffix of the measure to create clean measure names:
  - If a measure name includes `(k)` or `(m)` (including the preceding space), remove that suffix to form **Clean Measure names**.
- Create a True Value (i.e. the correct number of zeros for the measure):
  - If the original measure name contains `(k)`, multiply the numeric Value by 1,000.
  - If the original measure name contains `(m)`, multiply the numeric Value by 1,000,000.
  - Otherwise multiply by 1.
  - Round the resulting True Value to a whole number and store it as an integer.
- Remove unneeded columns:
  - Do not include intermediate fields such as the original unclean measure name, the unscaled value, or any multiplier/helper fields in the final output.
- For deterministic output ordering, sort the final rows by:
  - Branch in this order: Lewisham, York, Wimbledon
  - Clean Measure names in this order: Sales, Profit, Number of Staff, Staff Cost
  - Recorded Year in descending order (2021 before 2020)
- Output the data.

## Output

- output_01.csv
  - 4 fields:
    - Branch
    - Clean Measure names
    - Recorded Year
    - True Value