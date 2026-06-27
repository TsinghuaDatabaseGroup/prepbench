## Context

You are producing a subject-level staffing and capacity summary for a school. Using the provided students, teachers, rooms, and age-based teaching-hours rules, calculate (by subject) the total weekly teaching hours required, the number of classes required, the total potential weekly teacher hours available, and the resulting utilization percentage.

## Requirements

- Input the data from the following files:
  - `input_01.csv`: teachers (includes at least teacher `Name`, `Subject`, and `Working Days`)
  - `input_02.csv`: students (includes at least student `Name`, `Age`, and `Subject`)
  - `input_03.csv`: rooms (includes at least `Subjects` and `Capacity`)
  - `input_04.csv`: weekly teaching hours requirement by age group (includes at least `Age Group` and `Hours teaching per week`)

- Determine how many students are in each year/age band for each subject:
  - If a student is listed with multiple subjects in the `Subject` field separated by `/`, treat this as enrollment in multiple subjects by splitting into one row per subject before counting.
  - Convert each student's `Age` into an `Age Group` using only these inclusive ranges:
    - `13-14` for ages 13–14
    - `15-16` for ages 15–16
    - `17-18` for ages 17–18
  - Count students at the grain of (`Subject`, `Age Group`) to produce `Student Count`.

- Work out how many hours of teaching are required for the students based on the age of the students:
  - Join the (`Subject`, `Age Group`) student counts to `input_04.csv` on `Age Group` to obtain `Hours teaching per week` for that age group.

- Work out the room capacity for each subject:
  - From `input_03.csv`, treat the column `Subjects` as the subject identifier and aggregate to total room capacity per subject:
    - `Total Capacity` (per `Subject`) = sum of `Capacity` across all rooms for that subject.

- Compute classes needed and teaching hours needed at the (`Subject`, `Age Group`) level:
  - Join in `Total Capacity` by `Subject`.
  - For each (`Subject`, `Age Group`):
    - `Classes Needed` = ceil(`Student Count` / `Total Capacity`)
    - `Teaching Hours` = `Classes Needed` * `Hours teaching per week`

- Aggregate to subject-level requirements:
  - `Classes required` (per `Subject`) is based on the sum of `Classes Needed` across all age groups for that subject, plus a subject-specific increment:
    - If `Subject` is `Physics`: `Classes required` = sum(`Classes Needed`) + 2
    - Otherwise: `Classes required` = sum(`Classes Needed`) + 1
  - `Total Teaching Hours needed` (per `Subject`) is based on the sum of `Teaching Hours` across all age groups for that subject, plus a subject-specific increment:
    - If `Subject` is `Physics`: `Total Teaching Hours needed` = sum(`Teaching Hours`) + 6
    - Otherwise: `Total Teaching Hours needed` = sum(`Teaching Hours`) + 1

- By assessing the number of days someone works, how many hours of teaching are potentially available within a week:
  - Each day has 6 hours of potential teaching (9–12 and 1–4), so weekly hours are based on working days.
  - For each teacher record, compute:
    - `Working Days Count` = number of comma-separated day tokens in `Working Days`
    - `Weekly Hours` = `Working Days Count` * 6
  - Teachers who cover multiple subjects should have an even allocation of their time between those subjects:
    - For each teacher `Name`, compute `Subject Count` = number of distinct subjects they teach (based on distinct `Subject` values across all rows for that `Name`).
    - For each teacher-subject row, allocate `Teacher Hours` = `Weekly Hours` / `Subject Count`.
  - `Potential Teachers Hours` (per `Subject`) = sum of `Teacher Hours` across all teacher-subject rows for that subject.

- Using that dataset calculate, at the subject level:
  - `Potential Teachers Hours`
  - `Total Teaching Hours needed`
  - `Classes required`
  - `% utilised` = round((`Total Teaching Hours needed` / `Potential Teachers Hours`) * 100) to the nearest whole percent
    - If `Potential Teachers Hours` is 0 for a subject, set `% utilised` to 0.

- Combine results into a single subject-level output table:
  - Use a full outer join on `Subject` so that subjects present in any intermediate result (requirements or potential hours) appear in the final output.
  - Cast `Potential Teachers Hours`, `Total Teaching Hours needed`, `Classes required`, and `% utilised` to integers in the final output.
  - Sort the final output by `Subject` ascending.

- Output the data.

## Output

- output_01.csv
  - 5 fields:
    - Subject
    - Potential Teachers Hours
    - Total Teaching Hours needed
    - Classes required
    - % utilised