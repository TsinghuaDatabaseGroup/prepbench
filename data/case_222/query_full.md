## Context
The Prep School needs fact-based information to address PTA concerns about how many meal options are vegan, vegetarian, or meat-based, and whether plant-based options cost more on average. Using the provided menu classification and pricing data, produce a summary by meal type showing the average price and the share of total meal options.

## Requirements
- Input the data.
- Input both data sources from here:
  - Use `input_01.csv` as the source of each meal option’s meal type (it includes at least `Meal Option` and `Type`).
  - Use `input_02.csv` as the source of each meal option’s price (it includes at least `Meal Option` and `Price`).
- Group meal types by standardising the `Type` values as follows (apply before joining):
  - Treat “veggie” and “vegetarian” as the same type and output them as `Vegetarian`.
  - Treat “meat based” (including the “meat-based” wording) as `Meat-based`.
  - Keep `Vegan` as `Vegan`.
  - For any other `Type` value not covered above, keep the original value as-is.
- Join the data sets together so you have the meal type and price for each meal:
  - Join `input_01.csv` to `input_02.csv` on `Meal Option` using an inner join.
  - Only retain matched meal options (i.e., exclude meal options that do not appear in both inputs).
- Remove the irrelevant fields:
  - After joining, do not carry forward any fields beyond what is needed to compute the final summary (i.e., compute from `Type`, `Meal Option`, and `Price`, and do not include other fields in the output).
- Aggregate the data by meal type and average their price:
  - Group by `Type`.
  - Compute `Average Price` as the mean of `Price` within each `Type`.
  - Round `Average Price` to 2 decimal places.
- Calculate the percentage of total for each meal type:
  - Define the total as the total number of joined meal options (row count after the inner join).
  - For each `Type`, compute `Percent of Total` as `(count of meal options in that Type / total count) * 100`.
  - Round `Percent of Total` to 0 decimal places and output it as an integer.
- Rename the fields to match the output data example exactly: `Type`, `Average Price`, `Percent of Total`.
- Ensure the output ordering of rows is:
  1. `Meat-based`
  2. `Vegan`
  3. `Vegetarian`
  (If other types exist due to unmapped values, place them after these.)
- Output the data as a CSV.
- Output the data.

## Output

- output_01.csv
  - 3 fields:
    - Type
    - Average Price
    - Percent of Total