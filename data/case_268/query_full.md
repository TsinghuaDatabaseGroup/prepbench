## Context
Chin & Beard Suds Co releases Easter-themed products each year starting 12 weeks before Easter Sunday. Because Easter shifts across calendar dates each year, the business needs a consistent “Easter Week Number” (with weeks starting on Monday) so sales can be compared year-over-year on an aligned week timeline. The dataset should also support weekday-based visualisations.

## Requirements
- Input the data.
- Bring all the years together in a single table by appending (stacking) all provided yearly input files into one combined dataset (keep all rows; do not deduplicate).
- Work out the Easter Week Number so the years can be compared, matching the logic implied by the first line chart:
  - Ensure that weeks begin on a Monday.
  - For each row, compute Easter Sunday for that row’s calendar year, then define **Easter-week Monday** as the Monday of the week that contains Easter Sunday.
  - Define **Week 1 Monday** as **11 weeks (77 days) before Easter-week Monday** for that year (so that the week containing Easter is **Easter Week Number = 12**).
  - Compute **Easter Week Number** as the integer week index of the Sales Date relative to Week 1 Monday for the same year:
    - Normalize Sales Date to its calendar date (ignore time-of-day if present).
    - Easter Week Number = `floor((Sales Date - Week 1 Monday) / 7 days) + 1`.
- Make sure there is a field for which day of the week each Sales Date is in order to create the 2nd chart:
  - Derive the weekday from Sales Date where Monday is the first day of the week.
  - Abbreviate weekday names exactly as: **M, Tu, W, Th, F, Sa, Su**.
- Add in a field for the Weekday Order so the visualisation can be sorted Monday–Sunday:
  - Map Monday→1, Tuesday→2, Wednesday→3, Thursday→4, Friday→5, Saturday→6, Sunday→7.
- Calculate the Sales per Product per Sales Date:
  - Compute **Sales** as `Price * Quantity Sold` for each row (i.e., at the same grain as the input rows).
- Output the data:
  - Format **Sales Date** as `DD/MM/YYYY` in the final output.
  - Output exactly the required fields in the required order.

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