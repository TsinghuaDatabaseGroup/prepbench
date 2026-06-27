## Context
Now that Veganuary has come and gone we thought it would be interesting to take a look at some common supermarket products and use Prep to figure out whether or not they are vegan. Some results may surprise you! For the sake of this analysis we're taking bee by-products as non-vegan (beeswax, honey, etc).

## Requirements

- Input the data
- Prepare the keyword data
  - Add an 'E' in front of every E number.
  - Stack Animal Ingredients and E Numbers on top of each other.
  - Get every ingredient and E number onto separate rows.
- Append the keywords onto the product list.
- Check whether each product contains any non-vegan ingredients.
- Prepare a final shopping list of vegan products.
  - Aggregate the products into vegan and non-vegan.
  - Filter out the non-vegan products.
- Prepare a list explaining why the other products aren't vegan.
  - Keep only non-vegan products.
  - Duplicate the keyword field.
  - Rows to columns pivot the keywords using the duplicate as a header.
  - Write a calculation to concatenate all the keywords into a single comma-separated list for each product, e.g. "whey, milk, egg".
- Output the data

## Output

- output_01.csv
  - 2 fields:
    - Product
    - Description

- output_02.csv
  - 3 fields:
    - Product
    - Description
    - Contains
