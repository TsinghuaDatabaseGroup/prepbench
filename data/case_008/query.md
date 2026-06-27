## Context
As we saw last week, Profits are rolling in nicely from Chin & Beard Suds Co. but all is not perfect at the company. Recently our Suds shops have been the victim of a number of thefts. Thankfully our systems allow our stores to record the thefts, when the theft occurred and when we adjusted the inventory to reflect the reduced amounts.
The data has all the parts we need to answer a few questions:
1. What product is stolen the most?
2. How many items of stock haven't been updated in the inventory levels yet?
3. What stores need to update their inventory levels?
4. Which store is the fastest at updating inventory levels post a theft?
5. Which stores have updated their stock levels incorrectly?
To be able to answer these questions, we need you to create the following data set.

## Requirements

- Input the data
- Input data from both sheets
- Update Store IDs to use the Store Names
- Clean up the Product Type to just return two products types: Bar and Liquid
- Measure the difference in days between when the theft occurred and when the stock was updated
- Measure the variance in stolen stock and inventory adjustment
- Output the data

## Output

- output_01.csv
  - 9 fields:
    - Branch Name
    - Crime Ref Number
    - Days to complete adjustment
    - Number of Records
    - Stock Adjusted
    - Stock Variance
    - Stolen volume
    - Theft
    - Type
