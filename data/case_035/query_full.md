## Context
You have a time series of inbound stock movements and a list of store top-up requests. The goal is to (1) determine, for each store request, whether it can be fulfilled by its required date and, if not, when it will be fulfilled and how many days it is delayed, and (2) identify specific situations where inbound stock is surplus relative to store demand.

## Requirements
- Input the data:
  - Read `input_01.csv` as the stock schedule, containing at least `Supplier`, `Product`, `Scent`, `Date`, and `Quantity`.
  - Read `input_02.csv` as store requests, containing at least `Store`, `Product`, `Scent`, `Date Required`, and `Quantity Requested`.
  - Parse `Date` and `Date Required` as dates (not strings) for all calculations.

- Attach supplier information to each store request:
  - Build a mapping of `Product` + `Scent` to `Supplier` using the unique combinations present in the stock data.
  - Left-join this mapping onto the store requests on (`Product`, `Scent`) to add `Supplier` to each request. If no match exists, keep the request with a missing `Supplier`.

- Form a running total of our stock levels for each product & scent:
  - Sort stock records by `Product`, `Scent`, `Supplier`, then `Date` ascending.
  - Within each (`Product`, `Scent`, `Supplier`) group, compute a cumulative sum of `Quantity` to create a cumulative stock position over time.

- Form a running total of the requested quantities for each product & scent:
  - Sort supplier-attributed store requests by `Product`, `Scent`, `Supplier`, then `Date Required` ascending.
  - Within each (`Product`, `Scent`, `Supplier`) group, compute a cumulative sum of `Quantity Requested` to create a cumulative requested quantity over time.

- Compare stock levels to determine which store requests can be met on their requested date and, if not, how long the store has to wait:
  - Each output row corresponds to one original store request.
  - For a given request, find the earliest stock `Date` (within the same `Product`, `Scent`, `Supplier`) where `Cumulative Stock >= Cumulative Requested` for that request. Call this `first_available_date`.
  - Define `Date Fulfilled` as:
    - If a `first_available_date` exists: the later of (`Date Required`, `first_available_date`).
    - If no such stock date exists: `Date Fulfilled` is blank/null.
  - Compute `Days Request Delayed` as the number of days between `Date Fulfilled` and `Date Required`, with negative values clipped to 0. If `Date Fulfilled` is null, `Days Request Delayed` remains null.
  - Set `Stock Ready?` to `True` when `Days Request Delayed` equals 0; otherwise `False` (including when delay is null).
  - Format `Date Required` and `Date Fulfilled` as `DD/MM/YYYY` strings in the final output.

- Determine whether any products held in stock are not actually needed by any stores, and quantify surplus in the specific cases below:
  - Produce `output_01.csv` at the grain of (`Supplier`, `Product`, `Scent`) for rows that meet either of these surplus definitions:
    1) **Never requested anywhere** (ignoring supplier):
       - If a (`Product`, `Scent`) appears in the stock data but never appears in the store requests data at all, then for each `Supplier` shipping that (`Product`, `Scent`), define `Surplus Product` as the total sum of `Quantity` across all stock records for that (`Supplier`, `Product`, `Scent`).
    2) **Exactly one request, and it is delayed** (ignoring supplier for the “exactly one” condition):
       - Identify (`Product`, `Scent`) pairs that have exactly one store request in total.
       - For that single request, if `Date Fulfilled` is later than `Date Required` (i.e., the request is delayed), then for the corresponding (`Supplier`, `Product`, `Scent`) define `Surplus Product` as the sum of stock `Quantity` for stock records with `Date` strictly greater than that request’s `Date Fulfilled`.
       - Include the row only if this computed surplus is greater than 0.
  - Combine the rows from (1) and (2) into a single `output_01.csv` (do not deduplicate across the two rule sets).

- Output the data:
  - Create the two CSV outputs with exactly the required fields.

## Output

- output_01.csv
  - 4 fields:
    - Supplier
    - Product
    - Scent
    - Surplus Product

- output_02.csv
  - 9 fields:
    - Store
    - Product
    - Scent
    - Supplier
    - Quantity Requested
    - Date Required
    - Stock Ready?
    - Date Fulfilled
    - Days Request Delayed