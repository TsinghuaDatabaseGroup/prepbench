## Context
SuperBytes has identified a set of products that must be recalled due to a manufacturing issue. The goal is to quantify the financial loss caused by recalled items currently held in stores, summarizing losses by product category and by store, and flagging stores by priority based on total loss.

## Requirements
- Input the data from:
  - `input_01.csv`: the list of recalled items (must include at least `Category`, `Product ID`, and `Unit Price`).
  - `input_02.csv`: store inventory lines (must include at least `Store`, `Category`, `Product ID`, `Unit Price`, and `Quantity`).
- Identify which recalled items are located in each store by matching store inventory lines to the recall list using an **inner join** on the keys:
  - `Category`
  - `Product ID`
  Only matched (recalled) inventory lines should be retained; non-matching inventory lines are excluded.
- Create a line-level field for financial loss for each recalled inventory line:
  - `Lost Amount = (store Unit Price) * Quantity`
- Produce the first output dataset by aggregating the recalled inventory lines to the **category** level:
  - Group by `Category`
  - Sum `Lost Amount` within each category
  - Round the resulting total to **2 decimal places** and store it in `Total Price Rounded`
- Output this first dataset.
- Produce the second output dataset by aggregating the recalled inventory lines to the **store** level:
  - Group by `Store`
  - Sum `Lost Amount` within each store
  - Round the resulting total to **2 decimal places** and store it in `Total Price Rounded`
  - Create `Issue Level` based on the rounded total:
    - `High Priority` if `Total Price Rounded` is **£5000 or more** (i.e., `>= 5000`)
    - `Low Priority` if `Total Price Rounded` is **below £5000**
- Output this second dataset.

## Output

- output_01.csv
  - 2 fields:
    - Category
    - Total Price Rounded

- output_02.csv
  - 3 fields:
    - Store
    - Total Price Rounded
    - Issue Level