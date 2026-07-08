## Context
Chin & Beard Suds Co release Easter themed products each year, 12 weeks before Easter Sunday. Since the date of Easter Sunday changes each year, they have trouble comparing sales to previous years as the weeks don't line up. They need to calculate Easter Week Number to enable year-over-year comparison.

## Requirements
- Input the data
- Bring all the years together in a single table
- Work out the Easter Week Number, as per the first line chart, so the years can be compared
  - Ensure that the weeks begin on a Monday
- Make sure there is a field for which day of the week each Sales Date is in order to create the 2nd chart
  - Abbreviate these weekday names as: Monday = M, Tuesday = Tu, etc.
- Add in a field for the Weekday Order so the visualisation can be sorted Monday-Sunday (i.e. Monday = 1, Tuesday = 2 etc.)
- Calculate the Sales per Product per Sales Date
- Output the data

## Output

- output_01.csv
  - 9 fields:
    - Year
    - Sales Date
    - Easter Week Number
    - Weekday
    - Weekday Order
    - Product
    - Price
    - Quantity Sold
    - Sales
