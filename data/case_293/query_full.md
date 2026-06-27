## Context

You are preparing a cleaned, standardized view of consultant engagements. The goal is to (1) derive consultant initials, (2) construct proper engagement start/end dates using a fixed year, (3) standardize each consultant’s grade to their minimum grade in the dataset, (4) order engagements chronologically per consultant, (5) remove overlapping engagements per consultant based on that order, and (6) enrich the result with grade name and day rate.

## Requirements

- Input the data.
  - Read engagements from `input_01.csv`.
  - Read grade reference data from `input_02.csv` (contains grade identifier, grade name, and day rate).
  - Read the initials lookup from `input_03.csv` (maps an ID to a single-letter initial).

- Create an `Initials` field that is formed as two letters.
  - Use the `Consultant Forename` and `Consultant Surname` fields from the engagements data as keys into the initials lookup.
  - Construct `Initials` as: (forename initial letter) + (surname initial letter), yielding a 2-character string (e.g., “CA”).

- Create an engagement start date and an engagement end date (the year is 2024 in case you are doing this task after the normal release week).
  - Build `Engagement Start Date` from `Engagement Start Day` and `Engagement Start Month` with year fixed to 2024.
  - Build `Engagement End Date` from `Engagement End Day` and `Engagement End Month` with year fixed to 2024.

- Clean up the Grade field by finding the minimum grade per person within the data set (call this field “Corrected Grade”).
  - Treat each person as identified by `Initials`.
  - For each `Initials`, compute the minimum numeric value of `Grade` across that person’s engagements; use this as the corrected grade identifier for all of that person’s engagements.

- Apply a validation rule for inverted date ranges on duplicated start dates.
  - Within each person (`Initials`), if there are multiple engagements sharing the same `Engagement Start Date`, remove only those rows among that duplicated-start-date set where `Engagement End Date` is earlier than `Engagement Start Date`.
  - Do not apply this removal to rows whose start date is unique for that person.

- Join on the Grade details and remove the join clause fields.
  - Join the engagements to the grade reference data using the corrected grade identifier (the minimum grade per person) as the key.
  - Use a left join so that all engagements remain even if grade details are missing.
  - After the join, retain only the fields required in the output (i.e., do not carry join-key/helper columns into the final output).

- Create an “Engagement Order” based on the Engagement Start Date.
  - For each `Initials`, sort engagements by `Engagement Start Date` ascending; for ties on the same start date, sort by `Engagement End Date` ascending.
  - Assign `Engagement Order` as a 1-based sequence number in this sorted order for each person.
  - Do not recompute or renumber `Engagement Order` after subsequent filtering steps.

- For each individual person (identified by unique initials), remove any engagements where the start date occurs before the previous Engagement End Date.
  - Using the sorted order described above, compare each row’s `Engagement Start Date` to the immediately previous row’s `Engagement End Date` for the same `Initials`.
  - Keep a row if it is the first engagement for that person, or if `Engagement Start Date` is greater than or equal to the previous row’s `Engagement End Date`.
  - Remove a row if `Engagement Start Date` is strictly earlier than the previous row’s `Engagement End Date`.

- Output the data.
  - Format `Engagement Start Date` and `Engagement End Date` as `DD/MM/YYYY` text in the output file.

## Output

- output_01.csv
  - 6 fields:
    - Engagement Start Date
    - Engagement End Date
    - Initials
    - Engagement Order
    - Grade Name
    - Day Rate