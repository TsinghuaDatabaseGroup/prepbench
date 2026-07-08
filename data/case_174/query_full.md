## Context

You are preparing an opportunity stage timeline dataset by combining (a) key milestone dates from the core Opportunity table and (b) all recorded stage-transition events from the Opportunity History table. The final result should be a single, row-based event log where each row represents one opportunity at one point-in-time with an associated stage label and a numeric sort order.

## Requirements

- Input the data.
- Use two inputs:
  - **Opportunity table** (from `input_02.csv`), using the fields `Id`, `CreatedDate`, `CloseDate`, and `StageName`.
  - **Opportunity History table** (from `input_01.csv`), using the fields `OppID`, `CreatedDate`, `StageName`, and `SortOrder`.
- For the Opportunity table, reshape the data so it contributes milestone rows to the timeline:
  - Rename `Id` to `OppID`.
  - Create an **Opened** milestone row for every opportunity:
    - Set `Date` = `CreatedDate`
    - Set `Stage` = `Opened`
    - Set `SortOrder` = `0`
  - Create an **ExpectedCloseDate** milestone row only for opportunities that are **not closed** (i.e., whose `StageName` is neither `Closed Won` nor `Closed Lost`):
    - Set `Date` = `CloseDate`
    - Set `Stage` = `ExpectedCloseDate`
    - Set `SortOrder` = `11`
  - Keep only the four output fields from these milestone rows (`OppID`, `Date`, `Stage`, `SortOrder`) and remove all other Opportunity fields.
- Bring in the additional information from the Opportunity History table about when each opportunity moved between each stage:
  - Rename `CreatedDate` to `Date`.
  - Rename `StageName` to `Stage`.
  - Keep only `OppID`, `Date`, `Stage`, and `SortOrder`.
- Combine (union/append) the Opportunity-derived milestone rows with the Opportunity History rows into a single dataset (do not require matches; include all rows from both sources).
- Ensure each row has a `SortOrder`:
  - The generated **Opened** rows must have `SortOrder = 0`.
  - The generated **ExpectedCloseDate** rows must have `SortOrder = 11`.
  - History rows must use the `SortOrder` provided by the Opportunity History input.
- Remove duplicate rows that may have occurred when bringing together the two tables:
  - Treat rows as duplicates if all four fields match: `OppID`, `Date`, `Stage`, `SortOrder`.
  - Keep the first occurrence of each duplicate group.
- Output the data.

## Output

- output_01.csv
  - 4 fields:
    - OppID
    - Date
    - Stage
    - SortOrder