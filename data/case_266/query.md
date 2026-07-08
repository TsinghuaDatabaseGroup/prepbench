## Requirements

- Input the data
- Create a row for each day of the year
  - I've chosen to use 2024 for the challenge so results will be different if you select a non-leap year
- Calculate the new months of the year such that the first 28 days of the month are month 1, the next 28 days are month 2, etc
  - This will give you 14 months, with the 14th month containing just 2 days
- Create a new date with the format:
  - New day of the month / New month / 2024
  - e.g. 20/11/2024 becomes 17/12/2024
- Filter the data to only contain dates for which the month has changed in the new system
- Output the data

## Output

- output_01.csv
  - 2 fields:
    - Date
    - New Date
