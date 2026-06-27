## Context

You are preparing a curated transaction-level dataset for year-on-year analysis, enriched with product and loyalty attributes and extended to include dates when the store was closed. The final output should cover only 2023 and 2024 and include calculated quantity, discounted sales, and profit.

## Requirements

- Input the data from the three provided CSV files:
  - Transactions (input_03.csv)
  - Products (input_02.csv)
  - Loyalty customers (input_01.csv)

- Filter transactions to the last 2 years of data, i.e. keep only transactions whose Transaction Date falls in calendar years 2023 and 2024 (inclusive), to allow for year on year comparison.

- Create additional rows of data for the days the store was closed, ensuring all other fields will have null values.
  - Treat any calendar date in this range that has no transactions as a “closed day”; this will at least include Sundays and Public Holidays.
  - Implement this by ensuring the transaction dataset contains a continuous daily calendar from the minimum to the maximum Transaction Date present after the 2023–2024 filter; for each such missing date in that range (i.e. dates with no transactions), append a new row where Transaction Date is populated and all other fields are null.

- Update the Cash_or_Card field so that:
  - 1=Card
  - 2=Cash
  - Values outside these codes should result in a null Cash_or_Card in the output.

- Join the Product Table (input_02.csv) to the transactions using a left join.
  - You'll need to prepare the join clause fields first by deriving the product attributes from the transaction Product_ID:
    - Split Product_ID into three fields using “-” as the separator: Product_Type, Product_Scent, Product_Size.
    - Use these derived fields as the join keys to Products on (Product_Type, Product_Scent, Product_Size).
  - From the Product Table, bring in Unit_Cost and Selling_Price for downstream calculations.

- Calculate the Quantity of each transaction.
  - Defined as the Sales_Before_Discount / Selling_Price.
  - If Selling_Price is missing or zero, Quantity must be null.
  - Quantity must be the floored (rounded down) value of the division.

- In the Loyalty Table (input_01.csv):
  - The Customer_Name is currently reading Last Name, First Name. Update it to read First Name Last Name in Title case.
  - Group together the Loyalty_Tiers into Gold, Silver and Bronze: if the original tier value (case-insensitive) is exactly one of "Gold", "Silver" or "Bronze", keep that canonical value; any other original tier values must result in a null Loyalty_Tier in the output.
  - Update the Loyalty_Discount to be a numeric field expressed as a decimal rate (e.g., 10% becomes 0.10).

- Join the Loyalty Table to transactions using a left join on Loyalty_Number.
  - Transactions without a matching Loyalty_Number should retain null loyalty attributes.

- Create a Sales_After_Discount field to apply the Loyalty_Discount for transactions with a Loyalty_Number.
  - Compute Sales_After_Discount only when Loyalty_Number, Loyalty_Discount, and Sales_Before_Discount are all present; otherwise leave it null.
  - Formula: Sales_After_Discount = Sales_Before_Discount * (1 - Loyalty_Discount).
  - Round Sales_After_Discount to 4 decimal places.

- Calculate the Profit, defined as:
  - Profit = Sales_After_Discount (using the unrounded value from the discount formula) - (Unit_Cost * Quantity)
  - Compute Profit only when Sales_After_Discount, Unit_Cost, and Quantity are all present; otherwise leave it null.
  - Round Profit to 2 decimal places using half-up rounding.

- Format Transaction Date as a date string in the form `DD/MM/YYYY` (zero-padded) and output it exactly in that format.
- Format Quantity as a decimal string with exactly 1 decimal place (e.g., `2.0`); output blanks for missing values.
- Format Sales Before Discount as a decimal string with 1 or 2 decimal places; integer values must include `.0`, with no thousand separators; output blanks for missing values.

- Update the field names to remove all underscores and replace them with spaces (final column names must match the required output schema exactly).

- Remove any unnecessary fields so that the output contains only the specified 14 fields.

- Output the data to the required CSV.

Note: the output CSV must be de-duplicated by rows (drop exact duplicates).

## Output

- output_01.csv
  - 14 fields:
    - Transaction Date
    - Transanction Number
    - Product Type
    - Product Scent
    - Product Size
    - Cash or Card
    - Loyalty Number
    - Customer Name
    - Loyalty Tier
    - Loyalty Discount
    - Quantity
    - Sales Before Discount
    - Sales After Discount
    - Profit
  - Transaction Date must be formatted exactly as `DD/MM/YYYY` (zero-padded).
  - Quantity must be a decimal string with exactly 1 decimal place (e.g., `2.0`); blank if missing.
  - Sales Before Discount must be a decimal string with 1 or 2 decimal places; integer values must include `.0`; no thousand separators; blank if missing.
