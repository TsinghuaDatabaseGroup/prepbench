## Context
Produce a qualifying classification table for a Formula 1 event by determining each driver’s best (fastest) recorded lap time from the available lap records, then ranking all drivers by that best lap time and enriching the results with driver and constructor details.

## Requirements
- Input the data.
  - Read lap records from `input_01.csv`.
  - Read driver reference data from `input_02.csv`.

- Validate the lap records used for timing.
  - Ensure `lap_duration` is usable as a numeric value; treat non-numeric or missing values as invalid.
  - Exclude any lap rows where `lap_duration` is missing/invalid.
  - Exclude any lap rows where `driver_number` is missing, since results must be produced per driver.

- Determine each driver’s best qualifying lap (output grain = one row per driver).
  - Group the valid lap records by `driver_number`.
  - For each driver, compute their best lap as the minimum `lap_duration`.

- Join to driver data.
  - Left-join the per-driver best-lap table to the driver reference table on `driver_number`.
  - Keep the driver attributes needed for the output (`driver_code`, `driver_name`, `constructor_sponsor_name`); if a driver number has no match in the driver reference table, retain the row with nulls for the missing attributes.

- Rank drivers to assign `Position`.
  - Rank all drivers by `lap_duration` ascending (fastest lap gets `Position` = 1).
  - Break ties using “first occurrence” tie-breaking based on the current row order at the time of ranking (i.e., if two drivers share the same `lap_duration`, the one appearing earlier in the pre-ranking table receives the better position).

- Finalize and output.
  - Select exactly the required output columns and names.
  - Sort the final results by `Position` ascending for readability.
  - Output the data.

## Output

- output_01.csv
  - 6 fields:
    - Position
    - driver_number
    - driver_code
    - driver_name
    - constructor_sponsor_name
    - lap_duration