## Context
Data Source Bank needs to construct International Bank Account Numbers (IBANs) for transactions that take place in the UK. All required components exist across the transactions data and a bank lookup, and must be concatenated in a specific order to form each IBAN.

The IBAN structure to build is:

1. Country Code (GB)
2. Check Digits
3. Bank Code (SWIFT code)
4. Sort Code (6 digits, with any dashes removed)
5. Account Number

## Requirements
- Input the data.
- Use two inputs:
  - A Transactions table (input file) containing at least: `Transaction ID`, `Bank`, `Sort Code`, and `Account Number`.
  - A SWIFT Bank Code lookup table (input file) containing at least: `Bank`, `SWIFT code`, and `Check Digits`.
- In the Transactions table, transform `Sort Code` by removing dashes (`-`) so the result is a continuous 6-character string.
- Enrich each transaction by joining to the SWIFT Bank Code lookup to bring in `SWIFT code` and `Check Digits`:
  - Join key: `Bank`.
  - Join type: left join (retain all transactions).
  - Relationship constraint: each `Bank` value in the lookup must map to at most one row (many transactions to one bank record).
- Add the Country Code as `GB` (all transactions are in the UK). This country code should be used as the leading prefix when constructing the IBAN.
- Create the `IBAN` by concatenating the following components in order as text (ensure components are treated as strings before concatenation):
  1. `GB`
  2. `Check Digits`
  3. `SWIFT code`
  4. `Sort Code` (with dashes removed)
  5. `Account Number`
- Remove unnecessary fields so that only the required output fields remain.
- Output the data.

## Output

- output_01.csv
  - 2 fields:
    - Transaction ID
    - IBAN