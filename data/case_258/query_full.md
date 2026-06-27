## Context
You are given quarterly targets and detailed sales records for the same year. The goal is to align sales to targets by month and travel class, then report sales performance versus target at the Class–Month level.

## Requirements
- Input the data.
  - Read the targets data from four input files (one per quarter): `input_01.csv`, `input_02.csv`, `input_03.csv`, and `input_04.csv`.
  - Read the sales data from two input files: `input_05.csv` and `input_06.csv`.
- Prepare (standardize) the targets dataset:
  - Keep only the fields needed for joining and calculations: Month, Class, and Target.
  - Ensure `Month` is treated as a month number and `Target` is numeric.
- Prepare the sales dataset:
  - Correct the Classes being incorrect by swapping the labels:
    - Economy → First Class
    - First Class → Economy
    (Apply this correction before creating the join key/class code.)
  - Find the first letter from each word in the (corrected) Class to create the Class code used for joining:
    - First Class → `FC`
    - Business Class → `BC`
    - Premium Economy → `PE`
    - Economy → `E`
  - Change the sales `Date` to a month number by parsing the date and extracting its month.
  - Ensure `Price` is numeric.
  - Exclude sales rows where the derived month number or the derived Class code is missing (so they do not contribute to the aggregation).
- Total up (aggregate) sales at the level of:
  - Class (using the Class code)
  - Month
  Specifically, sum `Price` within each Month–Class group.
- Join the Targets data on to the aggregated Sales data:
  - Join type: inner join.
  - Join keys: Month and Class.
  - The result must contain 48 rows after the join (i.e., the complete set of Month–Class combinations that exist in both datasets).
  - Enforce that the join is one-to-one at the Month–Class level (each Month–Class pair matches at most one target row and one aggregated sales row).
- Calculate the difference between the Sales and Target values per Class and Month:
  - `Difference to Target = Price - Target`
- Set the output `Date` field to the numeric month number used for grouping/joining.
- For a deterministic output, order rows by month ascending, then by Class in this order: `FC`, `BC`, `PE`, `E`.
- Output the data.

## Output

- output_01.csv
  - 5 fields:
    - Difference to Target
    - Date
    - Price
    - Class
    - Target