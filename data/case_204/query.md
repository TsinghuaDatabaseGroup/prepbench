## Context

The subject for January will be our new (fake) bank -- The Data Source Bank (DSB). This week we have had a report with a number of transactions that have not just our transactions but other banks' too. Can you help clean up the data?

## Requirements

- Input the data
- Split the Transaction Code to extract the letters at the start of the transaction code. These identify the bank who processes the transaction
  - Rename the new field with the Bank code 'Bank'.
- Rename the values in the Online or In-person field, Online of the 1 values and In-Person for the 2 values.
- Change the date to be the day of the week
- Different levels of detail are required in the outputs. You will need to sum up the values of the transactions in three ways:
  - 1. Total Values of Transactions by each bank
  - 2. Total Values by Bank, Day of the Week and Type of Transaction (Online or In-Person)
  - 3. Total Values by Bank and Customer Code
- Output the data

## Output

- output_01.csv
  - 2 fields:
    - Bank
    - Value

- output_02.csv
  - 4 fields:
    - Bank
    - Online or In-Person
    - Transaction Date
    - Value

- output_03.csv
  - 3 fields:
    - Bank
    - Customer Code
    - Value
