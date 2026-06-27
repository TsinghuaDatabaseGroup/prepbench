## Context
This challenge uses data from the Women's Heptathlon at the 2023 World Athletics Championship to analyze whether being a specialist in a few events or a generalist across all events yields better results.

## Requirements
- Input the data
- Rename fields in the results table: POS → Position, ATHLETE → Athlete, NAT → Nationality, POINTS → Total Points
- Remove the duplicate field for the 800m Run event
- Fill down values in the first 4 fields to eliminate nulls
- Remove letters from the Total Points field
- Pivot the data to have one row per event
- Reshape the data to include fields: Event Score, Event Time/Distance, Rolling Total
- Join with the Event Lookup Table
- Split position info (in brackets) from Event Time/Distance and Rolling Total fields, renaming to Event Position and Position After Event
- Sort rows by Position and Event No. order
- Output the data

## Output

- output_01.csv
  - 13 fields:
    - Sort
    - Position
    - Athlete
    - Nationality
    - Total Points
    - Event Name
    - Event Type
    - Event No.
    - Event Time/Distance
    - Event Points
    - Event Position
    - Rolling Total Points
    - Position After Event
