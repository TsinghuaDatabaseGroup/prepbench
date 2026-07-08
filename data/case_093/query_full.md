## Context
Prep Air wants to analyze flight delays to and from its key destinations using two provided datasets: (1) delayed-flight details that are split across multiple rows per delay record, and (2) an aggregated count of flights that were not delayed. The goal is to restructure the delayed-flight input, validate airport codes, and produce delay-rate and average-delay metrics by airport and journey type.

## Requirements
- Input the data from:
  - `input_01.csv`: delayed-flight details recorded across multiple lines per delayed flight.
  - `input_02.csv`: aggregated counts of flights which were not delayed, by Airport and Type.

- Aggregate/restructure the delayed-flight input so that it contains **1 row per delayed flight record** (instead of the current 3 rows per record):
  - First sort the delayed-flight rows by `RecordID` ascending.
  - Treat each consecutive block of 3 `RecordID` values as one delayed-flight record, using the grouping rule: `group_id = (RecordID - 1) // 3`.
  - For each `group_id`, produce a single row with the fields `Airport`, `Type`, and `Delay` by taking the first non-null value for each field within the group.

- Make sure all Airport codes are valid, and group those which are not:
  - Define the set of **valid Airport codes** as the distinct `Airport` values present in `input_02.csv`.
  - For each delayed-flight `Airport` code:
    - If it exactly matches a valid Airport code, keep it.
    - Otherwise, attempt to map it to a valid code by comparing the sorted characters of the code to the sorted characters of each valid code; if there is **exactly one** matching valid code under this rule, use that match.
      - **Mapping rule details**: When comparing sorted characters, convert both codes to uppercase, then sort the characters of each code in alphabetical order (e.g., "JKF" → "FJK", "JFK" → "FJK"). If the sorted character sequences match exactly, consider it a match. The comparison is case-insensitive and ignores any whitespace or special characters (only alphanumeric characters are considered).
    - If no match exists, or multiple matches exist, classify the delayed-flight Airport as `Invalid`.

- Calculate delayed-flight totals by Airport and journey type:
  - Group the (restructured) delayed-flight records by `Airport` and `Type`.
  - Compute:
    - `delayed_flights` = count of delayed-flight records in the group.
    - `total_delay` = sum of `Delay` minutes in the group.

- Combine with information on flights which were not delayed:
  - Join the delayed-flight summary to `input_02.csv` on (`Airport`, `Type`) using a left join from `input_02.csv`.
    - **Join behavior**: Since this is a left join from `input_02.csv`, all (`Airport`, `Type`) combinations present in `input_02.csv` will be retained in the result. Any (`Airport`, `Type`) combinations that exist in the delayed-flight summary but not in `input_02.csv` will be excluded from the final output.
  - Where there is no matching delayed-flight summary, treat `delayed_flights` as 0 and `total_delay` as 0.

- Calculate the average delay and % of flights which were delayed for each Airport, for each journey type:
  - For each (`Airport`, `Type`) row after the join:
    - `Total Flights` = (`Number of flights` from `input_02.csv`) + `delayed_flights`.
    - `% Flights Delayed` = if `Total Flights` equals 0 then 0, else `(delayed_flights / Total Flights) * 100`.
    - `Avg Delay (mins)` = if `Total Flights` equals 0 then 0, else `total_delay / Total Flights`.
  - Exclude rows where `Airport` is `Invalid` from the final output.
  - Round `% Flights Delayed` and `Avg Delay (mins)` to **2 decimal places** using **round-half-up** rules.
  - Ensure deterministic ordering by sorting the final output by `Airport` ascending, then `Type` ascending.

- Output the data.

## Output

- output_01.csv
  - 4 fields:
    - Airport
    - Type
    - % Flights Delayed
    - Avg Delay (mins)