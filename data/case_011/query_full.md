## Context

You are given a flat file representation of a JSON-like structure where the path to each value is stored in a dot-delimited `JSON_Name` field and the corresponding value is stored in `JSON_ValueString`. The goal is to transform these records into a single OHLCV-style table where each row represents one indexed observation (“Row”), with columns for open, high, low, close, adjclose, volume, and a human-readable Date derived from a Unix epoch timestamp.

## Requirements

- Input the data from `input_01.csv`, treating `JSON_Name` and `JSON_ValueString` as text fields.
- Break up the `JSON_Name` field by splitting on the `.` delimiter so its tokens can be used to classify each record.
- Exclude records where `JSON_Name` is blank, and exclude any record whose `JSON_Name` tokens include `meta`. (This leaves only records relevant to `indicators` and `timestamp` pathways.)
- Derive a “Data Type” classification from the tokens in `JSON_Name`:
  - If the tokens include `timestamp`, set Data Type to `timestamp`.
  - If the tokens include `indicators` and `quote`, set Data Type to exactly one of: `open`, `high`, `low`, `close`, `volume` based on which of those tokens appears in the path.
  - If the tokens include `indicators` and `adjclose`, set Data Type to `adjclose`.
  - If none of the above apply, exclude the record.
- Derive the row identifier:
  - Take the last token of `JSON_Name`; it must be numeric.
  - Convert it to an integer and rename this field to `Row`.
  - If the last token is not numeric, exclude the record.
- Rename `JSON_ValueString` to `Value`.
- Keep only the renamed/derived fields needed for the transformation: `Row`, Data Type, and `Value`.
- Convert `Value` to a numeric type:
  - For Data Type = `timestamp`, treat `Value` as an integer count of Unix epoch seconds.
  - For all other Data Types, treat `Value` as numeric (floating-point where applicable).
- Pivot fields to form the final table structure:
  - One output row per `Row`.
  - Columns created from Data Type values (`timestamp`, `open`, `high`, `low`, `close`, `adjclose`, `volume`), using the first available value per (`Row`, Data Type) if duplicates exist.
- Turn Unix Epoch time into a real date:
  - Convert `timestamp` (seconds since epoch) to a datetime and format it as `DD/MM/YYYY HH:MM:SS`.
  - Store this formatted string in a `Date` column.
- Ensure the final dataset contains all required metric columns (`volume`, `high`, `low`, `adjclose`, `close`, `open`) even if some are missing for certain rows (leave missing values as null).
- Output the data.

## Output

- output_01.csv
  - 8 fields:
    - Date
    - volume
    - high
    - low
    - adjclose
    - close
    - open
    - Row