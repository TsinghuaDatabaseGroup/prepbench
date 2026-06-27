## Context
A stakeholder at AllChains has provided a “cleaned” dataset in a pivoted (wide) format that is not ideal for analysis in tools like Tableau Desktop. The goal is to convert this wide, pivot-style table into a tidy, row-based structure by un-pivoting the measure columns into records and producing separate Sales and Profit fields.

## Requirements
- Input the data from `input_01.csv`.
- Treat `Region` as the identifier column that should remain as-is, and treat all other columns as pivoted value columns to be un-pivoted.
- Dynamically standardize/interpret the pivoted column names so there is a consistent separator between the three embedded attributes:
  - Bike Type
  - Month (as a month token)
  - Measure Name  
  Specifically, the value-column names must be handled as a single string that encodes these three parts separated by a common delimiter (three underscores).
- Pivot the data from wide to long so that:
  - each original value column becomes a row with:
    - `Region`
    - a column holding the original value-column name (the combined “Bike Type / Month / Measure” token)
    - a numeric value
- Split (parse) the combined value-column name into three fields:
  - `Bike Type`
  - a temporary month token (e.g., `Month_str`)
  - `Measure` (must distinguish Sales vs Profit)
- Convert the parsed month token into a `Month` field formatted as a date string representing the first day of that month, in `DD/MM/YYYY` format.
- Create separate numeric fields for `Sales` and `Profit` by reshaping the long data so that Sales and Profit become two columns aligned on the same keys:
  - Use `Bike Type`, `Region`, and `Month` as the unique key.
  - Keep only key-combinations where both Sales and Profit exist for the same `Bike Type` + `Region` + `Month`.
- Ensure `Sales` and `Profit` are numeric and round both to 9 decimal places.
- Output the final dataset with one row per `Bike Type` + `Region` + `Month`, containing both measures.
- Sort the final output by `Bike Type`, then `Region`, then `Month` in ascending chronological order.

## Output

- output_01.csv
  - 5 fields:
    - Bike Type
    - Region
    - Month
    - Sales
    - Profit