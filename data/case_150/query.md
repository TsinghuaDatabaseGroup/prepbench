## Context
It's the IT department's turn to receive our help this week. Rather than optimising the data for feeding into a data visualisation tool, we're going to think about how to optimally store data. In particular, we're going to be thinking about breaking a dataset down into fact and dimension tables. In many challenges, we focus on bringing datasets together that have a common ID field. Databases will often follow a star schema, where each dimension is a separate table that can join onto the main fact table. We have received the following desired schema from IT:

## Requirements

- Input the data
- Split out the store name from the OrderID
- Turn the Return State field into a binary Returned field
- Create a Sales field
- Create 3 dimension tables for Store, Customer and Product
  - When assigning IDs, these should be created using the dimension and minimum order date fields so that the IDs do not change when later orders are placed
  - For the Customer dimension table, we want to include additional fields detailing their total number of orders and the % of products they have returned
- Replace the dimensions with their IDs in the original dataset to create the fact table
- Output the data

## Output

- output_01.csv
  - 5 fields:
    - CustomerID
    - Customer
    - Return %
    - Number of Orders
    - First Order
  - CustomerID must be an integer string with no decimals.
  - First Order must be formatted exactly as `DD/MM/YYYY` (zero-padded); blank if missing.

- output_02.csv
  - 8 fields:
    - StoreID
    - CustomerID
    - OrderID
    - Order Date
    - ProductID
    - Returned
    - Quantity
    - Sales
  - StoreID, CustomerID, OrderID, and ProductID must be integer strings with no decimals.
  - Order Date must be formatted exactly as `DD/MM/YYYY` (zero-padded); blank if missing.

- output_03.csv
  - 6 fields:
    - ProductID
    - Category
    - Sub-Category
    - Product Name
    - Unit Price
    - First Sold
  - ProductID must be an integer string with no decimals.
  - First Sold must be formatted exactly as `DD/MM/YYYY` (zero-padded); blank if missing.

- output_04.csv
  - 3 fields:
    - StoreID
    - Store
    - First Order
  - StoreID must be an integer string with no decimals.
  - First Order must be formatted exactly as `DD/MM/YYYY` (zero-padded); blank if missing.
