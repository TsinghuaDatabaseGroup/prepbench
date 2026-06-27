## Context
This week's challenge sees us looking at the Accessory Sales at our Bike Store.
Input: One Excel sheet with 5 tabs of data: London, Leeds, York, Manchester, Birmingham. The structure of the data is the same in each worksheet.

## Requirements

- Input the data
- Pivot 'New' columns and 'Existing' columns
- Split the former column headers to form:
  - Customer Type
  - Product
- Rename the measure created by the Pivot as 'Products Sold'
- Create a Store column from the data
- Remove any unnecessary data fields
- Turn Date into Quarter
- Aggregate to form two separate outputs of the number of products sold by:
  - Product, Quarter
  - Store, Customer Type, Product
- Output the data

## Output

- output_01.csv
  - 3 fields:
    - Product
    - Quarter
    - Products Sold

- output_02.csv
  - 4 fields:
    - Store
    - Customer Types
    - Product
    - Products Sold
