# query_r.md

## Context
The challenge this week is pulling together multiple weeks worth of data that get added by an additional worksheet being added to an Excel Workbook. But, all the files to reference needed to be added in to context using a different spreadsheet (in the same workbook) from our Financial Planner, Jules. Jules' data source is a mess - it's your job to turn it into something useful. Remember no typed calculations or filters! The input data was updated on 20th Feb at 9pm GMT.

## Requirements
- Input the data
- Pull all the Week worksheets together
- Form weekly sales volume and value figures per product
- Prepare the data in the Profit table for comparison against the actual volumes and values
- Join the tables but only bring back those that have exceeded their Profit Min points for both Value and Volume
- Prepare the Budget Volumes and Values for comparison against the actual volumes and values
- Join the tables but only return those that haven't reached the budget expected for either Value or Volume
- Prepare the outputs
- Output the data. Make sure to remove duplicates.

## Output

- output_01.csv
  - 6 fields:
    - Type
    - Week
    - Sales Volume
    - Budget Volume
    - Sales Value
    - Budget Value

- output_02.csv
  - 6 fields:
    - Type
    - Week
    - Sales Volume
    - Sales Value
    - Profit Min Sales Volume
    - Profit Min Sales Value
