## Context

Using three different company's data who buy our products, we are looking at the balance of credit that they hold with us. We want to know: What is the average weekly, monthly and quarterly balance? What is the average weekly, monthly and quarterly transaction value? How many days does the customer have a negative balance? How many days does the customer exceed their credit limit? Credit limit is a positive number in the input but needs to be made negative as it how much we allow the customer to owe us.

## Requirements

- Input the data
- Input of Customer Details
- Input of Transactions
- Input data
- Create an average (mean) for balance to two decimal places and average (mean) for transactions per customer to no decimal places, per time period
- Each row will be a customer per time period
- Date recorded will be the beginning of that time period
- Bring in the customer name
- Determine the number of days a customer's balance is below zero
- Determine the number of days a customer's balance is below their credit limit
- Output the data

## Output

- output_01.csv
  - 8 fields:
    - Days Beyond Max Credit
    - Days Below Zero balance?
    - Monthly Avg Transactions
    - Monthly Avg Balances
    - Month
    - Account
    - Name
    - Date

- output_02.csv
  - 8 fields:
    - Beyond Max Credit
    - Below Zero balance?
    - Quarter
    - Account
    - Name
    - Quartlery Avg Transaction
    - Quarterly Avg Balance
    - Date

- output_03.csv
  - 8 fields:
    - Weekly Avg Transactions
    - Weekly Avg Balances
    - Days Below Zero balance?
    - Days Beyond Max Credit
    - Week
    - Account
    - Name
    - Date
