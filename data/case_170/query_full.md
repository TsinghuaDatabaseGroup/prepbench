## Context
Chin & Beard Suds Co (C&BSCo) suspects that while sales are being recorded, store teams are frequently recording the wrong product size. Each product has a single correct size defined in the product set. Your task is to prepare two outputs: one showing sales recorded with the correct size, and another quantifying sales recorded with an incorrect size and stating what the size should have been.

## Requirements
- Input the data.
  - Use three input files representing the three source worksheets:
    - `input_01.csv`: product set (authoritative product list including each product’s correct size and scent, keyed by Product Code)
    - `input_02.csv`: sales transactions (includes Product, Store, and a size identifier in the `Size` field)
    - `input_03.csv`: size lookup table (maps `Size ID` to the actual size value)
- Convert the sales size identifier into an actual recorded size value:
  - Build a mapping from `input_03.csv` where `Size ID` → `Size`.
  - In the sales table, map the sales `Size` field through this lookup to create a new field, **Recorded Size**.
- Link sales to product attributes (Scent and correct size):
  - Convert the sales `Product` value into a **Product Code** using this rule derived from the product set:
    - If a product code in the product set starts with `SB` and has a numeric suffix `n`, then the corresponding sales `Product` is `B{n}`.
    - If a product code in the product set starts with `LS` and has a numeric suffix `n`, then the corresponding sales `Product` is `L{n}`.
  - Use the resulting Product Code to look up the product’s **Correct Size** and **Scent** from the product set.
- Determine whether each sale is recorded correctly:
  - A sale is **correct** when `Recorded Size == Correct Size`.
  - A sale is **wrong** when `Recorded Size != Correct Size`.
- Create Output1: products sold with sizes recorded correctly.
  - Include one row per (Product Size, Scent, Product, Store) combination from the correct sales.
  - Deduplicate records so duplicate rows do not affect evaluation (drop exact duplicate rows across all output fields).
  - Use the recorded size as the Product Size in this output.
- Create Output2: products sold with incorrect sizes and what the sizes should have been.
  - For wrong sales, treat **Product Size** as the **Correct Size** (the size that should have been recorded).
  - Aggregate wrong sales to show, for each unique combination of:
    - Product (as recorded in sales),
    - the correct Product Size,
    - and Scent,
    the count of sales recorded with the wrong size.
  - Output the aggregated count as an integer in the field “Sales with the wrong size”.
  - Populate the “Product Code” output field with the sales Product value used in the aggregation (i.e., the same value grouped as Product in sales).
- Output the data to the required CSV files.

## Output

- output_01.csv
  - 4 fields:
    - Product Size
    - Scent
    - Product
    - Store

- output_02.csv
  - 4 fields:
    - Sales with the wrong size
    - Product Code
    - Product Size
    - Scent