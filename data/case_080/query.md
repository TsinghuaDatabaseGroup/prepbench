## Context
This week is a follow on from last week's challenge. Chin & Beard Suds Co execs were very interested in our profitability analysis and want to see if we can make any suggestions for improvement. The first place to start is challenging the assumption that each Scent sells 100 bars a day on average. Once we calculate the actual average sales of each Scent per week, we'll see if ordering based on this figure improves profitability for C&BS Co.

## Requirements

- Input the data
- Calculate the Average Units Sold each day for each Scent
- Round this upwards to the nearest whole number
- Round this to the nearest 10
- Multiply this by 7
- Use the Average Units Sold as the new Units Ordered value and calculate the Waste (=Units Ordered - Units Sold) in this new scenario
- For negative values, this means we need to adjust our weekly sales as we would have run out of stock
- Calculate the new Profit values for each Scent
- Compare them to previous Profit values and calculate the difference
- Output the data

## Output

- output_01.csv
  - 4 fields:
    - Scent
    - Total Profit
    - New Profit
    - Difference
