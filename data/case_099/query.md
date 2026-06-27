## Context

2020 - what a year! Much has changed, few things have stayed the same. Even our star signs weren't safe! The introduction of a 13th star sign, Ophiuchus, threw things into disarray. Were you born on a day where your star sign has remained unchanged? Let's make a list of all those affected by the changes.

## Requirements

- Input the data
- Be careful your data isn't mistaken for a header.
- Reshape and clean up the data so you have a column for the star sign, along with the start and end dates.
- Create a date range for the new star signs.
- Scaffold the data so you have a row for every date of the year (2020 is a good year to base this off, since it's even a leap year!)
- For the output, we're looking for a list of dates that have changed their star sign. For dates on the cusp, if at least one of their new star signs matches at least one of their old star signs, we consider their star sign not to have changed and so they are excluded from the output.
  - Edit: For example, 19th February is on the cusp in the old world, with a star sign of either Aquarius or Pisces. Its new star sign is Aquarius and so it hasn't necessarily "changed" and should be excluded from the output
- Create a birthday field.
- Output the data

## Output

- output_01.csv
  - 4 fields:
    - Birthday
    - Old Star Sign
    - New Star Sign
    - Date Range
