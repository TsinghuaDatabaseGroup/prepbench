## Context

You are preparing a schedule to help a school plan when to buy birthday cakes for students during the current school year. The school year runs from 1 September through 31 August of the following year. Because cakes are only provided on school days (and are moved earlier when birthdays fall on non-school days), you must calculate each student’s effective “Cake Day” within the school calendar and then count how many cakes are needed on each cake distribution date.

## Requirements

- Input the data.
  - Read the student list from `input_01.csv` and the school calendar (terms/holidays) from `input_02.csv`.

- Determine each student's birthday for this school year.
  - The school year starts on 1st September and ends on 31st August the following year.
  - For each student, construct the “school-year birthday” by taking the month and day from their `Date of Birth` and assigning the year as:
    - 2024 if the birth month is September (9) through December (12),
    - 2025 if the birth month is January (1) through August (8).

- Use the school calendar to define when a date is a “school day”.
  - Interpret each row in `input_02.csv` as a date range with fields:
    - `Term` (name/label),
    - `Starts` (start date, inclusive),
    - `Ends` (end date, inclusive).
  - Classify each range as:
    - a **teaching term** if the `Term` text contains “, term” and does not contain “half term”, “holiday”, or “bank holiday” (case-insensitive),
    - otherwise a **holiday/non-teaching** range.
  - A date is a **school day** if and only if all of the following are true:
    - it is Monday–Friday,
    - it falls within at least one teaching-term date range,
    - it does not fall within any holiday/non-teaching date range.

- Create a Cake Day field that shows when the school needs to buy each student a cake to celebrate their birthday, following these Cake Day rules and boundary behaviors:
  - Identify the start of the cake-eligible period as the start date of the earliest teaching term (chronologically) from the calendar.
  - If a student’s computed school-year birthday falls before that earliest teaching-term start date, exclude the student from cake scheduling for this output (i.e., no Cake Day is produced for them). This aligns with the note that if 1st Sept is a weekend day, those kids will have received their birthday cake in the previous school year.
  - If the birthday falls on a school day, the Cake Day is that same date.
  - If the birthday falls on a Saturday or Sunday:
    - first attempt to set Cake Day to the Friday immediately before that weekend (the most recent Friday prior to the birthday),
    - if that Friday is not a school day, instead set Cake Day to the distribution date for “the previous school term” as defined below.
  - If the birthday falls on a weekday that is not a school day (i.e., during a holiday/non-teaching period), set Cake Day to the last distribution date in the previous school term as defined below.
  - “Last distribution date in the previous school term” must be determined as:
    - Find the most recent teaching term whose end date is strictly earlier than the birthday date.
    - Within that previous teaching term, find the last Friday on or before the term end date that is a school day (searching backward from the term end date).
    - Special case: if the previous term ends on a Monday or Tuesday and that end date is within 4 days after the computed last-Friday date, use the term end date itself as the Cake Day instead of the Friday.
    - If there is no prior teaching term before the birthday date, no Cake Day is produced for that student.

- Count how many cakes are needed for each school day and what day of the week that day is.
  - Keep only students with a non-null Cake Day.
  - For each Cake Day:
    - format `Cake Needed On Date` as `DD/MM/YYYY`,
    - derive `Cake Weekday` as the full weekday name for the Cake Day (e.g., Monday, Tuesday, etc.).
  - Aggregate to one row per unique combination of (`Cake Needed On Date`, `Cake Weekday`) and compute `Count of Cakes` as the number of students assigned to that Cake Day.

- Output the data.

## Output

- output_01.csv
  - 3 fields:
    - Cake Needed On Date
    - Cake Weekday
    - Count of Cakes