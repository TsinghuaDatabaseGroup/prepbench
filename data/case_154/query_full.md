## Context
The Prep School wants to understand how its students are performing across subjects, including whether students are passing and whether performance differs by gender. You will combine student information with subject grades, reshape the grades into an analyzable structure, and then produce per-student summary metrics while anonymising any non-essential personal/parental details.

## Requirements
- Input the data from the two provided files.
- Join the datasets so that each student’s grades are associated with that student’s gender:
  - Join `input_01.csv` (grades) to `input_02.csv` (student details) using an inner join where `input_01.csv`.`Student ID` matches `input_02.csv`.`id`.
  - From the student-details data, retain only the fields needed for this task (gender and the join key) and exclude parental fields from the joined result.
- Reshape the joined grades so that grades are at a consistent grain:
  - Pivot the subject grade columns into a long format that produces one row per **student and subject**, keeping `Student ID` and gender as identifier columns.
  - The resulting pivoted fields must be named exactly:
    - `Subject` (the subject name)
    - `Score` (the grade value)
  - Treat `Score` as numeric for downstream calculations; non-numeric/unparseable values should be handled as missing for calculations.
- Create a per-student average score:
  - For each `Student ID`, compute the mean of `Score` across all subjects (based on the long/pivoted grade rows).
  - Round the per-student average score to **one decimal place**.
  - If the rounded value is a whole number, output it without a decimal (e.g., `83` not `83.0`).
- Create a per-subject pass indicator and then count passed subjects per student:
  - For each student-subject row, record whether the student passed that subject.
  - A subject is passed when `Score` is **75 or above** (inclusive).
  - Aggregate to the student level and count how many subjects each student passed (i.e., sum the pass indicator across that student’s subjects).
- Produce the final per-student dataset:
  - Grain: **one row per student**.
  - Include gender for each student (one value per `Student ID`).
  - Remove any unnecessary intermediate fields so the output contains only the required columns.
  - Sort the final output by `Student ID` in ascending order.
- Output the data.
  - Output `Student ID` and `Passed Subjects` as integer strings with no decimals.

## Output

- output_01.csv
  - 4 fields:
    - Passed Subjects
    - Student's Avg Score
    - Student ID
    - Gender
