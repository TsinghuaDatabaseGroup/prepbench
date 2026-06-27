## Context
The data for this challenge comes from Wikipedia's Forbes list of the world's highest-paid athletes page, which contains a table for each year and a source table. The goal is to clean and combine these tables into a single dataset for temporal analysis.

## Requirements

- Input the data
- Bring all the year tables together into a single table
- Merge any mismatched fields (there should not be any Null values)
- Create a numeric Year field
- Clean up the fields with the monetary amounts
  - One way of doing this could be pivot all 3 columns into a single column to do these cleaning calculations once and then pivot back to 3 columns
  - Make sure that any value in millions is translated to that amount (e.g. $6 million becomes 6,000,000)
- Bring in the source information so that it is associated with each row
- Remove unnecessary fields
- Output the data

## Output

- output_01.csv
  - 9 fields:
    - Year
    - Rank
    - Name
    - Sport
    - Country
    - Total earnings
    - Salary/Winnings
    - Endorsements
    - Source
