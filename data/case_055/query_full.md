## Context

You are preparing a poll-by-candidate dataset suitable for comparison across polls and polling periods. Starting from the provided poll table, you will remove non-poll summary rows, standardize the polling end date and sample type, reshape the data to one row per candidate per poll-period, and then compute within-poll rankings and the spread between first and second place.

## Requirements

- Input the data from `input_01.csv`.

- Remove the Average Record for the polls:
  - Exclude any rows where `Poll` equals `RCP Average`.

- Clean up your Dates:
  - Use the `Date` field to derive an `End Date` representing the end of the polling period.
  - Extract the end date as the substring after `" - "` in `Date`.
  - Interpret the extracted end date as `M/D` and assign the year as:
    - `2019` if the month is `12`
    - otherwise `2020`
  - Format `End Date` as `DD/MM/YYYY`.
  - If an end date cannot be parsed, set `End Date` to null.

- Rename Sample Types: RV = Registered Voter, LV = Likely Voter, null = Unknown
  - Derive `Sample Type` from the `Sample` field:
    - If `Sample` indicates `LV`, set `Sample Type` to `Likely Voter`.
    - If `Sample` indicates `RV`, set `Sample Type` to `Registered Voter`.
    - If `Sample` is null/blank or does not indicate `LV` or `RV`, set `Sample Type` to `Unknown`.

- Reshape poll results to candidate-level rows:
  - Convert the wide candidate result columns into a long format with:
    - `Candidate` (candidate name)
    - `Poll Results` (the candidate’s result for that poll record)
  - The candidate columns to unpivot are:
    - Sanders, Biden, Bloomberg, Warren, Buttigieg, Klobuchar, Steyer, Gabbard
  - Keep `Poll`, `End Date`, and `Sample Type` as identifier fields for each unpivoted row.

- Remove any Null Poll Results:
  - Remove rows where `Poll Results` is null or is `"--"`.
  - Convert `Poll Results` to a numeric value; remove rows where numeric conversion fails (resulting in null).

- Form a Rank (modified competition) of the candidates per Poll based on their results:
  - Compute ranks within each `(Poll, End Date)` group based on `Poll Results` in descending order.
  - Use modified competition ranking such that ties share the same rank and the next rank reflects the number of tied entries (i.e., equivalent to assigning each value the maximum rank it would occupy among ties).

- Determine the spread for each poll from 1st Place to 2nd Place:
  - For each `(Poll, End Date)` group, compute:
    - `Spread from 1st to 2nd Place` = (highest `Poll Results`) − (second-highest `Poll Results`)
  - If a group has fewer than two valid candidates, set the spread to `0`.
  - Assign the same spread value to all candidate rows within the same `(Poll, End Date)` group.

- Finalize and output the data:
  - Ensure the output has exactly the fields listed below.
  - Use numeric types for `Poll Results` and `Spread from 1st to 2nd Place`, and integer type for `Rank`.
  - Sort the output rows by:
    1. `End Date` ascending (by date value using `DD/MM/YYYY`)
    2. `Poll` ascending
    3. `Rank` ascending
    4. `Candidate` ascending
  - Output the data.

## Output

- output_01.csv
  - 7 fields:
    - Candidate
    - Poll Results
    - Spread from 1st to 2nd Place
    - Rank
    - End Date
    - Sample Type
    - Poll