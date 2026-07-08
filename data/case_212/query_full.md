## Context

Customers of Data Source Bank want a statement-style view that shows how their account balance changes after each transaction, rather than only receiving a month-end balance. Using the provided banking data (the same source data used previously), produce a per-transaction running balance statement for each account based on the Transaction Path, Transaction Detail, and Account Information tables.

## Requirements

- Note: This was originally found to trigger a bug in Tableau 2022.4.1, but it works in 2022.3. Update: the bug is fixed in 2022.4.2. (If you are using Tableau and encounter issues, consider using the non-wavey line option or updating versions.)
- Input the data from the three provided tables/files:
  - Account Information
  - Transaction Detail
  - Transaction Path
- For the Transaction Path table:
  - Make sure field naming convention matches the other tables by renaming fields to use spaces:
    - Rename `Account_From` to `Account From`
    - Rename `Account_To` to `Account To`
- Filter out cancelled transactions:
  - Exclude any transactions where the cancellation flag indicates the transaction was cancelled (i.e., remove rows where `Cancelled?` = `Y` from Transaction Detail before combining with Transaction Path).
- Combine Transaction Path with Transaction Detail:
  - Join Transaction Path to the (non-cancelled) Transaction Detail on `Transaction ID` using an inner join so that only transactions present in both tables are kept.
  - Bring through, at minimum, `Transaction Date` and `Value` from Transaction Detail along with the account routing fields from Transaction Path.
- Split the flow into incoming and outgoing transactions, creating an account-level transaction table:
  - Outgoing transactions:
    - Use `Account From` as the `Account Number`.
    - Multiply the transaction `Value` by `-1` so outgoing transactions reduce the account balance.
  - Incoming transactions:
    - Use `Account To` as the `Account Number`.
    - Keep the transaction `Value` as positive so incoming transactions increase the account balance.
  - Union (append) the incoming and outgoing rows together into a single table of account-level transaction movements (do not deduplicate).
- Bring the data together with the Balance as of 31st Jan (starting balance):
  - From Account Information, take each account’s month-end balance snapshot (balance as of 31 January) and append it into the same table as an additional row per account:
    - Use the snapshot’s `Balance Date` as the date for this row.
    - Set the transaction amount/value for this snapshot row to NULL (this row represents the starting point rather than a transaction).
    - Carry the snapshot `Balance` as the starting balance for that account.
  - The resulting grain should be: one row per account per transaction movement, plus one additional starting-balance row for each account.
- Work out the order that transactions occur for each account:
  - Within each `Account Number`, sort by `Transaction Date` ascending.
  - Where multiple transactions happen on the same day for the same account, order them by transaction amount descending (i.e., the highest value transactions happen first).
  - Use this ordering to assign a sequential transaction order within each account.
- Use a running sum to calculate the Balance for each account on each day:
  - Treat the appended 31 Jan balance snapshot as the initial balance for the account.
  - For subsequent rows in transaction order, compute:
    - `Balance` = previous row’s `Balance` + current row’s signed transaction `Value` (incoming positive, outgoing negative).
  - Ensure balances are rounded to 2 decimal places.
- The Transaction Value should be null for 31st Jan, as this is the starting balance:
  - Output `Transaction Value` as NULL for the starting-balance row (the initial snapshot row).
  - For all other rows, output the signed transaction value (rounded to 2 decimal places if needed).
- Format and output:
  - Output `Balance Date` as a day/month/year string in the format `DD/MM/YYYY`.
  - Ensure the output is deterministically ordered by `Account Number`, then `Balance Date` ascending, then `Transaction Value` ascending with NULLs last (so statement rows are consistently ordered).
  - Output the data to the required file.

## Output

- output_01.csv
  - 4 fields:
    - Account Number
    - Balance Date
    - Transaction Value
    - Balance