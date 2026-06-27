## Context

Data Source Bank (DSB) is considering launching a 12-month Regular Savings Account. To benchmark the market and support decisions on (1) the interest rate and (2) the maximum monthly deposit allowed, DSB wants to compare existing 12-month products and illustrate how a customer’s balance would grow month by month when they contribute the maximum amount each month.

## Requirements

- Input the data from `input_01.csv`.

- Standardise and type key input fields so calculations and customer-facing labels are consistent:
  - Convert **Max Monthly Deposit** to a numeric value (so it can be used in arithmetic).
  - Convert **Interest** from a percentage representation to a numeric annual rate in decimal form (e.g., 8% → 0.08).
  - Update **Provider** so customers can see in a single field which accounts have additional conditions:
    - If **Has Additional Conditions** indicates “Y”, append `" (Conditions Apply)"` to the Provider name.
    - Otherwise, leave the Provider name unchanged.
  - After using it to update Provider, do not include **Has Additional Conditions** in the output.

- Ensure the output contains one row per account per month across the 12-month term:
  - For each unique account (defined by Provider, Interest, and Max Monthly Deposit after the updates above), generate rows for **Month = 1, 2, …, 12**.
  - This means each account must have exactly 12 rows in the final output.

- Calculate the customer’s accumulated savings each month assuming they deposit the **Max Monthly Deposit** every month and interest compounds monthly:
  - Let `r` be the annual interest rate in decimal form and let `q = 1 + (r / 12)`.
  - For each account and each `Month = m`, compute **Savings each month** as the value at month `m` of a series of `m` equal monthly deposits, with the oldest deposit accruing the most months of interest and the newest deposit accruing one month of interest.
  - Use the closed-form equivalent of that accumulation:
    - **Savings each month (at month m)** = `Max Monthly Deposit * q * (q^m - 1) / (q - 1)`.
  - Round **Savings each month** to 2 decimal places.

- Create summary metrics per account (repeated on each of the 12 rows for that account):
  - **Max Possible Savings**: the maximum value of **Savings each month** across the 12 months for that account (i.e., the peak over months 1–12). Round to 2 decimal places.
  - **Total Interest**: `Max Possible Savings - (Max Monthly Deposit * 12)`. Round to 2 decimal places.

- Rank accounts (providers) using dense ranking (no gaps in rank values) with higher values receiving better ranks (rank 1 is highest):
  - **Providers Ranked by Max Savings**: dense rank of **Max Possible Savings** in descending order.
  - **Providers Ranked by Total Interest**: dense rank of **Total Interest** in descending order.
  - These rank values must be constant across all 12 rows for the same account.

- Create a **Sort** field to define the final row ordering:
  - Sort the full dataset by **Providers Ranked by Total Interest** ascending (best rank first), then by **Month** ascending.
  - Assign **Sort** as a 1-based sequential index in this sorted order (first row has Sort = 1, next row Sort = 2, etc.).

- Round all monetary values to 2 decimal places (this applies to **Savings each month**, **Max Possible Savings**, and **Total Interest**).

- Output the data exactly in the required structure and field order.

## Output

- output_01.csv
  - 10 fields:
    - Providers Ranked by Max Savings
    - Providers Ranked by Total Interest
    - Provider
    - Interest
    - Max Monthly Deposit
    - Month
    - Savings each month
    - Max Possible Savings
    - Total Interest
    - Sort