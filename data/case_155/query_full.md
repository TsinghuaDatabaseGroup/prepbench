## Context

You are preparing a summarized view of pupils’ school travel choices by weekday. The goal is to reshape the input so each trip is represented at the weekday level, standardize travel method labels to remove spelling inconsistencies, classify each method as Sustainable vs Non-Sustainable, and then compute daily trip counts and percentages by method.

## Requirements

- Input the data.
- Join the data sets together based on their common field.
  - If only a single input table is provided for this task, no join is required; proceed using that table as the combined dataset.
- Remove any fields you don't need for the challenge, keeping only the fields required to compute the requested outputs.
- Change the weekdays from separate columns to one column of weekdays and one of the pupil's travel choice:
  - Treat each pupil as taking one trip per weekday recorded in the input.
  - Reshape the weekday columns `M`, `Tu`, `W`, `Th`, `F` into a long format with:
    - `Weekday` containing the weekday code (`M`, `Tu`, `W`, `Th`, `F`)
    - `Method of Travel` containing the corresponding travel choice for that weekday
  - The output grain after reshaping is: one row per (pupil, weekday) trip.
- Group the travel choices together to remove spelling mistakes:
  - Standardize `Method of Travel` to a consistent canonical set so that spelling variations collapse into the same method name.
  - The canonical method names to use (when applicable) are:
    - `Bicycle`, `Car`, `Scooter`, `Walk`, `Van`, `Aeroplane`, `Helicopter`, `Mum's Shoulders`, `Dad's Shoulders`, `Hopped`, `Skipped`, `Jumped`.
- Create a Sustainable (non-motorised) vs Non-Sustainable (motorised) data field:
  - Create a field named `Sustainable?` with values `Sustainable` or `Non-Sustainable`.
  - Classify as `Sustainable` if `Method of Travel` is one of:
    - `Walk`, `Bicycle`, `Scooter`, `Mum's Shoulders`, `Dad's Shoulders`, `Hopped`, `Skipped`, `Jumped`
  - Otherwise classify as `Non-Sustainable`.
  - Scooters are the child type rather than the motorised type (i.e., treat `Scooter` as `Sustainable`).
- Total up the number of pupil's travelling by each method of travel:
  - Aggregate to counts at the level of (`Sustainable?`, `Method of Travel`, `Weekday`).
  - The count must be output as `Number of Trips`.
- Work out the % of trips taken by each method of travel each day:
  - Define `Trips per day` as the total number of pupils (i.e., the number of distinct rows/students in the original wide input table), so it is constant across weekdays.
  - Compute `% of trips per day` as:
    - `Number of Trips / Trips per day`
    - Round to 2 decimal places.
- Output the data:
  - Output exactly the 6 required fields with the specified names.
  - Sort the final output rows by:
    1) `% of trips per day` descending
    2) `Sustainable?` ascending
    3) `Weekday` ascending
    4) `Method of Travel` ascending

## Output

- output_01.csv
  - 6 fields:
    - Sustainable?
    - % of trips per day
    - Trips per day
    - Number of Trips
    - Weekday
    - Method of Travel