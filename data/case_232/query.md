## Context

For this challenge we're continuing to play around with the new features in the latest 2023.2 version of Tableau Prep. These will be:
- % Difference From
- Lookup function
Both these calculations will help us work across multiple rows of data in slightly different ways. We'll be using them to help AllChains analyse the performance of their Stores over the last financial year.

## Requirements

- Input the data
- Bring all the Months together into a single table
- Merge together misaligned fields
- Create an Order Date field
- The financial year for Allchains starts in July. Convert the dates to Fiscal Quarters
- Aggregate the data to a Quarterly level for each Store, ignoring the product details
- Calculate the % Difference in Sales from the Previous Quarter
  - Multiply this value by 100 and round to 1 decimal place
- Use the lookup function so that we can compare the % Difference for all Quarters in a single row
- Evaluate each Store's performance by categorising them in the following way:
  - If a Store has seen consistent growth - "Going from strength to strength"
  - If a Store has seen consistent decline - "Going from bad to worse"
  - If a Store has 1 negative Quarter:
    - In Q2 - "Good growth in last half"
    - In Q3 - "Some good growth, but concerns in Q3"
    - In Q4 - "Good growth, until Q4"
  - If a Store has only 1 positive Quarter:
    - In Q2 - "Concerning performance in last half"
    - In Q3 - "Concerning performance, excluding Q3"
    - In Q4 - "Concerning performance, but improving in Q4"
- Output the data

## Output

- output_01.csv
  - 5 fields:
    - Store
    - Quarter
    - Sales
    - % Difference Q on Q
    - Store Evaluation
