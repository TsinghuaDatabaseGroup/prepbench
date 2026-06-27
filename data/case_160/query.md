## Context
Here are the definitions for how we will classify the customers:
- New = this is the first year the customer has ordered
- Consistent = the customer ordered this year and last year
- Sleeping = the customer has ordered in the past, but not this year
- Returning = the customer did not order last year, but has ordered this year
You may recognise this as the sample superstore dataset that comes with Tableau Desktop by default. We're using just the Orders table.

## Requirements

- Input the data
- Aggregate the data to the years each customer made an order
- Calculate the year each customer made their First Purchase
- Scaffold the dataset so that there is a row for each year after a customers First Purchase, even if they did not make an order
- Create a field to flag these new rows, making it clear whether a customer placed an order in that year or not
- Calculate the Year on Year difference in the number of customers from each Cohort in each year
  - Cohort = Year of First Purchase
- Create a field which flags whether or not a customer placed an order in the previous year
- Create the Customer Classification using the above definitions
- Join back to the original input data
  - Ensure that in rows where a customer did not place an order, the majority of the original fields are null. The exceptions to this are the Customer Name and Customer ID fields.
- Output formatting for exact-text fields:
  - Output `Order?` as exact text values `0` or `1` (not boolean).
  - Output `Order Date` and `Ship Date` as exact text in `DD/MM/YYYY` format; if missing, output blank.
- Output the data

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
