## Context
Identify which SuperBytes customers spent the most on different days of the week, using last year’s transaction data and a separate customer reference list. The immediate deliverable for this task is the ranked list of Monday transactions, while keeping customer names private.

## Requirements
- Input the data:
  - Read the customer reference sheet (customer names and IDs).
  - Read the transaction sheet (transaction-level details, including transaction date, receipt number, channel indicator, and sale total).
- Join the two sheets to bring Customer ID onto the transaction records:
  - Join on `First Name` and `Last Name`.
  - Use a left join so every transaction remains in the result even if no matching customer record is found.
- Remove names to maintain privacy:
  - After the join, exclude `First Name` and `Last Name` from any downstream dataset and from the final output.
- Group Online and In Person into one field:
  - Create `Online or In Person` such that transactions marked as online (where the `Online` field indicates “yes”) are labeled `Online`; all other transactions are labeled `In-Person`.
- Add a field for the day of the week the transaction was completed:
  - Parse the transaction `Date` as a date/time and derive `Weekday` as the day name (e.g., Monday, Tuesday, etc.).
- Define Sales:
  - Create `Sales` by converting `Sale Total` to a numeric value.
- Rank sales for each weekday:
  - For the selected weekday’s transactions, compute `Rank` based on `Sales` in descending order (largest sale = rank 1).
  - Use competition ranking: ties share the same rank, and the next rank reflects the position after the tie (i.e., “min” rank among tied values).
  - For deterministic ordering in the output, sort records by `Sales` descending, then by `Receipt Number` ascending.
- Create a parameter to output a data set for each day of the week:
  - Structure the logic so a single weekday can be selected for output.
- Add day of week to the title of the worksheet:
  - Ensure the selected weekday is explicitly reflected as the output’s weekday context (for this task, the weekday is Monday).
- Output the data for Monday:
  - Filter the dataset to `Weekday == 'Monday'`.
  - Output one row per Monday transaction with the required fields only, in the order specified.

## Output

- output_01.csv
  - 7 fields:
    - Rank
    - Customer ID
    - Receipt Number
    - Gender
    - Online or In Person
    - Sales
    - Weekday