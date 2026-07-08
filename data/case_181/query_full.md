## Context

Chin & Beard Suds Co (C&BSCo) track the percentage contribution of the top 3 sales people in each store, but they now want to translate those percentages into actual sales values. This task builds a single dataset across regions, enriches it with store details and annual store sales totals, and then calculates each sales person’s sales value from their percentage contribution.

## Requirements

- Input the data.
- Combine these files (a union/append of the two regional sales-people files, keeping all rows from both files):
  - Bring both regional datasets into one table by stacking rows and aligning fields by name.
  - Assign a region identifier to each row based on which regional file it came from (East vs West). If you do not derive region from file context, you may instead rely on the Region field supplied later via the Store Lookup step.
- Standardise the store identifier field used for lookups:
  - Rename the sales-people store identifier field from `Store` to `StoreID`.
- Input the `Store Lookup` file to provide the name of the stores instead of the ID number:
  - Join the combined sales-people dataset to `Store Lookup` using a left join on `StoreID`.
  - Retain the store descriptive fields (`Store Name` and `Region`) from the lookup.
- Remove any duplicate fields you have in the data set so far:
  - If the dataset contains multiple Region fields after the lookup join, keep the Region from `Store Lookup` and remove the duplicate.
- Input the Week 27 Input file.
- Use Week 27 Input file to create Sales Values for each Store:
  - Treat the Week 27 Input as transaction-level sales.
  - Compute each store’s total sales by grouping by `Store Name` and summing `Sale Value`.
  - Name this aggregate as the store’s total sales for the year (used for later calculations).
- Combine this data with the rest of the prepared data:
  - Join the sales-people-plus-store dataset to the store totals using a left join on `Store Name`.
- Use the data set you have created to determine the actual sales value (rather than percentage) for each sales person:
  - Multiply the sales person percentage contribution against their store’s total sales for the year:
    - `Sales per Person = (Percent of Store Sales / 100) * (Store total sales)`
  - In the final output, `Sale Value` must represent the store’s total sales (the store total used in the calculation), not an individual transaction value.
- Formatting rules:
  - Round `Sales per Person` to 4 decimal places.
  - Ensure `Percent of Store Sales` is an integer.
  - Round `Sale Value` (store total sales) to 2 decimal places.
- Output the data.

## Output

- output_01.csv
  - 6 fields:
    - Sales per Person
    - Region
    - Store Name
    - Sales Person
    - Percent of Store Sales
    - Sale Value