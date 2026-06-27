## Requirements

- Input the data
- Split the data into the years and the x-axis of the chart i.e. the day and month
- For the years, make sure there is a row per year and keep the generated column name field i.e. F1, F2 etc.
- For the day and month rows, number them
- Pivot so we have a row per day/month
- Pivot so we have the days in one field and the months in the other
  - Still keeping the generated column name field
- Fill down the month names
  - That generated column name field will come come in handy for ordering
- Join years back to day & month
- Filter the dataset so that we only have past dates
  - i.e. 1700 - 2023
- Create an Easter Sunday date field and remove all other fields
- Output the data

## Output

- output_01.csv
  - 2 fields:
    - Calculation1
    - Easter Sunday
