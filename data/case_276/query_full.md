## Context

You are given a customer-level dataset that includes each customer’s sale total and gender. The goal is to compute loyalty points from spending, assign each record to a loyalty “byte” category, and then report—by category—the gender split as percentages.

## Requirements

- Input the data from `inputs/input_01.csv`.
- For each input record, compute **Loyalty Points** based on the sale value:
  - Loyalty Points = (Sale Total) ÷ 50
  - Round Loyalty Points to **1 decimal place**.
- Create a **Category** field based on Loyalty Points using these rules:
  - If Loyalty Points are **greater than or equal to 7**, categorise as **"Mega Byte"**.
  - If Loyalty Points are **greater than or equal to 5** (but **less than 7**), categorise as **"Byte"**.
  - Categorise the remaining as **"No Byte"**.
- Using the categorised records, compute the number of customers (i.e., number of records) in each **Category**, split by **Gender** (Female vs Male).
  - Ensure genders are treated as the two labels **Female** and **Male** for the split.
- For each Category, convert the gender counts into **percentages within that Category**:
  - Percentage = (Gender count in the Category ÷ Total count in the Category) × 100
  - Round percentages to **1 decimal place**.
- Pivot the result so that **Female** and **Male** are separate fields (columns).
  - If a category has no customers for a given gender, output **0.0** for that gender’s percentage in that category.
- Output the final dataset with one row per Category.

## Output

- output_01.csv
  - 3 fields:
    - Category
    - Female
    - Male