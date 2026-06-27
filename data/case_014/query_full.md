## Context
Whyte’s Cafe in Stevenage (UK) is evaluating the financial impact of introducing a fixed-price Meal Deal on its menu. The input data is at the line-item level, where each row represents a product sold as part of a customer order (“ticket”). The objective is to compare original ticket income to the income that would result under the new Meal Deal pricing model, where qualifying items are bundled into Meal Deals and any remaining items are charged as “excess” on top of the deals. Note: you will need version 2019.1 because the workflow requires a Rows-to-Columns (pivot) operation.

## Requirements
- Input the data from `input_01.csv` (each row is a product line within a ticket/order).
- Apply the following corrections due to a system error:
  - For rows where `Price` is null, set `Price` to `1.5`.
  - For rows where `MemberID` is null, set `MemberID` to `0`, and treat `MemberID` as an integer identifier thereafter.
- Perform the analysis at the ticket level, with one output row per unique combination of `TicketID` and `MemberID`.
- Convert the line-item data into ticket-level counts and sums by product `Type`:
  - For each (`TicketID`, `MemberID`), compute the count of items and the sum of `Price` for each `Type`.
  - The Meal Deal logic is based on three item types: `Drink`, `Main`, and `Snack`.
- Determine how many Meal Deals apply to each ticket:
  - `Number of Meal Deals` = the minimum of (`Drink` item count, `Main` item count, `Snack` item count) for that ticket.
- Compute original income per ticket:
  - `Total Ticket Price` = (sum of `Price` for `Drink`) + (sum of `Price` for `Main`) + (sum of `Price` for `Snack`) for that ticket.
- We only want to analyse tickets that would be affected by the Meal Deal:
  - Keep only tickets where `Number of Meal Deals` > 0.
- Apply the Meal Deal pricing model:
  - The Meal Deal is set at £5 each.
  - `Total Meal Deal Earnings` = `Number of Meal Deals` * 5.
- Not every product goes into the Meal Deal; compute the “Excess Items” cost on top of the Meal Deals using the average cost per type within that ticket:
  - For each type (`Drink`, `Main`, `Snack`), compute the ticket-level average unit price as (type sum / type count). If the count for a type is 0, use 0 for that type’s average.
  - For each type, compute excess item value as: (type count − `Number of Meal Deals`) * (type average unit price).
  - `Total Excess` = sum of the three excess item values, rounded to 2 decimal places.
- Compute the difference between original income and Meal Deal model income:
  - `Ticket Price Variance to Meal Deal Earnings` = `Total Ticket Price` − (`Total Meal Deal Earnings` + `Total Excess`).
- Note: you will need version2019.1 as the solutions we created all needed Rows to Columns.
- Output the data exactly as specified below.

## Output

- output_01.csv
  - 6 fields:
    - Total Ticket Price
    - Ticket Price Variance to Meal Deal Earnings
    - Total Meal Deal Earnings
    - Total Excess
    - TicketID
    - MemberID