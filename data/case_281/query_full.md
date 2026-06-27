## Context
SuperBytes maintains a complaints log where each row represents a single customer complaint along with identifiers, received/resolved dates, a “Timely Response” indicator, and product/issue metadata. The objective is to produce a standardized extract of the complaints log with a consistent set of fields and a correctly typed “Timely Response” value for downstream reporting.

## Requirements
- Input the data from `input_01.csv`.
- Treat all columns as text on input, then normalize the `Timely Response` field to a boolean as follows:
  - Map `true` (case-insensitive) to `True`.
  - Map `false` (case-insensitive) to `False`.
  - Any other value should be treated as `False`.
- Do not derive or add any new fields (e.g., do not calculate “Days to Resolve” / “Days Open”), and do not apply any filtering (e.g., do not separate “In Progress” vs “Closed”) in the output.
- Produce the output by selecting only the required fields listed in the output specification, in exactly that order.
- Output the data to the specified file.

## Output

- output_01.csv
  - 11 fields:
    - Complaint ID
    - Receipt Number
    - Customer ID
    - Date Received
    - Date Resolved
    - Timely Response
    - Response to Consumer
    - Issue Type
    - Product Category
    - Product ID
    - Complaint Description