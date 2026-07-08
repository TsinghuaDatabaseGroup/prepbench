## Context
Create a rolling weekly total and average for each Prep Air destination and an overall number for all destinations. The rolling week is as detailed above,3 days before and3 days after a date as well as that day itself.

## Requirements

- Input the data
- Create a data set that gives7 rows per date (unless those dates aren't included in the data set).
  - ie 1st Jan only has4 rows of data (1st,2nd,3rd &4th)
- Remove any additional fields you don't need
- Create the Rolling Week Total and Rolling Week Average per destination
  - Records that have less than7 days data should remain included in the output
- Create the Rolling Week Total and Rolling Week Average for the whole data set
- Pull the data together for the previous two requirements
- Output the data

## Output

- output_01.csv
  - 4 fields:
    - Destination
    - Date
    - Rolling Week Avg
    - Rolling Week Total
