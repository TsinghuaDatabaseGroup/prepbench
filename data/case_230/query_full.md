## Context
The Prep School wants to identify the strongest sprint athletes among its students by comparing each student’s recorded sprint time (100m or 200m) against an age- and gender-specific benchmark, and then ranking qualifying students within each event.

## Requirements
- Input the data from the three provided CSV files:
  - A benchmark table containing benchmark thresholds by Gender, Age, and Event.
  - A student table containing each student’s basic information (including `id`, name, gender, and age).
  - A times table containing each student’s sprint event and recorded time (including `id`, event, and time).
- Join student basic information to sprint results:
  - Perform an inner join between the student table and the times table on `id`, so that only students with recorded times are retained.
  - After this join, each row should represent one student’s participation in one sprint event with a recorded time.
- Join the benchmark table to the student-event records:
  - Join benchmarks to the student-event records using the combination of Gender, Age, and Event (i.e., match student gender to benchmark Gender, student age to benchmark Age, and the recorded event to benchmark Event).
  - Use a left join from the student-event records to the benchmark table.
  - Note: the number of rows should still be 300 after the join (i.e., the join must not multiply rows).
- Filter to only students who fall within the benchmark:
  - Keep only rows where the student’s `time` is less than or equal to the matched `Benchmark`.
  - Rows without a matched benchmark must not be kept.
- Apply the time-collection correction rule:
  - Remove any rows for the 200m event where `time` is strictly below 25 seconds.
- Rank students within each event:
  - Compute ranks separately for each Event, ordering from fastest to slowest (ascending `time`).
  - Use competition ranking so that ties receive the same rank and the next rank is skipped accordingly (i.e., the minimum rank within each tie group).
- Output the resulting dataset with the required fields.

## Output

- output_01.csv
  - 9 fields:
    - Rank
    - id
    - first_name
    - last_name
    - Gender
    - Age
    - Event
    - time
    - Benchmark