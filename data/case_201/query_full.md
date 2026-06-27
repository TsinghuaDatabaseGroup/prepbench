## Context

The Talent Acquisition team wants to understand where in the hiring process candidates are choosing to withdraw. For each status that preceded a withdrawal, calculate the percentage of candidates who withdrew after reaching that status.

## Requirements

- Input the data from `input_01.csv`.
- Parse the `ts` column as a datetime using format `DD/MM/YYYY HH:MM:SS`.
- For each (candidate_id, position_id) combination, rank statuses by timestamp descending (most recent = rank 1). Use method `first` for tie-breaking.
- Identify candidate-position pairs where the most recent status (rank 1) is "Candidate Withdrew".
- For those pairs, find the previous status (rank 2) and label it as the status before withdrawal.
- Count the number of withdrawals grouped by the status before withdrawal.
- Separately, count the total number of distinct (candidate_id, position_id) pairs that have ever been in each status.
- Join the withdrawal counts to the total counts by status, using a left join on the total counts side so that statuses with zero withdrawals are included.
- Fill missing withdrawal counts with 0.
- Calculate `pct_withdrawn` as `(withdrawals / total_in_status) * 100`, rounded to 1 decimal place.
- Output columns in order: `status_before_withdrawal`, `withdrawals`, `total_in_status`, `pct_withdrawn`.

## Output

- output_01.csv
  - 4 fields:
    - status_before_withdrawal
    - withdrawals
    - total_in_status
    - pct_withdrawn
