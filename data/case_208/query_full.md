## Context
You are preparing a shareable dataset that pre-computes common analytical fields (monthly totals, within-month ranks, and cross-month averages) so downstream users do not need to recreate ranking or level-of-detail style calculations in their BI tool.

## Requirements
- Input the data from `input_01.csv`.

- Create a new field called **Bank** from **Transaction Code** by extracting the leading letter code (i.e., split the transaction code at the first hyphen `-` and take the portion before the hyphen).

- Convert **Transaction Date** to represent only the **month of the transaction**:
  - Parse the existing transaction date/time value and replace it with the month name (full month name such as “January”, “February”, etc.), not the full date.

- Aggregate transaction values to monthly totals so the dataset has **one row per (Transaction Date month, Bank)**:
  - Group by **Transaction Date** (month) and **Bank**.
  - Compute **Value** as the **sum** of transaction values within each group.

- For each month, rank banks by their aggregated **Value** against the other banks in that same month:
  - Create **Bank Rank per Month** where **1 = highest Value** within the month.
  - If multiple banks tie on Value within a month, assign the same rank using “minimum rank” tie-handling (i.e., tied banks share the best/lowest rank number for that tie).

- Without losing the other required fields, compute and attach these two averages to every applicable row:
  - **Avg Rank per Bank**: for each **Bank**, take the **mean** of **Bank Rank per Month** across all months in which the bank appears; add this value back to each row for that bank.
  - **Avg Transaction Value per Rank**: for each **Bank Rank per Month** value (rank number), take the **mean** of **Value** across all rows having that rank (across all months); add this value back to each row with that rank.
  - Round **Avg Rank per Bank** and **Avg Transaction Value per Rank** to **9 decimal places**.

- Output the final dataset containing exactly the required fields. For deterministic output, sort rows by **Transaction Date** (month name) ascending, then by **Bank Rank per Month** ascending.

## Output

- output_01.csv
  - 6 fields:
    - Transaction Date
    - Bank
    - Value
    - Bank Rank per Month
    - Avg Transaction Value per Rank
    - Avg Rank per Bank