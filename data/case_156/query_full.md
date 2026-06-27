## Context
You are given student assessment scores by subject and need to convert numeric scores into (1) letter grades that are evenly distributed within each subject and (2) “high school application points” based on those grades. The analysis goal is to compare students’ total application points against the typical total points earned by students who have achieved at least one A, and then focus only on higher-performing, non‑A grade records.

## Requirements
- Input the data.
- Reshape the input from wide to long format so that each row represents one student’s score in one subject, with at least these columns:
  - `Student ID`
  - `Subject` (the original subject column name)
  - `Score` (the numeric value from that subject column)
- For each `Subject` independently, assign students into 6 evenly distributed groups using this ordering:
  - Primary sort: `Score` descending
  - Tie-breaker: `Student ID` ascending
  - “Evenly distributed” means the subject’s rows are split into six tiles of (as close as possible to) equal size based on rank position in that sorted order; implement this deterministically as:
    - Let `pos` be the zero-based rank position within the subject after sorting (0 for the highest score, 1 for the next, etc.).
    - Let `group_sz` be the total number of rows in that subject.
    - Compute `tile = floor(pos * 6 / group_sz) + 1`, yielding integers 1–6.
- Convert each `tile` into:
  - A letter `Grade` using: 1→A, 2→B, 3→C, 4→D, 5→E, 6→F.
  - A numeric `Points` value using: A→10, B→8, C→6, D→4, E→2, F→1 (equivalently, 1→10, 2→8, 3→6, 4→4, 5→2, 6→1).
- Determine how many high school application points each student has received across all their subjects:
  - For each `Student ID`, compute `Total Points per Student` as the sum of `Points` across all subjects for that student, and attach this total back to every row for that student.
- Work out the average total points per student by grade:
  - For each `Grade`, compute `Avg student total points per grade` as the mean of `Total Points per Student` among rows with that grade.
  - Round `Avg student total points per grade` to 2 decimal places and attach it to each row.
- Take the average total score you get for students who have received at least one A and remove anyone who scored less than this:
  - Use a fixed threshold value of `41.15` for this “average total points for students with at least one A”.
  - Keep only rows where `Total Points per Student` is strictly greater than `41.15`.
- Remove results where students received an A grade (requirement updated2/2/22):
  - After applying the threshold filter, remove any remaining rows where `Grade` is `A`.
- Output the data.

## Output

- output_01.csv
  - 7 fields:
    - Avg student total points per grade
    - Total Points per Student
    - Grade
    - Points
    - Subject
    - Score
    - Student ID