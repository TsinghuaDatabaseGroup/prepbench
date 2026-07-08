## Context
Prep Air have asked for What If? Analysis to compare 2 different loyalty reward systems, understanding their impact on cost and the number of customers who might benefit from the program.

## Requirements
- Input the data
- To be part of either Prep Air Loyalty Scheme, Customers must have flown in the last year (on or after 21st February 2023)
- Create a parameter so that the number of flights a customer has taken is either bucketed into groups of 5 or groups to 10
  - e.g. if the parameter selected is 5, the groupings will be 1-4, 5-9 etc
  - if the parameter selected is 10, the groupings will be 1-9, 10-19 etc
- Create a field to categorize customers based on the selected parameter, called Tier
- Estimate the average number of flights a customer takes per year
- Filter the Prep Air Loyalty dataset to the selected parameter value
- Join the Prep Air Loyalty to the Customer dataset in a way that each customer also experiences the benefits of lower Tiers
  - e.g. a Tier 2 customer gets all the benefits of Tier 0, Tier 1 and Tier 2
- Split out the Benefits and make sure that each Benefit has its own row
- Join on the Costing dataset
- Calculate the Yearly Cost of each Benefit
  - e.g. if the Benefit Cost is per flight then make sure to multiply it by the Avg Number of Flights that customer takes in a year
- Total up the Yearly Cost for each Tier and count the Number of Customers in Each Tier
- Output the data

## Output

- output_01.csv
  - 3 fields:
    - Tier
    - Year Cost
    - Number of Customers

- output_02.csv
  - 3 fields:
    - Tier
    - Year Cost
    - Number of Customers
