## Context
We have collected the sales data for two stores and our online shop from the start of the year for a few weeks. We'd like to know how long between the orders of each of the types of products in the different locations.

## Requirements

- Input the data
- Link the Instore and Online sales together to be one data source
  - Call the Nulls in the Stores field Online
- Link in the product Lookup to name the products instead of having their ID number
- Create the 'Product Type' field by taking the first word of the product name
- Create a data set from your work so far that includes the next sale after the one made in the SAME store of the same product type
- Workout how long it took between the original sale and the next sale in minutes
  - Remove any negative differences. These are sales that got refunded.
- Create a data set that shows the average of these values for each store and product type. Call this field 'Average mins to next sale'
- Output the data

## Output

- output_01.csv
  - 3 fields:
    - Average mins to next sale
    - Product Type
    - Store
