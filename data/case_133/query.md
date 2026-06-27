## Context

As we come to the end of our excel challenges month, it seems only right to think about vlookups and index matches. In Excel, these are great functions for bringing together data from different worksheets without having to manually copy and paste. Our scenario this week is looking at Employee Sales at Allchains for each month of the year so far and we want to compare this to their Monthly Targets, stored on another sheet.

## Requirements

- Input the data
- Calculate the Average Monthly Sales for each employee
- In the Targets sheet the Store Name needs cleaning up
- Filter the data so that only employees who are below 90% of their target on average remain
- For these employees, we also want to know the % of months that they met/exceeded their target
- Output the data

## Output

- output_01.csv
  - 5 fields:
    - Store
    - Employee
    - Avg monthly Sales
    - % of months target met
    - Monthly Target
