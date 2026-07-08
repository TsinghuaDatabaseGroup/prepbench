## Context

You are preparing a customer contact dataset for downstream use by removing duplicate customer records and standardizing the resulting table structure. The goal is to produce a single, deduplicated customer list with a fixed set of output columns.

## Requirements

- Input the data.
- Step 1: Connect to the Data  
  - Read the source file `input_01.csv`.
- Step 2: Add a Cleaning Step  
  - Ensure the `Customer ID` field is treated as a numeric identifier (convert it to a numeric type; values that cannot be interpreted as numbers should become null).
- Step 3: Identify Duplicates  
  - Define duplicates as multiple rows sharing the same `Customer ID`.
- Step 4: Remove Duplicates  
  - Deduplicate by `Customer ID`, keeping the first occurrence of each `Customer ID` and removing subsequent occurrences.
  - After deduplication, keep only the required output columns and arrange them exactly as specified.
- Output the data.

## Output

- output_01.csv
  - 5 fields:
    - Customer ID
    - First Name
    - Last Name
    - Phone Number
    - Address