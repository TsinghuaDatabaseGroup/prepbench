## Context
You have sales transactions from two physical stores and an online shop covering the first few weeks of the year, plus a product lookup table. The goal is to measure, by location and product type, the typical time gap between a sale and the next subsequent sale of the same product type in the same location.

## Requirements
- Input the data from the three provided sources: in-store sales, online sales, and the product lookup.
- Create a single combined sales dataset by appending in-store and online sales records together.
  - Standardize the online sales timestamp field so it is named **Sales Date** (to match the in-store feed’s date field).
  - Ensure every online sale has **Store = "Online"** (i.e., online transactions are explicitly labeled as the Online location).
- Link the product lookup onto the combined sales dataset so sales use product names rather than only product IDs.
  - Join sales to the lookup on the product identifier (sales **Product** to lookup **Product ID**) using a left join (retain all sales even if a product name is missing).
- Create **Product Type** as the first word of **Product Name**.
  - If **Product Name** is missing (NULL) after the left join, set **Product Type** to NULL as well.
- Convert **Sales Date** to a true datetime using the format `%d/%m/%Y %H:%M:%S`.
- Before calculating "next sale", de-duplicate only the in-store transactions as follows:
  - Within each in-store **Store + Product Type + Sales Date** combination, keep the first record and drop any additional records with the same keys.
  - To determine the "first record" when multiple records share the same **Store + Product Type + Sales Date** combination, sort the records by **Store**, **Product Type**, and **Sales Date** in ascending order. After sorting, keep the first record from each group.
  - Do not apply this de-duplication rule to the online records.
- Create a dataset that, for each sale, identifies the next sale of the same **Product Type** in the same **Store**:
  - Sort records within each **Store + Product Type** by **Sales Date** ascending (and if an **ID** field is present, use it as an additional ascending tie-breaker for consistent ordering).
  - For each row, assign **Next Sale Date** as the subsequent **Sales Date** within the same **Store + Product Type** group.
- Compute the time difference in minutes between the original sale and the next sale:
  - **Time Diff Minutes = (Next Sale Date − Sales Date) in minutes**.
  - Exclude rows where there is no next sale (i.e., Next Sale Date is missing).
  - Remove any rows where the time difference is negative (these represent refunded sales per the business definition).
- Aggregate to produce the average time-to-next-sale by **Store** and **Product Type**:
  - Compute the mean of **Time Diff Minutes** for each **Store + Product Type** group.
  - Name this aggregated field **Average mins to next sale**.
  - Round **Average mins to next sale** to 1 decimal place.
- Output the final aggregated dataset.

## Output

- output_01.csv
  - 3 fields:
    - Average mins to next sale
    - Product Type
    - Store
