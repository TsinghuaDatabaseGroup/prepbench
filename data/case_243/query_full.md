## Context

The school captured each student’s subject selections in a timetable-oriented layout, including both current classes and classes the student later dropped. The goal is to reshape this log into a subject-level summary that shows how many enrollments remain active versus have dropped, and to calculate each subject’s drop-out rate. Because subjects were manually entered, subject names must be standardised before reporting.

## Requirements

- Input the data from `input_01.csv`, ensuring the first row is interpreted as column headers.
- Reshape the data so that each student–class-choice appears as a separate row:
  - Treat `Name` as the student identifier.
  - Unpivot (pivot longer) all columns whose header contains the word `Class` into two fields:
    - `class_flag` = the original column name (e.g., a class slot indicator)
    - `Subject` = the recorded subject value for that slot
- Standardise subject names and exclude null subject selections:
  - If `Subject` is missing/blank or explicitly indicates a null, treat it as null.
  - Map each non-null subject entry to a single canonical subject name by assigning it to the closest match among the following canonical set:
    - French, English, Science, History, Math, Physical Education, Geography
  - After standardisation, remove rows where `Subject` is null.
- Create an `Active Flag` field to classify each class-choice row as either active or dropped:
  - Derive the status from `class_flag` by removing any digits and trimming the result.
  - Map status labels as follows:
    - `Class` → `Active`
    - `Dropped Class` → `Drop Outs`
  - Remove any rows where `Active Flag` cannot be determined from this mapping.
- Aggregate to count enrollments by subject and status:
  - Group by `Subject` and `Active Flag`.
  - Count rows using a non-distinct count of student records (i.e., use simple count, not count distinct).
- Pivot the aggregated results to produce one row per `Subject` with separate columns for:
  - `Active` (count of active enrollments)
  - `Drop Outs` (count of dropped enrollments)
  - If a subject has no rows for one of the statuses, set the missing status count to 0.
- Create row-level calculations:
  - `Total Enrolled` = `Active` + `Drop Outs`
  - `Drop Out Rate` = `Drop Outs` / `Total Enrolled`, rounded to 9 decimal places
- Order the final output by subject in this sequence: French, English, Science, History, Math, Physical Education, Geography.
- Output the data as specified.

## Output

- output_01.csv
  - 5 fields:
    - Subject
    - Drop Outs
    - Active
    - Total Enrolled
    - Drop Out Rate