## Context
This week's challenge involves picking up some more of the fundamental skills and gives you some chances to practice some of the skills you've picked up over the last few weeks. The new technique for you to learn this week is Joins. Joins allow us to bring two data sources together. This allows for much easier, richer and deeper analysis as data is often in many different locations. The input file may seem familiar from last week. We still have 5 worksheets, each containing one Store's product sales. What's new is there is also a set of Quarterly Targets that each store is expected to achieve.

## Requirements

- Input the data
- Union the Stores data together
- Remove any unnecessary data fields your Input step might create and rename the 'Table Names' as 'Store'
- Pivot the product columns
- Split the 'Customer Type - Product' field to create:
  - Customer Type
  - Product
  - Also rename the Values column resulting from you pivot as 'Products Sold'
- Turn the date into a 'Quarter' number
- Sum up the products sold by Store and Quarter
- Add the Targets data
- Join the Targets data with the aggregated Stores data
  - Note: this should give you 20 rows of data
- Remove any duplicate fields formed by the Join
- Calculate the Variance between each Store's Quarterly actual sales and the target. Call this field 'Variance to Target'
- Rank the Store's based on the Variance to Target in each quarter
  - The greater the variance the better the rank
- Output the data

## Output

- output_01.csv
  - 6 fields:
    - Quarter
    - Rank
    - Store
    - Products Sold
    - Target
    - Variance to Target
