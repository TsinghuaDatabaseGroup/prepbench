## Context
Following the delivery of the Prep Air “New Trolley Inventory” project at the end of May 2021, the goal is to identify products that are being sold at notably higher prices than their typical selling price, segmented by destination and by whether the sale occurred before or after the new inventory went live. The analysis focuses on the highest positive price variances and returns the top-ranked rows per destination for each time period.

## Requirements
- Input the data from all provided monthly files (e.g., `input_*.csv`).
- Bring all the sheets/files together by stacking/unioning them into a single dataset at the transaction (purchase) level (one row per original purchase record).
- Derive the purchase month from the input source name:
  - Parse the month number from the input filename pattern `input_<month>.csv` (e.g., `input_01.csv` → month 1).
- Use **Day of Month** together with the derived **month** (from the source name) and a fixed **year of 2021** to form a purchase date field called **`Date`**.
- Create **`New Trolley Inventory?`** to indicate whether the purchase was made **on or after 1st June 2021** (i.e., `Date >= 2021-06-01`). This must be a boolean field.
- Remove detail from the product name to standardize product grouping:
  - Return only the portion of the product name **before the first `-` (hyphen)**.
  - If a product name does not contain a hyphen, keep the full product name.
  - Use this standardized product name as **`Product`** in the output and for product-level averaging.
- Make **Price** a numeric field for calculation purposes (a floating-point number).
- Work out **`Avg Price per Product`**:
  - Compute the average of numeric **Price** for each standardized **Product**, using all rows in the combined dataset.
  - Round **`Avg Price per Product`** to **9 decimal places**.
  - Attach this product-level average back to each purchase row (left join by standardized Product so every purchase keeps its row).
- Work out **`Variance`** for each purchase row as:
  - `Variance = Price - Avg Price per Product`
  - Round **`Variance`** to **9 decimal places**.
- Rank the variances within each combination of:
  - **Destination**, and
  - **New Trolley Inventory?**
  using **descending Variance** so that **rank 1 is the largest positive variance**.
  - If multiple rows have the same variance, break ties by assigning ranks in first-encountered order (i.e., a deterministic “first” tie-break).
- Return only ranks **1 through 5** (inclusive) based on **`Variance Rank by Destination`**.
- Format **`Date`** in the output as a text date in **`DD/MM/YYYY`** format.
- Output the data to the required file and fields.

## Output

- output_01.csv
  - 11 fields:
    - New Trolley Inventory?
    - Variance Rank by Destination
    - Variance
    - Avg Price per Product
    - Date
    - Product
    - first_name
    - last_name
    - email
    - Price
    - Destination