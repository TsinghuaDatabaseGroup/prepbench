## Context
For week 2 of our beginner month, Data Source Bank has a requirement to construct International Bank Account Numbers (IBANs), even for Transactions taking place in the UK. We have all the information in separate fields, we just need to put it altogether in the following order:

1. Country Code: (e.g., GB)
2. Check Digits: (e.g., 12)
3. Bank Code: (e.g., ABCD)
4. Sort Code: (e.g., 102030)
5. Account Number: (e.g., 12345678)

Example: GB12ABCD10203012345678

## Requirements

- Input the data
- In the Transactions table, there is a Sort Code field which contains dashes. We need to remove these so just have a 6 digit string
- Use the SWIFT Bank Code lookup table to bring in additional information about the SWIFT code and Check Digits of the receiving bank account
- Add a field for the Country Code
  - Hint: all these transactions take place in the UK so the Country Code should be GB
- Create the IBAN as above
  - Hint: watch out for trying to combine sting fields with numeric fields - check data types
- Remove unnecessary fields
- Output the data

## Output

- output_01.csv
  - 2 fields:
    - Transaction ID
    - IBAN
