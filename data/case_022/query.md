## Context

As heavy Tableau users at Chin & Beard Suds Co, our users keep asking us to show if it is possible to create a Moving Average. As any Tableau User will know, this is super easy to set up in a table calculation but harder to do at the data preparation stage to hard code that value for use in other calculations that you might want to have happen earlier in Tableau's Order of Operations. Therefore, this week is focused on our daily sales at the start of 2019 and how we can work out the weekly average (using the 7 days before the current date) to work that out.

## Requirements

- Input the data
- Determine the weekly average sales for the current day and the previous six
- Don't create a moving average if it isn't the average of seven days sales.
- Clean-up the data for output by removing unnecessary columns
- Output the data

## Output

- output_01.csv
  - 3 fields:
    - Date
    - Sales
    - Moving Avg Sales
