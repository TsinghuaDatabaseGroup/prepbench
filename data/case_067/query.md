## Context
Chin & Beard Suds Co are relatively new players in the Soap Market and are looking to do a bit of analysis around their competitors. To do this, they'll be looking at a variety of different metrics.
Market Share = Company Sales / Total Market Sales
Growth = (This Month Sales - Last Month Sales) / Last Month Sales
Contribution to Growth = (This Month Sales - Last Month Sales) / Overall Last Month Sales
e.g. if calculating the Contribution to the Market's Growth then the numerator would use each Company's sales whilst the denominator would be the Total Market sales
Outperformance = Company A's Growth - The Growth of the Rest of the Market excluding Company A

## Requirements

- Input the data
- At a total sales level for each company (i.e. not taking Soap Scent into consideration):
  - Calculate each company's Market Share for April. How many bps* has this changed from March's Market Share?
  - *10 bps = 0.01%
  - Calculate each company's Growth in April.
  - Make sure everything is formatted nicely for a quick overview of each company's performance in April.
  - Output the data
- We notice that whilst Chin & Beard Suds Co have the smallest Market Share, they experienced the greatest growth this month!
  - Calculate the contribution to growth for the rest of the market excluding C&BS Co for each Soap Scent.
  - Calculate C&BS Co's contribution to growth for each soap scent.
  - Calculate the Outperformance of C&BS Co vs the Rest of the Market for each soap scent.
  - Output the data

## Output

- output_01.csv
  - 4 fields:
    - Company
    - Growth
    - April Market Share
    - Bps Change

- output_02.csv
  - 4 fields:
    - Soap Scent
    - CBBS Co Contribution to Growth
    - Rest of Market Contribution to Growth
    - Outperformance
