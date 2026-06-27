## Context

Data Source Bank usually waits until the end of the month to let customers know their bank account balance. Customers want more control and the ability to see how their balance changes after each transaction. Let's create bank statements for them! The data for this week should feel very familiar! We used this data already in week 7, but we'll only need 3 of the 4 tables this week: Transaction Path, Transaction Detail, Account Information.

## Requirements

Note: I found doing this in 2022.4.1 caused a bug. However, it worked in 22.3 so consider going back to non-wavey lines for this challenge! Update: the bug is fixed in 2022.4.2!

- Input the data
- For the Transaction Path table:
  - Make sure field naming convention matches the other tables
    - i.e. instead of *Account\\_From* it should be *Account From*
- Filter out the cancelled transactions
- Split the flow into incoming and outgoing transactions
- Bring the data together with the Balance as of 31st Jan
- Work out the order that transactions occur for each account
  - Hint: where multiple transactions happen on the same day, assume the highest value transactions happen first
- Use a running sum to calculate the Balance for each account on each day
- The Transaction Value should be null for 31st Jan, as this is the starting balance
- Output the data

## Output

- output_01.csv
  - 4 fields:
    - Account Number
    - Balance Date
    - Transaction Value
    - Balance
