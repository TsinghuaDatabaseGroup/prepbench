## Context

Santa has a master list of intended recipients and two separate lists classifying recipients as “Nice” or “Naughty”. The goal is to (1) determine, for each recipient on Santa’s master list, whether they match the Nice list or the Naughty list based on name/address matching logic, and (2) summarize total elf build time by list in whole hours (rounded up).

## Requirements

- Input the data.
- Input all three tables/files:
  - `input_01.csv`: Santa’s master list of recipients and the gift/build-time details to be used in outputs.
  - `input_02.csv`: the Nice list, containing recipient identification details and a reason.
  - `input_03.csv`: the Naughty list, containing recipient identification details and a reason.
- Pull together the Naughty and Nice list by matching each list to Santa’s master list using **both** name-derived matching and address matching:
  - Create a name abbreviation key `__abbr` for each table as: take `Name`, convert to string, strip leading/trailing spaces, convert to lowercase, remove internal spaces, then take the first 3 characters. (If `Name` is missing, treat it as empty.)
  - Create normalized address strings:
    - For Santa’s master list (`input_01.csv`), normalize `Address` as lowercase trimmed text (missing treated as empty); call this the base address string.
    - For the Nice/Naughty lists, normalize `Address` as lowercase trimmed text (missing treated as empty); call this the full address string.
  - For each of the Nice and Naughty lists independently:
    - Perform an **inner join** between that list and Santa's master list on `__abbr`.
    - From joined rows, keep only those where the normalized base address string from Santa's master list is a substring of the normalized full address string from the Nice/Naughty list.
      - **Address substring matching rule**: The substring check is a simple string containment check (e.g., "wimbledon" is contained in "15 big house, wimbledon, london, sw1 4pw"). It does not require word boundaries, so partial word matches are allowed (e.g., "ton" would match "boston"). However, in practice, the base address strings from Santa's master list are typically complete place names or address components, so this should not cause unintended matches.
- Produce `output_01.csv` with **only one row per recipient name** from Santa's master list across both lists:
  - **Definition of "recipient name"**: "Recipient name" refers to the `Name` field value from Santa's master list (`input_01.csv`). Each unique `Name` value in `input_01.csv` should appear at most once in `output_01.csv`. If the same `Name` appears in multiple rows in `input_01.csv`, each row is matched independently, but after matching and combining Nice/Naughty results, only one row per unique `Name` is kept (with Nice taking priority if the same name matches both lists).
  - First generate matched rows for the Nice list and for the Naughty list, then combine them.
  - If a recipient name appears in both lists after matching, keep the Nice list row and drop the Naughty list row (Nice takes priority).
  - If a recipient from Santa’s master list does not match either list under the rules above, they will not appear in `output_01.csv`.
- Also aggregate the Nice and Naughty results to understand how many hours have been allocated to building presents for each list:
  - For each `List`, sum `Elves Build Time (min)` across the rows in `output_01.csv`.
  - Convert total minutes to hours as `ceil(total_minutes / 60)`, and output as an integer number of hours (rounding up to whole hours).
  - Output the summary with Naughty first, then Nice.
- Output the data.

## Output

- output_01.csv
  - 7 fields:
    - List
    - Name
    - Item
    - Family Role
    - Elves Build Time (min)
    - Address-1
    - Reason

- output_02.csv
  - 2 fields:
    - Total Hours Build Time
    - List