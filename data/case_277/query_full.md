## Context

SuperBytes wants to identify and reward the highest-loyalty customers at each store. Starting from the Loyalty Points data, you will derive standardized customer name components, enrich the records with customer address details and store information, then rank customers within each store by loyalty points to keep the top performers (including ties).

## Requirements

- Input the data.

- Start with the Loyalty Points table (one row represents one loyalty points record for a customer):
  - Convert `DateTime_Out` into a new `Date` field representing the calendar date, formatted as `DD/MM/YYYY`.
  - Convert the `Loyalty Points` field to a numeric value by extracting the numeric portion (including decimals when present) and treating it as a floating-point number.
  - From `Email Address`, derive:
    - `First Name`: take the part before `@`, split on `.`, use the first segment as the first name, and capitalize it.
    - `Last Name`: take the second segment (after splitting the local-part on `.`) and keep only its first character as an uppercase initial. (This field is the last-name initial, not the full last name.)

- Join to the Customer Details table, ensuring the number of rows remains at 999:
  - Create join keys in both tables:
    - `First Key`: the customer first name standardized to match the capitalization used for `First Name` above.
    - `Last Initial`: the first character of the customer `Last Name`, uppercased.
  - Perform a left join from the Loyalty Points table to the Customer Details table on `First Key` and `Last Initial`, bringing in `First Name`, `Last Name`, `Postcode`, and `address` from Customer Details.
  - The join must not increase the row count; it should preserve the Loyalty Points row count (999 rows) after this step.

- Join on the Store Data table:
  - Join the current dataset to Store Data using `Store ID` as the key (left join), adding store attributes needed for the output (including `City` and `Store`).

- Remove unnecessary fields:
  - Retain only the fields required for the final output.

- Filter out customers without postcodes:
  - Exclude rows where `Postcode` is missing or blank.

- For each store, rank the customers:
  - Define “store” as the combination of `City` and `Store`.
  - Rank customers within each store by `Loyalty Points` in descending order, where the highest number of loyalty points receives rank `1`.
  - Use dense ranking so that ties share the same rank and the next distinct value increments by 1 (e.g., 1, 1, 2).

- Filter to the top 5 customers for each store:
  - Keep all rows with rank `<= 5`.
  - This may result in more than 5 customers per store when there are ties in `Loyalty Points`; include all tied customers within the top-5 ranks.

- Output the data.

## Output

- output_01.csv
  - 10 fields:
    - City
    - Store
    - Rank
    - Email Address
    - First Name
    - Last Name
    - Loyalty Points
    - Date
    - Postcode
    - address