## Context
You are given multiple weeks of sales data spread across separate inputs, plus a separate planning file from a financial planner that contains profit-threshold and budget reference tables. The goal is to consolidate the weekly sales, compare actual performance against (1) profit minimum targets and (2) budget expectations, and then output two exception-style extracts for further review.

## Ambiguity Resolution

This section clarifies how to handle ambiguous cases in the data processing:

### Type Mapping Rules
The budget table contains Type values in formats like `Bar_01893` and `91374__Liquid`, which need to be mapped to the standardized lowercase categories used in sales data (`bar` and `liquid`). The mapping rules are:
- If the Type value contains "Bar" (case-insensitive), map it to `bar`
- If the Type value contains "Liquid" (case-insensitive), map it to `liquid`
- After mapping, convert to lowercase to match the sales data format

### Date Column Identification
Date-based columns in the budget table are identified by:
- Column headers that can be parsed as valid date/time values (e.g., `2020-02-01 00:00:00`)
- Columns that appear after the `Measure` column in the budget section header row

### Date Column Selection
When selecting date columns from the budget table:
- Sort all identified date-based columns chronologically in ascending order (earliest to latest)
- The "middle" date column is the second column when ordered chronologically (if there are 3 columns, it's the middle one; if there are 2 columns, it's the first one; if there's only 1 column, use it for both mid and latest)
- The "latest" date column is the last column when ordered chronologically

### Week Boundary Handling
When determining which budget values to use based on Week:
- For `Week <= 5`: use `Budget Volume_mid` and `Budget Value_mid` (this includes Week 5)
- For `Week >= 6`: use `Budget Volume_latest` and `Budget Value_latest` (this includes Week 6)
- Note: Week 5 uses mid values, Week 6 uses latest values

### Week Range Limitation
The budget comparison output is limited to weeks 5 through 8 inclusive because:
- Weeks 1-4 use early budget expectations (not included in the exception report)
- Weeks 5-8 are the focus period for budget performance review
- This is a business rule for the exception reporting scope

### Exclusion Logic Execution Order
When preparing `output_01.csv`:
1. First, perform the left join of weekly sales to the reshaped budget table on `Type`
2. Then, apply the Week-based budget field derivation (mid vs latest)
3. Next, filter to weeks 5-8 inclusive
4. Then, exclude any (`Type`, `Week`) combinations that exceeded profit minimums for both value and volume (these are already captured in `output_02.csv`)
5. Finally, keep only rows where at least one budget measure has not been reached

## Requirements
- Input the data.
- Pull all the Week worksheets together by compiling all available sales inputs into a single fact table:
  - Treat each sales input row as a dated transaction with at least: `Date`, `Type`, and volume/value measures.
  - Accept either measure naming convention:
    - `Sales Volume` and `Sales Value`, or
    - `Volume` and `Value` (rename these to `Sales Volume` and `Sales Value`).
  - Parse `Date` as a date/time.
  - Derive `Week` as the ISO week number of `Date` (integer).
  - Convert `Type` to lowercase representation.
- Form weekly sales volume and value figures per product:
  - Aggregate to one row per (`Type`, `Week`).
  - Compute:
    - `Sales Volume` = sum of transaction-level sales volumes for that (`Type`, `Week`).
    - `Sales Value` = sum of transaction-level sales values for that (`Type`, `Week`).
- Prepare the data in the Profit table for comparison against the actual volumes and values:
  - Read the profit-minimum reference table from the planning input.
  - Identify the profit-minimum section by locating its header row that includes `Week`, `Type`, `Profit Min Sales Volume`, and `Profit Min Sales Value`.
  - Keep only rows that contain a valid week identifier in the form `2020_<week_number>`, and extract `<week_number>` as an integer `Week`.
  - Convert `Type` to the same lowercase representation used in sales.
  - Ensure `Profit Min Sales Volume` and `Profit Min Sales Value` are numeric.
  - Grain of this reference: one row per (`Type`, `Week`).
- Join the tables but only bring back those that have exceeded their Profit Min points for both Value and Volume:
  - Inner join weekly sales to the profit-minimum reference on (`Type`, `Week`).
  - Keep only rows where:
    - `Sales Volume` >= `Profit Min Sales Volume`, AND
    - `Sales Value` >= `Profit Min Sales Value`.
  - Select only the fields required for `output_02.csv`.
- Prepare the Budget Volumes and Values for comparison against the actual volumes and values:
  - Read the budget reference table from the planning input.
  - Identify the budget section by locating a header row containing `Type` and `Measure` plus multiple date-based columns (see "Date Column Identification" in Ambiguity Resolution section).
  - From the available date-based budget columns, select:
    - the chronologically "middle" date column (see "Date Column Selection" in Ambiguity Resolution section for detailed rules), and
    - the latest date column (see "Date Column Selection" in Ambiguity Resolution section for detailed rules).
  - Convert the selected budget columns to numeric.
  - Convert the budget `Type` to lowercase and map it to the appropriate `Type` category using the mapping rules specified in the "Type Mapping Rules" section of Ambiguity Resolution (e.g., "bar" vs "liquid").
  - Reshape the budget table so that each `Type` has separate budget measures for each selected date column:
    - `Budget Volume_mid`, `Budget Value_mid` from the middle date column
    - `Budget Volume_latest`, `Budget Value_latest` from the latest date column
  - This budget reference should be one row per `Type`.
- Join the tables but only return those that haven't reached the budget expected for either Value or Volume:
  - Left join weekly sales to the reshaped budget table on `Type`.
  - For each weekly row, derive the comparable budget fields based on Week value (see "Week Boundary Handling" in Ambiguity Resolution section for boundary cases):
    - If `Week` <= 5:
      - `Budget Volume` = `Budget Volume_mid`
      - `Budget Value` = `Budget Value_mid`
    - If `Week` >= 6:
      - `Budget Volume` = `Budget Volume_latest`
      - `Budget Value` = `Budget Value_latest`
  - Limit the budget comparison output to weeks 5 through 8 inclusive (see "Week Range Limitation" in Ambiguity Resolution section for the business reason).
  - Exclude any (`Type`, `Week`) combinations that exceeded profit minimums for both value and volume (as defined in the profit-minimum comparison above). This exclusion is applied after the join and Week-based budget field derivation, as specified in "Exclusion Logic Execution Order" in the Ambiguity Resolution section.
  - Keep only rows where at least one budget measure has not been reached:
    - `Sales Volume` < `Budget Volume` OR
    - `Sales Value` < `Budget Value`
  - Select only the fields required for `output_01.csv`.
- Prepare the outputs:
  - For determinism, sort both outputs by `Type` ascending, then `Week` ascending.
- Output the data.

## Output

- output_01.csv
  - 6 fields:
    - Type
    - Week
    - Sales Volume
    - Budget Volume
    - Sales Value
    - Budget Value

- output_02.csv
  - 6 fields:
    - Type
    - Week
    - Sales Volume
    - Sales Value
    - Profit Min Sales Volume
    - Profit Min Sales Value