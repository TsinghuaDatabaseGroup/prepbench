## Context

You are given engagement assignments for consultants, including an engagement identifier, grade, day rate, and a start/end date. The objective is to (1) expand each assignment into daily participation records, excluding weekends, (2) compute the calendar-day span of each engagement from its start and end dates (including weekends), (3) aggregate to consultant–engagement level revenue and associated attributes, and (4) rank consultants by earned day-rate totals overall and within grade for each engagement record.

## Requirements

- Input the data from `input_01.csv`.

- For each input record, compute **Calendar Days** as the difference in whole days between `Engagement End Date` and `Engagement Start Date`, equivalent to `DATEDIFF('day', start_date, end_date)`.  
  - This value may be negative if the start date is after the end date.

- Create a daily row for each day a consultant is on the engagement, then remove weekend days:
  - If `Engagement Start Date` ≤ `Engagement End Date`, generate the full inclusive daily date sequence from start through end (one row per calendar date).
  - If `Engagement Start Date` > `Engagement End Date`, do not generate an in-between range; instead, consider only the two dates `{start, end}` as the set of candidate days.
  - Keep only weekdays (Monday–Friday). Discard Saturday and Sunday rows.

- Aggregate the resulting weekday-level rows to the consultant–engagement level using:
  - Grouping keys: `Initials`, `Engagement Order`, `Grade Name`.
  - **Day Rate (output field)**: sum of the input `Day Rate` across all retained weekday rows in the group (i.e., day rate multiplied by the number of retained weekdays, summed across any contributing records).
  - **Calendar Days**: attach the previously computed calendar-day value for that same (`Initials`, `Engagement Order`, `Grade Name`) combination (if multiple source records exist for the same key, use the calendar-day value from the first occurrence).
  - Retain `Initials`, `Engagement Order`, and `Grade Name` in the aggregated output.
  - Only include groups that have at least one retained weekday row (i.e., at least one non-weekend day generated).

- Rank the aggregated rows by **Day Rate** (descending), using competition ranking (ties receive the same rank, and the next rank is not skipped within the tie group’s minimum position):
  - **Overall Rank**: rank across all aggregated rows.
  - **Grade Rank**: rank within each `Grade Name` subgroup.

- Output the final dataset with the required fields and types:
  - Cast numeric output fields to integers: `Calendar Days`, `Engagement Order`, `Day Rate`, `Overall Rank`, `Grade Rank`.

- Output the data (for a deterministic file), sorting rows by: `Overall Rank` ascending, then `Grade Rank` ascending, then `Initials` ascending, then `Engagement Order` ascending.

## Output

- output_01.csv
  - 7 fields:
    - Calendar Days
    - Initials
    - Engagement Order
    - Grade Name
    - Day Rate
    - Overall Rank
    - Grade Rank