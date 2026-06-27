## Context

You are preparing a summary table of animal outcomes that focuses only on cats and dogs. The goal is to collapse detailed outcome types into two high-level outcome groupings and report, for each animal type, what percentage of records fall into each grouping.

## Requirements

- Input the data:
  - Read all available CSV files from the input directory and concatenate them into a single dataset.
  - The analysis requires fields equivalent to **Animal Type** and **Outcome Type**.
- Remove the duplicated date field:
  - If a duplicated date column/field exists in the inputs, exclude it from further processing (it is not used for any calculations in this task).
- Filter to only cats and dogs (the other animals have too small a data sample):
  - Keep only rows where **Animal Type** is Cat or Dog.
- Group up the Outcome Type field into 2 groups:
  - Create an **Outcome Type Grouping** using **Outcome Type**:
    - Map outcomes representing Adoption/Adopted, Return to Owner/Returned to Owner, and Transfer/Transferred into:
      - **Adopted, Returned to Owner or Transferred**
    - Map all other outcomes (including missing Outcome Type) into:
      - **Other**
- Calculate the % of Total for each Outcome Type Grouping and for each Animal Type:
  - For each **Animal Type** (Cat, Dog), compute:
    - **% of Total** = (count of rows in the grouping for that animal type ÷ total count of rows for that animal type) × 100
  - Reshape the result so there is one row per **Animal Type**, with separate columns for the two groupings.
  - If an animal type has zero rows in a grouping, output 0.0 for that grouping.
  - Round the percentages to 1 decimal place.
  - Order output rows as Dog first, then Cat.
- Output the data.

## Output

- output_01.csv
  - 3 fields:
    - Animal Type
    - Adopted, Returned to Owner or Transferred
    - Other