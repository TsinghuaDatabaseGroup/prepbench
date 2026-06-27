## Context
The UK income tax bands (2024) are essential for tax calculation:
- 0% tax on annual earnings up to £12,570
- 20% tax on annual earnings between £12,571 and £50,270
- 40% tax on annual earnings between £50,271 and £125,140
- 45% tax on annual earnings above £125,140

## Requirements
- Input the data
- Add a row number to the data set
- Find the latest row (largest row number) to capture the individuals correct salary information
- Find each team member's annual salary
- Find each team member's maximum tax band based on their annual salary (rates: 20%, 40%, 45%)
- Work out how much tax an individual paid for each of the % bands. Call these fields:
  - 20% tax rate paid
  - 40% tax rate paid
  - 45% tax rate paid
- Total the tax paid across all three % bands. Call this field 'Total Tax Paid'
- Output the data

## Output

- output_01.csv
  - 7 fields:
    - StaffID
    - Salary
    - Max Tax Rate
    - Total Tax Paid
    - 20% rate tax paid
    - 40% rate paid
    - 45% rate tax paid
