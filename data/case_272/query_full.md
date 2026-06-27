## Context

You are given one input file containing annual budget amounts by spending category, plus a set of input files representing monthly actual spending. The goal is to identify, for each month, which spending category has the greatest overspend versus its (evenly spread) monthly budget—but only among categories that are overspent at the annual level.

## Requirements

- Input the data.
- Combine the Monthly sheets into a single table:
  - Treat each monthly input file (all `input_*.csv` except the budget file) as one month of actual spending.
  - Associate each month’s data with a month date derived from that file’s month identifier, then use it to label the month in the output.
- Budget preparation:
  - From the budget input, build a table of `Category` and `AnnualBudget` (annual budget amount).
  - Compute a `MonthlyBudget` for each category by evenly spreading the annual budget across 12 months:
    - `MonthlyBudget = round(AnnualBudget / 12)`
    - Apply rounding to the nearest whole number using “round half to even” (banker’s rounding), and store as an integer.
- Exclude any area that is below budget at an annual level:
  - First, reshape the combined monthly actuals to a long format with one row per (`month`, `Category`) and a numeric `Actual Spending`.
  - Compute `AnnualActual` per `Category` as the sum of `Actual Spending` across all available months.
  - Keep only categories where `AnnualActual > AnnualBudget` (i.e., exclude categories that are at or below annual budget).
  - Categories used for comparisons must be those that exist in the budget table (use the budget categories as the canonical set).
- For the remaining areas, work out the difference between forecasted and actual expenditure on a monthly basis:
  - Attach `Budget` for each (`month`, `Category`) as that category’s `MonthlyBudget` (the evenly spread monthly budget).
  - Round `Actual Spending` to the nearest whole number using “round half to even” (banker’s rounding), and store as an integer.
  - Compute `Difference = Actual Spending - Budget` (integer arithmetic).
  - Derive `Month` as the month name from the month date, using these exact labels:
    - January, February, March, April, May, June, July, August, **Sepetember**, October, November, December.
- For each month, find the category which has the highest overspending:
  - For each `Month`, select the single row with the maximum `Difference` value among the included categories.
  - If multiple categories tie for the maximum `Difference` within a month, select the one that appears first in the combined long table order (based on the processing order of monthly files, then the category order within each month).
- Output the data.

## Output

- output_01.csv
  - 5 fields:
    - Month
    - Category
    - Actual Spending
    - Budget
    - Difference