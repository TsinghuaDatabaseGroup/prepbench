## Context
Formula 1 qualifying data should be reduced to one best lap per driver and enriched with driver details for the final classification.

## Requirements
- Input the data
- Clean the lap_duration field so qualifying lap times can be compared
- Identify the quickest lap time per driver
- Join to your driver data
- Rank the drivers by quickest lap time
- Sort to get the correct order for the output
- Output the data

## Output

- output_01.csv
  - 6 fields:
    - Position
    - driver_number
    - driver_code
    - driver_name
    - constructor_sponsor_name
    - lap_duration
