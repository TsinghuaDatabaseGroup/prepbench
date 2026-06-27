# query_r.md

## Context
This week we are back in the (home) office after a week at Tableau Conference-ish and want to know how we are performing so far this year. As for most businesses, it's been a tough year so we want to find some comparisons between our sales this year, last year and our targets. We have two inputs:  
1, Transactions  
This is a list of our daily sales for each product. It contains the Price, Quantity and Income.  
2, Targets  
This is a list of targets that have been provided by the finance team. It is a weekly breakdown for this year by product.  

Assumptions:  
- The latest date/today is Friday 9th October 2020  
- Week's in Tableau Prep work from Sunday to Saturday, apart from the start of the year where this could be different.

## Requirements
- Input the data
- Create a daily Targets table. Assume there are 7 days in the week and the daily demand is split evenly throughout the week. Eg, if the weekly target is 700, then 100 per day.
- Categorise whether a row/transaction happened this year, last year or is a target.
- Combine the Transactions & Targets tables.
- Only keep the Year to Date for each period. As the 9th October can fall on a different day each year, we don’t want to base this on a date. Instead work on the same Week/Day number. Eg, 9th October is Week 41 Day 6 so we want to keep up this point for each period (This Year, Last Year, Target).
- Calculate the Year to Date, Month to Date, and Week to Date values for each product and metric (Income & Quantity).
- Round all metric values to 0 decimal places.
- Calculate the % difference from This Year to Last Year, and also from This Year to Target for each product and time period (YTD, MTD, WTD). This should be to 2 decimal places.
- Output the data

## Output

- output_01.csv
  - 8 fields:
    - ProductName
    - Metric
    - Time Period
    - This Year
    - Last Year
    - Target
    - % Difference to Last Year
    - % Difference to Target
