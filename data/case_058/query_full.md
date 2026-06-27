## Context
Chin & Beard Suds Co have weekly sales totals aggregated at the scent level, but the business needs those totals broken back down by product size for each scent-week. A separate table provides the percentage split of sales by product size (and product type) for each product and week, and a lookup table links scents to product identifiers and sizes. The task is to reconstruct weekly sales by scent and product size by joining and applying these percentages.

## Requirements
- Input the data.
- Use three inputs:
  - **Total Sales** (input_01.csv): weekly total sales per scent, with a field named **Year Week Number** and a total-sales measure.
  - **Percentages** (input_02.csv): percentage of sales by **Product ID**, **Size**, and **Week Commencing**, plus **Product Type**.
  - **Lookup** (input_03.csv): mapping between **Scent** and a concatenated **Product** field that contains both Product ID and Size.
- Ensure the week identifier is in **Year Week Number** format:
  - Treat **Year Week Number** in the Total Sales input as the week key for those records.
  - For the Percentages input, derive a comparable week key from **Week Commencing** using the ISO calendar year and ISO week number, formatted as an integer `YYYYWW` (week padded to two digits).
- Exclude irrelevant size splits:
  - Remove any rows from the Percentages input where **Percentage of Sales** is not greater than 0 (i.e., keep only strictly positive percentages).
- Fix the Lookup table structure:
  - Split the concatenated **Product** field into:
    - **Size** = the trailing size suffix (one of: `50g`, `100g`, `250ml`, `0.5l`).
    - **Product_ID** = the remaining leading portion after removing the size suffix.
  - Keep only **Scent**, **Product_ID**, and **Size** from the lookup for downstream joins.
- Prepare fields for joining:
  - Standardize the **Scent** values in the Total Sales input so they align with the scent values used in the Lookup table (so that the join on Scent succeeds).
  - Rename Percentages fields for consistency: **Product ID → Product_ID** and **Percentage of Sales → Percentage**.
- Join and compute weekly sales by scent and size:
  - Left-join Total Sales to the Lookup on **Scent** to attach **Product_ID** and **Size** to each scent-week.
  - Left-join the result to the Percentages table on **Product_ID**, derived week key (`Year_Week`), and **Size** to bring in **Percentage** and **Product Type**.
  - Remove any rows where **Percentage** is missing after the join (i.e., keep only rows with a matching percentage record).
  - Compute **Sales** for each resulting row as: `Sales = Total_Sales * Percentage`.
- Output formatting rules:
  - Rename **Scent** to **Secnt** in the final output (retain this exact misspelling).
  - Cast **Year Week Number** to an integer.
  - Cast **Sales** to a float and round it to **2 decimal places**.
  - Remove exact duplicate output rows (duplicates across all output fields).
  - Sort the final output by:
    1) **Year Week Number** ascending, then
    2) **Secnt** in this order: Coconut, Honey, Lavendar, Lemongrass, Mint, Orange, Tea Tree, Vanilla, then
    3) **Size** in this order: 50g, 250ml, 100g, 0.5l.
- Output the data.

## Output

- output_01.csv
  - 5 fields:
    - Year Week Number
    - Secnt
    - Size
    - Product Type
    - Sales