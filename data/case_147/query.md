## Context
This December we wanted to challenge you to take on some tricky challenges that each week will focus on a different department in your organisation. We're starting with Finance. Finance uses a lot of data to understand the cash flow and liquidity of your organisation. They also typically have some really useful data locked away in files with an annoying format. One of our clients actually had to solve this structure of data last week so I thought it would make a great Preppin' challenge. The input is one Excel file with one worksheet.

## Requirements
** for those using Tableau Prep, avoid typing in field names and see how few you can do. Naming calculations is ok**
- Input the data
- Extract each data table within the Excel workbook
- Extract the branch name from the table structure
- Create a row per measure and year
- Remove the word 'Year' from the year values
- Create a True Value (i.e. the correct number of zeros for the measure)
- Remove the suffix of the measure (i.e. the (k) or (m) if the measure name has the units)
- Remove unneeded columns
- Output the data

## Output

- output_01.csv
  - 4 fields:
    - Branch
    - Clean Measure names
    - Recorded Year
    - True Value
