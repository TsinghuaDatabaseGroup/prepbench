## Context

You are preparing a summary of student nationalities by classroom. The goal is to identify, for each classroom, which nationality has the highest number of students (after applying specified spelling standardization to the Nationality field), and output that top nationality per classroom along with its student count.

## Requirements

- Input the data from:
  - `input_01.csv`, which contains at minimum `Student ID`, `Nationality`, and `Classroom`.
  - `input_02.csv`, which contains at minimum `Student ID` and `Name`.
- Join both datasets on the Student ID. If the join does not affect the required final fields, it may be omitted as long as the final results are computed correctly from the available inputs.
- Group Values by Spelling to get rid of spelling mistakes in the Nationality field by applying these standardizations to `Nationality`:
  - Replace `Meksiko` with `Mexico`
  - Replace `Frans` with `France`
  - Replace `Egipt` with `Egypt`
- Aggregate the dataset to get a count of students within each `Nationality` and `Classroom`:
  - Group by `Classroom` and `Nationality`.
  - Compute the number of distinct students using `Student ID`.
  - Store this count in an output column named `Name` (this field represents the student count).
- Create a calculated field to output the Rank of each Nationality by classroom in descending order:
  - Rank (or equivalently select) nationalities within each classroom by the student count (`Name`) descending.
  - If there is a tie on the count within a classroom, break ties by `Nationality` in ascending (alphabetical) order.
- Filter the Dataset to keep the first-ranking Nationality in each classroom (one row per classroom after applying the ranking/tie-break rules).
- Remove unnecessary fields so that only the required output columns remain.
- Output the data.

## Output

- output_01.csv
  - 3 fields:
    - Nationality
    - Classroom
    - Name