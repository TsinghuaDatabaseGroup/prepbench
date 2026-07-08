## Context
A new school-year schedule for birthday celebrations must account for the Early May Bank Holiday on 05/05/2025 (during term time). Any birthday that would be celebrated on that Monday should instead be celebrated on Friday 02/05/2025 so cakes are ready before the long weekend.

## Requirements
- Input the data.
- Update the input to use the 2024 Week 34 input.
- Treat each student’s birthday as a celebration date within the school’s academic year calendar, using:
  - `input_01.csv` for pupils (including at least `pupil first name`, `pupil last name`, and `Date of Birth`).
  - `input_02.csv` for the academic calendar, where each row has a `Term`, `Starts`, and `Ends` date (with `Starts`/`Ends` interpreted as inclusive bounds).
- Watch out for duplicate rows!
- Build the set of valid school days from the calendar:
  - Interpret calendar rows whose `Term` name matches the structure “Autumn, Term N”, “Spring, Term N”, or “Summer, Term N” (for any integer N) as *teaching terms* (included intervals).
  - Treat all other calendar rows (e.g., holidays, half-terms, bank holidays) as *exclusions*.
  - A date is a school day if and only if it:
    - Falls on a weekday (Monday–Friday),
    - Falls within at least one included (teaching term) interval, and
    - Does not fall within any excluded interval.
  - Define the academic-year bounds as:
    - `min_day` = the earliest start date across included intervals
    - `max_day` = the latest end date across included intervals
- Map each student’s `Date of Birth` to a celebration date in the academic year:
  - Extract the month and day from the date of birth.
  - Assign the celebration year as:
    - `min_day.year` if the birthday month is September–December,
    - otherwise `max_day.year` (January–August).
  - Construct the initial “mapped birthday” date from that year plus the birth month/day.
- Convert the mapped birthday into a final “Cake Day”:
  - If the mapped birthday is a school day, use it unchanged.
  - If the mapped birthday is not a school day, roll it back one day at a time until reaching the most recent prior school day.
  - Special case required: if the mapped birthday is exactly 05/05/2025, set the Cake Day explicitly to Friday 02/05/2025 (regardless of other rules).
  - If rolling back would move earlier than `min_day`, drop that student from the output (no Cake Day).
  - After adjustment, keep only Cake Days that fall within the inclusive range [`min_day`, `max_day`].
- Aggregate results:
  - Group by Cake Day and count how many students are assigned to each Cake Day.
  - Derive `Cake Weekday` as the weekday name of the Cake Day.
  - Format `Cake Day` as `DD/MM/YYYY` and `Cake Weekday` as the full weekday name in English.
- Output the data.

## Output

- output_01.csv
  - 3 fields:
    - Cake Day
    - Cake Weekday
    - Count of Cakes