## Context

Using customer account and transaction data from multiple companies that buy our products, produce weekly, monthly, and quarterly summaries of account balances and transaction values. The summaries must also quantify how often customers are in a negative balance and how often they exceed their allowed credit limit. The credit limit is provided as a positive number representing the maximum amount the customer is allowed to owe; exceeding the credit limit is therefore evaluated by comparing the balance to the negative of this limit.

## Requirements

- Input the data.
- Input of Customer Details from `input_02.csv`, containing at least:
  - `Account` (customer account identifier)
  - `Name` (customer name)
  - `Max Credit` (positive numeric credit limit)
- Input of Transactions from `input_01.csv`, containing at least:
  - `Account` (customer account identifier)
  - `Date` (transaction date, parsed as a date)
  - `Transaction` (transaction value, numeric)
  - `Balance` (account balance, numeric)
- Join customer details onto transactions using a left join on `Account` so that every transaction row is retained and `Name` and `Max Credit` are brought in.
- For each transaction row, derive two indicator fields used for counting days:
  - “below zero” indicator = 1 when `Balance < 0`, else 0.
  - “beyond max credit” indicator = 1 when `Balance < - (Max Credit)`, else 0 (because `Max Credit` is stored as a positive limit on how much the customer may owe).
- Create an average (mean) for balance to two decimal places and an average (mean) for transactions per customer to no decimal places, per time period.
  - Balance averages: mean of `Balance`, rounded to 2 decimal places.
  - Transaction averages: mean of `Transaction`, rounded to 0 decimal places and output as an integer.
- Each output row will be a customer per time period, grouped by `Account` and `Name` plus the relevant period identifier.
- Date recorded will be the beginning of that time period, formatted as `DD/MM/YYYY`.
- Determine the number of days a customer's balance is below zero by summing the “below zero” indicator within each time period.
- Determine the number of days a customer's balance is below their credit limit by summing the “beyond max credit” indicator within each time period.

### Monthly summary logic (output_01.csv)

- Define `Month` as the calendar month number (1–12) from `Date`.
- Define the period start date as the first day of that month in the same year as the transaction date.
- Group by `Account`, `Name`, `Month`, and the month start date; within each group compute:
  - Days Below Zero balance? = sum of “below zero” indicator
  - Days Beyond Max Credit = sum of “beyond max credit” indicator
  - Monthly Avg Transactions = mean of `Transaction`, rounded to 0 decimals and cast to integer
  - Monthly Avg Balances = mean of `Balance`, rounded to 2 decimals
- Set the output `Date` to the month start date, formatted `DD/MM/YYYY`.

### Quarterly summary logic (output_02.csv)

- Define natural quarters as:
  - Quarter 1 = months 1–3, Quarter 2 = months 4–6, Quarter 3 = months 7–9, Quarter 4 = months 10–12.
- Define the period start date as the first day of the quarter (Jan 1, Apr 1, Jul 1, Oct 1) in the same year as the transaction date.
- Group by `Account`, `Name`, `Quarter`, and the quarter start date; within each group compute:
  - Below Zero balance? = sum of “below zero” indicator
  - Beyond Max Credit = sum of “beyond max credit” indicator
  - Quartlery Avg Transaction = mean of `Transaction`, rounded to 0 decimals and cast to integer
  - Quarterly Avg Balance = mean of `Balance`, rounded to 2 decimals
- Set the output `Date` to the quarter start date, formatted `DD/MM/YYYY`.

### Weekly summary logic (output_03.csv)

- Use a custom week numbering and anchoring rule per calendar year:
  - Week 1 runs from January 1 up to (but not including) the first Sunday of that year; Week 1’s period start date is January 1.
  - Week 2 starts on the first Sunday of the year, and each subsequent week is a contiguous 7-day period starting on Sunday.
  - For weeks 2+, the period start date is that week’s Sunday anchor date.
- Group by `Account`, `Name`, `Week`, and the week anchor date; within each group compute:
  - Days Below Zero balance? = sum of “below zero” indicator
  - Days Beyond Max Credit = sum of “beyond max credit” indicator
  - Weekly Avg Transactions = mean of `Transaction`, rounded to 0 decimals and cast to integer
  - Weekly Avg Balances = mean of `Balance`, rounded to 2 decimals
- Set the output `Date` to the period start date (January 1 for Week 1; otherwise the Sunday anchor), formatted `DD/MM/YYYY`.
- Output the data to the three required CSVs with exactly the specified fields and field order.

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