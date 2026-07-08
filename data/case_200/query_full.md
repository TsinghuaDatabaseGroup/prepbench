## Context

The applicant tracking system records a history of status changes as each candidate progresses through the hiring process for a given position. Each daily load contains all statuses known so far for any candidate/position that changed during the prior day, meaning previously received statuses are repeated alongside any newly added status. The goal is to remove these repeated histories by retaining only the statuses from the most recently received file for each candidate/position pair, and then identify the current (most recent) status per candidate/position.

## Requirements

- Input the data from `inputs/input_01.csv`. The dataset includes (at minimum) `candidate_id`, `position_id`, `status`, `ts` (a status timestamp), and `filename` (the source file name for the load).
- For each `(candidate_id, position_id)` combination, identify the most recent source file and keep only records coming from that file:
  - Derive a file timestamp from `filename` as the 19 characters immediately preceding the string `.csv` (the vendor naming is inconsistent outside of this rule).
  - Parse this extracted file timestamp using the datetime format `YYYY-MM-DD_HH-MM-SS`.
  - For each `(candidate_id, position_id)`, compute the maximum parsed file timestamp.
  - Filter the input to rows whose parsed file timestamp equals that maximum for their `(candidate_id, position_id)`. Rows without a usable parsed file timestamp must not be retained by this filter.
- Produce Output #1 (cleaned status history):
  - Keep only the columns `candidate_id`, `position_id`, `status`, `ts`, and `filename`.
  - Format `ts` as `DD/MM/YYYY HH:MM:SS`.
  - Ensure `candidate_id` and `position_id` are integers in the output.
  - Sort Output #1 by `candidate_id`, then `position_id`, then `ts` (ascending).
  - Output the cleaned status history to a CSV file.
- Produce Output #2 (current status per candidate/position) from the cleaned dataset in Output #1’s underlying row set (i.e., the rows retained from the most recent file per candidate/position):
  - For each `(candidate_id, position_id)`, compute the maximum status timestamp based on `ts` interpreted as a datetime.
  - Keep the record(s) whose status timestamp equals that maximum for their `(candidate_id, position_id)` (if there are ties, retain all tied records).
  - Keep only `candidate_id`, `position_id`, and `status`, and rename `status` to `current_status`.
  - Ensure `candidate_id` and `position_id` are integers in the output.
  - Sort Output #2 by `candidate_id`, then `position_id` (ascending).
  - Output the data to a CSV file.

## Output

- output_01.csv
  - 5 fields:
    - candidate_id
    - position_id
    - status
    - ts
    - filename

- output_02.csv
  - 3 fields:
    - candidate_id
    - position_id
    - current_status