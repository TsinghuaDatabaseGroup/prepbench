## Context
You have two sources of performance data: (1) daily product transactions and (2) weekly product targets provided by Finance. The goal is to compare this year’s performance against last year and against targets, using consistent Year-to-Date (YTD), Month-to-Date (MTD), and Week-to-Date (WTD) cutoffs.

Assumptions:
- “Today” / the latest date is Friday 9th October 2020.
- Weeks run Sunday to Saturday, with a special Week 1 definition at the start of each year (see requirements).

## Requirements
- Input the data.

- Define the custom Week/Day calendar used throughout the task:
  - Day numbering: Sunday = 1, Monday = 2, …, Saturday = 7.
  - Week 1: starts on January 1 and runs through the first Saturday of the year (inclusive).
  - Week 2: starts on the first Sunday of the year and runs through the following Saturday (inclusive).
  - Week numbers then continue in 7-day blocks (Sunday–Saturday).

- Prepare the Transactions data:
  - Parse `TransactionDate` as a date.
  - Derive `Week` and `Day` for each transaction date using the custom Week/Day calendar above.
  - Categorise each transaction row into `Type`:
    - `This Year` for transactions in calendar year 2020
    - `Last Year` for transactions in calendar year 2019
  - Exclude transactions that are not in 2019 or 2020 (i.e., any rows that cannot be categorised as `This Year` or `Last Year`).

- Create a daily Targets table from the weekly Targets input:
  - For each weekly target row (by `Year`, `Week`, and `ProductName`), generate one row per calendar date that belongs to that target week according to the custom Week definition:
    - For Week 1, generate rows for each day from Jan 1 through the first Saturday (which may be fewer than 7 dates).
    - For all other weeks, generate exactly 7 daily rows (Sunday through Saturday).
  - Split weekly targets evenly across the week using:
    - `Quantity` per day = (`Quantity Target`) / 7
    - `Income` per day = (`Income Target`) / 7
    - Apply this same “divide by 7” rule even for Week 1 (so Week 1’s daily rows use weekly_target/7, and the sum of the generated Week 1 daily values will be less than the weekly target if Week 1 has fewer than 7 dates).
  - Assign `Type = Target` to these daily target rows.
  - Derive `Week` and `Day` for each generated target date using the same custom Week/Day calendar.

- Combine Transactions and daily Targets:
  - Union the transaction rows (with fields `Date`, `Week`, `Day`, `ProductName`, `Quantity`, `Income`, `Type`) with the generated daily target rows at the same daily grain.

- Apply a consistent Year-to-Date cutoff using Week/Day alignment (not calendar date) based on the anchor date Friday 9th October 2020:
  - Compute the anchor’s `Week` and `Day` within 2020 using the custom Week/Day calendar. (Under this calendar, the anchor is Week 41, Day 6.)
  - For all three Types (`This Year`, `Last Year`, `Target`), keep only rows with:
    - `Week` < anchor_week, OR
    - `Week` = anchor_week AND `Day` <= anchor_day.
  - This filtered dataset defines the YTD record set for each Type and is also the base data used for subsequent aggregations.

- Calculate YTD, MTD, and WTD values for each product and each metric:
  - Metrics to report: `Income` and `Quantity`.
  - Output grain: one row per (`ProductName`, `Metric`, `Time Period`), with side-by-side values for `This Year`, `Last Year`, and `Target`.
  - YTD:
    - For each product and metric, sum the metric over rows up to the anchor Week/Day (as defined above) separately for each `Type`.
  - MTD (October-to-date):
    - `This Year`: sum over dates from 2020-10-01 through 2020-10-09 inclusive.
    - `Target`: sum over dates from 2020-10-01 through 2020-10-09 inclusive.
    - `Last Year`: sum over dates from 2019-10-01 through an aligned cutoff date in 2019 inclusive, where the aligned cutoff date is the date in 2019 that matches the anchor’s position by:
      - using the same week index relative to the first Sunday of each year (Week 2 start), and
      - using the same Day-of-week position within that week (Day 1–7).
  - WTD:
    - For each `Type`, sum only rows in the anchor week (Week 41) with `Day` <= 6.

- Rounding and percentage calculations:
  - Round all aggregated metric values (`This Year`, `Last Year`, `Target`) to 0 decimal places and store them as integers.
  - Compute percentage differences using the rounded integer values:
    - `% Difference to Last Year` = round((This Year − Last Year) / Last Year, 2)
    - `% Difference to Target` = round((This Year − Target) / Target, 2)
    - If the denominator (Last Year or Target) is 0, set the corresponding percent difference to 0.0.
  - Percent differences must be to 2 decimal places.

- Output the data.

## Output

- output_01.csv
  - 8 fields:
    - ProductName
    - Metric
    - Time Period
    - This Year
    - Last Year
    - Target
    - % Difference to Last Year
    - % Difference to Target