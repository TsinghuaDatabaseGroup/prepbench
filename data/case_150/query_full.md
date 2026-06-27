## Context
The IT department wants the current orders dataset restructured into a simple star schema: three dimension tables (Store, Customer, Product) that can join onto a central fact table. The goal is to preserve the business meaning of the original records while making the resulting tables suitable for database storage and stable over time (i.e., dimension IDs should not change when new orders arrive).

## Requirements
- Input the data from the provided file.

- Derive core fields needed for the star schema:
  - Split `OrderID` into:
    - `Store`: the text prefix before the first hyphen (`-`).
    - A numeric order identifier: the portion after the first hyphen, stored as a number and ultimately output as `OrderID` in the fact table.
  - Convert `Return State` into a binary `Returned` flag:
    - `Returned = 1` when `Return State` is exactly `Return Processed`.
    - `Returned = 0` otherwise (including blanks/missing values).
  - Create a numeric `Sales` field as:
    - `Sales = Unit Price * Quantity`, rounded to 2 decimal places.
    - `Unit Price` must be interpreted as a numeric currency amount.
    - `Quantity` must be numeric and output as an integer (treat missing/non-numeric quantities as 0).

- Build three dimension tables. Each table must include the “first seen” date and a stable, sequential ID assignment rule so that IDs are reproducible and do not shift when later orders are appended:
  - General ID assignment rule (applies to StoreID, CustomerID, ProductID):
    - Compute the minimum relevant order date for the entity (as specified below).
    - Sort entities by that minimum date ascending, then apply a deterministic tie-breaker based on the entity name/label (alphabetical; use case-insensitive ordering where a name field is involved).
    - Assign IDs as consecutive integers starting at 1 in that sorted order.

  - Store dimension (`output_04.csv`):
    - One row per unique `Store`.
    - `First Order` = minimum `Order Date` for that store.
    - Assign `StoreID` using the general ID assignment rule, sorting by `First Order` then `Store`.

  - Customer dimension (`output_01.csv`):
    - One row per unique `Customer`.
    - `First Order` = minimum `Order Date` for that customer.
    - `Number of Orders` = count of distinct orders placed by that customer, where an “order” is uniquely identified by the combination of `Store` and the numeric portion of `OrderID`.
    - `Return %` = the proportion of line items returned by that customer:
      - Numerator: sum of `Returned` across that customer’s rows.
      - Denominator: total number of rows (line items) for that customer.
      - Round to 2 decimal places using half-up rounding.
      - If the denominator is 0, set `Return %` to 0.00.
    - Assign `CustomerID` using the general ID assignment rule, sorting by `First Order` then `Customer` (case-insensitive).

  - Product dimension (`output_03.csv`):
    - One row per unique product definition identified by the combination of:
      - `Category`, `Sub-Category`, `Product Name`, and numeric `Unit Price`.
    - `First Sold` = minimum `Order Date` for that product definition.
    - Assign `ProductID` using the general ID assignment rule, sorting by `First Sold` then `Product Name` (case-insensitive).

- Create the fact table (`output_02.csv`) by taking the original row-level grain (one row per original order line item) and replacing descriptive dimension attributes with their corresponding IDs:
  - Add `StoreID` by matching on `Store`.
  - Add `CustomerID` by matching on `Customer`.
  - Add `ProductID` by matching on the product-definition key (`Category`, `Sub-Category`, `Product Name`, numeric `Unit Price`).
  - Keep the derived fields `Returned`, `Sales`, the numeric `OrderID`, and integer `Quantity`.
  - Output `Order Date` as a date string formatted `DD/MM/YYYY` (zero-padded).

- Output all four tables as CSV files exactly as specified, with the required fields and names.

## Data Cleaning and Ambiguity Resolution

### Unit Price Comparison for Product Definition
When determining product uniqueness (for the Product dimension and ProductID matching), the numeric `Unit Price` must be compared with a small tolerance to account for floating-point rounding errors. Specifically:
- Parse `Unit Price` from the input (removing currency symbols, commas, etc.) to obtain a numeric value.
- Two `Unit Price` values are considered equal if the absolute difference between them is less than or equal to 0.01 (one cent).
- This tolerance accounts for potential floating-point representation differences while ensuring that products with the same `Category`, `Sub-Category`, `Product Name`, and effectively identical numeric `Unit Price` are treated as the same product definition.

## Output

- output_01.csv
  - 5 fields:
    - CustomerID
    - Customer
    - Return %
    - Number of Orders
    - First Order
  - CustomerID must be an integer string with no decimals.
  - First Order must be formatted exactly as `DD/MM/YYYY` (zero-padded); blank if missing.

- output_02.csv
  - 8 fields:
    - StoreID
    - CustomerID
    - OrderID
    - Order Date
    - ProductID
    - Returned
    - Quantity
    - Sales
  - StoreID, CustomerID, OrderID, and ProductID must be integer strings with no decimals.
  - Order Date must be formatted exactly as `DD/MM/YYYY` (zero-padded); blank if missing.

- output_03.csv
  - 6 fields:
    - ProductID
    - Category
    - Sub-Category
    - Product Name
    - Unit Price
    - First Sold
  - ProductID must be an integer string with no decimals.
  - First Sold must be formatted exactly as `DD/MM/YYYY` (zero-padded); blank if missing.

- output_04.csv
  - 3 fields:
    - StoreID
    - Store
    - First Order
  - StoreID must be an integer string with no decimals.
  - First Order must be formatted exactly as `DD/MM/YYYY` (zero-padded); blank if missing.
