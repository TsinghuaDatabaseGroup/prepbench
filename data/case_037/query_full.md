## Context

You have six monthly trading extracts of orders, each containing a product’s scent, product type, and whether the order was returned. The goal is to compute return-rate summaries across multiple “Type” groupings (overall, by month, by product type, and by fruit vs non-fruit scents) and deliver them in a single consolidated output table.

## Requirements

- Input the data (all six files).
  - Read `input_01.csv` through `input_06.csv`.
  - From each file, use only the fields needed for this task: `Scent`, `Product Type`, and `Return`.

- Form a Date using the file number as a month.
  - Treat the two-digit file number (`01`–`06`) as the month number.
  - Create a month label formatted as `YYYY-MM-01` using year `2019` (e.g., file `input_01.csv` maps to `2019-01-01`).

- Categorise Product Types as Fruit or Non-Fruit.
  - Create a `Fruit / Non-Fruit` classification based on `Scent`, where:
    - `Fruit` scents are exactly: `Apricot`, `Raspberry`, `Pineapple`, `Lemon`, `Lime`.
    - All other scents are `Non-Fruit`.

- Define the returned flag used in all calculations.
  - Interpret `Return` as a boolean indicator where values equivalent to `true` mean “returned” and values equivalent to `false` mean “not returned”.
  - Any non-recognized/missing return indicator is treated as “not returned” for calculation purposes.

- Form your % Return Rates for:
  - The full data set
    - Create a single row with `Type = All`.
  - Month of Trading
    - Create one row per month label (`2019-MM-01`) derived from the input file number.
  - Product Type
    - Create one row per distinct `Product Type`.
  - Fruit / Non-Fruit Scents
    - Create one row for `Fruit` and one row for `Non-Fruit`.

- For each row produced in any of the above groupings, compute the following metrics:
  - `Total Orders`: the count of orders (rows) in that group.
  - `Returned Orders`: the count of orders flagged as returned in that group.
  - `% Returned`: `(Returned Orders / Total Orders) * 100`, rounded to 1 decimal place.

- Create one output table.
  - Append/stack the grouping results into a single table with a shared schema.
  - `Type` must contain:
    - Product type values for the product-type section,
    - `All` for the overall section,
    - `Fruit` and `Non-Fruit` for the scent-category section,
    - Month labels (`2019-MM-01`) for the month section.
  - Preserve a deterministic row ordering in the final output as follows:
    1) Product types in this order: `Bar`, `Massage Bar`, `Bath Bomb`, `Liquid`
    2) Then: `All`, `Non-Fruit`, `Fruit`
    3) Then months in this order: `2019-05-01`, `2019-04-01`, `2019-03-01`, `2019-02-01`, `2019-01-01`, `2019-06-01`

- Optional - Build the visualisation too allowing the user to click on a 'Type' to set that as the benchmark rate of returns that all other types will be compared against.

- Output the data.

## Output

- output_01.csv
  - 4 fields:
    - Returned Orders
    - Total Orders
    - % Returned
    - Type