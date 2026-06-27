## Context
Chin & Beard Suds Co is introducing a subscription offering where customers choose one or more soap packages and a delivery frequency. One package type is a “Mystery” option that should probabilistically reflect what customers most commonly order among the non-mystery packages. To price the Mystery package, compute a frequency-weighted average price across the existing (non-mystery) packages based on how many orders per year customers generate for each package type.

## Requirements
- Input the data
  - Read three input files:
    - `input_01.csv`: a lookup that maps each customer “Frequency” code to a normalized frequency label (e.g., week/month/quarter/year).
    - `input_02.csv`: the subscription package catalog containing package identifiers, product names (aliases), and prices (the Mystery package price may be missing).
    - `input_03.csv`: customer subscriptions including customer `Name`, `Frequency`, and a `Packages` field listing one or more selected package identifiers.
- Calculate the price of the mystery package
  - Treat subscription package `7` as the Mystery package.
  - Expand the customer subscriptions so that each selected package becomes its own row:
    - Split `Packages` on the `|` delimiter to produce one row per `(customer, package)` selection.
    - Convert the resulting package identifier to a numeric value.
  - Convert each customer row’s `Frequency` into an annual order multiplier in two steps:
    1. Map the customer `Frequency` to the normalized frequency label using `input_01.csv` (left join / lookup; if no match, treat as unknown).
    2. Map the normalized label to an annual multiplier using:
       - `week` → 52  
       - `month` → 12  
       - `quarter` → 4  
       - `year` → 1  
       - unknown/unmapped → 0
  - Compute total annual orders contributed by each non-mystery package across all customers:
    - Exclude rows where the package is Mystery (`7`).
    - For each remaining package identifier, sum the annual multipliers across all customer-package rows; this sum is the package’s `annual_orders`.
  - Join package prices from `input_02.csv` onto these per-package annual order totals using the package identifier.
  - Compute the Mystery package price as the weighted average of package prices using `annual_orders` as weights:
    - `mystery_price = floor( sum(annual_orders * price) / sum(annual_orders) )`
    - If the total weight `sum(annual_orders)` is 0, set `mystery_price` to 0.
    - Ensure the resulting Mystery price is an integer (after flooring).
- Join back to original table containing product aliases and prices
  - Produce a finalized package-price table equal to the package catalog from `input_02.csv`, but with the Mystery package (`Subscription Package` = 7) price replaced by the computed `mystery_price`.
  - Ensure `Subscription Package` and `Price` are output as integers.
- Calculate total cost of each customers subscription normalised on an annual basis
  - Using the exploded customer-package rows and the same annual multiplier logic above:
    - Join the finalized package prices onto each customer-package row by package identifier.
    - If a package price is missing after the join, treat its price as 0 for cost calculations.
    - Compute each row’s annual cost as:
      - `annual_cost = price_per_period * annual_multiplier`
  - Aggregate to customer level:
    - Group by `Name` and sum `annual_cost` across all rows for that name (including cases where the same name appears in multiple input rows).
    - Output the summed annual cost as an integer.
- Output the data
  - Write the two required CSV outputs with exactly the specified columns.

## Output

- output_01.csv
  - 2 fields:
    - Subscription Cost (Per Annum)
    - Name

- output_02.csv
  - 3 fields:
    - Subscription Package
    - Product
    - Price