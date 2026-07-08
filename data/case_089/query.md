## Context
Sometimes when researching one Preppin' Data idea, you encounter a rather hideous data structure that makes you wonder, "could Prep handle this?" Suddenly you're on a completely different tangent to the challenge you were originally planning and you've got a chunky Prep workflow that just begs to be turned into a challenge itself. So here we are, looking at the most popular baby names for boys and girls in England and Wales in 2019. There is one input for boys names and one input for girls names. Each month is its own table and they are laid out next to each other in the Excel sheet. Pay particular attention to May and August which have additional rows as there have been ties in the rankings.

## Requirements

- Input the data
- I recommend starting with the boys names
  - Remove totals
  - Pivot to create a month field
  - Bring all the months together
  - Perhaps using the new grouping functionality and reusing steps may be useful to avoid tedious repetition
  - Still stuck? Check the hint below
- For the girls names, carry out the above steps
- For additional rows, that have not been picked up as part of the main tables:
  - Pivot so that information from headers is not lost
  - Restructure the data so it has the headings: Rank, Name, Count
  - Join it to cleaned girls names to bring through month information
  - Combine it with girls names
- Output the monthly rankings as a single datasource
- Aggregate to a year level and calculate new rankings
- Output the top 10 baby names for boys and girls in 2019 in England and Wales
- Output the data

## Output

- output_01.csv
  - 4 fields:
    - 2019 Rank
    - Count
    - Name
    - Gender

- output_02.csv
  - 5 fields:
    - Rank
    - Count
    - Name
    - Month
    - Gender
