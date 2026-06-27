## Context
Chin & Beard Suds Co (C&BS Co.) maintains a company data table that records monthly profit by product for Scotland and England. Scotland’s figures for the first three months of 2019 are already present, but England’s March 2019 profit by product still needs to be calculated from March sales and product pricing/cost information, then appended to the master company data.

## Requirements
- Input the data.
- Import the file(s) and use all 3 sheets/tables:
  - A master “Company Data” table containing existing monthly profit records (including Scotland through March 2019 and England prior to March).
  - A March sales table that lists units sold by city and product category.
  - A pricing/cost table that provides selling price per unit and manufacturing cost per unit by soap type.
- Define the output grain as: one row per **Country × Month × Product**, with **Profit** representing total profit for that product in that country for that monthly sales period.
- Prepare the base output from the master Company Data table:
  - Rename the existing product field from **Category** to **Product**.
  - Keep only the fields **Country**, **Month**, **Product**, **Profit**.
  - Preserve the existing row order from the master table.
- Compute England’s March profit by product using the March sales and pricing/cost tables:
  - Use only rows from the March sales table where **Country = England**.
  - Aggregate March sales to product level by summing **Units Sold** for each product category across all cities (i.e., total units sold per category in England).
  - Convert the pricing/cost table into profit-per-unit by soap type:
    - Compute **profit_per_unit = Selling Price per Unit − Manufacturing Cost per Unit**.
    - Map soap types to the Company Data product names as follows:
      - **Bar → Bar Soap**
      - **Liquid → Liquid Soap**
  - Join the aggregated England units (by product) to profit-per-unit on **Product** using an inner join (only products present in both sources should produce output rows).
  - Compute **Profit = Units Sold × profit_per_unit**, then round to the nearest whole number and store as an integer.
  - Set **Country = England** for these computed rows.
  - Apply the monthly sales period rule: since the C&BS Co monthly sales period starts on the 19th of each month, represent March 2019 as **Month = 2019-03-19** for the computed England rows.
  - Order the computed England March rows by **Product** as:
    1) Bar Soap  
    2) Liquid Soap
- Append (concatenate) the computed England March rows to the end of the base Company Data rows (do not interleave or reorder the existing master rows).
- Output the data.

## Output

- output_01.csv
  - 4 fields:
    - Country
    - Month
    - Product
    - Profit