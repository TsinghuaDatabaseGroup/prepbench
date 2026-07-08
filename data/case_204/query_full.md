## Context

The Data Source Bank (DSB) has received a January transaction report that includes transactions processed by multiple banks. The goal is to standardize key fields and produce three summarized outputs that reconcile transaction values at different levels of detail.

## Requirements

- Input the data from `inputs/input_01.csv`.

- Derive a bank identifier from the transaction code:
  - Split `Transaction Code` on the hyphen (`-`) and take the segment before the first hyphen.
  - Store this extracted bank code in a new field named `Bank`.

- Standardize the transaction channel field:
  - In `Online or In-Person`, rename values so that `1` becomes `Online` and `2` becomes `In-Person`.

- Convert the transaction date to the day of the week:
  - Parse `Transaction Date` as a datetime using the format `DD/MM/YYYY HH:MM:SS`.
  - Replace `Transaction Date` with the corresponding weekday name (e.g., Monday–Sunday).

- Produce three aggregated outputs by summing `Value` at different grains:
  1. **Total Values of Transactions by each bank**
     - Group by `Bank`.
     - Sum `Value` within each `Bank`.
     - Sort the result by `Bank` ascending.
     - Grain: one row per `Bank`.

  2. **Total Values by Bank, Day of the Week and Type of Transaction (Online or In-Person)**
     - Group by `Bank`, `Online or In-Person`, and `Transaction Date` (weekday name).
     - Sum `Value` within each group.
     - Sort the result by `Bank`, then `Online or In-Person`, then `Transaction Date`, all ascending.
     - Grain: one row per (`Bank`, `Online or In-Person`, `Transaction Date`).

  3. **Total Values by Bank and Customer Code**
     - Group by `Bank` and `Customer Code`.
     - Sum `Value` within each (`Bank`, `Customer Code`) pair.
     - Ensure `Customer Code` is output as a string.
     - Sort the result by `Bank` then `Customer Code`, both ascending.
     - Grain: one row per (`Bank`, `Customer Code`).

- Output the data to the three CSV files specified below.

## Output

- output_01.csv
  - 2 fields:
    - Bank
    - Value

- output_02.csv
  - 4 fields:
    - Bank
    - Online or In-Person
    - Transaction Date
    - Value

- output_03.csv
  - 3 fields:
    - Bank
    - Customer Code
    - Value