## Context
You work for a mobile/cell phone company and need to produce a monthly revenue report for the current set of customer contracts. The report should show, for each contract, the monthly payment dates during the period the contract is active and the running (cumulative) total paid over the life of the contract.

## Requirements
- Input the data.
  - Read contract data from `input_01.csv`, which includes at minimum: `Name`, `Start Date`, `Contract Length (months)`, and `Monthly Cost`.
  - Optionally read `input_02.csv` if it exists. This file, when present, provides a column `Length` representing integer month indices used to generate month-by-month rows.
  - Parse `Start Date` as a date using the format `YYYY-MM-DD` (invalid formats should be treated as errors).
- Calculate the End Date for each contract.
  - Define the contract end point as the last active monthly payment date:  
    `End Date = Start Date + (Contract Length - 1) months` (calendar-month offset).  
    (This end date is used to determine the active months; it is not required to be included as an output column.)
- Create a row for each month a person will hold the contract.
  - For each contract, generate one row per month index `Length` starting at 1 and ending at `Contract Length` (inclusive).
    - If `input_02.csv` is present and contains `Length`, use it as the source of month indices (and use only indices `<= Contract Length`).
    - If `input_02.csv` is absent (or does not provide `Length`), generate the month index sequence internally as `1..max(Contract Length)` across all contracts, then keep indices `<= Contract Length` per contract.
  - Compute `Payment Date` for each generated row as:  
    `Payment Date = Start Date + (Length - 1) months` (calendar-month offset so the day-of-month follows the start date’s day).
- Calculate the monthly cumulative cost of each person's contract.
  - Within each `Name`, sort rows by `Payment Date` ascending and compute `Cumulative Monthly Cost` as the running sum of `Monthly Cost`.
- Output the data.
  - Format `Payment Date` as text in `DD/MM/YYYY`.
  - Produce `output_01.csv` with exactly the four required fields.
  - Write rows in a deterministic order:
    - First order people by `Contract Length` ascending, then `Start Date` descending, then `Name` ascending.
    - Within each person, order by `Payment Date` ascending.

## Output

- output_01.csv
  - 4 fields:
    - Name
    - Payment Date
    - Monthly Cost
    - Cumulative Monthly Cost