## Context

You have two input sheets representing spending by category: one sheet contains forecasted (budget) amounts and the other contains actual amounts. The goal is to align both sources to a consistent structure, combine them by category, and compute the rounded difference between actual and forecasted spending.

## Requirements

- Input the data.
- Match Sheet 1 and Sheet 2 in formatting. Both should include:
  - Category field [String]
  - Budget/Actual field [Number (Decimal)]
- Join both sheets based on Category field to create a single table with 3 columns:
  - `Category` [String]
  - `Budget` [Number]
  - `Actual` [Number]
- Rename the fields to:
  - `Category`
  - `Forecasted Spending` (from Budget)
  - `Actual Spending` (from Actual)
- Create a new calculated column with the differences between forecasted and actual values. Values in the new column should be rounded to whole numbers [ROUND(...)].
- Output the data.

## Output

- output_01.csv
  - 4 fields:
    - Category
    - Forecasted Spending
    - Actual Spending
    - Difference