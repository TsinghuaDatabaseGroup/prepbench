## Context
Build a Pareto-style view of customer sales contribution to determine how many customers account for a target share of total sales (set to 80% in this task), and provide both the filtered customer-level detail and a plain-English summary statement.

## Requirements
- Input the data from `input_01.csv`.

- Produce a customer-level dataset (one row per `Customer ID`) by aggregating sales:
  - Group by `Customer ID`.
  - Compute `Sales` as the sum of `Sales` across all rows for that customer.
  - Carry forward customer name fields by taking the first observed `First Name` and the first observed `Surname` per `Customer ID`.
  - Rename `Surname` to `Last Name`.
  - Round aggregated `Sales` to 3 decimal places.

- Compute each customer’s share of total sales:
  - Compute total sales as the sum of the aggregated customer `Sales` over all customers.
  - Create `% of Total` as `(Sales / total_sales) * 100`.
  - Round `% of Total` to 9 decimal places.

- Compute the running cumulative contribution across customers:
  - Sort customers by `% of Total` in descending order.
  - Create `Running % of Total Sales` as the cumulative sum of `% of Total` in that sorted order.
  - Round `Running % of Total Sales` to 2 decimal places.

- Create a parameter representing the target cumulative percentage of sales to keep:
  - Use a target percentage value of `80.0`.

- Filter customers to the set whose running cumulative percentage is within the target:
  - Keep only rows where `Running % of Total Sales` is less than or equal to the target percentage (i.e., include all customers up to and including 80.0%, and exclude the first customer that would take the running total above 80.0%).

- Output the filtered customer detail as `output_01.csv` with exactly the fields listed in the Output section.

- Create a second output that describes the result in plain English:
  - Let `TotalCustomers` be the number of customers in the full customer-level dataset (before filtering).
  - Let `FilteredCustomers` be the number of customers remaining after the 80% running-total filter.
  - Compute the percentage of customers as `round(FilteredCustomers * 100 / TotalCustomers)` and express it as an integer percent.
  - Output a single-row, single-field text value in the form: `"<Pct>% of Customers account for 80% of Sales"`.

- Output the second result as `output_02.csv`.

## Output

- output_01.csv
  - 6 fields:
    - Customer ID
    - First Name
    - Last Name
    - Sales
    - % of Total
    - Running % of Total Sales

- output_02.csv
  - 1 fields:
    - Result