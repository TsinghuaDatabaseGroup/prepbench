## Context
Create a single, analysis-ready dataset for the Prep School to evaluate the relationship between student attendance and test performance by combining attendance records with test score records and standardising key fields.

## Requirements
- Input the data:
  - Read the attendance dataset from `input_01.csv`.
  - Read the test scores dataset from `input_02.csv`, treating the second row as the header row (i.e., skip the first row before parsing column names and values).
- Join the datasets:
  - Join attendance to test scores using an **inner join** on `student_name`.
  - The resulting dataset should contain only students whose `student_name` exists in both inputs.
  - Output grain: one row per joined test-score record for a `student_name` (i.e., per matched record after the join).
- Clean and standardise fields:
  - Subject spelling corrections: in the `subject` field, correct known misspellings so that:
    - `Sciece` becomes `Science`
    - `Engish` becomes `English`
  - Test score rounding:
    - Create `TestScoreInteger` by rounding `test_score` to the nearest whole number using standard “half up” rounding (e.g., `x -> floor(x + 0.5)`), and store it as an integer.
  - Student name splitting:
    - Split `student_name` into two columns using the first underscore (`_`) as the delimiter:
      - `First Name` = text before the first underscore
      - `Surname` = text after the first underscore
- Attendance flagging:
  - Create `Attendance Flag` from `attendance_percentage` using these rules:
    - If `attendance_percentage` is **greater than or equal to 0.90**, set to `High Attendance`
    - Else if `attendance_percentage` is **greater than or equal to 0.70**, set to `Medium Attendance`
    - Else (i.e., below 0.70), set to `Low Attendance`
- Prepare the final output columns:
  - Rename fields to match the required output naming:
    - `attendance_percentage` → `Attendance_Percentage`
    - `student_id` → `Student_ID`
    - `test_score` → `Test_score`
    - Use the cleaned/derived fields `Subject`, `Attendance Flag`, `First Name`, `Surname`, and `TestScoreInteger` as specified.
- Output the data to the required file.

## Output

- output_01.csv
  - 8 fields:
    - Attendance Flag
    - First Name
    - Surname
    - Attendance_Percentage
    - Student_ID
    - Subject
    - Test_score
    - TestScoreInteger