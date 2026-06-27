## Context
The Prep School is interested in monitoring the progress of their students. They are specifically trying to find students whose report grades have declined from 2021 to 2022. Each student’s report card has 4 categories when grading: attainment, attendance, effort, and behaviour. The report card grades of students from 2021 and 2022. Each category is on a scale of1-9; with9 being the best grade.

## Requirements

- Input the data
- Reshape the data so that each student has 4 rows each, with grades for 2021 and2022 being in separate fields
- Calculate the average grade for each year for each student
- Calculate the difference between the average grade of each student from 2021 to 2022
- Categorize each student into the following 3:
  - Improvement (>0)
  - No change (=0)
  - Cause for concern (<0)
- Filter out the data to leave only students with a ‘cause for concern’
- Output the data

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
