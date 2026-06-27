## Requirements

- Input the data
- For all cases where the Date Sold is after the Date Returned, swap the values in these fields
- Calculate the number of days between the Date Sold and Date Returned
- For returns within 60 days, customers get a full refund. For returns between 60 and 100 days, customers will be refunded half (rounded to the nearest penny). Returns after 100 days are not refunded
- MiniBytes want one output to be able to see, for each month:
  - Revenue (i.e. total amount through sales)
  - Total Returns Value (Refunds are counted in the month the return happens)
  - Number of Returns (in that month, regardless of Date Sold)
  - Avg Days to Return (for items returned that month)
- All values should be rounded to 2 decimal places
- Output the data

## Output

- output_01.csv
  - 5 fields:
    - Date
    - Revenue
    - Total Returns Value
    - Number of Returns
    - Avg Days to Return
