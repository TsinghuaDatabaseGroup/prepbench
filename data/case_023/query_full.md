## Context

Sales entries were captured inconsistently, with key details embedded in a free-text notes field and dates recorded only as day-of-week indicators. The goal is to consolidate the weekly files into a single tidy sales dataset with a proper sale date and structured product/customer fields suitable for analysis.

## Requirements

- Input the data.
- Bring in all provided input files (treat each file as one week of sales) and stack/append them into a single dataset (do not de-duplicate).
- Assume each input row represents one sale and preserve row-level granularity in the output.

- Create the date of the sale:
  - Each input file corresponds to a specific week, where the Monday of that week is:
    - `input_01.csv`: 2019-07-15
    - `input_02.csv`: 2019-07-22
    - `input_03.csv`: 2019-07-29
  - Within each file, compute `Date` by mapping the row’s `Day` value to an offset from Monday:
    - Monday = 0, Tuesday = 1, Wednesday = 2, Thursday = 3, Friday = 4, Saturday = 5, Sunday = 6
  - Add that offset (in days) to the file’s Monday date to produce the final `Date`.
  - When writing the CSV, format `Date` as `DD/MM/YYYY`.

- Create a column for the customer name:
  - Derive `Name` from the `Notes` text as the substring from the start of the string up to (but not including) the word `wants`.
  - Convert `Name` to Title Case in the output.

- Create a column for the sale value:
  - Derive `Value` from the `Notes` text as the integer amount immediately following the `£` symbol.

- Create a column for the scent of the product and a column for the product:
  - From `Notes`, take the text after the word `of` to the end of the string as the product description.
  - Set `Scent` to the first word of that product description, converted to Title Case, and ensure the output `Scent` value ends with a single trailing space.
  - Set `Product` to the remaining words (after the first word) of that product description, joined with single spaces and converted to Title Case.

- Standardise the `Notes` field for output:
  - Output `Notes` entirely in lowercase.

- Output the final dataset containing exactly the required fields in the specified order.

## Output

- output_01.csv
  - 6 fields:
    - Date
    - Name
    - Value
    - Scent
    - Product
    - Notes