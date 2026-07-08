## Context
This week we want to analyse the orders that customers have made over a period of time in our restaurant Serendipia. In order to identify how much money we earn each day of the week and also to discover who our top customer is. We are going to be using calculations, pivots and aggregations so lots of the fundamental techniques that are used within data prep!

## Requirements

- Input the data
- Modify the structure of the Menu table so we can have one column for the Type (pizza, pasta, house plate), the name of the plate, ID, and Price
- Modify the structure of the Orders table to have each item ID in a different row
- Join both tables
- On Monday's we offer a 50% discount on all items. Recalculate the prices to reflect this
- For Output 1, we want to calculate the total money for each day of the week
- For Output 2, we want to reward the customer who has made the most orders for their loyalty. Work out which customer has ordered the most single items
- Output the data

## Output

- output_01.csv
  - 2 fields:
    - Price
    - Weekday

- output_02.csv
  - 2 fields:
    - Count Items
    - Customer Name
