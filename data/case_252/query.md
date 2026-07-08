## Context

Data Source Bank (DSB) are looking to introduce a Regular Savings Account for their customers. There are 2 factors they need to decide:
- The interest rate
- The maximum amount a customer is able to pay into the account each month

DSB are looking to compare other 12 month products currently in the market, to help decide these factors. They want to understand which account offers the customer the biggest opportunity to increase their savings. They also want to educate their customers by showing how their savings would increase each month.

## Requirements

- Input the data
- Update the Max Monthly Amount so it is a numeric field
- Update the Provider field so it is easy for customers to see in 1 field which accounts have additional conditions
- Ensure we have a row for each month for each account i.e. 12 rows for each account
- Calculate the savings value in each account, each month after interest has been applied
  - Assume a customer is able to pay in the Max Monthly Deposit each month
  - Compound interest may come in useful (formula: A = P(1 + r/n)^(nt), where A is the final amount, P is the original principal sum, r is the nominal annual interest rate, n is the compounding frequency, and t is the overall length of time the interest is applied (expressed using the same time units as r, usually years))
- Create a field for the maximum possible savings a customer could get from each account
- Calculate the maximum total interest a customer could get from each account
- Rank the accounts by the maximum possible savings
- Rank the accounts by the maximum total interest
- Round all monetary values to 2 decimal places
- Output the data

## Output

- output_01.csv
  - 10 fields:
    - Providers Ranked by Max Savings
    - Providers Ranked by Total Interest
    - Provider
    - Interest
    - Max Monthly Deposit
    - Month
    - Savings each month
    - Max Possible Savings
    - Total Interest
    - Sort
