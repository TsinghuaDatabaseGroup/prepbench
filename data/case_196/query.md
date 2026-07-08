## Context
In this dataset, we have the Months going along the top of the table. The row below then gives the Sales and Profit measures for that Month.

## Requirements

- Input the data
- Split off the Year from the first row of data
- Pivot the remaining rows
- Remove the 'F' from all of the F1, F2 etc field names so we have row numbers
- Reshape the data so each row has a Month associated with it
- Reshape the data so the values fall under either Sales or Profit
- Create a Date field using the Month and Year fields
- Output the data

## Output

- output_01.csv
  - 4 fields:
    - Store
    - Date
    - Sales
    - Profit
