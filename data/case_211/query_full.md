## Context

You are given 12 monthly CSV input files containing stock purchase records. The goal is to standardise key numeric fields, derive a file-level date from each filename, bucket purchases and companies into defined size bands, and then identify the top 5 highest-value purchases within each month and category combination.

## Requirements

- Input the data.
- Input each of the 12 monthly files and process them consistently, then append (union) the results across all months into a single output table.

- Create a **File Date** from the month found in each input file name:
  - Extract the month number from the filename and set **File Date** to the first day of that month in 2023 (i.e., `2023-MM-01`).
  - If the month cannot be derived (i.e., is null/missing), replace it with `1` (January) before creating the date.

- Clean and standardise the market capitalisation field:
  - Create a numeric **Market Capitalisation** field representing the true monetary value of the input “Market Cap” (as a number of dollars).
  - Remove any rows where Market Cap is unavailable (e.g., recorded as `n/a`) or otherwise cannot be converted into a valid numeric Market Capitalisation.
  - Ensure the resulting monetary values are stored to 2 decimal places (rounding to 2 decimals).

- Clean and standardise the purchase price field:
  - Create a numeric **Purchase Price** field as a monetary value (number of dollars), also rounded to 2 decimal places.
  - (No additional filtering is required beyond what is needed to compute the downstream categorisation and ranking.)

- Categorise the **Purchase Price** into groupings using these numeric boundaries (inclusive/exclusive as implied by the ranges):
  - `0` up to but not including `25,000` → `Small`
  - `25,000` up to but not including `50,000` → `Medium`
  - `50,000` up to but not including `75,000` → `Large`
  - `75,000` and above → `Very Large`

- Categorise the **Market Capitalisation** into groupings:
  - Below `$100M` → `Small`
  - Between `$100M` and below `$1B` → `Medium`
  - Between `$1B` and below `$100B` → `Large`
  - `$100B` and above → `Huge`

- Rank the highest 5 purchases per combination of:
  - **File Date**
  - **Purchase Price Categorisation**
  - **Market Capitalisation Categorisation**
  Ranking rules:
  - Rank records within each group by **Purchase Price** in descending order (highest purchase price gets rank 1).
  - If multiple records have the same Purchase Price within a group, break ties deterministically by **Ticker** in ascending order.
  - Assign ranks as consecutive integers starting at 1 within each group.

- Output only records with a rank of 1 to 5 (inclusive).

- Output the data.

## Output

- output_01.csv
  - 10 fields:
    - Market Capitalisation Categorisation
    - Purchase Price Categorisation
    - File Date
    - Ticker
    - Sector
    - Market
    - Stock Name
    - Market Capitalisation
    - Purchase Price
    - Rank