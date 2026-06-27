## Context
You are given a customer “ID” string that encodes multiple attributes needed to link to lookup tables and compute product revenue by geographic area. The goal is to parse those strings into structured fields, join them to an area-code lookup and a product lookup (including price), then summarize and rank product revenue within each area and compute each product’s share of that area’s total revenue.

## Requirements
- Input the data.
- From the Customer Information file (the file containing an `IDs` field), split the values so that each individual ID token becomes its own row (i.e., one row per ID token).
- For each ID row, extract the following fields from the ID string:
  - **Phone Number**: the first occurrence of a 6-digit number in the ID.
  - **Area Code Suffix**: the first 2 digits immediately after the comma (`,`). This represents the last two digits of the area code.
  - **Area Initial**: the single letter immediately following the two digits after the comma; treat it as the first letter of the area name.
  - **Quantity**: the digits immediately following the area-initial letter and preceding the hyphen (`-`), interpreted as an integer quantity ordered.
  - **Product ID**: the letters after the hyphen (`-`) through the end of the ID, treated as the product identifier.
- Rename these fields appropriately, and remove any unwanted columns—leaving only these 5 columns in the workflow (Phone Number, Area Code Suffix, Area Initial, Quantity, Product ID).
- Input the Area Code Lookup Table and create a join key that allows it to match the parsed customer rows:
  - Derive **Area Code Suffix** from the lookup’s area code by taking the last two digits of the code.
  - Derive **Area Initial** from the lookup’s Area name as its first letter.
- We don’t actually sell products in Clevedon, Fakenham, or Stornoway. Exclude these from our dataset (exclude these Areas from the area lookup prior to joining).
- Join the parsed customer data to the filtered area lookup table using an **inner join** on:
  - Area Code Suffix
  - Area Initial
  Keep only the customer fields plus the matched Area field, and remove any other unwanted fields created by the join.
- In some cases, the ID field does not provide accurate enough conditions to know where the customer is from. Exclude any phone numbers where the join has produced duplicated records:
  - After the area join, if a given Phone Number appears in more than one joined row (for any reason), treat it as ambiguous and remove **all** rows for that Phone Number from further processing.
- Join this dataset to the product lookup table using an **inner join** on Product ID, bringing in at least Product Name and Price.
- Compute revenue at the transaction level as:
  - Revenue (in pence) = Quantity × Price (converted to pence as an integer).
- For each Area and Product Name, aggregate total revenue as the sum of revenue (in pence), then convert to pounds and round to **zero decimal places** using standard half-up rounding to produce the final **Revenue** value.
- Rank how well each product sold in each area:
  - Within each Area, rank products by Revenue in descending order.
  - If multiple products tie on Revenue, assign the same rank using “minimum rank” tie handling (i.e., ties receive the lowest rank number in the tied group).
- For each area, work out the percent of total that each different product contributes to the overall revenue of that Area:
  - Within each Area, compute `% of Total - Product` = (Revenue / sum of Revenue for the Area) × 100.
  - Round to **2 decimal places** using half-up rounding.
- Output the data.

## Output

- output_01.csv
  - 5 fields:
    - Rank
    - Area
    - Product Name
    - Revenue
    - % of Total - Product