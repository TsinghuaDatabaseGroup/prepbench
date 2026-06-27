## Context
The intermediate month begins by building on the aggregation technique covered in week 1. This week's challenge looks at two analytical calculations that can make the use of the data source much easier for end users. If you are a user of Tableau Desktop, you have likely had to create rank's and use Level of Detail calculations (these are just calculations at a different level of granularity to the data set or visual you are creating). These aren't easy calculations for new users to understand so if you can add them to your data set before sharing then you can make the end user's life easier.

## Requirements

- Input the data
- Create the bank code by splitting out off the letters from the Transaction code, call this field 'Bank'
- Change transaction date to the just be the month of the transaction
- Total up the transaction values so you have one row for each bank and month combination
- Rank each bank for their value of transactions each month against the other banks. 1st is the highest value of transactions, 3rd the lowest.
- Without losing all of the other data fields, find:
  - The average rank a bank has across all of the months, call this field 'Avg Rank per Bank'
  - The average transaction value per rank, call this field 'Avg Transaction Value per Rank'
- Output the data

## Output

- output_01.csv
  - 6 fields:
    - Transaction Date
    - Bank
    - Value
    - Bank Rank per Month
    - Avg Transaction Value per Rank
    - Avg Rank per Bank
