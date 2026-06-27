## Context
As in many organisations, sometimes the answer to a question can only be found by combining multiple datasets together. Data Source Bank are looking to find transactions which may possibly be fraudulent. They define potentially fraudulent transactions as: Being more than £1,000 in value; Excluding cancelled transactions; Platinum Bank Accounts have different rules for identifying fraudulent transactions so we will exclude them from our analysis. What the fraud team need is the ability to make phone calls to customers to double check whether these transactions are genuine.

## Requirements

- Input the data
- For the Transaction Path table:
  - Make sure field naming convention matches the other tables
    - i.e. instead of *Account\\_From* it should be *Account From*
- For the Account Information table:
  - Make sure there are no null values in the Account Holder ID
  - Ensure there is one row per Account Holder ID
    - Joint accounts will have 2 Account Holders, we want a row for each of them
- For the Account Holders table:
  - Make sure the phone numbers start with *07*
- Bring the tables together
- Filter out cancelled transactions
- Filter to transactions greater than £1,000 in value
- Filter out Platinum accounts
- Output the data

## Output

- output_01.csv
  - 12 fields:
    - Transaction ID
    - Account To
    - Transaction Date
    - Value
    - Name
    - Date of Birth
    - Contact Number
    - First Line of Address
    - Account Number
    - Account Type
    - Balance Date
    - Balance
