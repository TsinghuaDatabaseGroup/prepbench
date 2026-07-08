## Context

You are the Prep School principal and want to analyze student punctuality using the building entry swipe log. The log records each student’s scheduled start time and actual arrival time for each school day in 2022; a missing arrival time indicates the student was absent. Your goals are (1) to determine which day of the week has the latest average arrivals and (2) to identify which students are “very late” most frequently.

## Requirements

- Input the data from `input_01.csv`.

- Treat attendance as follows:
  - Exclude any records where `Arrival Time` is null (these represent absent days and must not contribute to any calculations).

- Construct datetime timestamps needed for lateness calculations:
  - Parse `Date` as a calendar date.
  - Create a scheduled arrival datetime by combining `Date` with `Scheduled Start Time`.
  - Create an actual arrival datetime by combining `Date` with `Arrival Time`.

- Compute daily lateness per record:
  - Calculate `LatenessSeconds = ArrivalDatetime - ScheduledDatetime` in total seconds.
  - This value must be negative when a student arrives before the scheduled time.

### Output 1: Day-of-week lateness ranking

- For each `Day of Week`, compute the average of `LatenessSeconds` across all included (present) records for that day of week.
- For display and ranking in this output:
  - Round the average lateness (in seconds) to the nearest whole second.
  - Replace negative rounded values with 0 (i.e., early arrivals should not reduce the reported lateness for this output).
- Convert the non-negative rounded seconds into two integer fields:
  - `Minutes Late` = floor(seconds / 60)
  - `Seconds Late` = seconds mod 60
- Rank days of the week by this non-negative rounded average lateness in descending order:
  - Sort by the rounded seconds value descending.
  - Assign `Rank` as consecutive integers starting at 1 in the sorted order.
- Ensure the day field is labeled exactly as `Day of the Week` in the final output.

### Output 2: Student “very late” ranking

- Define a “very late” day as a record where `LatenessSeconds` is strictly greater than 5 minutes (i.e., > 300 seconds).
- For each `Student ID`, compute:
  - `present_days`: the count of included (non-null arrival) records for that student.
  - `very_late_days`: the count of that student’s included records where the “very late” condition is met.
- Calculate `% Days Very Late` as:
  - `(very_late_days / present_days) * 100`
  - Round `% Days Very Late` to 1 decimal place.
- Rank students by `% Days Very Late` in descending order, breaking ties by `Student ID` ascending:
  - After sorting, assign `Rank` as consecutive integers starting at 1.

- Create both outputs and write them to the required CSV files.

## Output

- output_01.csv
  - 4 fields:
    - Rank
    - Day of the Week
    - Minutes Late
    - Seconds Late

- output_02.csv
  - 3 fields:
    - Rank
    - Student ID
    - % Days Very Late