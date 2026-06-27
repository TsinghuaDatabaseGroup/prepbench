## Context

A subscription deal offers up to 5 drinks per day for £20 per month. The goal is to evaluate, for each Dr Prepper, how much they would spend at menu prices over a representative week of orders (scaled to a month) and whether subscribing would save them money.

## Requirements

- Input the data.
- Restructure the menu price list into a single two-column representation of items and their prices:
  - The price list is provided in multiple item/price column pairs; convert these into one consolidated list of `(Item, Price)` rows by stacking all pairs.
  - If the same item name appears more than once across the stacked pairs, use the last value encountered when building the definitive item-to-price mapping.
- Restructure the orders so you can correctly count and price everything each person orders during the week:
  - The orders data is in a wide format with one row per person and separate fields for days of the week; pivot it to a long format so each record represents a person's order text for a given day.
  - Treat the daily order entries as text that may contain multiple ordered items; ensure that any priced add-ons (such as extra shots or syrups) are counted and priced independently from the base drink whenever their priced item names appear in the order text.
- Join ordered items to their prices in a way that reflects how ordered item names appear in the order text:
  - Identify each priced item by counting how many times its menu name occurs within the full set of that person’s weekly order text (across all days).
  - To avoid double-counting when one menu item name is a substring of another, evaluate matches in descending order of menu item name length, and after counting an item’s occurrences, remove those matched text segments from further matching for that person’s weekly order text.
  - Ordered text that does not match any priced menu item name contributes £0 (i.e., it is ignored for spend calculation).
- Calculate spend metrics at the person level (one output row per person):
  - Weekly spend = sum over all menu items of `(count of occurrences in that person’s weekly order text) × (menu price)`.
  - Monthly Spend = Weekly spend × 4 (assume exactly 4 weeks per month; the month starts on a Monday and ends on a Sunday).
  - Potential Savings = Monthly Spend − 20.
  - Worthwhile? = `true` if Potential Savings > 0, otherwise `false`.
  - Round Monthly Spend and Potential Savings to 2 decimal places.
- Output the data.

## Output

- output_01.csv
  - 4 fields:
    - Person
    - Monthly Spend
    - Potential Savings
    - Worthwhile?