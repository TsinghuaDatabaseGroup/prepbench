## Context
You are performing market basket analysis on transaction-level basket data to compute the standard association-rule metrics: support, confidence, and lift. The focus is limited to one-to-one association rules between individual items (directional rules of the form “X --> Y”), not multi-item itemsets.

## Requirements
- Input the data.
- Reshape the dataset so the grain includes one row per `(TransactionID, Item)` occurrence by splitting the transaction’s comma-delimited item list into individual items.
  - While doing this, retain a field that preserves the original comma-delimited item list for each transaction (the un-split basket string).
- Define the total number of transactions as the count of distinct transactions in the input.
- Calculate item support for each individual item:
  - For each item, count the number of distinct transactions that contain that item.
  - `Item Support = (distinct transaction count containing the item) / (total distinct transactions)`.
- Create one-to-one association rules for ordered item pairs:
  - Generate directional rules for all ordered pairs `(LHSItem, RHSItem)` where `LHSItem != RHSItem`.
  - Exclude “impossible” rules by keeping only pairs that co-occur in at least one transaction (i.e., at least one transaction contains both the LHS item and the RHS item).
  - Create a string representation of each rule as `LHSItem + ' --> ' + RHSItem` (including spaces around the arrow).
- For each retained association rule `(LHSItem --> RHSItem)`, compute the co-occurrence and conditional metrics using distinct transaction counts:
  - `Both_Count` = number of distinct transactions containing both `LHSItem` and `RHSItem`.
  - `LHS_Count` = number of distinct transactions containing `LHSItem`.
  - `RHS_Count` = number of distinct transactions containing `RHSItem`.
  - `LHS Support = LHS_Count / TotalTransactions`.
  - `RHS Support = RHS_Count / TotalTransactions`.
  - `Confidence = Both_Count / LHS_Count`.
  - `Lift = Confidence / (RHS Support)` (equivalently `(Both_Count / TotalTransactions) / (LHS Support * RHS Support)`).
- Output one row per valid directional association rule, including the required fields.
- Sort the final output by `AssociationRule` in ascending order before writing the file.
- Output the data.

## Output

- output_01.csv
  - 7 fields:
    - AssociationRule
    - LHSItem
    - RHSItem
    - LHS Support
    - RHS Support
    - Confidence
    - Lift