## Context
The challenge focuses on Whyte's Cafe based in Stevenage in the UK. The cafe wants to know how much it would cost them to install a Meal Deal option (set at £5 each meal) on their menu. Each row of data is a product sold as part of an order (ticket). The overall goal is to determine the difference between original income and the income using the new Meal Deal pricing model. Note: you will need version 2019.1 as the solutions we created all needed Rows to Columns.

## Requirements

- Input the data
- There's been a system error so clean up:
  - Null Price should be 1.5
  - Null MemberIDs should be 0
- Not every product goes in to the Meal Deal so we need to work out the 'Excess Items' cost on top of the Meal Deals. Use the average cost per type of product within that ticket to work this out.
- We only want to analyse tickets that would be affected by the Meal Deal
- The Meal Deal is set at £5 each
- Overall goal is to determine the difference between our original income and the income using the new pricing model
- Note: you will need version2019.1 as the solutions we created all needed Rows to Columns
- Output the data

## Output

- output_01.csv
  - 6 fields:
    - Total Ticket Price
    - Ticket Price Variance to Meal Deal Earnings
    - Total Meal Deal Earnings
    - Total Excess
    - TicketID
    - MemberID
