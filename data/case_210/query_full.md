## Context
Data Source Bank wants to identify transactions that may be fraudulent so the fraud team can contact customers to verify whether the transactions are genuine. A transaction is considered potentially fraudulent for this task if it is greater than £1,000 in value, is not cancelled, and is not associated with a Platinum account (Platinum accounts follow different fraud rules and are excluded).

## Requirements
- Input the data.
- Use the following inputs:
  - Account Holders table: `input_01.csv`
  - Account Information table: `input_02.csv`
  - Transaction Detail table: `input_03.csv`
  - Transaction Path table: `input_04.csv`
- For the Transaction Path table:
  - Make sure field naming convention matches the other tables:
    - Rename `Account_From` to `Account From`
    - Rename `Account_To` to `Account To`
- For the Account Information table:
  - Make sure there are no null values in the Account Holder ID (exclude records where Account Holder ID is missing).
  - Ensure there is one row per Account Holder ID for each account by expanding joint accounts:
    - Identify joint accounts: Only accounts where `Account Type` is `Joint` need to be expanded. For these accounts, the `Account Holder ID` field contains multiple IDs recorded together.
    - Split joint accounts: For accounts that need expansion, split the `Account Holder ID` field by comma (`,`), trim whitespace from each ID, and create separate rows for each Account Holder ID. Each resulting row should retain the same account attributes (e.g., Account Number, Account Type, Balance Date, Balance).
    - Example: If a row has `Account Type = "Joint"` and `Account Holder ID = "89920386, 97325900"`, split it into two rows: one with `Account Holder ID = "89920386"` and another with `Account Holder ID = "97325900"`, both keeping the same Account Number, Account Type, Balance Date, and Balance.
- For the Account Holders table:
  - Make sure the phone numbers start with `07` (adjust values so that any valid mobile number is represented with a leading `0` such that the final format begins with `07`).
- Bring the tables together using inner joins (keep only records that successfully match in each step):
  1. Join Transaction Detail to Transaction Path on `Transaction ID`.
  2. Filter out cancelled transactions (keep only rows where `Cancelled?` indicates the transaction is not cancelled).
  3. Convert `Value` to a numeric field and filter to transactions strictly greater than £1,000.
  4. Join to Account Information using the originating account:
     - Match `Account From` (from Transaction Path) to `Account Number` (from Account Information).
     - This associates the transaction with the account that sent the money.
  5. Filter out Platinum accounts (exclude rows where `Account Type` is `Platinum`).
  6. Join to Account Holders on `Account Holder ID` to attach customer contact details.
- Format dates for output:
  - Output `Transaction Date` and `Balance Date` as `DD/MM/YYYY`.
- Define the output grain:
  - One row per qualifying transaction per associated account holder after expanding joint accounts (so a transaction on a joint account will produce one row for each account holder).
- Output the data.

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