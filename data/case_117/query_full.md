## Context
Prep Air wants analysis-ready project task data to support a Gantt chart and a dashboard explaining project overruns. The input data records scheduled dates and how many days each task took relative to schedule; you need to derive completion dates, calculate key phase-to-phase durations at the project/sub-project/owner level, and produce a clean, reporting-friendly dataset.

## Requirements
- Input the data from `input_01.csv`.

- Create/standardize the core schedule fields:
  - Parse `Scheduled Date` as a date using the format `YYYY-MM-DD` (fail if the value cannot be parsed).
  - Rename the field `Completed In Days from Scheduled Date` to `Days Difference to Schedule` and treat it as an integer number of days.
  - Calculate `Completed Date` as:
    - `Completed Date = Scheduled Date + (Days Difference to Schedule days)`

- Compute project-level phase durations (this is the point where the workflow conceptually branches to compute group-level metrics and then brings them back to the row level):
  - Define the project grouping keys as: `Project`, `Sub-project`, `Owner`.
  - Create a “wide” view with one row per (`Project`, `Sub-project`, `Owner`) and one column per `Task`, where each task column contains that task’s `Completed Date` for the group.
    - If a group has multiple records for the same `Task`, use the first available `Completed Date` for that task when calculating durations.
    - Ensure the tasks `Scope`, `Build`, and `Deliver` are available for duration calculations; if any are missing for a group, the resulting duration(s) for that group should be null.
  - Calculate two duration fields (in whole days) at the (`Project`, `Sub-project`, `Owner`) level:
    - `Scope to Build Time = (Build Completed Date - Scope Completed Date)` in days
    - `Build to Delivery Time = (Deliver Completed Date - Build Completed Date)` in days

- Bring the duration metrics back to the task-level dataset:
  - Join the group-level duration fields back onto the original row-level data using a left join on (`Project`, `Sub-project`, `Owner`) so every original task row is retained.

- Add calendar/label fields needed for dashboarding:
  - Calculate `Completed Weekday` as the weekday name derived from `Completed Date`.

- Finalize the dataset for output:
  - Format `Scheduled Date` and `Completed Date` as strings in `DD/MM/YYYY`.
  - Ensure `Scope to Build Time`, `Build to Delivery Time`, and `Days Difference to Schedule` are output as integers where values exist.
  - Keep only the required output fields and remove any intermediate/helper fields used for calculations.
  - Preserve a stable ordering of rows by:
    - the first-seen order of each (`Project`, `Sub-project`, `Owner`) group from the input, and within each group
    - `Task` in the order: `Scope`, then `Build`, then `Deliver`.

- Output the data to the required file.

## Output

- output_01.csv
  - 10 fields:
    - Completed Weekday
    - Task
    - Scope to Build Time
    - Build to Delivery Time
    - Days Difference to Schedule
    - Project
    - Sub-project
    - Owner
    - Scheduled Date
    - Completed Date