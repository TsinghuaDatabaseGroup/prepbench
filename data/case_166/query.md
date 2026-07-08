## Context
You work for a Property Management company and your boss has asked you to compile a report detailing how much revenue the business can expect to make from its existing office space rental contracts. The time frame in focus is from 2021 until 2026 and the board would like to see a cumulative total for each month of a contract. An additional requirement is to create a dynamic table that totals rent paid for completed years across all contracts, as well as year to date figures for the current year, which would update as time goes on.
Assume the "current date" for calculating months until expiry is 13 April 2022.

## Requirements

- Input the data
- Work out the length of each contract in months
- Work out the number of months until each contract expires
- Input the Office Space Prices data and join it to the contracts table
- Remove duplicated fields
- Create a row for each month that a rental contract will be live
  - Retain the details for each of the contracts in the new rows
- *Edit 14/04/2022: Be careful at this point that the number of rows for each Office ID is equal to the Contract length*
- Calculate the cumulative monthly cost of each office space contract
  - Remember we only have one contract per company
- This will create our first output
- Create a table that details total rent paid for completed years across all contracts and year to date figures for the current year, which would update as time goes on
- Output the data

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
