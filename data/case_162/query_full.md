## Context

The Prep School’s attendance records contain missing values for lesson metadata. Because each lesson is consistently delivered at the same weekday and time by the same teacher, those stable schedule attributes can be used to complete missing lesson details and then compute average attendance by lesson and subject within each weekday.

## Requirements

- Input the data from `input_01.csv`.
- Treat blank (empty-string) values in `Lesson Name` and `Subject` as missing.
- Fill in missing `Lesson Name` and `Subject` values using the assumption that they are constant within each schedule slot defined by:
  - `Weekday` + `Lesson Time` + `Teacher`
  - Within each such group, fill missing values using values available elsewhere in the same group (so that gaps at the beginning or end of the group can also be filled).
- After filling, compute the mean `Attendance` for each combination of:
  - `Weekday` + `Subject` + `Lesson Name`
  - Name this computed value `Avg. Attendance per Subject & Lesson`.
- Join (left-join) the computed average back onto the row-level dataset using the keys `Weekday`, `Subject`, and `Lesson Name`, so every original row is retained and receives its corresponding average.
- Create the output `Time` field from `Lesson Time` as follows:
  - If `Lesson Time` is in `HH:MM` format (string length 5), output `HH:MM:00`.
  - Otherwise, keep the original `Lesson Time` value as `Time`.
- Ensure the output data types are:
  - `Week` as integer
  - `Attendance` as integer
  - `Avg. Attendance per Subject & Lesson` as float
- Sort the final output rows by `Weekday` in weekday order Monday, Tuesday, Wednesday, Thursday, Friday; then by `Time`; then by `Week` (all ascending).
- Output the data with exactly the required fields and names.

## Output

- output_01.csv
  - 8 fields:
    - Weekday
    - Time
    - Week
    - Teacher
    - Subject
    - Lesson Name
    - Attendance
    - Avg. Attendance per Subject & Lesson