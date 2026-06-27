## Context

You are preparing a month-level sales dataset for a bicycle business. The goal is to report historical (non-forecast) performance through the last complete month (June 2023), ensure every Store × Bike Type has a continuous monthly time series over its active period, and compute a 3‑month moving average of Profit.

## Requirements

- Input the data from `input_01.csv`.

- Restrict the analysis to complete, historical months only:
  - Treat any records dated July 2023 or later as forecasted and exclude them.
  - Implement this by filtering to dates strictly earlier than `2023-07-01`, which results in data up to and including June 2023.

- Aggregate to a monthly level:
  - Derive `Month` from `Date` by assigning each record to its calendar month and representing the month as the month-start date (the first day of that month).
  - Group by `Month`, `Store`, and `Bike Type`.
  - For each group, compute:
    - `Sales` = sum of `Sales`
    - `Profit` = sum of `Profit`
  - The resulting grain must be one row per `Month` × `Store` × `Bike Type`.

- Scaffold the monthly series so that each `Store` × `Bike Type` has a continuous run of months:
  - For each `Store` × `Bike Type`, identify the first month in which it appears in the aggregated data (its start month).
  - Define the global end month as June 2023 (month-start date `2023-06-01`).
  - For each `Store` × `Bike Type`, generate all month-start dates from its start month through `2023-06-01`, inclusive.
  - Left join / merge this scaffold to the monthly aggregates on (`Month`, `Store`, `Bike Type`) so that months with no activity are present.
  - For scaffolded months where the aggregate is missing, set:
    - `Sales` to 0
    - `Profit` to 0
  - Ensure this scaffolding does not introduce duplicate rows for the same `Month` × `Store` × `Bike Type`.

- Calculate the 3 month Moving Average for the Profit for each Store and Bike Type:
  - Within each `Store` × `Bike Type`, order rows by `Month` ascending.
  - Compute `3 Month Moving Average Profit` as the simple mean of `Profit` over the current month and the prior 2 months (a 3-month rolling window).
  - Require a full 3 months of data to produce a value (i.e., the first two months of each `Store` × `Bike Type` series should have no moving-average value).

- Output the data:
  - Write the result to `output_01.csv`. If your broader process supports dynamic naming by run month/year, that may be applied externally, but the required deliverable for this task is the file named exactly as specified below.
  - Format `Month` as `DD/MM/YYYY` using the month-start date.
  - Ensure numeric outputs are written as text with these behaviors:
    - Missing moving-average values are output as blank.
    - Exact zeros are output as `0`.
    - `Sales` and `Profit` preserve up to 6 decimal places (without trailing zeros).
    - `3 Month Moving Average Profit` preserves up to 9 decimal places (without trailing zeros).

## Output

- output_01.csv
  - 6 fields:
    - Month
    - Store
    - Bike Type
    - Sales
    - Profit
    - 3 Month Moving Average Profit