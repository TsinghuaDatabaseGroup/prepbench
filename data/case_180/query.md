## Context
This week's challenge is a continuation of another introductory month for newer Preppers. When you work with data, you are likely to increasingly ask more and more questions as you find out new insights. These additional questions often means you need to combine data sets together. This uses a technique called Joins. For this week's challenge, you might want to use the supporting links if you haven't joined data sets together before. If you are newer to preparing data then you might want to use the following links to learn these techniques: Pivot, Joins, String calculations.

## Requirements

- Input the data
- Remove unnecessary values from the Product Name field to just leave the Product Type
- Total Sales for each Store and Product Type
- Change the Targets data set into three columns
  - Product
  - Store
  - Sales Target (k's)
- Multiple the Sales Target (k's) by 1000 to create the full sales target number (i.e.75 becomes75000)
- Prepare your data sets for joining together by choosing your next step:
  - Easy - make your Sales input Product Type and Store name UPPER CASE
  - Hard - make your Targets' Store and Product fields TitleCase
- Join the data sets together and remove any duplicated fields
- Calculate whether each product in each store beats the target
- Output the data

## Output

- output_01.csv
  - 6 fields:
    - Beats Target?
    - Target
    - Store Name
    - Region
    - Sale Value
    - PRODUCT
