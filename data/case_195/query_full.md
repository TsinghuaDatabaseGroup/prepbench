## Context

You are preparing an order extract where the order date is consolidated into a single field and each order is assigned a standardized 8-character Order ID based on the customer’s initials and the order number.

## Requirements

- Input the data.
- Combine the three available order-date fields into one consolidated `Order Date` field:
  - For each row, select the first non-empty date value in this priority order:
    1) `Date of Order`
    2) `Purchase Date`
    3) `Order Date`
  - Convert the selected value to the output display format `DD/MM/YYYY` when it is provided in a weekday-text format like `%a %d %b %Y` (e.g., `Wed 26 Oct 2022`).
  - If the selected value is already in `DD/MM/YYYY` format, keep it as-is.
  - If the selected value is in any other format that is not converted by the rules above, carry it through unchanged.
- Create a new `Order ID` field with the following structure:
  - The total length must be exactly 8 characters.
  - The first 2 characters are the customer's initials derived from the `Customer` field:
    - If the customer name contains two or more space-separated parts, use the first character of the first part plus the first character of the last part.
    - Otherwise, use the first two characters of the customer name.
    - Preserve the original letter casing of the initials.
  - The remaining 6 characters are the `Order Number` expressed as an integer and left-padded with `0` to 6 digits.
  - Concatenate initials + padded order number (e.g., `AJ000746`).
- Ensure `Order Number` is output as an integer.
- Output the data with one output row per input row (no aggregation).

## Output

- output_01.csv
  - 4 fields:
    - Order ID
    - Order Number
    - Customer
    - Order Date