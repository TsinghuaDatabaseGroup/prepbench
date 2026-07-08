## Context
You need to determine how many Valentine’s Days each couple has experienced together as of a fixed “today” date, and then assign an appropriate gift idea by matching that count to a gift-ideas lookup.

## Requirements
- Input the data from:
  - `input_01.csv` (couples), which includes at least `Couple` and `Relationship Start`.
  - `input_02.csv` (gift ideas), which includes at least `Year` and `Gift`.
- Fix/convert the `Relationship Start` field to a true Date/Datetime type. If a value cannot be parsed as a date, treat it as missing.
- Create/define “today” as a fixed date: **14/02/2024**.
- For each couple, compute **Number of Valentine's Days as a Couple** using logic that is not a simple date difference:
  - If `Relationship Start` is missing, the count must be `0`.
  - If `Relationship Start` is after 14/02/2024, the count must be `0`.
  - Otherwise, count how many dates of **February 14** occur on or after the relationship start date and on or before **February 14, 2024**, inclusive.
    - Equivalently: for each calendar year from the start year through 2024, include that year’s Feb 14 if and only if that Feb 14 is on/after the relationship start date.
- Create a join key field named `Year` from **Number of Valentine's Days as a Couple** by converting the integer count to an English ordinal string:
  - Use `st`, `nd`, `rd`, `th` suffixes based on standard rules, with the special-case rule that numbers ending in 11, 12, or 13 use `th` (e.g., 11th, 12th, 13th).
  - This `Year` field must match the data type/format used in the gift ideas dataset’s `Year` field so they can be joined.
- Join the couples data to the gift ideas data using a **left join** on `Year`:
  - Keep all couples even if no matching gift is found; unmatched gifts should remain null/blank.
- Remove unnecessary fields so the final dataset contains only the required output fields.
- Sort the final output ascending by:
  1) `Number of Valentine's Days as a Couple`
  2) `Couple`
- Output the data to the required file.

## Output

- output_01.csv
  - 3 fields:
    - Couple
    - Number of Valentine's Days as a Couple
    - Gift