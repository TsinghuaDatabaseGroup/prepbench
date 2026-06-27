## Context

Chin & Beard Suds Co. is evaluating potential overseas store sites and needs a cleaned, standardized list of candidate locations with their expected costs, sales potential, and an associated USD conversion value. An agency provided an input file with data-entry issues, so rows with inaccurate location information must be removed before selecting the best candidate per zip code.

## Requirements

- Input the data from:
  - `input_01.csv` (main store-site candidates)
  - `input_02.csv` (currency conversion lookup)
- DO NOT USE ANY TYPED CALCULATIONS  
  - Calculations created by Tableau from other features selected is fine  
  - You are allowed to change data field names
- Standardize/derive the following fields from the main input:
  - Split `Location` into:
    - `City` = the text before the first comma
    - `Country` = the text after the first comma
  - Rename `Potential Store Location` to `Zip Code` (treat `Zip Code` as text/string).
  - Parse `Store Cost` and `Store Potential Sales` as numeric amounts (whole numbers), and derive a 3-letter `Currency` code from the same fields when it is present in the source text.
    - If a currency code is available in both, use the one parsed from `Store Potential Sales`; otherwise use the one parsed from `Store Cost`.
    - Exclude rows where `Currency` cannot be determined.
- Remove the rows of any inaccurate City / Country names by keeping only rows whose `(City, Country)` pair is exactly one of:
  - (New York, United States)
  - (San Francisco, United States)
  - (Miami, United States)
  - (Monterrey, Mexico)
- Remove any instances where the Store Cost is higher than Potential Store Sales (keep only rows where `Store Cost <= Store Potential Sales`).
- We only want the store per zip code that could the most sales:
  - Group by `Zip Code` and keep only the row(s) with the maximum `Store Potential Sales` within each `Zip Code`.
  - If multiple rows within a `Zip Code` tie for the same maximum `Store Potential Sales`, keep the first occurrence from the original input order.
- Add Currency conversion rates (don't change everything to USD):
  - Join the filtered/selected rows to `input_02.csv` on `Currency` using a left join.
  - Do not convert `Store Cost` or `Store Potential Sales` to USD; retain their numeric amounts as-is and include the USD conversion value from the lookup as `Value in USD`.
- Output the data:
  - Ensure `Store Cost` and `Store Potential Sales` are integers in the output.
  - Produce the final dataset sorted by `City`, then `Country`, then `Zip Code` (ascending).

## Output

- output_01.csv
  - 7 fields:
    - City
    - Country
    - Zip Code
    - Store Cost
    - Store Potential Sales
    - Currency
    - Value in USD