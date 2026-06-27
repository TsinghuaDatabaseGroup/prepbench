## Context
Customers sometimes look up their account balance on days when no transactions occurred. If the dataset only contains rows for transaction days, filtering to a non-transaction date yields no results. Use scaffolding to ensure every account has a row for every day in a defined period, then allow the user to select a single date and view balances for that date.

## Requirements
- Input the data.
  - Read `inputs/input_01.csv`.
  - Parse **Balance Date** from format `DD/MM/YYYY` (e.g., `07/02/2023` represents February 7, 2023).

- Aggregate the data so we have a single balance for each day already in the dataset, for each account.
  - Treat **Account Number** and **Balance Date** as the keys for “a day for an account”.
  - For each Account Number + Balance Date:
    - Compute the day's **Transaction Value** as the **sum** of Transaction Value across all rows on that date for that account.
    - If there are multiple **Balance** values on the same Account Number + Balance Date, select the first occurrence based on the original row order in the input file.
    - The aggregated daily row must contain: Account Number, Balance Date, the summed Transaction Value for that date, and the selected Balance for that date.

- Scaffold the data so each account has a row between 31st Jan and 14th Feb.
  - Create a complete daily date series from **2023-01-31 through 2023-02-14 inclusive**.
  - For every distinct Account Number, generate one row per date in that range (even if that date did not exist in the original data).
  - Left-join the aggregated daily data onto this scaffold by **Account Number + Date** (where Date equals the aggregated Balance Date).

- Make sure new rows have a null in the Transaction Value field.
  - After joining to the scaffold, any scaffolded date with no matching aggregated daily record must have Transaction Value = null.

- Ensure each scaffolded row has the correct Balance for that date.
  - For dates that do have an aggregated daily record, use that day’s selected Balance.
  - For dates with no aggregated daily record, set Balance equal to the most recent prior date’s Balance for the same account within the scaffolded range (i.e., forward-fill within each account’s timeline). If the earliest scaffolded date for an account has no Balance, initialize it from that account’s earliest available Balance and then forward-fill.

- Create a parameter so a particular date can be selected.
  - The parameter represents a single calendar date.
  - Default the selected date to **2023-02-01**.

- Filter to just this date.
  - Keep only rows where the scaffolded Date equals the selected parameter date.
  - The resulting grain must be **one row per Account Number** for the selected date, with Transaction Value null if no transaction occurred on that date.

- Output the data.

## Output

- output_01.csv
  - 3 fields:
    - Account Number
    - Transaction Value
    - Balance