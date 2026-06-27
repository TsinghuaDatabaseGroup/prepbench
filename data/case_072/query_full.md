## Context
You are trying to reconcile product identifiers between an Internal system and a 3rd Party system. Some IDs can be matched exactly, while others require making structured “best guess” matches based on shared product attributes (Scent) and similarity in sales. The goal is to produce a single list that shows exact matches, inferred matches, and the remaining unmatched IDs from each source.

## Requirements
- Input the data from:
  - `input_01.csv` (Internal data) containing at least: `ID`, `Scent`, `Sales`
  - `input_02.csv` (3rd Party data) containing at least: `3rd Party ID`, `Scent`, `3rd Party Sales`

- Find the IDs that match perfectly and label them as such:
  - Perform an inner join where `input_01.ID == input_02.3rd Party ID`.
  - For these rows, set `Status = "Matched"`.
  - Keep only these output fields for the matched rows: `Status`, `ID`, `3rd Party ID`, `Scent`, `Sales`, `3rd Party Sales`.

- For the remaining unmatched Internal and 3rd Party IDs, create all the possible matching IDs for each Scent:
  - Exclude any Internal rows whose `ID` already appears in the exact matches.
  - Exclude any 3rd Party rows whose `3rd Party ID` already appears in the exact matches.
  - Create candidate pairs by performing an inner join of the remaining Internal and remaining 3rd Party rows on `Scent` (i.e., all combinations within each Scent).

- For candidate pairs, compute sales difference and filter candidates:
  - Compute `Sales_Diff = abs(Sales - 3rd Party Sales)`.
  - Keep a candidate pair only if either:
    - `Sales_Diff <= 12969.60`, OR
    - `abs(Sales_Diff - 29802.211101587) < 0.01`.

- For each 3rd Party ID, find the Internal ID with the lowest sales difference:
  - Sort the remaining candidate pairs by `Sales_Diff` ascending (stable sort for deterministic tie behavior).
  - Deduplicate by `3rd Party ID`, keeping the first row per `3rd Party ID` (thereby keeping the smallest `Sales_Diff` for each 3rd Party ID).

- For each Internal ID, find the 3rd Party ID with the lowest sales difference:
  - From the result of the previous step, deduplicate by `ID`, keeping the first row per `ID` (thereby keeping the smallest available `Sales_Diff` for each Internal ID).

- You should now have no duplicated IDs:
  - After the two-stage deduplication (first by `3rd Party ID`, then by `ID`), each `3rd Party ID` and each `ID` appears at most once among these inferred matches.

- Classify these IDs as "Matched on Scent":
  - For the deduplicated scent-based matches, set `Status = "Matched on Scent"`.
  - Keep only these output fields for the scent-matched rows: `Status`, `ID`, `3rd Party ID`, `Scent`, `Sales`, `3rd Party Sales`.

- Join these IDs to the "Matched IDs":
  - Combine (union/append) the exact matches (`Status = "Matched"`) and the scent-based matches (`Status = "Matched on Scent"`) into a single matched set.

- Classify IDs from Internal and 3rd Party Data which have not been matched and join these to create the output:
  - Unmatched Internal:
    - Take all rows from `input_01.csv` whose `ID` does not appear in any matched row (exact or scent-based).
    - Set `Status = "Unmatched - Internal"`.
    - Set `3rd Party ID` and `3rd Party Sales` to blank/empty in the output.
  - Unmatched 3rd Party:
    - Take all rows from `input_02.csv` whose `3rd Party ID` does not appear in any matched row (exact or scent-based).
    - Set `Status = "Unmatched - 3rd Party"`.
    - Set `ID` and `Sales` to blank/empty in the output.
  - Append these unmatched Internal rows and unmatched 3rd Party rows to the matched set to form the final output table.

- Output the data:
  - Output grain: one row represents either (a) a matched Internal–3rd Party pair, (b) an unmatched Internal ID, or (c) an unmatched 3rd Party ID.
  - Ensure missing values in `ID`, `3rd Party ID`, `Sales`, and `3rd Party Sales` that are intentionally blank are written as empty strings in the CSV.
  - When writing numeric values in `Sales` and `3rd Party Sales`, format them as decimal strings with up to 9 digits after the decimal point, removing trailing zeros and any trailing decimal point.

## Output

- output_01.csv
  - 6 fields:
    - Status
    - ID
    - 3rd Party ID
    - Scent
    - Sales
    - 3rd Party Sales