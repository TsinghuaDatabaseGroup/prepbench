## Context

The applicant tracking system records the statuses and timestamps as a candidate moves through in the hiring process. Each morning, any candidates/positions that changed during the previous day are loaded to the raw table. However, each time a candidate's status changes, we receive all of their previous statuses again, in addition to the new one. We call this dataset "The 12 Days of Christmas," because, like the song, each time a status is added, we get all of the history again. As a result, our dataset has a lot of duplicates! In this challenge, we want to clean up the data by keeping only the most recent set of statuses for each candidate/position.

### Example for candidate 36, position 1:

- Candidate 36 created their profile on 2021-01-12, and we received that status in the 2021-01-13 file.
- On 2021-02-11, candidate 36 completed the application. We received the Application Completed status, plus the Profile Created status (again).
- On 2021-02-12, candidate 36's application for position 1 was reviewed. We received that status (plus all of the previous statuses, again) in the 2021-02-13 file.
- In this example, for candidate 36/position 1, we would only want to keep the records from the 2021-02-28 file, because that is the most recent file received for candidate 36, position 1.

## Requirements

- Input the data
- For each combination of candidate and position, find the most recent file.
  - Watch out - the vendor has not been consistent with file naming. However, the file timestamp is always the 19 characters before ".csv"
  - Filter out any records that are not from the most recent file
- Output the cleaned status history to a CSV file (Output #1)
- Using the cleaned dataset (Output #1), find the most recent status for each candidate/position combination (Output #2)
  - For each candidate/position, find the max timestamp
  - Keep the record that has the max timestamp
  - Keep only the candidate_id, position_id, and status columns
  - Rename the status column to current_status
  - Output the data

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
