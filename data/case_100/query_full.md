## Context
You are preparing an orders dataset (provided as a single CSV file) so it is clean and consistently structured for stakeholder analysis.

## Requirements
- Input the data from the provided CSV file.
- Split the combined store/bike field into two separate fields:
  - Use the field named `Store - Bike` as the source.
  - Split on the delimiter `" - "` into:
    - `Store` (the part before the delimiter)
    - `Bike` (the part after the delimiter)
- Standardize the `Bike` field so it contains only these three category values:
  - `Mountain`
  - `Gravel`
  - `Road`
  Any non-canonical spellings that correspond to one of these three categories should be converted to the appropriate canonical value.
- Create two derived date fields from the existing `Date` field:
  - `Quarter`: the calendar quarter number (1–4) of the `Date`
  - `Day of Month`: the day-of-month number (1–31) of the `Date`
- Remove the first 10 orders as they are test values by excluding any records with `Order ID` less than or equal to 10 (i.e., keep only rows where `Order ID` > 10).
- Output the data as a single dataset with one row per remaining order and with fields selected and ordered exactly as specified below.

## Output

- output_01.csv
  - 8 fields:
    - Quarter
    - Day of Month
    - Store
    - Bike
    - Order ID
    - Customer Age
    - Bike Value
    - Existing Customer?