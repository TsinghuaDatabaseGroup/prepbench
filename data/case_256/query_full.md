## Context
A stakeholder needs two structured datasets about passengers: one dataset for passengers who hold a Flow Card and another for passengers who do not. Each dataset must contain standardized flight attributes derived from a single “Flight Details” field, along with the passenger’s card status and onboard options.

## Requirements
- Input the data from `inputs/input_01.csv`.
- For each input row, parse the `Flight Details` field into the following components and use them as separate columns:
  - `Date`
  - `Flight Number`
  - `From`
  - `To`
  - `Class`
  - `Price`
- Parsing logic for `Flight Details`:
  - Split `Flight Details` into five parts using the delimiter `//` in order: `Date`, `Flight Number`, a combined `Route`, `Class`, `Price`.
  - Split `Route` into `From` and `To` using the first `-` character (left side = `From`, right side = `To`).
- Convert data types / formats:
  - Convert `Date` from its source representation into a date value and then output it formatted as `DD/MM/YYYY` (day first).
  - Convert `Price` to a numeric value:
    - If the value is an integer, keep it as an integer.
    - Otherwise, round/quantize it to exactly 1 decimal place.
    - If `Price` cannot be interpreted as a number, set it to null.
  - Convert `Bags Checked` to an integer.
- Convert the `Flow Card?` field to standardized values:
  - Map `"1"` to `"Yes"`.
  - Any other value is treated as `"No"`.
- Create two output tables at the same row grain as the input (one output row per input passenger record after parsing):
  - One table containing only rows where `Flow Card?` is `"Yes"`.
  - One table containing only rows where `Flow Card?` is `"No"`.
  - Preserve the original input row order within each table.
- Output the data to two separate CSV files with the required schemas.

## Output

- output_01.csv
  - 9 fields:
    - Date
    - Flight Number
    - From
    - To
    - Class
    - Price
    - Flow Card?
    - Bags Checked
    - Meal Type

- output_02.csv
  - 9 fields:
    - Date
    - Flight Number
    - From
    - To
    - Class
    - Price
    - Flow Card?
    - Bags Checked
    - Meal Type