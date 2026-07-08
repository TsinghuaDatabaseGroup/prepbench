## Context
This week we are going to be focusing on cleaning data ready to answer some questions from our stakeholders.
The input is a csv file (Text File input type on Prep Builder)

## Requirements

- Input the data
- Split the 'Store-Bike' field into 'Store' and 'Bike'
- Clean up the 'Bike' field to leave just three values in the 'Bike' field (Mountain, Gravel, Road)
- Create two different cuts of the date field: 'quarter' and 'day of month'
- Remove the first 10 orders as they are test values
- Output the data

## Output

- output_01.csv
  - 8 fields:
    - Quarter
    - Day of Month
    - Store
    - Bike
    - Order ID
    - Customer Age
    - Bike Value
    - Existing Customer?
