## Context

You have multiple CSV input files containing flight pricing records, including a date, cabin class, price, and whether the customer has a “Flow Card?”. The goal is to combine all inputs and produce a quarterly summary table of prices by Flow Card status and cabin class, where the summaries are stacked for three different aggregation measures (median, maximum, minimum).

## Requirements

- Input the data.
- Union the files together into a single dataset (append rows; do not deduplicate).
- Convert the `Date` field to a quarter number (1–4) and store it in a new field named `Quarter`.
  - Derive `Quarter` from the calendar quarter of `Date`.
- Limit the working dataset to the fields needed for aggregation: `Flow Card?`, `Quarter`, `Class`, and `Price`.
- Aggregate the data by the grouping keys `(Quarter, Flow Card?, Class)` and compute all of the following:
  - Median price per Quarter, Flow Card? and Class
  - Minimum price per Quarter, Flow Card? and Class
  - Maximum price per Quarter, Flow Card? and Class
- Create three separate flows where each has only one aggregated measure:
  - One for the minimum price
  - One for the median price
  - One for the maximum price
- For each of the three flows, pivot the data so that:
  - Each output row represents one `(Flow Card?, Quarter)` combination.
  - Each distinct `Class` becomes a separate column containing the aggregated `Price` value for that class.
  - If a class column does not exist for a given pivot result, include it in the schema and leave its values null.
- Union these three pivoted flows back together by stacking rows (not joining columns), in this block order:
  1) median block, then 2) maximum block, then 3) minimum block.
  - Note: the final output does not include a field identifying which aggregation a row came from; it is represented only by row order and stacking.
- Change the column names due to incorrect classification (apply after pivoting, to the pivoted class columns):
  - Economy → First
  - First Class → Economy
  - Business Class → Premium
  - Premium Economy → Business
- Ensure the final output contains exactly these columns in this order:
  `Flow Card?`, `Quarter`, `Economy`, `Premium`, `Business`, `First`.
- Format rules:
  - Round all numeric price columns (`Economy`, `Premium`, `Business`, `First`) to 2 decimal places.
  - Represent `Quarter` as an integer where present.
- Sort/order the final stacked output deterministically as follows:
  - Keep the three aggregation blocks in the union order: median first, then max, then min.
  - Within each block, order rows by the following `(Flow Card?, Quarter)` sequence:
    1. (Yes, 2)
    2. (No, 1)
    3. (No, 4)
    4. (Yes, 3)
    5. (Yes, 1)
    6. (No, 2)
    7. (No, 3)
    8. (Yes, 4)
- Output the data.

## Output

- output_01.csv
  - 6 fields:
    - Flow Card?
    - Quarter
    - Economy
    - Premium
    - Business
    - First