## Context
Data Source Bank acquires new customers every month. They are stored in separate tabs of an Excel workbook so it's "easy" to see which customers joined in which month. However, it's not so easy to do any comparisons between months. Therefore, we'd like to consolidate all the months into one dataset. There's an extra twist as well. The customer demographics are stored as rows rather than columns, which doesn't make for very easy reading. So we'd also like to restructure the data.

## Requirements

- Input the data
- We want to stack the tables on top of one another, since they have the same fields in each sheet. We can do this one of 2 ways:
  - Drag each table into the canvas and use a union step to stack them on top of one another
  - Use a wildcard union in the input step of one of the tables
- Some of the fields aren't matching up as we'd expect, due to differences in spelling. Merge these fields together
- Make a Joining Date field based on the Joining Day, Table Names and the year 2023
- Now we want to reshape our data so we have a field for each demographic, for each new customer
- Make sure all the data types are correct for each field
- Remove duplicates:
  - If a customer appears multiple times take their earliest joining date
- Output the data

## Output

- output_01.csv
  - 5 fields:
    - ID
    - Joining Date
    - Account Type
    - Date of Birth
    - Ethnicity
