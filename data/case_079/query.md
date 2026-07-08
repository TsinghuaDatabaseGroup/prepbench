## Context
Since we had so many interesting approaches to Carl's fill down challenge last week, I thought we'd continue the theme of multi-row data prep problems! This week we're looking at Chin & Beard Suds Co's slightly odd inventory ordering process. Every Wednesday, they restock each scent with 700 new bars. This is working on the assumption that the average sales for each scent are 100 bars a day. Any unsold bars on the Tuesday evening are deemed "not fresh enough" and thrown away. We've been tasked with finding out how many bars are being wasted due to this process and how much that's costing the company!

## Requirements

- Input the data
- Edit 20/08 - Final 3 days in July Removed from Daily Sales
- Calculate the Units Sold (=Daily Sales/Price)
- For each week (Wednesday-Tuesday), calculate the Weekly Units Sold and Weekly Sales.
- Calculate the Waste (=Units Ordered - Units Sold)
- Calculate the Waste Cost (=Cost*Waste)
- Calculate the Profit (Weekly Sales - Waste Cost)
- Rank each Scent from most profitable overall to least profitable overall
- Output the data

## Output

- output_01.csv
  - 3 fields:
    - Profitability Rank
    - Scent
    - Total Profit
