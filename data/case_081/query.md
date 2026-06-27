## Context
This week we're looking at a slightly odd way that Chin & Beard Suds Co have been structuring their store sales and target data: As you can see, for each Store, there are 3 rows, the first being the Sales values, the second row containing the Target values for each month and the third row containing the difference between these values. It's your job to transform this monstrosity unique table into a more conventional output that we could use in Tableau Desktop.

## Requirements

- Input the data
- Make sure Store names have filled down correctly and remove nulls
- Pivot to create a Month column
- In the most dynamic way possible, assign each row a description of either Sales, Target or Difference
  - Hint: the Sales value will have the lowest Row ID value for each Store
  - Hint Hint: how can string calculations mid and findnth help you to extract the relevant value?
- Reshape the data so that there is one row for each Store for each Month
- Change the Month field to a Date data type (these months are all from 2020)
- Output the data

## Output

- output_01.csv
  - 5 fields:
    - Store
    - Month
    - Sales
    - Target
    - Difference
