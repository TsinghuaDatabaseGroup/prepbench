## Context
The Prep School wants to monitor student progress by identifying students whose overall report-card performance declined from 2021 to 2022. Each report card contains four graded categories—attainment, attendance, effort, and behaviour—on a 1–9 scale (9 is best). The task is to compare each student’s average grade across these four categories between 2021 and 2022 and retain only those students whose average decreased.

## Requirements
- Input the data from `inputs/input_01.csv`.

- Treat the following as student identifier and demographic fields and carry them through all steps:
  - `student_id`, `first_name`, `last_name`, `Gender`, `D.O.B`

- Reshape the grade data so that, for each student, there are 4 rows (one per category) and the two years’ grades appear in separate fields:
  - Convert the 2021 grade columns into a long format with:
    - a `category` field derived from the four 2021 columns (`2021-attainment`, `2021-effort`, `2021-attendance`, `2021-behaviour`) by removing the `2021-` prefix
    - a numeric `grade_2021` value containing the corresponding 2021 grade
  - Convert the 2022 grade columns into a long format with:
    - a `category` field derived from the four 2022 columns (`2022-attainment`, `2022-effort`, `2022-attendance`, `2022-behaviour`) by removing the `2022-` prefix
    - a numeric `grade_2022` value containing the corresponding 2022 grade
  - Join the 2021-long and 2022-long results using an inner join on:
    - `student_id`, `first_name`, `last_name`, `Gender`, `D.O.B`, and `category`
    - The result should have one row per student per category with both `grade_2021` and `grade_2022` present.

- Calculate the average grade for each year for each student:
  - Group by `student_id`, `first_name`, `last_name`, `Gender`, `D.O.B`
  - Compute:
    - `2021` = mean of `grade_2021` across the four categories
    - `2022` = mean of `grade_2022` across the four categories

- Calculate the difference between the average grade of each student from 2021 to 2022:
  - `Difference = 2022 - 2021`

- Categorize each student into the following 3, based on `Difference`:
  - Improvement (>0)
  - No change (=0)
  - Cause for concern (<0)

- Filter out the data to leave only students with a ‘Cause for concern’ classification.

- Prepare the output with exactly the fields listed in the Output section, and sort the resulting rows by `student_id` in ascending order.

- Output the data.

## Output

- output_01.csv
  - 9 fields:
    - student_id
    - first_name
    - last_name
    - Gender
    - D.O.B
    - 2021
    - 2022
    - Difference
    - Progress