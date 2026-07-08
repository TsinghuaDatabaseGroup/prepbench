## Context
Analyze customer orders for the Serendipia restaurant over time to (1) quantify revenue by weekday, accounting for a Monday discount, and (2) identify the most loyal customer based on the total number of individual items ordered.

## Requirements
- Input the data from the two provided CSV files:
  - `input_01.csv` as the Menu table
  - `input_02.csv` as the Orders table
- Reshape the Menu table from a wide format into a single long table with exactly these logical fields for each menu item:
  - `Type` (one of Pizza, Pasta, House Plates)
  - `Name` (item name)
  - `ID` (item identifier)
  - `Price` (item price)
  Build the long table by stacking the three menu groups (Pizza, Pasta, House Plates) into one dataset. Exclude any menu rows where `Name`, `ID`, or `Price` is missing after reshaping. Treat `ID` as a string identifier in the reshaped output.
- Reshape the Orders table so that each ordered item ID appears on its own row (one row per single item ordered):
  - Parse `Order Date` as a date and derive a `Weekday` field as the weekday name (e.g., Monday, Tuesday, etc.).
  - Split the `Order` field on the hyphen (`-`) delimiter to create multiple item IDs, then explode so each ID becomes a separate row while retaining the original order/customer context.
- Join the exploded Orders rows to the reshaped Menu table using a left join on `ID`, bringing in the menu `Price` for each ordered item. Keep order rows even if no matching menu item is found.
- Apply the Monday discount:
  - Create an adjusted price where items ordered on `Weekday == "Monday"` are charged at 50% of their menu price.
  - For all other weekdays, the adjusted price equals the menu price.
- Output 1 (weekday revenue):
  - Aggregate to one row per `Weekday`, summing the adjusted price across all exploded order items.
  - Rename the summed adjusted price to `Price`.
  - Round `Price` to 0 decimal places and output it as an integer.
  - Order the rows in standard weekday order: Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday (any unexpected weekday values, if present, should appear after these).
- Output 2 (top customer by number of single items):
  - Using the exploded Orders rows (counting one per item ID), compute the total number of items ordered per `Customer Name`.
  - Select exactly one customer: the customer with the maximum item count. If there is a tie, choose the tied customer whose `Customer Name` is alphabetically first (ascending).
  - Output the item count as an integer.
- Output the two CSV files exactly as specified below.

## Output

- output_01.csv
  - 2 fields:
    - Price
    - Weekday

- output_02.csv
  - 2 fields:
    - Count Items
    - Customer Name