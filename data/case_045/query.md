## Context
Data is everywhere and often in annoyingly small files that we need to piece together before we can begin analysis; Chin & Beard Suds Co is no different.
This week's challenge is to piece together data we have received from our Clapham and Wimbledon stores. We've heard there are lots of differences between our two stores in South West London for Sales Volumes and Values. We've heard there are duplicates in the dataset so help us remove these as the entries are the same, just doubled up due to some reporting issues.

## Requirements

- Input the data
- Remove Duplicates (identical rows)
- Work out the percentage of:
  - Scent sales per Store's Total Sales Values and Volumes
  - Weekday sales per Store Total Sales Values and Volumes
- Replace Weekday with full date
- Output the data

## Output

- output_01.csv
  - 4 fields:
    - Store
    - Scent
    - Scent % of Store Sales Volumes
    - Scent % of Store Sales Values

- output_02.csv
  - 4 fields:
    - Store
    - Dates
    - Weekday % of Store Sales Volumes
    - Weekday % of Store Sales Value
