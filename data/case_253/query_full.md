## Context
Data Source Bank (DSB) wants to assess which savings account provider best suits a customer based on how much the customer plans to deposit each month. Some accounts cap the maximum monthly deposit; any amount above that cap should still be saved but must not earn interest. The goal is to simulate 12 months of saving per provider under a single planned monthly deposit amount, then rank providers by final savings and by total interest earned.

## Requirements
- Data cleaning:
  - Parse `Interest` field: remove the `%` symbol and convert to decimal (e.g., `8%` → `0.08`, `7.50%` → `0.075`). The `Interest` field in the input contains percentage values with a `%` suffix; these must be converted to decimal values by removing the `%` and dividing by 100.
  - Parse `Max Monthly Deposit` field: remove currency symbols (e.g., `£200` → `200`, `£250` → `250`). The field may contain currency symbols like `£` which must be stripped before numeric processing.
  - Handle `Has Additional Conditions` field: if the field is missing or empty (null/empty string), treat it as if no additional conditions apply (equivalent to `N`). Only when the field value is explicitly `Y` (case-insensitive after trimming whitespace) should ` (Conditions Apply)` be appended to the provider name.

- Input the data.
  - Use `inputs/input_01.csv` as the source.
  - The input must provide, at minimum, these fields for each provider: `Provider`, `Interest` (APR), and `Max Monthly Deposit`.
  - If an optional field `Has Additional Conditions` is present and indicates additional conditions apply (value `Y`), then the output `Provider` value must append ` (Conditions Apply)`; otherwise keep the provider name unchanged.

- Introduce a field which allows a used to control their Planned Monthly Deposit.
  - Use a single planned monthly deposit value for the entire run. For this task, set `Customer Planned Deposit` to **300** and carry it through to the output for every provider and month.

- If this value is greater than the Max Monthly Deposit allowed by the Provider, then calculate how much will be left over and receive no interest.
  - For each provider, compute:
    - `Monthly Deposit` = min(`Customer Planned Deposit`, `Max Monthly Deposit`) (this portion earns interest).
    - `Leftover Savings which won't receive interest` = max(`Customer Planned Deposit` − `Monthly Deposit`, 0) (this portion never earns interest).
  - Simulate savings over 12 months per provider (12 rows per provider; `Month` = 1 through 12), using:
    - Monthly interest rate = `Interest` / 12, where `Interest` is the decimal value after data cleaning (e.g., if input is `8%`, after cleaning it becomes `0.08`, so monthly rate = `0.08 / 12`).
    - Start with two balances at 0: an interest-bearing balance and a non-interest-bearing balance.
    - For each month, apply these steps in order:
      1) Add `Monthly Deposit` to the interest-bearing balance.
      2) Apply interest only to the interest-bearing balance for that month.
      3) Add `Leftover Savings which won't receive interest` to the non-interest-bearing balance **after** interest is applied.
    - `Savings each month` must equal the sum of the interest-bearing balance (after interest) plus the non-interest-bearing balance at the end of that month.
  - Compute per-provider summary measures (and repeat them on every monthly row for that provider):
    - `Max Possible Savings`: the savings value at the end of month 12 (equivalently, the maximum of `Savings each month` across months 1–12).
    - `Total Interest`: the total interest accrued over the 12-month simulation (sum of monthly interest amounts).

- Rank providers based on the per-provider summary measures.
  - `Providers Ranked by Max Savings`: dense rank of providers by `Max Possible Savings` in descending order (highest value gets rank 1).
  - `Providers Ranked by Total Interest`: dense rank of providers by `Total Interest` in descending order (highest value gets rank 1).
  - Attach both ranks to each provider-month row.
  - Sort the final output rows by:
    1) `Providers Ranked by Max Savings` ascending,
    2) `Providers Ranked by Total Interest` ascending,
    3) `Provider` ascending,
    4) `Month` ascending.

- Output the data.
  - Make it clear what the Customer's Planned Monthly Deposit is in the title of the output file.
  - Output the data.

- Numeric formatting:
  - Round `Savings each month`, `Max Possible Savings`, and `Total Interest` to 2 decimal places.
  - Keep `Interest`, deposit fields, and `Month` as numeric values in the output.

## Output

- output_01.csv
  - 12 fields:
    - Providers Ranked by Max Savings
    - Providers Ranked by Total Interest
    - Provider
    - Interest
    - Max Monthly Deposit
    - Customer Planned Deposit
    - Monthly Deposit
    - Leftover Savings which won't receive interest
    - Month
    - Savings each month
    - Max Possible Savings
    - Total Interest