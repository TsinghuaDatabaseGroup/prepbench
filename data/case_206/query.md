## Context
For the third week of beginner month, we're going to be building on the skills that we've already learnt, as well as exploring new concepts. This week may feel a little more challenging, but I promise you're ready for it! Data Source Bank has some quarterly targets for the value of transactions that are being performed in-person and online. It's our job to compare the transactions to these target figures.

## Requirements

- Input the data
- For the transactions file:
  - Filter the transactions to just look at DSB
    - These will be transactions that contain DSB in the Transaction Code field
  - Rename the values in the Online or In-person field, Online of the 1 values and In-Person for the 2 values
  - Change the date to be the quarter
  - Sum the transaction values for each quarter and for each Type of Transaction (Online or In-Person)
- For the targets file:
  - Pivot the quarterly targets so we have a row for each Type of Transaction and each Quarter
  - Rename the fields
  - Remove the 'Q' from the quarter field and make the data type numeric
- Join the two datasets together
  - You may need more than one join clause!
- Remove unnecessary fields
- Calculate the Variance to Target for each row
- Output the data

## Output

- output_01.csv
  - 5 fields:
    - Online or In-Person
    - Quarter
    - Value
    - Quarterly Targets
    - Variance to Target
