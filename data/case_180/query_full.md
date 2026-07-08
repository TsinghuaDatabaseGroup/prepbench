## Context
You are analysing store sales performance against predefined sales targets. This requires deriving a consistent product category from the sales product descriptions, reshaping the targets data into a joinable structure, joining sales to targets, and then flagging whether each store–product combination meets or exceeds its target.

## Requirements
- Input the data from the provided files.
- From the Sales input, derive a **Product Type** from **Product Name** by removing the trailing detail so that only the product category remains; specifically, keep the text before the delimiter `" - "` (e.g., take the part before `" - "`).
- Compute **Total Sales** at the grain of **Store Name × Product Type**:
  - **Sale Value** = sum of Sale Value within each Store Name and Product Type group.
  - **Region** = carry through the store’s Region for that group (use the existing Region associated with the store in the grouped data).
- Reshape the Targets data set from wide to long so it becomes three columns:
  - Product
  - Store
  - Sales Target (k's)
  This means each original store column becomes a row under the Store field, with its corresponding target value under Sales Target (k's), and Product remains as the identifier.
- Convert **Sales Target (k's)** into a full target value by multiplying by **1000** (e.g., 75 becomes 75000).
- Prepare both datasets for joining by standardising the join keys to **Title Case**:
  - Convert Sales **Store Name** and derived **Product Type** to Title Case.
  - Convert Targets **Store** and **Product** to Title Case.
- Join the aggregated Sales data to the reshaped Targets data using a **left join** from Sales to Targets:
  - Match Sales (Store Name, Product Type) to Targets (Store, Product).
  - Keep all Store Name × Product Type rows from Sales even when no target is found (Target should be missing in that case).
  - Remove duplicated join fields from the joined result so only one set of store/product fields remains.
- Calculate whether each product in each store beats the target:
  - **Beats Target?** = `Sale Value >= Target`.
  - If Target is missing, this comparison should evaluate to False.
- Output the data in the required structure.

## Output

- output_01.csv
  - 6 fields:
    - Beats Target?
    - Target
    - Store Name
    - Region
    - Sale Value
    - PRODUCT