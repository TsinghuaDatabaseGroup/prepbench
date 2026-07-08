## Context
You are given staff pay records and need to calculate each person’s annual salary and the UK income tax they would pay under the 2024 tax band thresholds. The aim is to keep only the most recent record per staff member, determine their maximum tax rate band, compute tax paid within each applicable band (20%, 40%, 45%), and produce a single output file.

The tax thresholds to apply are:
- 0% tax on annual earnings up to £12,570
- 20% tax on annual earnings between £12,571 and £50,270
- 40% tax on annual earnings between £50,271 and £125,140
- 45% tax on annual earnings above £125,140

## Requirements
- Input the data from `input_01.csv`.
- Add a row number to the dataset that reflects the input file order (first row = 1, then 2, etc.). Treat a larger row number as a more recent record.
- Find the latest row (largest row number) for each `StaffID` and keep only that latest record per staff member. The output grain must be one row per `StaffID`, based on that latest record.
- Find each team member's annual salary:
  - The input is expected to contain monthly pay columns named `1` through `12`.
  - Compute `Salary` as the sum of the 12 monthly values (`1` + `2` + … + `12`) for the latest record.
  - If any of the monthly columns `1`–`12` are missing, treat the missing month(s) as 0 for the purpose of the annual sum. If monthly values are non-numeric, treat them as 0 in the sum.
- Find each team member's maximum tax band based on their annual salary (rates: 20%, 40%, 45%):
  - If `Salary` is greater than £125,140, `Max Tax Rate` is `45% rate`.
  - Else if `Salary` is greater than £50,270, `Max Tax Rate` is `40% rate`.
  - Else, `Max Tax Rate` is `20% rate`.
- Work out how much tax an individual paid for each of the % bands using these taxable portions:
  - 20% band taxable portion = `min(max(Salary − 12,570, 0), 50,270 − 12,570)`; tax = that amount × 0.20.
  - 40% band taxable portion = `min(max(Salary − 50,270, 0), 125,140 − 50,270)`; tax = that amount × 0.40.
  - 45% band taxable portion = `max(Salary − 125,140, 0)`; tax = that amount × 0.45.
- Populate the band tax output fields with these applicability rules:
  - `20% rate tax paid` should always be populated from the 20% calculation (it may be 0).
  - `40% rate paid` must be blank/null unless the person’s `Salary` is greater than £50,270; otherwise populate with the 40% calculation.
  - `45% rate tax paid` must be blank/null unless the person’s `Salary` is greater than £125,140; otherwise populate with the 45% calculation.
- Total the tax paid across all three % bands. Call this field `Total Tax Paid`:
  - Compute it as the sum of the three band tax amounts, treating any blank/null band fields as 0 in the total.
- Output the data with exactly the required fields and names, without adding additional output columns.

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