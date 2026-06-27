## Context
Chin & Beard Suds Co is investigating unusual customer behaviour in the North of England. The expected lifecycle is:
1) A customer places an order (Purchased)  
2) The order is sent (Sent)  
3) The customer reviews the products (Reviewed)

Using the first 10 days of sales for 2019, produce four analytical outputs to quantify lifecycle timing and identify where orders are not being sent promptly (or at all).

## Requirements
- Input the data from `input_01.csv`.
- Treat each **order** as the entity being tracked through statuses, identified by `Order` and associated with a single `Customer` and `City`.
- Parse `Date` as a date value and treat `Order` as numeric for correct ordering/sorting.

### Reshape to one row per order
- Create a single order-level table with one row per unique combination of:
  - `Order`, `Customer`, `City`
- For each order, derive up to three date fields:
  - `Purchased` = the first (earliest) `Date` where `Status` is Purchased
  - `Sent` = the first (earliest) `Date` where `Status` is Sent
  - `Reviewed` = the first (earliest) `Date` where `Status` is Reviewed
- If an order never reaches a given status, leave that status date as null.

### Duration calculations (in whole days)
- For each order compute:
  - `time_to_send` = (`Sent` - `Purchased`) in whole days; null if either date is missing
  - `time_to_review_from_send` = (`Reviewed` - `Sent`) in whole days; null if either date is missing
- **Whole days calculation**: The difference between two dates is computed as the number of calendar days between them, excluding the start date and including the end date. For example, if `Purchased` is 2019-01-01 and `Sent` is 2019-01-03, then `time_to_send` = 2 days. The result should be a non-negative integer representing the number of complete days elapsed.

### Output 01 (Average time to send by customer)
- Compute the average of `time_to_send` per `Customer`, using only orders where `time_to_send` is not null (i.e., the order was sent and has a purchased date).
- Include all customers present in the order-level table even if they have no sent orders; their average should be null.
- Order rows using this customer sequence when present, otherwise after it in alphabetical order:
  - Jenny, Bona, Andy, Craig, Phil, Jonathan, Tina, Toni
- Keep exactly the two output fields specified.

### Output 02 (Average time from sending to review by customer)
- Compute the average of `time_to_review_from_send` per `Customer`, using only orders where `time_to_review_from_send` is not null (i.e., both sent and reviewed dates exist).
- Only customers with at least one qualifying reviewed order should appear.
- Order rows using this customer sequence when present, otherwise after it in alphabetical order:
  - Jenny, Andy, Tina, Toni
- Keep exactly the two output fields specified.

### Output 03 (Orders not sent)
- Filter to orders where `Sent` is null (not sent).
- Output one row per such order with:
  - `City` = the city value from the order-level table
  - `Order not sent` set to the constant text `Not Sent`
  - `Purchased` formatted as `DD/MM/YYYY`
  - `Sent` formatted as `DD/MM/YYYY` (and blank/null for these rows since `Sent` is missing)
  - `Order` = the order number from the order-level table
  - `Customer` = the customer name from the order-level table
- Sort rows by `City`, then `Order`, then `Customer` (ascending).
- Keep exactly the six output fields specified.

### Output 04 (% of orders meeting 3-day sending KPI by city)
- For each `City`, compute:
  - `Orders per City` = total number of orders in that city (including orders that were never sent)
  - `Time to Send KPI` = count of orders where `time_to_send` is less than or equal to 3 days; orders with null `time_to_send` do not meet the KPI
  - `% Orders meeting 3 Day KPI` = (`Time to Send KPI` / `Orders per City`) * 100, rounded to 9 decimal places
- Order rows using this city sequence when present, otherwise after it in alphabetical order:
  - Leeds, Manchester, York, Newcastle
- Keep exactly the four output fields specified.

- Create four outputs, one for each answer.
- Answer the questions above by Tweeting answers with #PreppinData31.
- Output the data.

## Output

- output_01.csv
  - 2 fields:
    - Avg Time to Send
    - Customer

- output_02.csv
  - 2 fields:
    - Time to Review from Sending Order
    - Customer

- output_03.csv
  - 6 fields:
    - City
    - Order not sent
    - Purchased
    - Sent
    - Order
    - Customer

- output_04.csv
  - 4 fields:
    - City
    - % Orders meeting 3 Day KPI
    - Time to Send KPI
    - Orders per City