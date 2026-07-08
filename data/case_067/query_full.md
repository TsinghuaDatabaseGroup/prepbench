## Context
Chin & Beard Suds Co want a competitor performance readout using standard market metrics for March vs April.

Use the following metric definitions as the basis for the required outputs (with the exact calculation and formatting rules specified below):
- Market Share = Company Sales / Total Market Sales
- Growth = (This Month Sales - Last Month Sales) / Last Month Sales
- Contribution to Growth = (This Month Sales - Last Month Sales) / Overall Last Month Sales  
  (i.e., when attributing growth, the numerator is for the entity being measured, while the denominator is the relevant overall March total for the benchmark group)
- Outperformance = Company A’s Growth − Growth of the rest of the market excluding Company A

## Requirements

- Input the data.
  - Use `input_01.csv` as the single source table. Treat `Sales` as numeric.
  - Use only the months `March` and `April`.
- At a total sales level for each company (i.e. not taking Soap Scent into consideration):
  - Compute each company’s total `March` sales and total `April` sales by summing `Sales` across all soap scents.
  - Compute market totals for March and April as the sum of company totals in each respective month.
  - Calculate each company's Market Share for April:
    - April Market Share (as a percent) = (Company April Sales / Total Market April Sales) * 100.
    - Format April Market Share to 2 decimal places using round-half-up.
  - How many bps* has this changed from March's Market Share?
    - March Market Share (as a proportion) = Company March Sales / Total Market March Sales.
    - April Market Share (as a proportion) = Company April Sales / Total Market April Sales.
    - Bps Change = round((April Share − March Share) * 10000) to the nearest integer (0 decimals) and output as an integer.
    - *10 bps = 0.01%
  - Calculate each company's Growth in April:
    - Growth = ((Company April Sales − Company March Sales) / Company March Sales) * 100.
    - Format Growth to 2 decimal places using round-half-up.
  - Make sure everything is formatted nicely for a quick overview of each company's performance in April:
    - Output one row per company.
    - Keep the column names exactly as specified in the Output section.
    - Order the rows by company in this exact sequence:
      1) British Soaps  
      2) Soap and Splendour  
      3) Sudsie Malone  
      4) Chin & Beard Suds Co  
      5) Squeaky Cleanies
  - Output the data.
- We notice that whilst Chin & Beard Suds Co have the smallest Market Share, they experienced the greatest growth this month!
  - Work at the Soap Scent level, producing one row per scent, and split the market into:
    - Chin & Beard Suds Co (“CBBS”), and
    - Rest of market (all companies excluding Chin & Beard Suds Co).
  - Compute the March total sales for each group (CBBS March total across all scents; Rest-of-market March total across all scents). These totals are the denominators used for contribution-to-growth calculations.
  - For each Soap Scent, compute CBBS Co Contribution to Growth:
    - CBBS signed contribution (percentage points) = (CBBS April sales for the scent − CBBS March sales for the scent) / (CBBS March total sales across all scents) * 100.
    - Round this signed value to 2 decimals using round-half-up.
    - Output the signed rounded value, keeping negative values when sales decreased.
  - Calculate the contribution to growth for the rest of the market excluding C&BS Co for each Soap Scent:
    - Rest-of-market signed contribution (percentage points) = (Rest April sales for the scent − Rest March sales for the scent) / (Rest March total sales across all scents) * 100.
    - Round this signed value to 2 decimals using round-half-up.
    - Output the signed rounded value, keeping negative values when sales decreased.
  - Calculate the Outperformance of C&BS Co vs the Rest of the Market for each Soap Scent:
    - Outperformance = (rounded CBBS signed contribution − rounded Rest-of-market signed contribution), then round-half-up to 2 decimals.
  - Order the rows by Soap Scent in this exact sequence:
    - Rose, Orange, Lime, Coconut, Watermelon, Pineapple, Jasmine.
  - Output the data.

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
