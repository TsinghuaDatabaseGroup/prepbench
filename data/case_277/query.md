## Requirements

- Input the data
- Start with the Loyalty Points table:
  - Change the DateTime_Out field to a Date data type
  - Extract the numeric part of the Loyalty Points field
  - Extract the First Name and Last Name Initial from the Email Address
- Join to the Customer Details table, ensuring the number of rows remains at 999
- Join on the Store Data table
- Remove unnecessary fields
- Filter out customers without postcodes (it will be difficult to send gifts to these customers!)
- For each store, rank the customers
  - Customers with the highest number of loyalty points should be ranked #1
- Filter to the top 5 customers for each store
  - This may result in more than 5 customers per store if there has been ties in the number of loyalty points. SuperBytes wants to reward all these customers.
- Output the data

## Output

- output_01.csv
  - 10 fields:
    - City
    - Store
    - Rank
    - Email Address
    - First Name
    - Last Name
    - Loyalty Points
    - Date
    - Postcode
    - address
