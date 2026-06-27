## Context
Would you believe that Chin & Beard Suds Co have encountered yet more messy data? It seems someone was trying to be helpful by creating an aggregated view of sales per week for each scent of soap. However, in doing so we've lost the lower level of detail of the product sizes that make up these sales for each scent. We really need this for other analysis we've been carrying out!
Fortunately, we know what percentage of sales each product size makes up for each product in each week. Unfortunately, the data isn't stored in a way that will make it easy to join all the necessary information together.

## Requirements

- Input the data
- Our final output requires the Date to be in in the Year Week Number format.
- We don't care about any product sizes that make up 0% of sales.
- In the Lookup Table, it seems the Product ID and Size have been erroneously concatenated. These need to be separated.
- You'll need to do some cleaning of the Scent fields to join together the Total Sales and the Lookup Table.
- Calculate the sales per week for each scent and product size.
- Output the data

## Output

- output_01.csv
  - 5 fields:
    - Year Week Number
    - Secnt
    - Size
    - Product Type
    - Sales
