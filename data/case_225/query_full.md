## Context
The Prep School wants to evaluate teaching quality by identifying, for each course/subject, which class performed worst on average over the past year. This will help the school target support and adjust the curriculum where needed.

## Requirements
- Input the data.
  - Use `input_01.csv` as the student score table keyed by `Student ID`, where each subject is represented as a separate column of grades.
  - Use `input_02.csv` as the student metadata table keyed by `Student ID`, containing at least the `Class` assignment for each student.
- Reshape the scores data so that each row represents one student’s grade in one subject (i.e., pivot the subject columns into a single `Subject` column and a single `Grade` column, keeping `Student ID`).
- Join the reshaped scores to the metadata to attach `Class` to each student’s subject-grade record.
  - Join type: left join from the reshaped scores table to the metadata table on `Student ID`.
  - If a student has no matching `Class`, that record cannot contribute to a class average and should not be included in the class-level aggregation.
- Aggregate to compute the average grade for each `(Subject, Class)` combination.
  - Use the mean of `Grade` within each `(Subject, Class)` group.
  - Round the resulting average `Grade` to 1 decimal place.
- Reduce the data to one row per `Subject` by selecting the worst-performing class per subject.
  - “Worst-performing” means the lowest average `Grade` within that `Subject`.
  - If multiple classes are tied for the lowest average grade (after rounding), select the class that comes first in ascending order of `Class`.
  - This step may be implemented via a rank calculation grouped by `Subject` (ranking lower averages as worse) and filtering to rank 1.
- Keep exactly three columns named `Subject`, `Grade`, and `Class`.
- Output the results.

## Output

- output_01.csv
  - 3 fields:
    - Subject
    - Grade
    - Class