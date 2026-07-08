## Context

You are preparing a cleaned complaints dataset for analysis. Each complaint record includes a composite “Complaint Description” field that embeds a product identifier and issue type, and the product’s category must be derived from the product identifier. The output should retain only validated complaints where the resolution date occurs strictly after the receipt date, and should include only the required fields.

## Requirements

- Input the data.
  - Use the complaints dataset as the primary input.
  - Use the product category lookup table to translate category codes to product categories.
- Split the `Complaint Description` field into three components and store them as separate fields:
  - `Product ID`
  - `Issue Type`
  - `Complaint Description` (the remaining free-text description written by the customer)
  - Perform the split using the expected structure: `Product ID - Issue Type: Complaint Description`.
  - If a row’s `Complaint Description` does not match this structure, leave `Product ID` and `Issue Type` as null and keep the original description text as `Complaint Description`.
  - If the extracted free-text description is wrapped in matching single or double quotes, remove the outermost quotes.
- Extract the first 2 letters of the `Product ID` as the `Category Code`.
- Use this `Category Code` to join on / map to the `Product Category` using the lookup table mapping:
  - `BE` → `Beauty`
  - `CL` → `Clothes`
  - `EL` → `Electronic`
  - `GR` → `Groceries`
  - `HO` → `Home`
- Parse `Date Received` and `Date Resolved` as dates using the following format priority (try each format in order until one succeeds):
  1. `YYYY-MM-DD HH:MM:SS` (e.g., `2023-10-10 00:00:00`)
  2. `M/D/YYYY` (e.g., `9/28/2023`, `6/26/2023`)
  3. `YYYY-MM-DD` (e.g., `2023-10-10`)
- If either `Date Received` or `Date Resolved` cannot be parsed using any of the above formats, exclude that row from the output (the comparison cannot be evaluated).
- Filter the dataset to only contain rows where `Date Resolved` happens after `Date Received` (strictly greater than; exclude equal dates and any rows where the comparison cannot be evaluated).
- Ensure `Timely Response` is represented as a boolean value in the output.
- Remove unnecessary fields by selecting only the required output columns and keeping them in the specified order.
- Output the data.

## Output

- output_01.csv
  - 11 fields:
    - Complaint ID
    - Receipt Number
    - Customer ID
    - Date Received
    - Date Resolved
    - Timely Response
    - Response to Consumer
    - Issue Type
    - Product Category
    - Product ID
    - Complaint Description