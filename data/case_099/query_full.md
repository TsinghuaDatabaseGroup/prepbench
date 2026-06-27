## Context

A revised astrology system introduced a 13th star sign (Ophiuchus), changing the star-sign date ranges compared with the traditional 12-sign system. The goal is to identify which calendar dates in 2020 would be assigned a different star sign under the new system versus the old system, and list those changes.

## Requirements

- Input the data.
- Be careful your data isn't mistaken for a header:
  - Treat the star-sign definition files as having no header rows.
  - Treat the dates file as having a header row that includes a `Date` column.

- Reshape and clean up the star-sign definition inputs into consistent “sign range” tables.

  - **New system (13 signs, includes Ophiuchus)**:
    - From `input_01.csv`, parse each sign definition into:
      - the star sign name
      - a start month and day
      - an end month and day
    - Convert each start and end into a “day-of-year” value using year 2020 (a leap year), so ranges can be evaluated against any 2020 date.
    - Create a human-readable date-range label for each new-system sign in the format:
      - `"<start_day> <start_month_abbrev> - <end_day> <end_month_abbrev>"` (month abbreviation as Jan/Feb/…/Dec).
    - Preserve the original order of sign definitions as a tie-breaker when multiple ranges match the same date.

  - **Old system (12 signs, no Ophiuchus)**:
    - From `input_02.csv`, reshape the data so each star sign is paired with its corresponding date-range entry, then parse each pair into:
      - the star sign name
      - a start month and day
      - an end month and day
    - Date ranges in `input_02.csv` are in **M/D format** (month/day, where month comes first), e.g., `1/20–2/19` represents January 20 to February 19.
    - Convert each start and end into a "day-of-year" value using year 2020.
    - Preserve the definition order (based on the input layout) as a tie-breaker when multiple ranges match the same date.

- Create a date range for the new star signs (this is the “Date Range” label described above), and ensure it is available for any output row.

- Scaffold the analysis over dates for a full leap-year calendar:
  - Use `input_03.csv` as the source of dates to evaluate.
  - Parse `input_03.csv[Date]` using the **DD/MM/YYYY format** (day/month/year, where day comes first).
  - Keep only valid dates that fall in year 2020.
  - The unit of evaluation is one calendar date (birthday) in 2020.

- For each 2020 date, determine which star-sign ranges contain that day-of-year in each system:
  - A sign range “contains” a date if the date falls inclusively between the start and end day-of-year.
  - Ranges may wrap across the end of the year (i.e., start day-of-year greater than end day-of-year); treat those as spanning year-end and still inclusive.
  - **Special case**: Exclude June 21, 2020 from the output entirely (do not generate any change rows for this date).
  - For each system, if multiple signs match a date, order the matches by:
    1) the cyclic distance in days from the sign’s start date to the target date (using modulo 366), then
    2) the sign definition order from the input.

- Identify dates whose star sign has changed between the old and new systems, with cusp handling aligned to the following deterministic rule:

  - Let `old_set` be the set of matched old-system sign names for the date, and `new_set` the set of matched new-system sign names.
  - Exclude the date entirely (treat as “not changed”) if **either** of these is true:
    - the old system yields exactly one unique sign and that sign is included in `new_set`, or
    - the new system yields exactly one unique sign and that sign is included in `old_set`.
  - Otherwise, emit change rows using these pairing rules:
    - If one system yields exactly 1 match and the other yields exactly 2 matches, output one row for each pairing where the old and new sign names differ (i.e., pair the single sign with each of the two on the other side, excluding any equal-name pairing).
    - In all other cases, pair matches by their ordered position (first-to-first, second-to-second, etc.) up to `min(number_of_old_matches, number_of_new_matches)`, and output a row for each paired position where the old and new sign names differ.

- Create a birthday field:
  - Format as `"<month_abbrev> <day_number>"` (e.g., `Feb 19`), using the 2020 date’s month abbreviation and day-of-month without leading zeros.

- Finalize the output rows:
  - Each output row represents one detected old-vs-new star-sign change for a specific birthday (a date in 2020), after applying the cusp exclusion logic above.
  - Populate:
    - `Old Star Sign` from the old-system matched sign in that pairing,
    - `New Star Sign` from the new-system matched sign in that pairing,
    - `Date Range` from the **new-system** sign’s formatted range label.
  - Remove duplicate rows (identical across all four output fields).
  - Sort the output by:
    1) birthday month (Jan to Dec),
    2) birthday day number ascending,
    3) `Old Star Sign` ascending,
    4) `New Star Sign` ascending.

- Output the data.

## Ambiguity Resolution

The following ambiguities in date format parsing are resolved as follows:

- **`input_03.csv` date format**: The `Date` column uses **DD/MM/YYYY format** (day/month/year, where day comes first). For example, `01/01/2020` represents January 1, 2020, and `02/01/2020` represents January 2, 2020.

- **`input_02.csv` date range format**: Date ranges are in **M/D format** (month/day, where month comes first). For example, `1/20–2/19` represents January 20 to February 19, and `12/22–1/20` represents December 22 to January 20 (wrapping across year-end).

## Output

- output_01.csv
  - 4 fields:
    - Birthday
    - Old Star Sign
    - New Star Sign
    - Date Range