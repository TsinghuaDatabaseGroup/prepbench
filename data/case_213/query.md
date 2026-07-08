## Context
Bank's customers are thrilled with the recent developments. However, they're not always the smartest... If a transaction isn't made on a particular day, how can the customer find out their balance? They filter the data and no values appear. Looks like we'll need to use a technique called scaffolding to ensure we have a row for each date in the dataset.

## Requirements

- Input the data
- Aggregate the data so we have a single balance for each day already in the dataset, for each account
- Scaffold the data so each account has a row between 31st Jan and 14th Feb
- Make sure new rows have a null in the Transaction Value field
- Create a parameter so a particular date can be selected
- Filter to just this date
- Output the data

## Output

- output_01.csv
  - 3 fields:
    - Account Number
    - Transaction Value
    - Balance
