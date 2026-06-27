## Context

It's always been interesting to me how reporting dates can be so different for different industries. There is often a table that is centrally maintained explaining how the reporting date translates to the calendar date. This way any dataset can be easily enriched with the reporting dates.
This challenge will be all about creating a dynamically updating reporting date table.
Imagine a company uses the following logic:
- Their reporting year begins on the Monday before 1st February
  - e.g. In 2023, 1st February fell on a Wednesday. Therefore the first day of the reporting year will be 30th January
- Each Reporting Month contains exactly 4 Reporting Weeks
This is the logic we will use for this challenge, but you can imagine how it could be easily updated to fit another organisation's logic.

## Requirements

- Input the data
- Create a way for the user to choose which calendar year they want to get the reporting dates for
- Make sure to have a row for each date in the selected year
- Create a field for the Reporting Year (based off the above logic)
- Create a field for the Reporting Day
  - Day 1 will be the Monday before the 1st Feb
- Create a field for the Reporting Week
- Create a field for the Reporting Month
  - Each month contains exactly 4 weeks
- Output the data, naming the file according to calendar year selected when the workflow runs

## Output

- output_01.csv
  - 5 fields:
    - Calendar Date
    - Reporting Year
    - Reporting Month
    - Reporting Week
    - Reporting Day
