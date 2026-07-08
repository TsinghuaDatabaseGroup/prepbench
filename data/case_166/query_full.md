## Context
You work for a Property Management company and need to compile a report showing how much revenue the business can expect to make from its existing office space rental contracts. The focus period is 2021 through 2026. The board wants (1) a contract-level monthly schedule with a cumulative total by month over the life of each contract, and (2) a dynamic year summary showing total rent for completed years and a year-to-date figure for the current year that updates over time.

Assume the “current date” for all “months until expiry” calculations is 13 April 2022.

## Requirements
- Input the data:
  - Read the contracts dataset (input_02.csv), which includes contract attributes such as ID, location fields, company, office size, people, per-person metrics, and the contract start and end dates.
  - Read the office space prices dataset (input_01.csv), which provides “Rent per Month” by office characteristics.

- Work out the length of each contract in months:
  - Parse “Contract Start” and “Contract End” as dates.
  - Define **Contract Length** as the number of whole months between the start month and the end month, computed as:  
    \[
    (EndYear - StartYear)\times 12 + (EndMonth - StartMonth)
    \]
  - Treat this value as an integer, and use it as the number of monthly rows to generate for that contract.

- Work out the number of months until each contract expires:
  - Define **Months Until Expiry** as the whole-month difference between **April 2022** and the contract end month (ignoring day-of-month), computed as:  
    \[
    (EndYear - 2022)\times 12 + (EndMonth - 4)
    \]
  - Treat this value as an integer.

- Input the Office Space Prices data and join it to the contracts table:
  - Perform a left join from contracts to prices using the keys **City** and **Office Size**.
  - Keep all contracts even if no matching price is found (resulting price fields will be null in that case).

- Remove duplicated fields:
  - After the join, ensure the output uses a single consistent set of fields (do not retain duplicate/suffixed duplicates of the same business field).

- Create a row for each month that a rental contract will be live:
  - For each contract, generate exactly **Contract Length** rows.
  - The monthly sequence must start at the first day of the contract’s start month (month start), and proceed in monthly steps (one row per month).
  - Retain the contract’s details (ID, location, company, office size, dates, people, per-person, and rent) on every generated monthly row.
  - *Edit 14/04/2022: Be careful at this point that the number of rows for each Office ID is equal to the Contract length* (i.e., each contract must expand to exactly Contract Length monthly rows).

- Calculate the cumulative monthly cost of each office space contract:
  - Within each contract (by ID), compute **Cumulative Monthly Cost** as the running total of “Rent per Month” over the generated monthly rows in chronological month order.
  - Remember we only have one contract per company (i.e., cumulative totals should be computed per contract/ID, not across multiple contracts for the same company).

- This will create our first output:
  - Format the date fields “Contract Start”, “Contract End”, and “Month Divider” as **DD/MM/YYYY** strings (zero-padded).
  - Ensure “ID” is represented as a string in the output.
  - Output the following fields as integer strings with no decimals: Cumulative Monthly Cost, Contract Length, Months Until Expiry, People, Per Person, Rent per Month.

- Create a table that details total rent paid for completed years across all contracts and year to date figures for the current year, which would update as time goes on:
  - Build this summary from the expanded monthly table (one row per contract-month).
  - Create one row per year for **each year from 2021 through 2026 (inclusive)**.
  - For **Year = 2021**: set “EoY and Current” to the sum of “Rent per Month” across all expanded rows whose Month Divider year is 2021.
  - For **Year = 2022 (current year as of 13 April 2022)**: set “EoY and Current” to the year-to-date sum of “Rent per Month” across all expanded rows whose Month Divider year is 2022 and whose Month Divider month is **January through April (month ≤ 4)**.
  - For **Years 2023–2026**: leave “EoY and Current” blank/null.

- Output the data:
  - Produce the two CSVs exactly as specified below.

## Output

- output_01.csv
  - 15 fields:
    - Cumulative Monthly Cost
    - ID
    - Country
    - City
    - Address
    - Company
    - Office Size
    - Contract Start
    - Contract End
    - Contract Length
    - Months Until Expiry
    - People
    - Per Person
    - Rent per Month
    - Month Divider
  - Contract Start, Contract End, and Month Divider must be formatted exactly as `DD/MM/YYYY` (zero-padded).
  - The following fields must be integer strings with no decimals: Cumulative Monthly Cost, Contract Length, Months Until Expiry, People, Per Person, Rent per Month.

- output_02.csv
  - 2 fields:
    - Year
    - EoY and Current
  - Year must be a 4-digit integer string with no decimals.
  - EoY and Current must be an integer string with no decimals; blank if missing.
