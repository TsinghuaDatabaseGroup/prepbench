## Context
If you haven't had a chance to try out Parameters in Prep yet then here's the perfect opportunity! We're going to create a classic use case of the Pareto chart. How many customers make up 80% of our Sales?

## Requirements

- Input the data
- Aggregate the data to the total sales for each customer
- Calculate the percent of total sales each customer represents
- Calculate the running total of sales across customers
  - Order by the percent of total in a descending order
  - Round to 2 decimal places
- Create a parameter that will allow the user to decide the percentage of sales they wish to filter to
- Output the data, including the parameter in the output name
- Create a second output that describes the result in plain English
  - e.g. 50% of Customers account for 80% of Sales
- Output the data

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
