## Context
This challenge advances data preparation skills by focusing on two core steps:
- Aggregation: changing the level of granularity by redefining what each row represents via categorical field combinations. This differs from how aggregation is typically performed in visualization tools and requires clarity on the row-level entity.
- Calculations: deriving required variables from existing fields when they are not directly present in the dataset.
Planning the order of transformation steps is crucial to avoid repeated work. In this task, we explore bike Brands available in stores to identify top sellers and compare whether customers of different brands experience similar outcomes. We will produce concise summary tables for a quick tabular view; optional visualization can be added if desired.

## Requirements

- Input the data
- Clean up the Model field to leave only the letters to represent the Brand of the bike
- Workout the Order Value using Value per Bike and Quantity.
- Aggregate Value per Bike, Order Value and Quantity by Brand and Bike Type to form:
  - Quantity Sold
  - Order Value
  - Average Value Sold per Brand, Type
- Calculate Days to ship by measuring the difference between when an order was placed and when it was shipped as 'Days to Ship'
- Aggregate Order Value, Quantity and Days to Ship by Brand and Store to form:
  - Total Quantity Sold
  - Total Order Value
  - Average Days to Ship
- Round any averaged values to one decimal place to make the values easier to read
- Output the data

## Output

- output_01.csv
  - 5 fields:
    - Brand
    - Bike Type
    - Quantity Sold
    - Order Value
    - Avg Bike Value per Brand

- output_02.csv
  - 5 fields:
    - Brand
    - Store
    - Total Quantity Sold
    - Total Order Value
    - Avg Days to Ship
