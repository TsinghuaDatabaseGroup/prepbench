## Context

You have separate input files for multiple Regions, each containing store-level monthly Sales and Profit in a wide layout. The goal is to reshape each regional file into a consistent long-format table (one row per Region–Store–Month), then combine all Regions into a single output without introducing duplicated rows from the workflow logic.

## Requirements

- Input the data.
  - Use all regional input CSV files named `input_*.csv` (specifically `input_01.csv` through `input_04.csv`).
  - Determine `Region` from the input file name:
    - `input_01.csv` → `London`
    - `input_02.csv` → `Northern`
    - `input_03.csv` → `Scotland`
    - `input_04.csv` → `Wales`
- For each regional input file, convert the wide monthly structure to a long table.
  - Treat the first column in the data section as the store identifier (`Store`).
  - Read the list of months from the dedicated month header row (the row containing month abbreviations such as Jan–Dec); these months define how many month blocks exist.
  - For each store row, generate one output row per month, taking values from the two columns associated with that month in the wide layout:
    - `Sales` = the Sales value for that month
    - `Profit` = the Profit value for that month
  - Create `Date` as a string in `DD/MM/YYYY` format using:
    - day = `01`
    - month = the month number mapped from the month abbreviation (`Jan`→`01`, `Feb`→`02`, …, `Dec`→`12`)
    - year = `2022`
    - resulting format: `01/MM/2022`
- Bring in the data from all the Regions and update the workflow so that no rows get duplicated.
  - Append (union/concatenate) the transformed rows from all regions into a single dataset, ensuring each input file contributes its rows exactly once (i.e., do not accidentally duplicate rows due to repeated reads or repeated unions).
- Output the data.

## Output

- output_01.csv
  - 5 fields:
    - Region
    - Store
    - Date
    - Sales
    - Profit