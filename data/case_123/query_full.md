## Context
Chin & Beard Suds Co needs a day-by-day view of unscheduled absences to understand how many employees were off work on each calendar day during the period 1 April 2021 to 31 May 2021. The source records absences using a start date and a number of days off, so the task is to expand these records into daily absences, align them to a complete daily date scaffold for the analysis window, and then count how many distinct people are off each day.

## Requirements
- Input the data.
  - Use the absences input (with at least `Name`, `Start Date`, and `Days Off`).
  - Use the scaffold input that provides day offsets to generate the full set of dates in the analysis window.
- Build a data set that has each date listed out between 1st April to 31st May 2021.
  - Treat 2021-04-01 as the base date.
  - Create a `Date` for each scaffold row as: `2021-04-01 + (scaffold_offset in days)`.
  - Keep only dates within the inclusive range 2021-04-01 through 2021-05-31.
  - The resulting scaffold represents the full set of calendar dates (one row per date) for the analysis period.
- Build a data set containing each date someone will be off work.
  - For each absence record, expand it into one row per day of absence.
  - The expanded date list must be inclusive of the `Start Date` and span `Days Off` consecutive calendar days, i.e. the dates are:
    - `Start Date`, `Start Date + 1 day`, …, `Start Date + (Days Off - 1) days`.
  - Each expanded daily row must retain the person identifier (`Name`) and the daily `Date`.
- Merge these two data sets together.
  - First, aggregate the expanded daily absences to daily counts by grouping on `Date` and counting the number of distinct `Name` values per date.
  - Left join the date scaffold (all dates in the analysis window) to the daily counts on `Date` so every scaffold date is present even if nobody was off.
  - For any scaffold date with no matching daily count, set the count to 0.
- Workout the number of people off each day.
  - The metric is the distinct count of people (`Name`) off on each `Date`.
  - Ensure the daily count is an integer.
- Output the data.
  - Output grain: one row per calendar date in the scaffolded analysis window (inclusive from 1 April 2021 to 31 May 2021).
  - Format `Date` as the string `DD/MM/YYYY 00:00:00`.

## Output

- output_01.csv
  - 2 fields:
    - Date
    - Number of people off each day