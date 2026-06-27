## Context

You are analysing AllChains store performance over the last financial year using features introduced in Tableau Prep 2023.2 (notably “% Difference From” and a row-aware “lookup” approach). The goal is to summarise sales at a fiscal-quarter level per Store, compute quarter-on-quarter percentage changes, and then categorise each Store’s overall quarterly performance pattern.

## Requirements

- Input the data.
  - Use the 12 monthly input files (`input_01.csv` through `input_12.csv`) as sources.

- Bring all the Months together into a single table.
  - Union (stack) the 12 inputs into one dataset (do not deduplicate).

- Merge together misaligned fields.
  - Ensure all monthly files map into a consistent set of core fields needed for the rest of the workflow: `Store`, `Sales`, and an `Order Date` field (even if the original headers differ between files).

- Create an Order Date field.
  - Standardise the input to a single `Order Date` field and extract the calendar year from it (this year is used for fiscal-quarter assignment).

- The financial year for Allchains starts in July. Convert the dates to Fiscal Quarters.
  - Use fiscal quarters defined as: Q1 = Jul–Sep, Q2 = Oct–Dec, Q3 = Jan–Mar, Q4 = Apr–Jun.
  - Assign each record to a fiscal quarter using the extracted calendar year and the originating input file number (`input_01` … `input_12`) according to the following deterministic mapping:
    - For records with year = 2022:
      - Quarter 1 if the record came from `input_02`, `input_06`, or `input_12`
      - Quarter 2 if the record came from `input_03`, `input_10`, or `input_11`
    - For records with year = 2023:
      - Quarter 3 if the record came from `input_04`, `input_05`, or `input_08`
      - Quarter 4 if the record came from `input_01`, `input_07`, or `input_09`
  - If a record cannot be assigned to a Quarter using the rules above, exclude it from downstream steps.

- Aggregate the data to a Quarterly level for each Store, ignoring the product details.
  - Group by `Store` and `Quarter`.
  - Compute `Sales` as the sum of sales within each Store–Quarter group.
  - The resulting grain should be one row per `Store` per `Quarter`.

- Calculate the % Difference in Sales from the Previous Quarter.
  - Within each `Store`, order quarters ascending (1 → 4).
  - For each Store–Quarter row, compute quarter-on-quarter percent difference from the immediately previous quarter’s Sales as:
    - `% Difference Q on Q = ((Sales - PrevQuarterSales) / PrevQuarterSales) * 100`
  - Set `% Difference Q on Q` to null for:
    - Quarter 1, and/or
    - any case where the previous quarter’s Sales is missing or equals 0.
  - Multiply this value by 100 and round to 1 decimal place (i.e., the stored value is a percentage, rounded to 1 decimal).

- Use the lookup function so that we can compare the % Difference for all Quarters in a single row.
  - For each `Store`, bring the three quarter-on-quarter values for Q2, Q3, and Q4 onto a single Store-level row (conceptually, a pivot/lookup across the Store’s rows) so the Store can be evaluated based on the pattern across all three changes.

- Evaluate each Store's performance by categorising them in the following way:
  - Determine the sign of each Store’s `% Difference Q on Q` for Q2, Q3, and Q4 using strict comparisons (> 0 is positive, < 0 is negative; values equal to 0 are neither).
  - Assign exactly one `Store Evaluation` per Store using these rules:
    - If a Store has seen consistent growth - "Going from strength to strength" (Q2>0, Q3>0, Q4>0)
    - If a Store has seen consistent decline - "Going from bad to worse" (Q2<0, Q3<0, Q4<0)
    - If a Store has 1 negative Quarter:
      - In Q2 - "Good growth in last half" (Q2<0, Q3>0, Q4>0)
      - In Q3 - "Some good growth, but concerns in Q3" (Q2>0, Q3<0, Q4>0)
      - In Q4 - "Good growth, until Q4" (Q2>0, Q3>0, Q4<0)
    - If a Store has only 1 positive Quarter:
      - In Q2 - "Concerning performance in last half" (Q2>0, Q3<0, Q4<0)
      - In Q3 - "Concerning performance, excluding Q3" (Q2<0, Q3>0, Q4<0)
      - In Q4 - "Concerning performance, but improving in Q4" (Q2<0, Q3<0, Q4>0)
  - For any Store that does not meet any of the conditions above (including cases involving 0 or missing values), set `Store Evaluation` to "Concerning performance in last half".
  - Attach the resulting Store-level `Store Evaluation` back onto every Store–Quarter row for that Store.

- Output the data.

## Output

- output_01.csv
  - 5 fields:
    - Store
    - Quarter
    - Sales
    - % Difference Q on Q
    - Store Evaluation