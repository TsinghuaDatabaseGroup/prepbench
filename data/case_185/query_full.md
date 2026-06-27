## Context

You have a dataset of spin class sessions that includes a numeric session measure (`Value`), a `Date`, and a final “unnamed” text field that encodes additional attributes. The goal is to parse the embedded attributes, standardize the relevant fields, filter to a specific parameter configuration (music type and coach), and return the Top N sessions ranked by calories burned.

## Requirements

- Input the data from `input_01.csv`.

- Parse the final (unnamed) column into three fields by splitting on the delimiter ` - ` (three parts, left to right):
  - `Coach`
  - `Calories`
  - `Music Type`
  - Treat `Calories` as an integer.
  - Convert `Music Type` values to Title Case (first letter of each word capitalised). This conversion must be completed before applying any filtering operations that use `Music Type` values.

- Merge km’s and min’s into a single minutes measure as follows:
  - Treat every record’s `Value` as an already‑measured duration in minutes, regardless of whether the original unit label was recorded as `km` or `min` in the source system.
  - Create a field named `Mins` from the existing `Value` field (i.e., `Mins = Value`), without performing any numeric conversion between different physical units.
  - Ignore any separate unit indicator column in the dataset; the numeric `Value` itself is the authoritative minutes value.
  - This implements “Change `Value` to Mins” and provides a unified minutes column for output.

- Standardize the `Date` field to the string format `DD/MM/YYYY` where the input value can be interpreted as a date.

- Create three parameters and apply them to produce the output for this run:
  - `Music Type` = `Everything Rock`
  - `Coach` = `Kym`
  - `Top N` = `5`

- Filter the dataset so only rows matching the parameter selections remain:
  - First ensure that all `Music Type` values have been converted to Title Case (as specified in the parsing step above).
  - Then keep rows where `Music Type` equals the selected `Music Type` parameter and `Coach` equals the selected `Coach` parameter.
  - The matching is performed after the Title Case conversion, so the parameter value `Everything Rock` will match data values that have been converted to `Everything Rock` from their original format (e.g., `everything rock`).

- Return the Top N records and order the results with the highest calories burned at the top:
  - Sort the filtered rows by `Calories` in descending order (highest first).
  - Keep only the first `Top N` rows after sorting.
  - Create `Rank` as 1 for the top row, increasing by 1 down to N, based on this sorted order.

- Produce the final output dataset containing only the required fields, in the required order.

- Output the data to the required filename.

## Output

- output_01.csv
  - 6 fields:
    - Rank
    - Coach
    - Calories
    - Music Type
    - Date
    - Mins