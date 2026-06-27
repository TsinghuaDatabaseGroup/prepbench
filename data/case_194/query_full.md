## Context

You are given training session scores for players across multiple dates. Previous logic already handles filling in missing sessions after their first occurrence by carrying forward scores. Now, for sessions whose first recorded date is after the earliest date in the dataset, dates between the global minimum date and the day before that first session must be filled with a score of 0 and flagged as "Pre First Session."

## Requirements

- Input the data from `input_01.csv`.
- Parse the `Date` column as a datetime field.
- For each unique (Player, Session) combination, identify the first session date.
- Compute the global minimum date across the entire dataset.
- For every (Player, Session), generate rows for all weekdays (Monday through Friday) from the global minimum date up to (but not including) that combination's first session date:
  - Set `Score` to 0.
  - Set `Flag` to "Pre First Session".
- For all existing sessions and missing weekdays between sessions (up to the global maximum date):
  - Mark rows with actual data as `Flag = "Actual"`.
  - Carry forward the previous score for missing weekdays and mark them as `Flag = "Carried over"`.
- Combine the "Pre First Session" rows with the "Actual" and "Carried over" rows.
- Deduplicate by (Player, Session, Date), keeping the first occurrence (which preserves "Pre First Session" rows over "Carried over" rows when they overlap).
- Exclude all weekend dates (Saturday and Sunday) from the final output.
- Format `Session Date` as `DD/MM/YYYY`.
- Output columns in order: `Flag`, `Session Date`, `Player`, `Session`, `Score`.

## Output

- output_01.csv
  - 5 fields:
    - Player
    - Session
    - Session Date
    - Score
    - Flag
