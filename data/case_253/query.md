## Context
Data Source Bank (DSB) were thrilled with the workflow produced for a recent analysis. As often happens with great analysis, further questions were raised. Which would be the best account for a customer given the amount they're able to deposit each month? Of course, it made sense that the accounts that allowed higher monthly deposits ranked highly, but what if a customer only has a fraction of that monthly deposit, which account would best suit them then?

## Requirements

- Input the data
- Introduce a field which allows a used to control their Planned Monthly Deposit
- If this value is greater than the Max Monthly Deposit allowed by the Provider, then calculate how much will be left over and receive no interest
  - Although you'll want to make sure these leftovers are added on after the interest has been applied
- Output the data
  - Make it clear what the Customer's Planned Monthly Deposit is in the title of the output file
- Output the data

## Output

- output_01.csv
  - 12 fields:
    - Providers Ranked by Max Savings
    - Providers Ranked by Total Interest
    - Provider
    - Interest
    - Max Monthly Deposit
    - Customer Planned Deposit
    - Monthly Deposit
    - Leftover Savings which won't receive interest
    - Month
    - Savings each month
    - Max Possible Savings
    - Total Interest
