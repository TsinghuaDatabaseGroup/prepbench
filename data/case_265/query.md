## Requirements

- Input the data
- Filter to the last 2 years of data i.e. only 2023 and 2024 transactions
  - This will allow for year on year comparison
- Create additional rows of data for the days the store was closed, ensuring all other fields will have null values
  - The store is closed on Sundays and Public Holidays
- Update the Cash_or_Card field so that:
  - 1=Card
  - 2=Cash
- Join the Product Table
  - You'll need to prepare the join clause fields first
- Calculate the Quantity of each transaction
  - Defined as the Sales_Before_Discount / Selling_Price
- In the Loyalty Table:
  - The Customer_Name is currently reading Last Name, First Name. Update it to read First Name Last Name in Title case
    - e.g. knell, libby becomes Libby Knell
  - Group together the Loyalty_Tiers into Gold, Silver and Bronze
  - Update the Loyalty_Discount to be a numeric field
- Join the Loyalty Table
- Create a Sales_After_Discount field to apply the Loyalty_Discount for transactions with a Loyalty_Number
- Calculate the Profit, defined as:
  - Sales_After_Discount - (Unit_Cost * Quantity)
- Update the field names to remove all underscores and replace them with spaces
- Remove any unnecessary fields
- Output the data

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
