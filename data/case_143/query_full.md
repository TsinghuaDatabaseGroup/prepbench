## Context

You are preparing a daily cycling summary for Carl, splitting total riding distance between outdoor rides and turbo-trainer sessions, and counting how many activities occurred each day. The final dataset must cover every calendar date in a fixed period, including days with no activity.

## Requirements

- Input the data from `inputs/input_01.csv`.
- Treat each input row as a recorded cycling session with at least:
  - `Date` (session date),
  - `Measure` (the unit the session was recorded in),
  - `Value` (the magnitude in that unit),
  - `Detail` (used to determine whether certain sessions are valid activities).
- Convert the `Value` field into kilometres ridden:
  - If `Measure` indicates minutes, convert minutes to kilometres using Carl’s average speed of **30 km/h**, i.e. **0.5 km per minute** (kilometres = minutes × 0.5).
  - If `Measure` indicates kilometres, use the recorded kilometres as the distance **only when the session is considered a valid activity** (see activity rules below); otherwise set the distance to 0 for that row.
- Create a field (conceptually “measure”/category) with exactly two values:
  - `Outdoors` for sessions measured in kilometres (`Measure` = km).
  - `Turbo Trainer` for sessions measured in minutes (`Measure` = min).
- Define whether each input row counts as an “activity” for the daily activity count:
  - All `Measure` = min rows count as 1 activity.
  - `Measure` = km rows count as 1 activity **only if** `Detail` is present (non-empty); otherwise they count as 0 activities.
- Aggregate to a daily grain:
  - One output row must represent **one calendar date**.
  - For each date, compute:
    - Total kilometres for `Turbo Trainer` (sum of converted kilometres for min-measured sessions on that date).
    - Total kilometres for `Outdoors` (sum of kilometres for valid km-measured sessions on that date).
    - `Activities per day` as the total count of activities on that date (sum of the per-row activity indicator across all sessions that date).
- Create separate output columns for `Outdoors` and `Turbo Trainer` distances (wide format).
- Ensure there is a row for **every date** between **1st Jan 2021 and 1st Nov 2021 inclusive**:
  - If a date has no sessions, include it with zero distances and zero activities.
- Change any null/missing values in the output metrics to zero:
  - Distances should be numeric zeros.
  - `Activities per day` should be 0.
- “Work out how many days I did no activities” by ensuring the dataset clearly identifies such days via `Activities per day = 0` (no additional output file or field is required beyond what is specified).
- Output the data:
  - Write `Date` to the CSV in `DD/MM/YYYY` format.
  - Use the exact column names and column order specified below.

## Output

- output_01.csv
  - 4 fields:
    - Turbo Trainer
    - Outdoors
    - Date
    - Activities per day