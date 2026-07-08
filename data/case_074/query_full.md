## Context
You are preparing a cleaned, analysis-ready extract from a Summer Olympics host-cities dataset. The source is provided as a single file and includes (a) an Olympics “Games” identifier expressed as a Roman numeral and (b) a textual date range for when the Games occurred. Your goal is to convert the Roman numeral to a numeric sequence, derive the Olympics year on a fixed four-year cycle, parse the date range into explicit start/end date fields, remove cancelled/invalid rows that lack valid dates, and retain only the fields required for downstream analysis.

## Requirements
- Input the data.
  - Read `inputs/input_01.csv`.
  - Treat each input row as one Olympics edition (one “Games” entry) with its associated host and counts.
- Convert the Roman numerals to numerical values.
  - Convert the `Games` Roman numeral to an integer “game number” (e.g., I → 1, II → 2, etc.) using standard Roman numeral rules (including subtractive notation).
- Determine the Year of the Olympics.
  - Use a fixed four-year cadence: the first Olympics (game number 1 / “I”) is year **1896**, and each subsequent game number increases the year by **4**:
    - `Year = 1896 + (Game_Number - 1) * 4`
  - Apply this even if the Games were not held for a given cycle (i.e., do not skip year increments).
- Create a Start Date for the Games (in M/D/YYYY format).
  - Parse the `Dates` field as a single range describing start and end within the derived `Year`.
  - The range is separated by an en dash (–).
  - The start portion may be either:
    - a day-of-month only (month is implied from the end portion), or
    - a day-of-month plus month name.
  - When the start portion is day-only, always use the month from the end portion, even if the date range spans multiple months (the start and end dates will be in the same month as specified in the end portion).
  - Construct `Start Date` as a string formatted `M/D/YYYY` using the derived `Year` (no requirement to zero-pad month/day).
- Create an End Date for the Games (in M/D/YYYY format).
  - Parse the end portion of `Dates` as `day monthname`, and construct `End Date` as `M/D/YYYY` using the derived `Year`.
- Remove unnecessary fields.
  - Keep only the fields required in the specified output and drop all others.
- Remove the null dates.
  - Exclude any rows where either `Start Date` or `End Date` cannot be produced (these correspond to cancelled/invalid entries for this task).
- Ensure numeric count fields are integers.
  - Output `Nations`, `Sports`, and `Events` as integers.
- Output the data.

## Output

- output_01.csv
  - 7 fields:
    - Start Date
    - End Date
    - Games
    - Host
    - Nations
    - Sports
    - Events