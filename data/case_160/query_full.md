## Context
You are performing a customer cohort analysis using only the Orders data (as in Tableau’s Sample Superstore). Each customer-year must be classified based on ordering behavior, and the result must be returned at a grain that includes both real order rows and scaffolded “no order” rows for years in which the customer did not purchase.

Customer classification definitions:
- **New** = this is the first year the customer has ordered
- **Consistent** = the customer ordered this year and last year
- **Sleeping** = the customer has ordered in the past, but not this year
- **Returning** = the customer did not order last year, but has ordered this year

## Requirements
- Input the data.
  - Use `input_01.csv` as the Orders table.
  - Parse `Order Date` and `Ship Date` as dates for year derivation.
- Derive a calendar year field:
  - Create `Year` as the year component of `Order Date` (integer).
- Aggregate the data to the years each customer made an order.
  - At minimum, identify whether each (`Customer ID`, `Year`) pair has one or more orders.
- Calculate the year each customer made their First Purchase.
  - Define `First Purchase` as the minimum `Year` observed for each `Customer ID` (integer).
- Scaffold the dataset so that there is a row for each year after a customers First Purchase, even if they did not make an order.
  - For every `Customer ID`, generate one row per `Year` from that customer’s `First Purchase` through the maximum `Year` present anywhere in the orders dataset (inclusive).
  - Each scaffold row must carry `Customer ID`, `Year`, and `First Purchase`.
- Create a field to flag these new rows, making it clear whether a customer placed an order in that year or not.
  - Create `Order?` as a flag with values:
    - `1` if the customer placed at least one order in that year
    - `0` if the scaffolded customer-year has no orders
- Calculate the Year on Year difference in the number of customers from each Cohort in each year
  - Cohort = Year of First Purchase
  - For each (`First Purchase`, `Year`), compute `Customer_Count` as the number of distinct `Customer ID` with `Order? = 1` in that cohort-year.
  - Compute `YoY Difference` within each cohort (`First Purchase`) as:
    - `Customer_Count` minus the prior year’s `Customer_Count` for that same cohort (i.e., shift by one `Year` within `First Purchase`).
  - If there is no prior year value for the cohort-year, `YoY Difference` must be left missing at this stage (and later rendered as blank in the output).
- Create a field which flags whether or not a customer placed an order in the previous year.
  - Within each `Customer ID`, sort by `Year` ascending and compute `Prev_Year_Order` as the prior row’s `Order?`; if no prior year exists, treat as `0`.
- Create the Customer Classification using the above definitions.
  - Determine `Customer Classification` per scaffolded customer-year using this precedence:
    1) If `Order? = 0` → `Sleeping`
    2) Else if `Year = First Purchase` → `New`
    3) Else if `Prev_Year_Order = 1` → `Consistent`
    4) Else → `Returning`
- Join back to the original input data.
  - For years where `Order? = 1`, return one output row per original order row, preserving the original order-level fields, and attach the customer-year fields (`Customer Classification`, `YoY Difference`, `Order?`, `Year`, `First Purchase`).
  - For years where `Order? = 0`, output exactly one synthetic row per (`Customer ID`, `Year`) scaffold row.
    - Ensure that in rows where a customer did not place an order, the majority of the original fields are null. The exceptions to this are the Customer Name and Customer ID fields.
- Output formatting rules that affect values:
  - Format `Order Date` and `Ship Date` as `DD/MM/YYYY` exact text; if the date is missing (synthetic no-order rows), output a blank string.
  - Output `Order?` as exact text `0` or `1` (do not treat as boolean).
  - Output `Year` and `First Purchase` as integers.
  - Output `YoY Difference` as a blank string when missing; otherwise as an integer.
  - For numeric fields `Sales`, `Quantity`, `Discount`, and `Profit`, round to 4 decimal places when a numeric value is present; keep them blank on synthetic no-order rows.
  - Output `Postal Code` as an integer when present; otherwise output a blank string.
- Output ordering (to make results deterministic):
  - Sort rows by `Customer Classification` in this order: New, Sleeping, Returning, Consistent; then by `Year`, `First Purchase`, `Customer ID`, `Order?`, and `Row ID` ascending (with nulls last).
- Output the data.

## Output

- output_01.csv
  - 26 fields:
    - Customer Classification
    - YoY Difference
    - Order?
    - Year
    - First Purchase
    - Row ID
    - Order ID
    - Order Date
    - Ship Date
    - Ship Mode
    - Customer Name
    - Segment
    - Country/Region
    - City
    - State
    - Postal Code
    - Region
    - Product ID
    - Category
    - Sub-Category
    - Product Name
    - Sales
    - Quantity
    - Discount
    - Profit
    - Customer ID
